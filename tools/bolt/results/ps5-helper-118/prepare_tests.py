from pathlib import Path
import shutil,json,difflib,ast
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=B/'tools/bolt/results/ps5-helper-118';O=B/'tools/bolt/results/ps5-helper-114';T=E/'tests';T.mkdir()
copied=[];diffs=[]
for folder in ['', 'environment','helper-suite','external']:
 src=O/'tests'/folder;dest=T/folder;dest.mkdir(exist_ok=True)
 files=list(src.glob('*')) if folder!='external' else list(src.rglob('*'))
 for p in files:
  if not p.is_file() or (folder=='' and p.suffix!='.py'):continue
  if '__pycache__' in p.parts:continue
  q=dest/p.relative_to(src);q.parent.mkdir(parents=True,exist_ok=True)
  data=p.read_bytes()
  if p.suffix=='.py':
   before=data.decode();after=before.replace('/temp/ps5-helper-114/source','/temp/ps5-helper-118/source').replace('/results/ps5-helper-114/','/results/ps5-helper-118/')
   data=after.encode()
   if before!=after:diffs.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=str(p),tofile=str(q)))
  q.write_bytes(data);copied.append({'source':str(p),'target':str(q),'bytes':len(data)})
for name in ['test_p1p2.py','post_macro_gate.py']:
 before=(O/name).read_text();after=before.replace('temp/ps5-helper-114/source','temp/ps5-helper-118/source')
 # 118 uses one-shot resource-constrained services, not the 114 task's process
 # admission scanner (which would inspect unrelated project processes).
 after=after.replace("__import__('runpy').run_path(str(E/'test-admission.py'))['check']()", "# Admission controlled by the task118 service resource limits.")
 (E/name).write_text(after);diffs.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=str(O/name),tofile=str(E/name)))
(E/'test-copy-manifest.json').write_text(json.dumps(copied,indent=2))
(E/'test-path-adaptation.diff').write_text(''.join(diffs))
p=T/'test_114.py';before=p.read_text();s=before
s=s.replace("self.assertEqual(output.getvalue(),'SESSION_KILL_MODE=fallback-recheck\\n')","self.assertEqual(output.getvalue(),'SESSION_KILL_MODE=fallback-recheck'+(' errno='+errno.errorcode[error.errno] if isinstance(error,OSError) else '')+'\\n')")
s=s.replace("patch.object(h,'live_session_members',return_value=[(31,'R',1),(32,'S',2)]),patch.object(h,'kill_session_member',side_effect=[PermissionError('denied 31'),None])", "patch.object(h,'live_session_members',side_effect=[[(31,'R',1),(32,'S',2)],[(31,'R',1),(32,'S',2)],[]]),patch.object(h,'kill_session_member',side_effect=[PermissionError('denied 31'),None,None,None])")
s=s.replace("self.assertEqual([c.args[1] for c in kill.call_args_list],[31,32])","self.assertEqual([c.args[1] for c in kill.call_args_list],[31,32,31,32])")
def replace_method(name,body):
 global s
 tree=ast.parse(s);node=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==name)
 lines=s.splitlines(True);s=''.join(lines[:node.lineno-1])+body+'\n'+''.join(lines[node.end_lineno:])
replace_method('test_deadline_partial_scan_never_empty_success',"""    def test_deadline_partial_scan_never_empty_success(self):
        h=self.h; clock=[0]
        a,b=self.scan_context({31:(31,'R',31,1,42,1),32:(32,'R',32,1,42,2)})
        with a,b:
            original=h.proc_stat.side_effect
            def stat(path):
                result=original(path)
                if path=='/proc/31/stat':clock[0]=2
                return result
            h.proc_stat.side_effect=stat
            with patch.object(h.time,'monotonic',side_effect=lambda:clock[0]),self.assertRaisesRegex(h.SessionDeadlineError,'scan incomplete') as caught:
                h.live_session_members(42,1)
        self.assertEqual(caught.exception.members,[(31,'R',1)])
""")
replace_method('test_deadline_after_empty_scan_fails',"""    def test_deadline_after_empty_scan_fails(self):
        h=self.h;clock=[0];a,b=self.scan_context({})
        def entries():
            clock[0]=2
            yield from ()
        with a,b,patch.object(h.time,'monotonic',side_effect=lambda:clock[0]):
            h.os.scandir.return_value.__enter__.return_value=entries()
            with self.assertRaisesRegex(h.GateError,'scan incomplete'):h.live_session_members(42,1)
""")
replace_method('test_deadline_checked_between_kills',"""    def test_deadline_checked_between_kills(self):
        h=self.h;clock=[0]
        def kill_one(*args):clock[0]=2
        with patch.object(h,'live_session_members',return_value=[(31,'R',1),(32,'R',2)]),patch.object(h.time,'monotonic',side_effect=lambda:clock[0]),patch.object(h,'kill_session_member',side_effect=kill_one) as kill:
            with self.assertRaisesRegex(h.GateError,'deadline'):h.wait_session_exit(42,1,kill=True)
        self.assertEqual(kill.call_count,1)
""")
replace_method('test_deadline_after_pidfd_read_no_signal',"""    def test_deadline_after_pidfd_read_no_signal(self):
        h=self.h;h._SESSION_KILL_MODE='pidfd';clock=[0]
        def stat(*args):clock[0]=2;return (31,'R',31,1,42,1)
        with patch.object(h.os,'pidfd_open',return_value=71),patch.object(h.os,'close') as close,patch.object(h,'proc_stat',side_effect=stat),patch.object(h.time,'monotonic',side_effect=lambda:clock[0]),patch.object(h.signal,'pidfd_send_signal') as send:
            with self.assertRaises(h.SessionDeadlineError):h.kill_session_member(42,31,1,1)
        send.assert_not_called();close.assert_called_once_with(71)
""")
p.write_text(s);(E/'test-114-authorized-adaptation.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),s.splitlines(True),fromfile='114/test_114.py',tofile='118/test_114.py')))
for f in T.rglob('*.py'):compile(f.read_text(),str(f),'exec')
print('copied',len(copied),'test114',sum(isinstance(n,ast.FunctionDef) and n.name.startswith('test_') for n in ast.walk(ast.parse(s))))
print('invocation', (B/'tools/bolt/results/fifth-review-20261111/rerun3/test-invocation.json').read_text()[:2500])
