from pathlib import Path
import os, json, fcntl, datetime, subprocess, shutil, time
E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/night-102-112-20261116')
UNIT='task112-step4-20261116.service'
def now(): return datetime.datetime.now().astimezone().isoformat()
def avail():
 return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
heavy=[]
for p in Path('/proc').glob('[0-9]*'):
 try:
  c=(p/'comm').read_text().strip()
  if c in ('gbs','rpmbuild','ninja','llvm-bolt'): heavy.append({'pid':int(p.name),'comm':c})
 except (FileNotFoundError,ProcessLookupError,PermissionError): pass
obs={'time':now(),'MemAvailable':avail(),'home_free':shutil.disk_usage('/home').free,'heavy':heavy}
if obs['MemAvailable']<12*1024**3 or heavy:
 obs['status']='WAITING'; (E/'step4-start.json').write_text(json.dumps(obs,indent=2)+'\n'); print(obs,flush=True); raise SystemExit(3)
lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','rb')
try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:
 obs['status']='LOCK_UNAVAILABLE'; (E/'step4-start.json').write_text(json.dumps(obs,indent=2)+'\n'); print(obs,flush=True); raise SystemExit(3)
obs.update(status='ADMITTED',shared_lock=str(lock.name))
(E/'step4-start.json').write_text(json.dumps(obs,indent=2)+'\n'); print(json.dumps(obs),flush=True)
while not (E/'step4-finish.json').exists():
 a=avail()
 with (E/'step4-watchdog.jsonl').open('a') as f: f.write(json.dumps({'time':now(),'MemAvailable':a,'stop':a<6*1024**3})+'\n')
 if a<6*1024**3:
  print('112 step4 已结束 '+now()+' status=STOP watchdog',flush=True)
  subprocess.run(['systemctl','--user','stop','--no-block',UNIT]); break
 time.sleep(30)
else:
 print('112 step4 已结束 '+now()+' '+(E/'step4-finish.json').read_text(),flush=True)
