# Isolated coordinator fixtures: no real systemd services or builds.
from pathlib import Path
import os,sys,subprocess,json,unittest
ENTRY=Path(os.environ.get('SERIAL_ENTRY',str(Path(__file__).parent)))
ROOT=Path(os.environ['SERIAL_TEST_ROOT']);ROOT.mkdir(exist_ok=False)
SHA='fea0fe464d56e17f2c7588c557bfffd9f6ac352b'
class SerialTests(unittest.TestCase):
 def scenario(self,*,launch_rc=0,live='',query_failure=False,missing=False,invalid=False,tstatus='ok',free=100*1024**3,dry=False,state='inactive',existing=False):
  d=ROOT/self._testMethodName;d.mkdir();work=d/'work';work.mkdir();entry=d/'entry';entry.mkdir();fake=d/'bin';fake.mkdir()
  text=(ENTRY/'run-night.sh').read_text();changed=text.replace('work=/home/linhao/Toolchain/development/llvm-optimize','work='+str(work));assert changed!=text
  (entry/'run-night.sh').write_text(changed)
  for project in ('toolchain','basedev'):
   p=entry/project;p.mkdir()
   script='''#!/bin/sh
set -eu
project=PROJECT
printf '%s\n' "$project" >> "$MOCK_CALLS"
root=$MOCK_WORK/temp/rebase-359934-20261111-r6/$project
mkdir -p "$root/evidence"
if [ "$project" = toolchain ]; then
 printf 'accepted\n' > "$root/controller-accepted"
 if [ "$MOCK_RC" -ne 0 ]; then exit "$MOCK_RC"; fi
fi
status=ok
if [ "$project" = toolchain ]; then status=$MOCK_TSTATUS; fi
if [ "$project" = toolchain ] && [ "$MOCK_MISSING" = yes ]; then exit 0; fi
if [ "$project" = toolchain ] && [ "$MOCK_INVALID" = yes ]; then
 printf 'invalid json\n' > "$root/evidence/result.json"
else
 printf '{"status":"%s","reason":"fixture"}\n' "$status" > "$root/evidence/result.json"
fi
printf 'fixture last build line\n' > "$root/evidence/rpm-build.log"
'''.replace('PROJECT',project)
   (p/'launch.sh').write_text(script)
  (fake/'systemctl').write_text('''#!/bin/sh
case "$*" in
 *list-units*)
  if [ "$MOCK_QUERY_FAILURE" = yes ]; then exit 5; fi
  if [ -n "$MOCK_LIVE" ]; then
   printf 'rebase359934r6-toolchain-full-prep-20261111.service loaded %s running fixture\n' "$MOCK_LIVE"
  else
   printf 'rebase359934r6-toolchain-full-controller-20261111.service loaded inactive dead fixture\n'
  fi ;;
 *show*) printf '%s\n' "$MOCK_STATE" ;;
 *) exit 8 ;;
esac
''');(fake/'systemctl').chmod(0o755)
  (fake/'python3').write_text('''#!/bin/sh
case "$*" in
 *'shutil.disk_usage("/home").free'*) printf '%s\n' "$MOCK_FREE" ;;
 *) exec REALPY "$@" ;;
esac
'''.replace('REALPY',sys.executable));(fake/'python3').chmod(0o755)
  env=dict(os.environ,PATH=str(fake)+':'+os.environ['PATH'],MOCK_CALLS=str(d/'calls'),MOCK_WORK=str(work),MOCK_RC=str(launch_rc),MOCK_LIVE=live,MOCK_QUERY_FAILURE='yes' if query_failure else 'no',MOCK_MISSING='yes' if missing else 'no',MOCK_INVALID='yes' if invalid else 'no',MOCK_TSTATUS=tstatus,MOCK_FREE=str(free),MOCK_STATE=state)
  if existing:(work/'temp/rebase-359934-20261111-r6/toolchain').mkdir(parents=True)
  argv=['/bin/sh',str(entry/'run-night.sh'),SHA]+(['--dry-run'] if dry else [])
  r=subprocess.run(argv,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True)
  calls=(d/'calls').read_text().splitlines() if (d/'calls').exists() else []
  log=work/'temp/night-20261111-r6/night.log';output=log.read_text() if log.exists() else ''
  (d/'result.json').write_text(json.dumps(dict(argv=argv,rc=r.returncode,calls=calls,stdout=r.stdout,stderr=r.stderr,night_log=output),indent=2)+'\n')
  if not dry:self.assertIn('NIGHT_PROJECT 已结束',output);self.assertIn('NIGHT 已结束',output);self.assertIn('reason=',output)
  return r,calls,output,work
 def stopped(self,**kw):
  r,calls,out,work=self.scenario(**kw);self.assertEqual(calls,['toolchain']);self.assertEqual(r.returncode,2);return out
 def test_controller_accepted_launch_returns7(self):self.assertIn('launcher-failed-rc-7',self.stopped(launch_rc=7))
 def test_controller_failed_prep_active(self):self.stopped(live='active',state='failed')
 def test_child_activating(self):self.stopped(live='activating')
 def test_child_deactivating(self):self.stopped(live='deactivating')
 def test_missing_result(self):self.assertIn('missing-or-invalid-result',self.stopped(missing=True))
 def test_invalid_result(self):self.stopped(invalid=True)
 def test_subservice_query_fails(self):self.assertIn('project-services-query-failed',self.stopped(query_failure=True))
 def test_T_failed_complete_runs_D(self):
  r,calls,out,w=self.scenario(tstatus='failed');self.assertEqual(calls,['toolchain','basedev']);self.assertEqual(r.returncode,1)
 def test_T_stopped_complete_runs_D(self):
  r,calls,out,w=self.scenario(tstatus='stopped');self.assertEqual(calls,['toolchain','basedev']);self.assertEqual(r.returncode,1)
 def test_disk_insufficient_before_D(self):
  out=self.stopped(free=79*1024**3);self.assertIn('available_bytes='+str(79*1024**3),out);self.assertIn('insufficient-space-before-D',out)
 def test_both_success(self):
  r,calls,out,w=self.scenario();self.assertEqual(calls,['toolchain','basedev']);self.assertEqual(r.returncode,0)
 def test_dry_run_no_effects(self):
  r,calls,out,w=self.scenario(dry=True);self.assertEqual(r.returncode,0);self.assertEqual(calls,[]);self.assertFalse((w/'temp').exists());self.assertIn('DRY_RUN',r.stdout)
 def test_launch_signal_codes(self):
  for signal_rc in (129,130,143):
   old=self._testMethodName;self._testMethodName=old+'-'+str(signal_rc)
   try:r,calls,out,w=self.scenario(launch_rc=signal_rc)
   finally:self._testMethodName=old
   self.assertEqual(calls,['toolchain']);self.assertEqual(r.returncode,signal_rc)
 def test_existing_root_refused(self):
  r,calls,out,w=self.scenario(existing=True);self.assertEqual(calls,[]);self.assertEqual(r.returncode,2);self.assertIn('fresh-root-required',out)
 def test_controller_state_empty(self):self.stopped(state='')
 def test_basedev_reject_legacy_branches(self):
  for args in ([SHA,'night'],[SHA,'rehearsal','toolchain'],[SHA,'rehearsal-02','toolchain'],[SHA,'full','toolchain']):
   r=subprocess.run(['/bin/sh',str(ENTRY/'basedev/launch.sh'),*args],capture_output=True,text=True);self.assertEqual(r.returncode,2,args)
if __name__=='__main__':unittest.main(verbosity=2,failfast=True)
