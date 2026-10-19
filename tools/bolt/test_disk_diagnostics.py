"""Disk observation, failure injection and measured-size forecasts; no LLVM build."""
import contextlib,errno,io,json,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import bolt_helper as h
from test_bolt_helper import Base,elf


def fixture(root):
    build=root/'build';work=build/'clang-bolt';installed=root/'root';work.mkdir(parents=True)
    (build/'bin').mkdir();(installed/'usr/bin').mkdir(parents=True)
    elf(installed/'usr/bin/clang-22',payload=b'\xc3',stripped=True)
    with (installed/'usr/bin/clang-22').open('ab') as f:f.write(b'\0'*(16384-(installed/'usr/bin/clang-22').stat().st_size))
    shutil.copyfile(installed/'usr/bin/clang-22',build/'bin/clang-22');shutil.copyfile(build/'bin/clang-22',work/'ordinary-clang-22')
    (installed/'usr/bin/clang').symlink_to('clang-22')
    cache=build/'lto.cache';cache.mkdir();(cache/'old').write_bytes(b'a'*4096)
    (work/'link.original').write_text('--thinlto-cache-dir='+str(cache))
    os.environ.update(BOLT_BUILD=str(build),BOLT_WORK=str(work),BOLT_INSTALL_ROOT=str(installed),BOLT_STEP_LOG='-')
    h._DISK_CONTEXT.clear()
    with contextlib.redirect_stdout(io.StringIO()):h.disk_report('begin',build,work,installed)
    descriptions=['Building CXX object tools/bolt/a.o','Building CXX object tools/bolt/b.o','Building CXX object tools/bolt/c.o','Linking CXX executable bin/llvm-bolt']
    (build/'tools/bolt').mkdir(parents=True)
    for name,size in [('a.o',4096),('b.o',8192),('c.o',4096)]: (build/'tools/bolt'/name).write_bytes(b'o'*size)
    (work/'tool-plan.json').write_text(json.dumps({'tasks':4,'descriptions':descriptions}))
    (work/'tool-build.txt').write_text('[1/4] '+descriptions[0]+'\n[2/4] '+descriptions[1]+'\n')
    (work/'reference-relocs-clang-22').write_bytes(b'r'*4096)
    (cache/'new').write_bytes(b'c'*4096)
    return build,work,installed


def fault_driver(kind, root):
    build,work,installed=fixture(root);entity=installed/'usr/bin/clang-22';before=h.digest(entity)
    args=['snapshot',str(installed),str(work/'snapshot.json')];manager=contextlib.nullcontext()
    if kind=='copy':
        args=['cache-copy',str(work/'link.original'),str(work/'copy'),str(work/'copy.json')]
        manager=patch.object(h.shutil,'copytree',side_effect=OSError(errno.ENOSPC,'No space left on device'))
    elif kind in ('json','corrupt-records','disk-diagnostic-exception'):
        (work/'snapshot.json').write_text('old JSON must survive')
        if kind=='corrupt-records':(work/'disk-baseline.json').write_text('{broken')
        manager=patch.object(h.os,'fsync',side_effect=OSError(errno.ENOSPC,'No space left on device'))
    elif kind=='subprocess':
        args=['run-step','fault-command',str(work/'process.log'),'--','/bin/sh','-c','printf "No space left on device\\n" >&2; exit 9']
    elif kind=='subprocess-log':
        log=work/'process.log';real=Path.open
        def opening(p,*a,**kw):
            if p==log and a and a[0]=='wb':raise OSError(errno.ENOSPC,'No space left on device')
            return real(p,*a,**kw)
        manager=patch.object(Path,'open',opening)
        args=['run-step','fault-log',str(log),'--',sys.executable,'-B','-c','print("not started")']
    elif kind.startswith('install'):
        candidate=work/'candidate';before_bolt=work/'before-bolt';elf(candidate,stripped=True);elf(before_bolt)
        identity={'before_path':str(before_bolt),'before_sha256':h.digest(before_bolt),'bolt_note_before':True,'after_sha256':h.digest(candidate)}
        (work/'identity.json').write_text(json.dumps(identity))
        args=['install',str(installed),str(candidate),str(work/'state.json'),str(work/'identity.json')]
        if kind=='install':
            real=h.shutil.copyfile
            def copying(src,dst,*a,**kw):
                if Path(dst).name=='.clang-bolt.new':
                    Path(dst).write_bytes(b'partial');raise OSError(errno.ENOSPC,'No space left on device')
                return real(src,dst,*a,**kw)
            manager=patch.object(h.shutil,'copyfile',copying)
        elif kind=='install-state':
            real=h.save
            def saving(path,value):
                if Path(path).name=='state.json':raise OSError(errno.ENOSPC,'No space left on device')
                return real(path,value)
            manager=patch.object(h,'save',saving)
        elif kind=='install-alias':manager=patch.object(Path,'symlink_to',side_effect=OSError(errno.ENOSPC,'No space left on device'))
        elif kind=='install-rename':
            real=h.os.replace
            def replace(src,dst):
                if Path(dst)==entity:raise OSError(errno.ENOSPC,'No space left on device')
                return real(src,dst)
            manager=patch.object(h.os,'replace',replace)
    elif kind in ('not-disk','diagnostic-exception','unknown'):
        log=work/'gate.log'
        if kind!='unknown':log.write_text('fixture original gate failure\n')
        os.environ['BOLT_STEP_LOG']=str(log)
        manager=patch.object(h,'root_snapshot',side_effect=h.GateError('fixture original gate failure'))
    else:raise ValueError(kind)
    with manager,patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':4096})()),patch.object(sys,'argv',['helper']+args):
        if kind in ('diagnostic-exception','disk-diagnostic-exception'):
            with patch.object(h,'disk_diagnose',side_effect=RuntimeError('corrupt diagnostic records')):rc=h.cli()
        else:rc=h.cli()
    state={'before_sha256':before,'after_sha256':h.digest(entity),'candidate_unchanged':before==h.digest(entity),'temporary_candidate_exists':(entity.parent/'.clang-bolt.new').exists()}
    if kind=='json':state['old_json_preserved']=(work/'snapshot.json').read_text()=='old JSON must survive'
    print('FAULT_STATE '+json.dumps(state))
    return rc


