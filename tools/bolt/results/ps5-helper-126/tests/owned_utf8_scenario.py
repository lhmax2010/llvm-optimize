import ctypes,importlib.util,json,os,select,signal,subprocess,sys,time
from pathlib import Path
H,W=sys.argv[1:3];W=Path(W)
assert ctypes.CDLL(None,use_errno=True).prctl(36,1,0,0,0)==0
ME=os.getpid()
def own_children():
 out=[]
 for entry in os.scandir('/proc'):
  if not entry.name.isdecimal():continue
  try:f=Path(entry.path+'/stat').read_bytes().rsplit(b')',1)[1].split()
  except OSError:continue
  if int(f[1])==ME:out.append((int(entry.name),f[0]))
 return out
spec=importlib.util.spec_from_file_location('h126',H);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
child="import ctypes,os,time; os.setpgid(0,0); assert ctypes.CDLL(None).prctl(15,b'\\xff\\xfe',0,0,0)==0; print('ready',flush=True); time.sleep(40)"
leader="import subprocess,sys,time,os,json; from pathlib import Path; p=subprocess.Popen([sys.executable,'-u','-c',"+repr(child)+"],stdout=subprocess.PIPE,text=True); assert p.stdout.readline().strip()=='ready'; Path(sys.argv[1]).write_text(json.dumps({'pid':p.pid,'sid':os.getsid(p.pid),'pgrp':os.getpgid(p.pid),'leader':os.getpid()})); time.sleep(40)"
observations=[];real=h.session_snapshot
def snapshot(members):
 text=real(members);observations.append(text);return text
h.session_snapshot=snapshot
result={}
try:
 try:h.call([sys.executable,'-u','-c',leader,str(W/'member.json')],W/'member.log',timeout=1)
 except h.GateError as e:result['error']=str(e)
 result['identity']=json.loads((W/'member.json').read_text());result['snapshots']=observations
 pid=result['identity']['pid'];owned=own_children();result['owned_after']= [(p,s.decode()) for p,s in owned]
 assert any(p==pid for p,s in owned),'member must be an owned unreaped adopted child'
 fd=os.pidfd_open(pid)
 try:result['member_dead']=bool(select.select([fd],[],[],0)[0])
 finally:os.close(fd)
finally:
 # All targets remain our own unreaped children; pidfds pin identity.
 for pid,state in own_children():
  if state not in (b'Z',b'X'):
   fd=os.pidfd_open(pid)
   try:signal.pidfd_send_signal(fd,signal.SIGKILL)
   finally:os.close(fd)
  os.waitpid(pid,0)
 result['remaining_owned']=own_children()
print(json.dumps(result))
