"""Host UID-only backstop; preserve privileged cleanup, reap abuild sessions."""
import os,sys,time,json,signal,shutil
from pathlib import Path
E=Path(__file__).resolve().parent;G=1024**3
cg=Path('/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/bolt-real-install-20261015.scope')
exempt=set()
for p in (cg/'cgroup.procs').read_text().split():
 try:
  if str(E/'in_scope.py').encode() in Path('/proc/'+p+'/cmdline').read_bytes():exempt.add(int(p))
 except OSError:pass
assert len(exempt)==1,exempt
(E/'supervisor-entry.json').write_text(json.dumps({'pid':os.getpid(),'exempt_pids':sorted(exempt),'effective_uid':os.geteuid(),'deadline_seconds':3300,'purpose':'Kill abuild descendants across sessions on resource abort while leaving root wrapper alive to unmount and audit'},indent=2)+'\n')

def victims():
 result=[]
 try:pids=(cg/'cgroup.procs').read_text().split()
 except OSError:return []
 for p in pids:
  pid=int(p)
  if pid in exempt:continue
  try:
   st=Path('/proc/'+p+'/status').read_text().splitlines();uid=int(next(x for x in st if x.startswith('Uid:')).split()[2]);state=next(x for x in st if x.startswith('State:')).split()[1]
   if uid==os.geteuid() and state not in ('Z','X'):result.append(pid)
  except (OSError,StopIteration):pass
 return result
while cg.exists() and not (E/'sudo-result.json').exists():
 now=time.monotonic();available=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
 reason=None
 if now-float((E/'lock-start-monotonic').read_text())>3300:reason='shared lock 3300-second deadline, leaving 300 seconds for cleanup/audit'
 if available<3*G:reason='host MemAvailable <3 GiB'
 if shutil.disk_usage(E).free<30*G:reason='filesystem free <30 GiB'
 if (E/'exception.txt').exists():reason='root wrapper exception; reap abuild sessions for cleanup'
 if reason:
  killed=[];deadline=time.monotonic()+10;quiet=None
  while time.monotonic()<deadline:
   ps=victims()
   if not ps:
    if quiet is None:quiet=time.monotonic()
    if time.monotonic()-quiet>.75:break
   else:
    quiet=None
    for pid in ps:
     try:os.kill(pid,signal.SIGKILL);killed.append(pid)
     except ProcessLookupError:pass
   time.sleep(.1)
  (E/'supervisor-abort.json').write_text(json.dumps({'time':time.time(),'reason':reason,'killed_abuild_pids':sorted(set(killed)),'survivors':victims(),'root_and_sudo_not_signalled':True},indent=2)+'\n');break
 time.sleep(.25)
(E/'supervisor-exit.json').write_text(json.dumps({'time':time.time(),'remaining_abuild_pids':victims()},indent=2)+'\n')
