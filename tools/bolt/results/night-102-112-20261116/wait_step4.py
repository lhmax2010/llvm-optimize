from pathlib import Path
import json,time,datetime,os,shutil
from zoneinfo import ZoneInfo
E=Path(__file__).parent
limit=datetime.datetime(2026,11,18,8,30,tzinfo=ZoneInfo('Asia/Shanghai')).timestamp()
while True:
 now=datetime.datetime.now().astimezone()
 mem=dict(l.split(':',1) for l in Path('/proc/meminfo').read_text().splitlines())
 available=int(mem['MemAvailable'].split()[0])*1024
 free=shutil.disk_usage('/home').free
 heavy=[]
 for p in Path('/proc').iterdir():
  if not p.name.isdecimal():continue
  try:comm=(p/'comm').read_text().strip()
  except (FileNotFoundError,PermissionError,ProcessLookupError):continue
  if comm in ('gbs','rpmbuild','ninja','llvm-bolt'):heavy.append({'pid':int(p.name),'comm':comm})
 row={'time':now.isoformat(),'MemAvailable':available,'home_free':free,'heavy':heavy,'status':'WAITING'}
 if time.time()>=limit:row['status']='DEADLINE'
 elif available>=24*1024**3 and not heavy:row['status']='RESOURCE_READY_LOCK_NOT_YET_CHECKED'
 with (E/'step4-admission.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 print(json.dumps(row),flush=True)
 if row['status']!='WAITING':
  (E/'step4-admission-result.json').write_text(json.dumps(row,indent=2))
  print('已结束 '+now.isoformat()+' step4-admission '+row['status'],flush=True)
  break
 time.sleep(min(1800,max(0,limit-time.time())))
