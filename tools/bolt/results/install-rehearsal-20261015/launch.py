import os,json,sys,time,subprocess,fcntl,uuid,signal
from pathlib import Path
E=Path(__file__).resolve().parent;W=E.parents[1];G=1024**3
lock=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock';record=None;fd=None

def available():return int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
try:
 # Resource ceiling from docs38; task's inherited admission remains >=12 GiB.
 started=time.monotonic()
 while True:
  v=available();row={'time':time.time(),'available':v,'minimum':12*G}
  with (E/'memory-admission.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  if v>=12*G:break
  if time.monotonic()-started>=3600:raise RuntimeError('memory admission timeout')
  time.sleep(300)
 fd=os.open('/home/linhao/Toolchain/development/heavy-stage.lock',os.O_CREAT|os.O_RDWR,0o600);wait=time.monotonic()
 while True:
  try:fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);break
  except BlockingIOError:
   if time.monotonic()-wait>7200:raise RuntimeError('shared lock wait timeout')
   time.sleep(1)
 record={'session':'bolt-install-rehearsal-'+uuid.uuid4().hex,'pid':os.getpid(),'started':time.time(),'evidence':str(E)}
 with os.fdopen(os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600),'w') as f:json.dump(record,f,indent=2)
 (E/'lock-acquired.json').write_text(json.dumps(dict(record,shared_wait_seconds=time.monotonic()-wait),indent=2)+'\n');(E/'lock-start-monotonic').write_text(str(time.monotonic()))
 plan=json.loads((E/'disk-plan.json').read_text());import shutil
 assert shutil.disk_usage(E).free-plan['planned_write_bytes']>=30*G,'disk changed since budget'
 cmd=['systemd-run','--user','--scope','--unit=bolt-real-install-20261015','-p','MemoryMax=19327352832','-p','MemorySwapMax=0','-p','OOMPolicy=stop','nice','-n','15','ionice','-c','3',sys.executable,str(E/'in_scope.py')]
 (E/'scope-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
 with (E/'scope.stdout').open('w') as out,(E/'scope.stderr').open('w') as err:r=subprocess.run(cmd,stdout=out,stderr=err)
 print('B_RESULT', (E/'rehearsal-result.json').read_text() if (E/'rehearsal-result.json').exists() else 'scope failed before sudo',flush=True)
except BaseException as exc:
 (E/'launcher-error.txt').write_text(repr(exc)+'\n')
 if not (E/'rehearsal-result.json').exists():(E/'rehearsal-result.json').write_text(json.dumps({'status':'NOT RUN','reason':repr(exc)},indent=2)+'\n')
 raise
finally:
 removed=False
 if record is not None and lock.exists() and json.loads(lock.read_text())==record:lock.unlink();removed=True
 if fd is not None:
  fcntl.flock(fd,fcntl.LOCK_UN);os.close(fd)
 (E/'lock-released.json').write_text(json.dumps({'time':time.time(),'project_lock_removed':removed,'shared_released':fd is not None,'held_seconds':time.monotonic()-float((E/'lock-start-monotonic').read_text()) if (E/'lock-start-monotonic').exists() else 0},indent=2)+'\n')
