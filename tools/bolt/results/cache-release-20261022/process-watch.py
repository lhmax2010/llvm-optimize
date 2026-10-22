import json,time,sys
from pathlib import Path
D=Path(__file__).resolve().parent;label=sys.argv[1]
cg=Path('/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice')/('bolt-cache-'+label+'.service')
while cg.exists():
 rows=[]
 try:pids=(cg/'cgroup.procs').read_text().split()
 except OSError:break
 for pid in pids:
  try:
   p=Path('/proc')/pid; st=(p/'stat').read_text().rsplit(')',1)[1].split()
   row={'pid':int(pid),'name':(p/'comm').read_text().strip(),'state':st[0],'utime_ticks':int(st[11]),'stime_ticks':int(st[12])}
   for line in (p/'status').read_text().splitlines():
    if line.startswith(('VmHWM:','VmRSS:')):row[line.split(':')[0]+'_KiB']=int(line.split()[1])
   rows.append(row)
  except OSError:pass
 data={'time_ns':time.time_ns(),'processes':rows}
 for name in ('memory.pressure','io.pressure'):
  try:data[name]=(cg/name).read_text()
  except OSError:pass
 with (D/label/'independent-processes.jsonl').open('a') as f:f.write(json.dumps(data)+'\n')
 time.sleep(5)
