import pathlib,json,hashlib,shutil,subprocess,os,datetime
E=pathlib.Path(__file__).resolve().parent;B=E.parents[3];W=pathlib.Path('/home/linhao/Toolchain/development/llvm-optimize')
entry=pathlib.Path('tools/bolt/rebase-launch-20261111-r6')
records=json.loads((B/'tools/bolt/results/handover-20261114/entry-copy-drift.json').read_text())
allowed=['run-night.sh','test_serial.py','basedev/launcher.py','README.md','SHA256SUMS']
assert [d['relative'] for d in records]==allowed
backup=E/'entry-before';backup.mkdir()
out={'status':'STOP','files':[],'tests':'NOT RUN','dry_run':'NOT RUN'}
def save():
 out['time']=datetime.datetime.now().astimezone().isoformat()
 (E/'step2-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print('86步骤2 已结束 '+out['time']+' status='+out['status']+' reason='+out.get('reason','completed'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n in allowed:
 src=B/entry/n;dst=W/entry/n;bk=backup/n;bk.parent.mkdir(exist_ok=True,parents=True)
 assert src.is_file() and dst.is_file() and not dst.is_symlink()
 shutil.copy2(dst,bk)
 out['files'].append({'relative':n,'before_sha256':sha(dst),'B_sha256':sha(src),'backup_sha256':sha(bk)})
(E/'entry-before-manifest.json').write_text(json.dumps(out['files'],indent=2)+'\n')
for n in allowed:shutil.copyfile(B/entry/n,W/entry/n)
for d in out['files']:
 d['after_sha256']=sha(W/entry/d['relative'])
 assert d['after_sha256']==d['B_sha256']
p=subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=W/entry,capture_output=True,text=True)
(E/'entry-sha-check.stdout').write_text(p.stdout);(E/'entry-sha-check.stderr').write_text(p.stderr)
out['sha256sum_rc']=p.returncode
if p.returncode:
 out['reason']='SHA256SUMS mismatch after authorized five-file sync; no rollback/retry'
 out['failed_lines']=[l for l in p.stdout.splitlines() if not l.endswith(': OK')]
 save();raise SystemExit(0)
env=dict(os.environ,SERIAL_ENTRY=str(W/entry),SERIAL_TEST_ROOT=str(E/'entry-fixtures'),PYTHONDONTWRITEBYTECODE='1')
try:
 p=subprocess.run(['python3','-B',str(W/entry/'test_serial.py'),'-v'],cwd=W/entry,env=env,capture_output=True,text=True,timeout=180)
except subprocess.TimeoutExpired as ex:
 out['reason']='test timeout; no retry';save();raise SystemExit(0)
(E/'entry-tests.stdout').write_text(p.stdout);(E/'entry-tests.stderr').write_text(p.stderr)
out['tests']=dict(rc=p.returncode,expected=30)
if p.returncode or 'Ran 30 tests' not in p.stderr:
 out['reason']='entry tests not 30/30 PASS';save();raise SystemExit(0)
p=subprocess.run(['/bin/sh',str(W/entry/'run-night.sh'),'fea0fe464d56e17f2c7588c557bfffd9f6ac352b','--dry-run'],cwd=W/entry,capture_output=True,text=True)
(E/'entry-dry-run.stdout').write_text(p.stdout);(E/'entry-dry-run.stderr').write_text(p.stderr)
out['dry_run']=dict(rc=p.returncode)
if p.returncode:out['reason']='dry-run failed';save();raise SystemExit(0)
out['status']='PASS';save()
