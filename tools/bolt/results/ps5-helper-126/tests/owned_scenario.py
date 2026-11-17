import ctypes, errno, importlib.util, json, os, select, signal, subprocess, sys, time, types
from pathlib import Path
H, directory, case=sys.argv[1:]
d=Path(directory);d.mkdir()
spec=importlib.util.spec_from_file_location('helper',H);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);h._SESSION_KILL_MODE='pidfd'
assert ctypes.CDLL(None,use_errno=True).prctl(36,1,0,0,0)==0
leader_code=r'''
import json,os,subprocess,sys,time
from pathlib import Path
d=Path(sys.argv[1]);kids=[]
def child():
 p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'],process_group=0)
 kids.append(p);(d/'children.json').write_text(json.dumps([p.pid for p in kids]))
child();child();(d/'ready').write_text('ready')
while True:
 if (d/'trigger').exists() and len(kids)==2:
  child();(d/'forked').write_text('forked')
 time.sleep(.005)
'''
p=subprocess.Popen([sys.executable,'-c',leader_code,str(d)],start_new_session=True)
fds={};opened=[];calls=[];real_open=os.pidfd_open;real_send=signal.pidfd_send_signal
def until(path):
 end=time.monotonic()+5
 while not path.exists() and time.monotonic()<end:time.sleep(.005)
 assert path.exists(),str(path)
def hold():
 for pid in [p.pid]+json.loads((d/'children.json').read_text()):
  if pid not in fds:fds[pid]=real_open(pid)
def fd_pid(fd):
 return int(next(l.split()[1] for l in Path('/proc/self/fdinfo/%d'%fd).read_text().splitlines() if l.startswith('Pid:')))
fired=False
def fault():
 global fired
 fired=True
 (d/'trigger').write_text('go');until(d/'forked');hold()
def open_proxy(pid,flags=0):
 calls.append(pid)
 if pid==p.pid and not fired and case in ('emfile','enomem'):
  fault();code={'emfile':errno.EMFILE,'enomem':errno.ENOMEM}[case]
  raise OSError(code,'injected member '+case)
 return real_open(pid,flags)
def send_proxy(fd,sig,info=None,flags=0):
 global fired
 pid=fd_pid(fd)
 if pid==p.pid and sig==signal.SIGKILL and not fired:
  if case=='permission':
   fault();raise PermissionError(errno.EPERM,'injected member denial')
  if case=='esrch':
   fired=True;real_send(fd,sig,info,flags)
   raise ProcessLookupError(errno.ESRCH,'exited between acquisition and send')
 return real_send(fd,sig,info,flags)
try:
 until(d/'ready');hold()
 h.os=types.SimpleNamespace(**vars(os));h.signal=types.SimpleNamespace(**vars(signal));h.os.pidfd_open=open_proxy;h.signal.pidfd_send_signal=send_proxy
 message=None
 try:h.wait_session_exit(p.pid,3,kill=True)
 except h.GateError as e:message=str(e)
 assert (message is None)==(case=='esrch'),message
 if case!='esrch':
  assert 'PID '+str(p.pid) in message,message
  assert len(fds)==4,len(fds)
  assert calls.count(p.pid)>=2,calls
 poll=select.poll()
 for fd in fds.values():poll.register(fd,select.POLLIN)
 remaining=set(fds.values());end=time.monotonic()+3
 while remaining and time.monotonic()<end:
  remaining-={fd for fd,ev in poll.poll(50) if ev&select.POLLIN}
 assert not remaining,remaining
 assert p.wait(timeout=3)==-signal.SIGKILL
 print(json.dumps({'case':case,'PASS':True,'owned_processes':len(fds),'member_attempts':calls,'error':message,'groups':[p.pid]+list(fds)[1:]}))
finally:
 # Only descriptors for children this scenario created; never arbitrary PIDs.
 for fd in fds.values():
  try:real_send(fd,signal.SIGKILL)
  except ProcessLookupError:pass
  finally:os.close(fd)
 if p.poll() is None:p.kill()
 p.wait(timeout=3)
 end=time.monotonic()+3
 while time.monotonic()<end:
  try:
   pid,_=os.waitpid(-1,os.WNOHANG)
   if not pid:time.sleep(.01)
  except ChildProcessError:break
