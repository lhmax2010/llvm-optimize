import ctypes, importlib.util, os, signal, subprocess, sys, time, json
from pathlib import Path
from unittest import mock
BASE=Path(os.environ['CODEX_SCRATCH'])

def load(name,file):
 s=importlib.util.spec_from_file_location(name,BASE/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
h=load('bolt','clang-bolt-helper.py');c=load('native','llvm-static-archives-native.py')
rows=[]
def result(name,**kw):
 rows.append(dict(test=name,**kw));print(json.dumps(rows[-1]),flush=True)
# Act as the test's subreaper so even forced-exit cases are fully cleaned up.
assert ctypes.CDLL(None).prctl(36,1,0,0,0)==0
runner='''import importlib.util,os,signal,sys
from pathlib import Path
p=Path(sys.argv[1]); mode=sys.argv[2]
s=importlib.util.spec_from_file_location('h',p/'clang-bolt-helper.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
real=h.subprocess.Popen
fired=False
def popen(*a,**k):
 if mode=='failure_second':
  os.kill(os.getpid(),signal.SIGTERM);os.kill(os.getpid(),signal.SIGTERM)
  raise FileNotFoundError('injected Popen error')
 child=real(*a,**k)
 (p/(mode+'.pid')).write_text(str(child.pid))
 if mode in ('first','second','finally_second','finally_third'):
  os.kill(os.getpid(),signal.SIGTERM)
 if mode in ('second','finally_third'):
  os.kill(os.getpid(),signal.SIGTERM)
 return child
def trace(frame,event,arg):
 global fired
 if event=='line' and frame.f_code.co_name=='call' and frame.f_lineno==318 and not fired and mode in ('finally_second','finally_third'):
  fired=True;os.kill(os.getpid(),signal.SIGHUP)
 return trace
h.subprocess.Popen=popen
sys.settrace(trace)
h.main=lambda:h.call(['/bin/sleep','30'],p/(mode+'.log'),timeout=1)
sys.exit(h.cli())
'''
for mode in ('first','second','finally_second','finally_third','failure_second'):
 p=subprocess.Popen([sys.executable,'-B','-c',runner,str(BASE),mode],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out,err=p.communicate(timeout=15)
 pidfile=BASE/(mode+'.pid');status=None
 if pidfile.exists():
  pid=int(pidfile.read_text())
  try:
   deadline=time.monotonic()+3
   while True:
    done,st=os.waitpid(pid,os.WNOHANG)
    if done:status=os.waitstatus_to_exitcode(st);break
    if time.monotonic()>deadline:
     os.killpg(pid,signal.SIGKILL);os.waitpid(pid,0);status='survived; cleaned by test';break
    time.sleep(.01)
  except ChildProcessError:status='already reaped by helper'
 result('H2_'+mode,helper_rc=p.returncode,child_status=status)
# H1 actual child success, error, timeout, and injected BaseExceptions.
for mode in ('success','error','timeout','SystemExit','KeyboardInterrupt'):
 children=[];real=h.subprocess.Popen
 def capture(*a,**k):
  p=real(*a,**k);children.append(p);return p
 old=signal.signal(signal.SIGCHLD,signal.SIG_IGN)
 h._CANCEL_SIGNAL=None
 try:
  with mock.patch.object(h.subprocess,'Popen',capture):
   cmd=['/bin/sh','-c','exit 0' if mode=='success' else 'exit 7' if mode=='error' else 'sleep 30']
   caught=None
   try:
    if mode in ('SystemExit','KeyboardInterrupt'):
     with mock.patch.object(h,'peek_child_exit',side_effect=SystemExit(2) if mode=='SystemExit' else KeyboardInterrupt()):h.call(cmd,BASE/(mode+'.log'),timeout=.05)
    else:h.call(cmd,BASE/(mode+'.log'),timeout=.05)
   except BaseException as e:caught=type(e).__name__
  reaped=[]
  for p in children:
   try:os.waitpid(p.pid,os.WNOHANG);reaped.append(False)
   except ChildProcessError:reaped.append(True)
  result('H1_'+mode,exception=caught,restored_IGN=signal.getsignal(signal.SIGCHLD)==signal.SIG_IGN,direct_children_reaped=all(reaped))
 finally:signal.signal(signal.SIGCHLD,old)
# H5 covers argparse and BaseException with outer restore.
for mode in ('argparse','success','error','SystemExit','KeyboardInterrupt'):
 old=signal.signal(signal.SIGCHLD,signal.SIG_IGN);caught=None
 try:
  try:
   if mode=='argparse':
    with mock.patch.object(sys,'argv',['native']):c.install_main()
   else:
    effect={'success':None,'error':RuntimeError('test'),'SystemExit':SystemExit(2),'KeyboardInterrupt':KeyboardInterrupt()}[mode]
    with mock.patch.object(c,'_install_main',return_value=0,side_effect=effect):c.install_main()
  except BaseException as e:caught=type(e).__name__
  result('H5_'+mode,exception=caught,restored_IGN=signal.getsignal(signal.SIGCHLD)==signal.SIG_IGN)
 finally:signal.signal(signal.SIGCHLD,old)
# N1 mocked non-Python disposition: neither helper may restore None.
for module in (h,c):
 real_get=signal.getsignal;real_set=signal.signal
 def get(sig):return None if sig==signal.SIGCHLD else real_get(sig)
 def set_(sig,handler):
  assert handler is not None
  return real_set(sig,handler)
 with mock.patch.object(signal,'getsignal',get),mock.patch.object(signal,'signal',set_):
  if module is h:h.call(['/bin/true'],BASE/'none.log')
  else:
   with mock.patch.object(c,'_install_main',return_value=0):c.install_main()
 result('N1_'+module.__name__,passed=True)
# H4 normal and thin archives, including first table empty.
def member(name,data,size=None):
 n=len(data) if size is None else size
 header=f'{name:<16}{0:<12}{0:<6}{0:<6}{0:<8}{n:<10}`\n'.encode()
 assert len(header)==60
 return header+data+(b'\n' if len(data)%2 else b'')
for thin in (False,True):
 for first in (b'',b'name.bc/\n'):
  p=BASE/f'ar-{thin}-{len(first)}.a';p.write_bytes((b'!<thin>\n' if thin else b'!<arch>\n')+member('//',first)+member('//',b'another.bc/\n'))
  try:c.inspect(p);verdict='ACCEPT'
  except ValueError as e:verdict=str(e)
  result('H4_duplicate',thin=thin,first_empty=not first,verdict=verdict)
 for table in (b'',b'long-name.bc/\n'):
  p=BASE/f'valid-{thin}-{len(table)}.a';data=(b'!<thin>\n' if thin else b'!<arch>\n')+member('//',table)
  if table:data+=member('/0',b'' if thin else b'BC\xc0\xde',size=4)
  p.write_bytes(data);v=c.inspect(p)
  result('H4_valid',thin=thin,table_empty=not table,members=v['member_count'])
# H3 missing path permitted for release; debug requires actual listing.
result('H3_release',value=h.debugfiles_gate(BASE/'nonexistent',{}))
lst=BASE/'space dir'/'debugfiles.list';lst.parent.mkdir();lst.write_text('/'+h.DEBUG_INSTALL_PATH+'\n')
result('H3_debug',required=h.debugfiles_gate(lst,{'debug_file':{}})['required'])
# Existing successful-leader descendant escape, caught and cleaned by this test.
code='import os,time\np=os.fork()\nif p: print(p,flush=True);os._exit(0)\ntime.sleep(30)\n'
log=BASE/'orphan.log'
try:
 h.call([sys.executable,'-c',code],log)
 raise AssertionError('R1 must reject a successful leader with live descendants')
except h.GateError as error:
 assert 'command exited successfully with live descendants' in str(error),str(error)
pid=int(log.read_text().strip())
_,status=os.waitpid(pid,0)
assert os.waitstatus_to_exitcode(status)==-signal.SIGKILL,status
result('successful_leader_descendant',call_rejected=True,descendant_status=os.waitstatus_to_exitcode(status))
# Reap any adopted grandchildren from shell timeout/interrupt cases.
while True:
 try:
  pid,status=os.waitpid(-1,os.WNOHANG)
  if not pid:break
 except ChildProcessError:break
(BASE/'test-results.json').write_text(json.dumps(rows,indent=2)+'\n')