class CopytreeEvidenceTests(Base):
    def test_wrapped_copytree_errno_is_step_evidence(self):
        source=self.d/'source';source.mkdir();(source/'file').write_bytes(b'data')
        with patch.object(h.shutil,'copy2',side_effect=OSError(errno.ENOSPC,'No space left on device')):
            try:h.shutil.copytree(source,self.d/'destination',copy_function=h.shutil.copy2)
            except h.shutil.Error as error:
                self.assertIn('copytree:No space left on device',h.disk_evidence('-',error))
            else:self.fail('expected native copytree failure')


class DiskFaultTests(Base):
    def run_fault(self,kind):
        root=self.d/kind;root.mkdir();p=subprocess.run([sys.executable,'-B',__file__,'--fault',kind,str(root)],capture_output=True,text=True,timeout=30)
        evidence=os.environ.get('BOLT_TEST_EVIDENCE')
        if evidence:
            d=Path(evidence);d.mkdir(parents=True,exist_ok=True)
            (d/(kind+'.stdout')).write_text(p.stdout);(d/(kind+'.stderr')).write_text(p.stderr)
            (d/(kind+'.json')).write_text(json.dumps({'rc':p.returncode,'argv':p.args},indent=2)+'\n')
        self.assertEqual(p.returncode,1,p.stdout+p.stderr)
        print('FAULT_CASE '+kind+' rc='+str(p.returncode)+'\n'+p.stdout+p.stderr,end='')
        rows=[json.loads(x.split(' ',1)[1]) for x in p.stdout.splitlines() if x.startswith('BOLT_DISK_DIAGNOSIS ')]
        state=json.loads(next(x.split(' ',1)[1] for x in p.stdout.splitlines() if x.startswith('FAULT_STATE ')))
        return p,rows,state
    def disk_fault(self,kind):
        p,rows,state=self.run_fault(kind);self.assertTrue(rows)
        d=rows[-1];self.assertEqual(d['cause'],'disk')
        for key in ('used_bytes','free_bytes','estimated_remaining_bytes','estimated_total_bytes','shortfall_bytes'):self.assertIn(key,d)
        self.assertEqual(d['shortfall_bytes'],max(0,d['estimated_remaining_bytes']-d['free_bytes']))
        if kind.startswith('install'):
            self.assertTrue(state['candidate_unchanged']);self.assertFalse(state['temporary_candidate_exists'])
        return p,rows,state
    def test_copy_enospc(self):self.disk_fault('copy')
    def test_json_enospc(self):self.assertTrue(self.disk_fault('json')[2]['old_json_preserved'])
    def test_subprocess_enospc(self):self.assertIn('COMMAND_FAILED rc=9',self.disk_fault('subprocess')[0].stderr)
    def test_log_open_enospc_stops_before_subprocess(self):self.disk_fault('subprocess-log')
    def test_install_copy_enospc_preserves_entity(self):self.disk_fault('install')
    def test_install_state_enospc_preserves_entity(self):self.disk_fault('install-state')
    def test_install_alias_enospc_preserves_entity(self):self.disk_fault('install-alias')
    def test_install_rename_enospc_preserves_entity(self):self.disk_fault('install-rename')
    def test_non_disk_original_error(self):
        p,rows,state=self.run_fault('not-disk');self.assertEqual(len(rows),1);self.assertEqual(rows[0]['cause'],'not-disk');self.assertNotIn('estimated_total_bytes',rows[0]);self.assertEqual(p.stderr,'BOLT_GATE_FAILED: fixture original gate failure\n')
    def test_missing_log_unknown_cli(self):
        p,rows,state=self.run_fault('unknown');self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['cause'],'unknown');self.assertEqual(rows[0]['reason'],'日志不可用，无法判定原因')
        self.assertIn('used_bytes',rows[0]);self.assertIn('free_bytes',rows[0]);self.assertNotIn('estimated_total_bytes',rows[0])
        self.assertEqual(p.stderr,'BOLT_GATE_FAILED: fixture original gate failure\n')
    def test_diagnosis_exception_preserves_exit_and_error(self):
        p,rows,state=self.run_fault('diagnostic-exception');self.assertEqual(rows,[]);self.assertEqual(p.stderr,'BOLT_GATE_FAILED: fixture original gate failure\n')
    def test_disk_error_survives_diagnosis_exception(self):
        p,rows,state=self.run_fault('disk-diagnostic-exception');self.assertEqual(rows,[]);self.assertIn('[Errno 28] No space left on device',p.stderr)
    def test_corrupt_records_degrade_without_throwing(self):
        p,rows,state=self.run_fault('corrupt-records');self.assertEqual(rows[-1]['cause'],'disk');self.assertIn('degraded',rows[-1]);self.assertIn('used_bytes',rows[-1]);self.assertIn('free_bytes',rows[-1])


