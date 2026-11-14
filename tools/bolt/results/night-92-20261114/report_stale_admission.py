import datetime,fcntl,json,os,re,shutil,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent
rows=[];blind=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  comm=(p/'comm').read_text().strip()
  if comm not in ('gbs','rpmbuild','ninja','llvm-bolt'):continue
  rows.append({'pid':int(p.name),'comm':comm,'cmdline':(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace'),'cgroup':(p/'cgroup').read_text(),'status':(p/'status').read_text()})
 except PermissionError:blind.append(p.name)
 except FileNotFoundError:pass
mem=Path('/proc/meminfo').read_text();avail=int(re.search(r'^MemAvailable:\s+(\d+)',mem,re.M)[1])*1024
free=shutil.disk_usage('/home').free
(E/'admission-meminfo.txt').write_text(mem)
(E/'admission-processes.json').write_text(json.dumps(rows,indent=2)+'\n')
for fn,argv in [('admission-df.txt',['df','-B1','/home']),('admission-units.txt',['systemctl','--user','list-units','--all','--no-pager','--plain'])]:
 r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(E/fn).write_text(r.stdout)
reasons=[]
if rows:reasons.append('other gbs/rpmbuild/ninja/llvm-bolt tasks are running')
if avail<20*1024**3:reasons.append('MemAvailable below 20 GiB')
if free<30*1024**3:reasons.append('/home free below 30 GiB')
# Only try the shared lock if every other precondition is met; never wait.
lock_status='NOT ATTEMPTED: other precondition failed';lock=None
if not reasons:
 lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+')
 try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);lock_status='acquired immediately'
 except BlockingIOError:reasons.append('shared lock busy');lock_status='busy'
r={'status':'SKIPPED' if reasons else 'READY','reasons':reasons,'time':datetime.datetime.now().astimezone().isoformat(),'MemAvailable':avail,'home_free_bytes':free,'lock':lock_status,'heavy_pids':[x['pid'] for x in rows],'permission_blind_spots':blind,'output_root_exists':Path('/home/linhao/Toolchain/development/llvm-optimize/temp/report-stale-20261114').exists(),'report_stale_executed':False}
(E/'report-stale-admission.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
if lock:lock.close()
print('92步骤3准入 已结束',r['time'],'status='+r['status'])
