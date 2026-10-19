from pathlib import Path
E=Path(__file__).parent;W=E.parents[1];B=W.parent/'llvm-optimize-bolt';S=W/'temp/bolt-v4-20261013/v41/llvm-source'
p=S/'packaging/clang-bolt-helper.py';s=p.read_text()
s=s.replace("        if cause in ('disk','unknown'):\n            value.update(filesystem_device=filesystem(target)['device'],\n                         evidence=evidence,\n                         estimate_note='估计值，依据本次构建实际文件大小',\n                         errno_messages=[os.strerror(int(item.split('=')[1])) for item in evidence if item.startswith('errno=')])", "        if cause in ('disk','unknown'):\n            device=filesystem(target)['device']\n            if cause == 'disk':\n                value.update(filesystem_device=device, evidence=evidence,\n                             estimate_note='估计值，依据本次构建实际文件大小',\n                             errno_messages=[os.strerror(int(item.split('=')[1])) for item in evidence if item.startswith('errno=')])",1)
s=s.replace("            device=value['filesystem_device']\n",'')
s=s.replace("            value['cache_delta_known']=measured['cache_delta_known']\n            if cause == 'unknown':\n                for key in ('evidence','estimate_note','errno_messages','cache_delta_known','filesystem_device'):\n                    value.pop(key,None)\n            elif baseline is None:","            if cause == 'disk': value['cache_delta_known']=measured['cache_delta_known']\n            if cause == 'unknown':\n                pass\n            elif baseline is None:",1)
p.write_text(s);(B/'tools/bolt/bolt_helper.py').write_text(s)
p=B/'tools/bolt/test_disk_diagnostics.py';s=p.read_text()
start=s.index("    elif kind=='subprocess-log':")
end=s.index("    elif kind.startswith('install'):",start)
s=s[:start]+'''    elif kind=='subprocess-log':
        log=work/'process.log';real=Path.open
        def opening(p,*a,**kw):
            if p==log and a and a[0]=='wb':raise OSError(errno.ENOSPC,'No space left on device')
            return real(p,*a,**kw)
        manager=patch.object(Path,'open',opening)
        args=['run-step','fault-log',str(log),'--',sys.executable,'-B','-c','print("not started")']
'''+s[end:]
s=s.replace("    elif kind in ('not-disk','diagnostic-exception'):\n        manager=patch.object", "    elif kind in ('not-disk','diagnostic-exception','unknown'):\n        log=work/'gate.log'\n        if kind!='unknown':log.write_text('fixture original gate failure\\n')\n        os.environ['BOLT_STEP_LOG']=str(log)\n        manager=patch.object",1)
s=s.replace('def test_parent_log_enospc_kills_child(self):','def test_log_open_enospc_stops_before_subprocess(self):')
needle="    def test_diagnosis_exception_preserves_exit_and_error(self):"
s=s.replace(needle,'''    def test_missing_log_unknown_cli(self):
        p,rows,state=self.run_fault('unknown');self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['cause'],'unknown');self.assertEqual(rows[0]['reason'],'日志不可用，无法判定原因')
        self.assertIn('used_bytes',rows[0]);self.assertIn('free_bytes',rows[0]);self.assertNotIn('estimated_total_bytes',rows[0])
        self.assertEqual(p.stderr,'BOLT_GATE_FAILED: fixture original gate failure\\n')
'''+needle,1)
s=s.replace("        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':0})()),contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('step','-',build=build,work=work)","        log=work/'ordinary.log';log.write_text('ordinary gate failure\\n')\n        with patch.object(h.shutil,'disk_usage',return_value=type('Disk',(),{'free':0})()),contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('step',log,build=build,work=work)",1)
s=s.replace("self.assertEqual(value['cause'],'not-disk')\n    def test_diagnose_performs_no_file_writes", "self.assertEqual(value['cause'],'unknown')\n    def test_empty_and_unreadable_log_are_unknown(self):\n        build,work,root=fixture(self.d);log=work/'empty.log';log.write_text('')\n        with contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('empty',log,build=build,work=work)\n        self.assertEqual(value['cause'],'unknown');self.assertIn('used_bytes',value)\n        original=Path.read_text\n        def reading(path,*a,**kw):\n            if path==log:raise PermissionError('fixture unreadable log')\n            return original(path,*a,**kw)\n        with patch.object(Path,'read_text',reading),contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('unreadable',log,build=build,work=work)\n        self.assertEqual(value['cause'],'unknown');self.assertIn('used_bytes',value);self.assertNotIn('formulas',value)\n    def test_successful_log_text_does_not_fail_call(self):\n        log=self.d/'success.log'\n        self.assertEqual(h.call(['/bin/sh','-c','printf ENOSPC'],log),'ENOSPC')\n        self.assertTrue(json.loads((self.d/'success.log.argv.json').read_text())['completed'])\n    def test_stdin_failure_log_consumed_once(self):\n        build,work,root=fixture(self.d);real=Path.read_text;count=[]\n        def reading(path,*a,**kw):\n            if path==Path('/dev/stdin'):\n                count.append(1);return 'Disk quota exceeded' if len(count)==1 else ''\n            return real(path,*a,**kw)\n        with patch.object(Path,'read_text',reading),contextlib.redirect_stdout(io.StringIO()):value=h.disk_diagnose('stdin','/dev/stdin',build=build,work=work)\n        self.assertEqual(value['cause'],'disk');self.assertEqual(value['evidence'],['Disk quota exceeded']);self.assertEqual(len(count),1)\n    def test_diagnose_performs_no_file_writes",1)
p.write_text(s)
