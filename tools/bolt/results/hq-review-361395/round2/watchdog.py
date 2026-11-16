import time,json,subprocess
from pathlib import Path
from datetime import datetime
p=Path(__file__).with_name('watchdog.jsonl')
while True:
 m=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
 with p.open('a') as f:f.write(json.dumps({'time':datetime.now().astimezone().isoformat(),'MemAvailable':m})+'\n')
 if m<6*1024**3:
  with p.open('a') as f:f.write('WATCHDOG STOP MemAvailable below 6GiB\n')
  subprocess.run(['systemctl','--user','stop','task104-light-20261116.service']);break
 time.sleep(30)
