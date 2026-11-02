"""Read-only 2s all-process sampling, 5s statvfs; boundary-only du.

Process HWM is lifetime HWM, not resettable at substage transitions. Samples can
miss short processes. Root disk figures are boundary observations, not true peaks.
"""
from common import *
import threading,queue
ANCHORS=[('ordinary-compile','Executing(%build)'),('ordinary-install','Executing(%install)'),('BOLT','BOLT_DISK_REPORT'),('cache-release','BOLT_COMPARE_ROOT_PASS'),('archive-install','BOLT_CACHE_RELEASE'),('platform-post','/usr/lib/rpm/find-debuginfo.sh'),('packaging','Processing files:')]
def phase_for(line,phase):
 if 'BOLT_DISK_REPORT' in line:return 'BOLT' if '"stage": "begin"' in line or '"stage":"begin"' in line else phase
 for name,anchor in ANCHORS:
  if name!='BOLT' and anchor in line:return name
 return phase
class Monitor:
 def __init__(self,unit,out,tree,log=None):
  self.unit=unit;self.out=out;self.tree=tree;self.log=log;self.stop=threading.Event();self.phase='setup';self.high={};self.q=queue.Queue();self.reason=None;self.offset=0;self.pending=b'';self.peakfd=None;self.cg=None;self.error=None
 def append(self,name,obj):
  with (self.out/name).open('a') as f:f.write(json.dumps(obj)+'\n')
 def boundary(self,new,anchor):
  now=time.time_ns()
  if self.peakfd:
   try:
    self.peakfd.seek(0);peak=int(self.peakfd.read());self.peakfd.seek(0);self.peakfd.write('0');self.peakfd.flush()
    self.append('phase-peaks.jsonl',{'time_ns':now,'phase':self.phase,'memory_peak_bytes':peak,'method':'same memory.peak FD reset at observed log boundary','anchor':anchor})
   except OSError as e:self.append('phase-peaks.jsonl',{'phase':self.phase,'UNKNOWN':str(e)})
  self.append('boundaries.jsonl',{'time_ns':now,'from':self.phase,'to':new,'anchor':anchor});self.q.put((now,new));self.phase=new
 def du(self):
  while True:
   item=self.q.get()
   if item is None:break
   now,phase=item;t=time.time_ns()
   try:
    # The root's du is allowed to read root-owned files through existing chroot authorization.
    if (self.tree/'usr/bin/du').exists():argv=['sudo','-n','/usr/sbin/chroot',str(self.tree),'/usr/bin/du','-sx','-B1','/']
    else:argv=['du','-sx','-B1',str(self.tree)]
    p=subprocess.run(argv,capture_output=True,text=True,timeout=90)
    self.append('du-boundaries.jsonl',{'boundary_ns':now,'phase':phase,'scan_start_ns':t,'scan_end_ns':time.time_ns(),'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'bytes':int(p.stdout.split()[0]) if p.returncode==0 else None})
   except Exception as e:self.append('du-boundaries.jsonl',{'boundary_ns':now,'phase':phase,'UNKNOWN':str(e)})
 def read_log(self):
  if self.log and self.log.exists():
   with self.log.open('rb') as f:f.seek(self.offset);data=f.read();self.offset+=len(data)
   self.pending+=data;lines=self.pending.split(b'\n');self.pending=lines.pop()
   for raw in lines:
    line=raw.decode(errors='replace');new=phase_for(line,self.phase)
    if new!=self.phase:self.boundary(new,line)
 def sample(self):
  nextfs=0;nextproc=0;self.boundary(self.phase,'service-start')
  while not self.stop.is_set():
   now=time.time_ns()
   if self.cg is None:
    p=subprocess.run(['systemctl','--user','show',self.unit,'-p','ControlGroup','--value'],capture_output=True,text=True)
    if p.stdout.strip():
     self.cg=Path('/sys/fs/cgroup')/p.stdout.strip().lstrip('/')
     try:self.peakfd=(self.cg/'memory.peak').open('r+');self.peakfd.write('0');self.peakfd.flush()
     except OSError as e:self.append('phase-peaks.jsonl',{'UNKNOWN':str(e),'phase':self.phase});self.peakfd=None
   self.read_log()
   if self.cg and self.cg.exists() and time.monotonic()>=nextproc:
    nextproc=time.monotonic()+2
    pids=set()
    for f in self.cg.rglob('cgroup.procs'):
     try:pids.update(f.read_text().split())
     except OSError:pass
    for pid in pids:
     try:
      base=Path('/proc')/pid;status=dict(l.split(':',1) for l in (base/'status').read_text().splitlines() if ':' in l)
      st=(base/'stat').read_text().rsplit(')',1)[1].split();start=st[19]
      row={'time_ns':now,'phase':self.phase,'pid':int(pid),'starttime_ticks':start,'name':status['Name'].strip(),'cmdline':(base/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace'),'VmHWM_bytes':int(status.get('VmHWM','0 kB').split()[0])*1024,'VmRSS_bytes':int(status.get('VmRSS','0 kB').split()[0])*1024}
      self.append('processes.jsonl',row);key=pid+':'+start;prev=self.high.get(key)
      if not prev or row['VmHWM_bytes']>prev['VmHWM_bytes']:self.high[key]=row
     except (OSError,ValueError,KeyError):pass
    row={'time_ns':now,'phase':self.phase}
    for n in ['memory.current','memory.peak','memory.events','memory.swap.current']:
     try:row[n]=(self.cg/n).read_text()
     except OSError:pass
    self.append('cgroup.jsonl',row)
   if time.monotonic()>=nextfs:
    s=os.statvfs('/home');free=s.f_bavail*s.f_frsize;self.append('filesystem.jsonl',{'time_ns':now,'phase':self.phase,'available_bytes':free,'device':os.stat('/home').st_dev});nextfs=time.monotonic()+5
    if free<20*1024**3:
     self.reason='home-below-20GiB';subprocess.run(['systemctl','--user','stop',self.unit],capture_output=True);break
   self.stop.wait(1)
  self.read_log()
  self.boundary('ended','service-end');save(self.out/'process-maxima.json',list(self.high.values()))
  if self.peakfd:
   try:self.peakfd.close()
   except OSError as e:self.append('phase-peaks.jsonl',{'close_error':str(e)})
 def guarded_sample(self):
  try:self.sample()
  except BaseException as e:
   self.error=repr(e);self.append('monitor-errors.jsonl',{'error':self.error});self.stop.set()
 def start(self):
  self.dt=threading.Thread(target=self.du);self.mt=threading.Thread(target=self.guarded_sample);self.dt.start();self.mt.start()
 def finish(self):
  self.stop.set();self.mt.join();self.q.put(None);self.dt.join()
  if self.error:raise RuntimeError(self.error)
