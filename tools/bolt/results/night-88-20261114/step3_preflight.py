import datetime,json,os,re,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent
rows=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  comm=(p/'comm').read_text().strip()
  if not re.search(r'(ninja|rpmbuild|gbs|llvm-bolt|clang|cc1|ld\.lld)',comm):continue
  row={'pid':int(p.name),'comm':comm,'cmdline':(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace'),'status':(p/'status').read_text(),'cgroup':(p/'cgroup').read_text()}
  for key in ('cwd','root','exe'):
   try:row[key]=os.readlink(p/key)
   except OSError as ex:row[key]=str(ex)
  rows.append(row)
 except (OSError,ProcessLookupError):pass
(E/'heavy-processes-preflight.json').write_text(json.dumps(rows,indent=2)+'\n')
parents=[];seen=set()
for row in rows:
 pid=int(re.search(r'^PPid:\s*(\d+)',row['status'],re.M)[1])
 while pid and pid not in seen:
  seen.add(pid);p=Path('/proc')/str(pid)
  try:
   s=(p/'status').read_text();parents.append({'pid':pid,'cmdline':(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace'),'status':s,'cgroup':(p/'cgroup').read_text()});pid=int(re.search(r'^PPid:\s*(\d+)',s,re.M)[1])
  except OSError:break
(E/'heavy-process-parents.json').write_text(json.dumps(parents,indent=2)+'\n')
for name,argv in [('services-preflight.txt',['systemctl','--user','list-units','--all','--no-pager','--plain']),('df-preflight.txt',['df','-B1','/home'])]:
 r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(E/name).write_text(r.stdout)
(E/'meminfo-preflight.txt').write_text(Path('/proc/meminfo').read_text())
reason='STOP: other heavy tasks are running; D report-stale not started; shared lock not acquired.'
assert rows,'process snapshot changed; inspect saved evidence before deciding'
result={'status':'STOP','reason':reason,'time':datetime.datetime.now().astimezone().isoformat(),'heavy_pids':[r['pid'] for r in rows],'output_root_exists':Path('/home/linhao/Toolchain/development/llvm-optimize/temp/report-stale-20261114').exists(),'bolt_executed':False,'shared_lock_acquired':False,'source_plan':'tools/bolt/results/night-87-20261114/report-stale-plan.json'}
(E/'step3-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(reason)
for r in rows:print(r['pid'],r['comm'],r['cgroup'].strip(),r['cmdline'][:200])
for r in parents:print('PARENT',r['pid'],r['cmdline'][:300])
print('88步骤3 已结束',result['time'],'status=STOP')
