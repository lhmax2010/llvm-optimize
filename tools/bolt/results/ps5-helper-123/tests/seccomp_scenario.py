import ctypes,errno,importlib.util,json,os,platform,subprocess,sys
from pathlib import Path
H,which,work=sys.argv[1:];denied=getattr(errno,which)
assert platform.machine()=='x86_64'
header=Path('/usr/include/x86_64-linux-gnu/asm/unistd_64.h').read_text()
assert '#define __NR_pidfd_open 434' in header
class Filter(ctypes.Structure):_fields_=[('code',ctypes.c_ushort),('jt',ctypes.c_ubyte),('jf',ctypes.c_ubyte),('k',ctypes.c_uint)]
class Program(ctypes.Structure):_fields_=[('len',ctypes.c_ushort),('filter',ctypes.POINTER(Filter))]
# Filter only this subprocess; never modify the parent or another process.
filters=(Filter*4)(Filter(0x20,0,0,0),Filter(0x15,0,1,434),Filter(0x06,0,0,0x50000|denied),Filter(0x06,0,0,0x7fff0000))
prog=Program(4,filters);libc=ctypes.CDLL(None,use_errno=True)
assert libc.prctl(38,1,0,0,0)==0,ctypes.get_errno()
assert libc.prctl(22,2,ctypes.byref(prog),0,0)==0,ctypes.get_errno()
sp=importlib.util.spec_from_file_location('h',H);h=importlib.util.module_from_spec(sp);sp.loader.exec_module(h)
real=h.subprocess.Popen;spawned=[]
def popen(*a,**k):spawned.append(True);return real(*a,**k)
h.subprocess.Popen=popen
try:
 h.call([sys.executable,'-c','pass'],Path(work)/'child.log')
 assert which!='EINVAL'
except h.GateError as e:
 assert which=='EINVAL',str(e)
 assert not spawned
print(json.dumps({'errno':which,'mode':h._SESSION_KILL_MODE,'spawned':len(spawned),'PASS':True}))