class DiskObservationTests(Base):
    def setUp(self):
        super().setUp();self.env=patch.dict(os.environ,{},clear=False);self.env.start();self.addCleanup(self.env.stop)
    def test_report_existing_and_missing_cli_return_zero(self):
        for relative in ['existing','missing/deep/work']:
            work=self.d/relative
            if relative=='existing':work.mkdir()
            p=subprocess.run([sys.executable,'-B',h.__file__,'disk-report','begin','--build',str(self.d),'--work',str(work)],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr);self.assertIn('BOLT_DISK_REPORT ',p.stdout)
    def test_report_save_enospc_returns_normally(self):
        with patch.object(h,'save',side_effect=OSError(28,'No space left on device')):
            self.assertIn('report_error',h.disk_report('begin',self.d,self.d/'work'))
    def test_report_internal_exception_cli_still_zero(self):
        with patch.object(h,'disk_report',side_effect=RuntimeError('broken')),patch.object(sys,'argv',['helper','disk-report','begin']):self.assertEqual(h.cli(),0)
    def test_diagnose_internal_exception_cli_still_zero(self):
        with patch.object(h,'disk_diagnose',side_effect=RuntimeError('broken')),patch.object(sys,'argv',['helper','disk-diagnose','step','-']):self.assertEqual(h.cli(),0)
    def test_full_matching_table(self):
        build,work,root=fixture(self.d)
        for message in ['No space left on device','Disk quota exceeded','ENOSPC','EDQUOT']:
            log=work/'failure.log';log.write_text(message)
            with contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('step',log,build=build,work=work)
            self.assertEqual(value['cause'],'disk')
    def test_errno_28_and_122_direct(self):
        build,work,root=fixture(self.d)
        for code in (28,122):
            with contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('step','-',OSError(code,'fixture'),build,work)
            self.assertEqual(value['cause'],'disk')
    def test_low_free_is_not_a_cause(self):
        build,work,root=fixture(self.d)
        log=work/'ordinary.log';log.write_text('ordinary gate failure\n')
        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':0})()),contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('step',log,build=build,work=work)
        self.assertEqual(value,{'cause':'not-disk','step':'step','free_bytes':0})
    def test_unrelated_log_and_error_text_are_not_evidence(self):
        build,work,root=fixture(self.d);(work/'other.log').write_text('ENOSPC')
        with contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('step','-',h.GateError('No space left on device'),build,work)
        self.assertEqual(value['cause'],'unknown')
    def test_empty_and_unreadable_log_are_unknown(self):
        build,work,root=fixture(self.d);log=work/'empty.log';log.write_text('')
        with contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('empty',log,build=build,work=work)
        self.assertEqual(value['cause'],'unknown');self.assertIn('used_bytes',value)
        original=Path.read_text
        def reading(path,*a,**kw):
            if path==log:raise PermissionError('fixture unreadable log')
            return original(path,*a,**kw)
        with patch.object(Path,'read_text',reading),contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('unreadable',log,build=build,work=work)
        self.assertEqual(value['cause'],'unknown');self.assertIn('used_bytes',value);self.assertNotIn('formulas',value)
    def test_successful_log_text_does_not_fail_call(self):
        log=self.d/'success.log'
        self.assertEqual(h.call(['/bin/sh','-c','printf ENOSPC'],log),'ENOSPC')
        self.assertTrue(json.loads((self.d/'success.log.argv.json').read_text())['completed'])
    def test_stdin_failure_log_consumed_once(self):
        build,work,root=fixture(self.d);real=Path.read_text;count=[]
        def reading(path,*a,**kw):
            if path==Path('/dev/stdin'):
                count.append(1);return 'Disk quota exceeded' if len(count)==1 else ''
            return real(path,*a,**kw)
        with patch.object(Path,'read_text',reading),contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('stdin','/dev/stdin',build=build,work=work)
        self.assertEqual(value['cause'],'disk');self.assertEqual(value['evidence'],['Disk quota exceeded']);self.assertEqual(len(count),1)
    def test_diagnose_performs_no_file_writes(self):
        build,work,root=fixture(self.d);log=work/'failure.log';log.write_text('ENOSPC');real=Path.open
        def guard(p,*args,**kwargs):
            mode=args[0] if args else kwargs.get('mode','r')
            self.assertFalse(any(x in mode for x in 'wax+'));return real(p,*args,**kwargs)
        with patch.object(Path,'open',guard),patch.object(h,'save',side_effect=AssertionError('diagnosis wrote JSON')),patch.object(h.os,'replace',side_effect=AssertionError('diagnosis renamed')),contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('step',log,build=build,work=work)
        self.assertEqual(value['cause'],'disk');self.assertNotIn('degraded',value)
    def test_cache_pruning_does_not_hide_new_allocations(self):
        build,work,root=fixture(self.d);baseline=json.loads((work/'disk-baseline.json').read_text());(build/'lto.cache/old').unlink()
        value=h.disk_measure(build,work,baseline);self.assertEqual(value['cache_delta_allocated_bytes'],4096);self.assertEqual(value['cache_net_allocation_delta_bytes'],0)
    def test_hardlinks_are_not_double_counted(self):
        build,work,root=fixture(self.d);(build/'lib64').mkdir();a=build/'lib64/libLLVMBOLTA.a';a.write_bytes(b'x'*4096);os.link(a,build/'bin/llvm-bolt')
        m=h.disk_measure(build,work,json.loads((work/'disk-baseline.json').read_text()));tool=sum(x['allocated_bytes'] for x in m['owned_paths'] if x['category'] in ('tool_executable','tool_library'));self.assertEqual(tool,4096)


