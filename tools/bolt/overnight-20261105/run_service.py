"""Unprivileged isolated service runner; no historical-tree writes or cleanup."""
from pathlib import Path
import subprocess,sys,json,time,datetime,os,signal

def now():return datetime.datetime.now().astimezone().isoformat()
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
if sys.argv[1]=='--worker':
 out=Path(sys.argv[2]);cmd=json.loads((out/'argv.json').read_text());rc=1;t=time.time_ns()
 try:rc=subprocess.run(cmd).returncode
 finally:
  cg=Path('/sys/fs/cgroup')/next(l.split(':',2)[2] for l in Path('/proc/self/cgroup').read_text().splitlines() if l.startswith('0::')).lstrip('/')
  stats={}
  for k in ('memory.peak','memory.events','memory.max','memory.swap.max','cpu.max'):
   try:stats[k]=(cg/k).read_text()
   except OSError as e:stats[k]='UNKNOWN '+str(e)
  save(out/'worker-result.json',{'rc':rc,'start_ns':t,'end_ns':time.time_ns(),'stats':stats})
  print('SERVICE 已结束',now(),'status='+('ok' if rc==0 else 'failed'),'reason=exit-'+str(rc),flush=True)
 sys.exit(rc if rc>=0 else 1)
out=Path(sys.argv[1]);unit=sys.argv[2];cmd=sys.argv[3:];out.mkdir(parents=True,exist_ok=False);save(out/'argv.json',cmd)
free=os.statvfs('/home');free=free.f_bavail*free.f_frsize
if free<30*1024**3:
 save(out/'result.json',{'status':'stopped','reason':'home-below-30GiB','available_bytes':free});print('SERVICE 已结束',now(),'status=stopped reason=home-below-30GiB',flush=True);sys.exit(2)
mem=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:')))*1024-8*1024**3
args=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax='+str(mem),'-p','MemorySwapMax=0','-p','CPUQuota=1200%','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','KillMode=control-group','-p','OOMPolicy=stop','-p','TimeoutStopSec=120','--setenv=PYTHONDONTWRITEBYTECODE=1','/usr/bin/python3','-B',__file__,'--worker',str(out)]
save(out/'systemd-command.json',args);start=time.time_ns();reason=None;high={};cg=None
with (out/'stdout').open('xb') as so,(out/'stderr').open('xb') as se:
 p=subprocess.Popen(args,stdout=so,stderr=se)
 while p.poll() is None:
  if cg is None:
   v=subprocess.run(['systemctl','--user','show',unit,'-p','ControlGroup','--value'],capture_output=True,text=True).stdout.strip()
   if v:cg=Path('/sys/fs/cgroup')/v.lstrip('/')
  s=os.statvfs('/home');available=s.f_bavail*s.f_frsize;r={'time_ns':time.time_ns(),'available_bytes':available}
  if cg and cg.exists():
   for k in ('memory.current','memory.peak','memory.events'):
    try:r[k]=(cg/k).read_text()
    except OSError:pass
   for pf in cg.rglob('cgroup.procs'):
    try:pids=pf.read_text().split()
    except OSError:continue
    for pid in pids:
     try:
      q=Path('/proc')/pid;st=dict(l.split(':',1) for l in (q/'status').read_text().splitlines() if ':' in l);h=int(st.get('VmHWM','0 kB').split()[0])*1024
      row={'pid':pid,'name':st['Name'].strip(),'VmHWM_bytes':h,'cmdline':(q/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace'),'time_ns':r['time_ns']}
      if h>high.get(pid,{}).get('VmHWM_bytes',-1):high[pid]=row
     except OSError:pass
  with (out/'resources.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
  if available<30*1024**3 and reason is None:
   reason='home-below-30GiB';subprocess.run(['systemctl','--user','stop',unit],capture_output=True)
  time.sleep(2)
 rc=p.wait()
status=subprocess.run(['systemctl','--user','show',unit,'-p','Result','-p','ActiveState','-p','SubState','-p','MainPID'],capture_output=True,text=True).stdout
save(out/'process-maxima.json',list(high.values()));save(out/'result.json',{'rc':rc,'status':'ok' if rc==0 else 'stopped' if reason else 'failed','reason':reason or 'exit-'+str(rc),'start_ns':start,'end_ns':time.time_ns(),'systemd':status})
line='SERVICE 已结束 '+now()+' status='+('ok' if rc==0 else 'stopped' if reason else 'failed')+' reason='+(reason or 'exit-'+str(rc));(out/'end.txt').write_text(line+'\n');print(line,flush=True);sys.exit(rc if rc>=0 else 1)
