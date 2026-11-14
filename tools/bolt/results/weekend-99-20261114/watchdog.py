import sys,time,subprocess,json,datetime
from pathlib import Path
unit,out,parent=sys.argv[1],Path(sys.argv[2]),Path('/proc')/sys.argv[3]
while parent.exists():
 mem=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
 with out.open('a') as f:f.write(json.dumps({'time':datetime.datetime.now().astimezone().isoformat(),'MemAvailable':mem,'triggered':mem<6*2**30})+'\n')
 if mem<6*2**30:
  subprocess.run(['systemctl','--user','stop','--no-block',unit]);break
 time.sleep(30)
