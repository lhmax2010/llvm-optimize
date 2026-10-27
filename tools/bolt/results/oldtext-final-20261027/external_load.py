"""Local measurement observer; no publication-code changes or process control."""
import os,time,threading,json
from pathlib import Path
class Observer:
 def __init__(self,path):
  self.path=Path(path);self.stop=threading.Event();self.heavy=[];self.active=False;self.last=0;self.errors=0
  self.own=next(x.split(':',2)[2] for x in Path('/proc/self/cgroup').read_text().splitlines() if x.startswith('0::'))
  self.thread=threading.Thread(target=self.run,daemon=True);self.thread.start()
 def snapshot(self):
  out={}
  for p in Path('/proc').iterdir():
   if not p.name.isdigit():continue
   try:
    if self.own in p.joinpath('cgroup').read_text():continue
    text=p.joinpath('stat').read_text();v=text[text.rfind(')')+2:].split();key=(int(p.name),int(v[19]));ticks=int(v[11])+int(v[12]);io=None
    try:
     d=dict(l.split(': ',1) for l in p.joinpath('io').read_text().splitlines());io=int(d['read_bytes'])+int(d['write_bytes'])
    except (OSError,ValueError,KeyError):pass
    out[key]={'ticks':ticks,'io':io,'comm':text[text.find('(')+1:text.rfind(')')]}
   except (OSError,ValueError,IndexError):self.errors+=1
  return out
 def run(self):
  prev=self.snapshot();stamp=time.time_ns();streak={};hz=os.sysconf('SC_CLK_TCK')
  while not self.stop.wait(2):
   now=time.time_ns();cur=self.snapshot();dt=(now-stamp)/1e9;busy=[];raw=[]
   for k,v in cur.items():
    if k not in prev:continue
    cpu=(v['ticks']-prev[k]['ticks'])/hz/dt;io=(v['io']-prev[k]['io'])/dt if v['io'] is not None and prev[k]['io'] is not None else None
    hit=cpu>=.5 or (io is not None and io>=32*1024**2);streak[k]=streak.get(k,0)+dt if hit else 0
    if hit:raw.append({'pid':k[0],'comm':v['comm'],'cpu_cores':cpu,'io_Bps':io,'streak_s':streak[k]})
    if streak[k]>=10:
     event={'pid':k[0],'comm':v['comm'],'start_ns':now-int(streak[k]*1e9),'end_ns':now,'cpu_cores':cpu,'io_Bps':io};busy.append(event);self.heavy.append(event)
   self.active=bool(raw);self.last=now
   with self.path.open('a') as f:f.write(json.dumps({'time_ns':now,'busy_samples':raw,'sustained_heavy':busy,'unreadable_or_exited_total':self.errors})+'\n')
   prev=cur;stamp=now
 def quiet(self):
  start=None
  while True:
   if self.last and not self.active:
    if start is None:start=time.monotonic()
    if time.monotonic()-start>=12:return
   else:start=None
   time.sleep(2)
 def overlapping(self,start,end):return [e for e in self.heavy if e['start_ns']<end and e['end_ns']>start]
 def close(self):self.stop.set();self.thread.join(10)