class DiskFormulaTests(Base):
    def setUp(self):
        super().setUp();self.env=patch.dict(os.environ,{},clear=False);self.env.start();self.addCleanup(self.env.stop)
    def test_known_sizes_and_tool_average(self):
        build,work,root=fixture(self.d);baseline=json.loads((work/'disk-baseline.json').read_text());measured=h.disk_measure(build,work,baseline);device=h.filesystem(work)['device']
        value=h.disk_prediction(build,work,root,measured,baseline,device)
        tool=next(x for x in value['formulas'] if x['item']=='tool-build')
        expected={'completed_output_bytes':12288,'completed_tasks':2,'remaining_tasks':2,'predicted_output_bytes':12288}
        self.assertEqual({k:tool[k] for k in expected},expected)
        self.assertEqual(value['estimated_remaining_bytes'],69632)
        print('FORMULA_FIXTURE '+json.dumps({'inputs':{'ordinary':16384,'completed_outputs':[4096,8192],'completed_tasks':2,'remaining_tasks':2,'partial_tool':4096,'partial_relink':4096},'expected_tool_output':12288,'actual_tool_output':tool['predicted_output_bytes'],'expected_remaining_peak':69632,'actual_remaining_peak':value['estimated_remaining_bytes']}))
    def test_failed_task_not_counted_completed(self):
        build,work,root=fixture(self.d);log=work/'tool-build.txt';log.write_text(log.read_text()+'FAILED: tools/bolt/b.o\n');baseline=json.loads((work/'disk-baseline.json').read_text());m=h.disk_measure(build,work,baseline);v=h.disk_prediction(build,work,root,m,baseline,h.filesystem(work)['device']);tool=next(x for x in v['formulas'] if x['item']=='tool-build');self.assertEqual(tool['completed_tasks'],1);self.assertEqual(tool['predicted_output_bytes'],12288)
    def test_zero_completed_does_not_fabricate_average(self):
        build,work,root=fixture(self.d);(work/'tool-build.txt').write_text('');baseline=json.loads((work/'disk-baseline.json').read_text());m=h.disk_measure(build,work,baseline);v=h.disk_prediction(build,work,root,m,baseline,h.filesystem(work)['device']);self.assertTrue(v['incomplete_estimate']);self.assertTrue(any('completed_tasks=0' in s for s in v['unknown_components']))

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--fault':sys.exit(fault_driver(sys.argv[2],Path(sys.argv[3])))
    unittest.main()
