"""Local-only restart after host reboot; no source/spec edits."""
from pathlib import Path
import os,subprocess,time,signal,json,traceback
C=Path('/home/abuild/oldtext-resume-20261027');C.mkdir(exist_ok=True)
cmd=['/usr/bin/rpmbuild','--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20','--define','_srcdefattr (-,root,root)','--nosignature','--target=x86_64','--define','_build_create_debug 1','-ba','--noprep','/home/abuild/rpmbuild/SOURCES/llvm.spec']
env={'SHELL':'/bin/bash','LC_ALL':'POSIX','USER':'abuild','PATH':'/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LANG':'POSIX','HOME':'/home/abuild','LOGNAME':'abuild'}
p=None;mounted=False;rc=1;signal_received=False

def stop(sig,frame):
 global signal_received
 signal_received=True
signal.signal(signal.SIGTERM,stop);signal.signal(signal.SIGINT,stop)
def abuild():os.setgroups([]);os.setgid(1000);os.setuid(1000)
try:
 subprocess.run(['/bin/mount','-n','-tproc','none','/proc'],check=True);mounted=True
 print('RESUME_PROC_MOUNTED',flush=True);print('RESUME_ARGV '+json.dumps(cmd),flush=True)
 p=subprocess.Popen(cmd,env=env,cwd='/home/abuild',preexec_fn=abuild,start_new_session=True)
 while p.poll() is None:
  if signal_received or (C/'STOP').exists():
   print('RESUME_NORMAL_STOP_REQUESTED',flush=True);os.killpg(p.pid,signal.SIGTERM)
   try:p.wait(timeout=90)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
   break
  time.sleep(2)
 rc=p.wait()
except BaseException:
 traceback.print_exc()
 if p is not None and p.poll() is None:
  os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=90)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
finally:
 if mounted:
  q=subprocess.run(['/bin/umount','/proc'],capture_output=True,text=True,timeout=30)
  print('RESUME_PROC_UMOUNT '+json.dumps({'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr}),flush=True)
 (C/'result.json').write_text(json.dumps({'rpm_rc':rc,'signal_received':signal_received})+'\n')
 print('RESUME_RPM_EXIT '+str(rc),flush=True)
raise SystemExit(0 if rc==0 else 1)
