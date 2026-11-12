# Isolated coordinator fixtures: no real systemd services or builds.
from pathlib import Path
import os,sys,subprocess,json,unittest,time,signal
ENTRY=Path(os.environ.get('SERIAL_ENTRY',str(Path(__file__).parent)))
ROOT=Path(os.environ['SERIAL_TEST_ROOT']);ROOT.mkdir(exist_ok=False)
SHA='fea0fe464d56e17f2c7588c557bfffd9f6ac352b'
class SerialTests(unittest.TestCase):
 def scenario(self,*,launch_rc=0,live='',query_failure=False,missing=False,invalid=False,tstatus='ok',free=100*1024**3,dry=False,state='inactive',existing=False,rows=None,missing_d=False,disk_rc=0,poll_signal=False,linger='yes'):
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
if [ "$project" = basedev ] && [ "$MOCK_MISSING_D" = yes ]; then exit 0; fi
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
  if [ "$MOCK_ROWS_SET" = yes ]; then printf '%s\\n' "$MOCK_ROWS"; exit 0; fi
  if [ -n "$MOCK_LIVE" ]; then
   printf 'rebase359934r6-toolchain-full-prep-20261111.service loaded %s running fixture\n' "$MOCK_LIVE"
  else
   printf 'rebase359934r6-toolchain-full-controller-20261111.service loaded inactive dead fixture\n'
  fi ;;
 *show*) : > "$MOCK_POLL_MARKER"; printf '%s\n' "$MOCK_STATE" ;;
 *) exit 8 ;;
esac
''');(fake/'systemctl').chmod(0o755)
  (fake/'python3').write_text('''#!/bin/sh
case "$*" in
 *'shutil.disk_usage("/home").free'*) [ "$MOCK_DISK_RC" -eq 0 ] || exit "$MOCK_DISK_RC"; printf '%s\n' "$MOCK_FREE" ;;
 *) exec REALPY "$@" ;;
esac
'''.replace('REALPY',sys.executable));(fake/'python3').chmod(0o755)
  (fake/'loginctl').write_text('#!/bin/sh\nprintf \'%s\\n\' "$MOCK_LINGER"\n');(fake/'loginctl').chmod(0o755)
  (fake/'sleep').write_text('#!/bin/sh\nexec '+sys.executable+' -B -c "import time; time.sleep(.05)"\n');(fake/'sleep').chmod(0o755)
  env=dict(os.environ,PATH=str(fake)+':'+os.environ['PATH'],MOCK_CALLS=str(d/'calls'),MOCK_WORK=str(work),MOCK_RC=str(launch_rc),MOCK_LIVE=live,MOCK_QUERY_FAILURE='yes' if query_failure else 'no',MOCK_MISSING='yes' if missing else 'no',MOCK_INVALID='yes' if invalid else 'no',MOCK_TSTATUS=tstatus,MOCK_FREE=str(free),MOCK_STATE=state,MOCK_ROWS_SET="no" if rows is None else "yes",MOCK_ROWS=rows or "",MOCK_MISSING_D="yes" if missing_d else "no",MOCK_DISK_RC=str(disk_rc),MOCK_POLL_MARKER=str(d/"poll-started"),MOCK_LINGER=linger)
  if existing:(work/'temp/rebase-359934-20261111-r6/toolchain').mkdir(parents=True)
  argv=['/bin/sh',str(entry/'run-night.sh'),SHA]+(['--dry-run'] if dry else [])
  if poll_signal:
   proc=subprocess.Popen(argv,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
   deadline=time.monotonic()+10
   while not (d/'poll-started').exists() and proc.poll() is None and time.monotonic()<deadline:time.sleep(.01)
   self.assertTrue((d/'poll-started').exists(),'poll marker missing')
   proc.send_signal(signal.SIGTERM);stdout,stderr=proc.communicate(timeout=10)
   r=subprocess.CompletedProcess(argv,proc.returncode,stdout,stderr)
  else:
   r=subprocess.run(argv,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=15)
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

 def check_case(self,rc,calls,reason,**kw):
  r,actual,out,w=self.scenario(**kw)
  self.assertEqual(r.returncode,rc);self.assertEqual(actual,calls);self.assertIn('reason='+reason,out)
  return out
 def test_child_reloading(self):
  self.check_case(2,['toolchain'],'project-services-not-confirmed-ended',live='reloading')
 def test_child_maintenance(self):
  self.check_case(2,['toolchain'],'project-services-not-confirmed-ended',live='maintenance')
 def test_short_list_units_row(self):
  self.check_case(2,['toolchain'],'project-services-not-confirmed-ended',rows='broken loaded')
 def test_disk_exactly_80_GiB(self):
  self.check_case(0,['toolchain','basedev'],'serial-builds-and-validation-finished',free=85899345920)
 def test_disk_one_byte_below_80_GiB(self):
  self.check_case(2,['toolchain'],'insufficient-space-before-D',free=85899345919)
 def test_disk_query_failure(self):
  self.check_case(2,['toolchain'],'disk-query-failed',disk_rc=7)
 def test_disk_query_nonnumeric(self):
  self.check_case(2,['toolchain'],'disk-query-failed',free='not-a-number')
 def test_D_missing_result(self):
  self.check_case(2,['toolchain','basedev'],'missing-or-invalid-result.json',missing_d=True)
 def test_SIGTERM_while_polling_T(self):
  out=self.check_case(143,['toolchain'],'signal-15',state='active',poll_signal=True)
  self.assertIn('T=started D=not_run',out)
 def test_old_night_basedev_refused(self):
  r=subprocess.run(['/bin/sh',str(ENTRY/'basedev/launch.sh'),SHA,'night','basedev'],capture_output=True,text=True)
  self.assertEqual(r.returncode,2)
  self.assertNotIn('NIGHT_PROJECT',r.stdout+r.stderr) # rejected before any queue/log creation
  (ROOT/'legacy-night-result.json').write_text(json.dumps({'rc':r.returncode,'D_started':False,'reason':'CLI rejects legacy night before coordinator log','stdout':r.stdout,'stderr':r.stderr},indent=2))
 def test_direct_basedev_requires_project(self):
  env=dict(os.environ,NIGHT_SOURCE_SHA=SHA);env.pop('FINAL_PROJECT',None)
  r=subprocess.run([sys.executable,'-B',str(ENTRY/'basedev/launcher.py'),'full'],env=env,capture_output=True,text=True)
  self.assertEqual(r.returncode,1)
  self.assertIn('AssertionError: Base-Dev launcher requires FINAL_PROJECT=basedev',r.stderr)
  self.assertNotIn('NIGHT_PROJECT',r.stdout+r.stderr)
  (ROOT/'direct-launcher-result.json').write_text(json.dumps({'rc':r.returncode,'D_started':False,'reason':'assertion before configuration/side effects','stdout':r.stdout,'stderr':r.stderr},indent=2))
 def test_empty_service_list_is_ended(self):
  self.check_case(0,['toolchain','basedev'],'serial-builds-and-validation-finished',rows='')
 def test_failed_service_is_ended(self):
  self.check_case(0,['toolchain','basedev'],'serial-builds-and-validation-finished',live='failed')
 def test_linger_no_warns_and_continues(self):
  out=self.check_case(0,['toolchain','basedev'],'serial-builds-and-validation-finished',linger='no')
  self.assertIn('NIGHT_WARNING',out);self.assertIn('queue depends on user remaining logged in',out)

if __name__=='__main__':unittest.main(verbosity=2,failfast=True)
