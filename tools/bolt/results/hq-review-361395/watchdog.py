import json,subprocess,time,sys,datetime
from pathlib import Path
unit=sys.argv[1]
with Path(sys.argv[2]).open('x') as out:
 while True:
  m={l.split(':')[0]:int(l.split()[1])*1024 for l in Path('/proc/meminfo').read_text().splitlines()}
  r=dict(time=datetime.datetime.now().astimezone().isoformat(),MemAvailable=m['MemAvailable'],unit=unit,triggered=m['MemAvailable']<6*1024**3)
  out.write(json.dumps(r)+'\n');out.flush()
  if r['triggered']:
   print('WATCHDOG',json.dumps(r),flush=True)
   subprocess.run(['systemctl','--user','stop','--no-block',unit]);break
  time.sleep(30)
