from pathlib import Path
import subprocess,json,datetime,os,time,threading
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt');E=B/'tools/bolt/results/disk-118';E.mkdir(exist_ok=False)
start=time.monotonic();rows=[];errors=[]
for root in sorted(W.parent.glob('llvm-optimize*')):
 if not root.is_dir() or root.is_symlink():continue
 label=root.name
 with (E/(label+'-du.txt')).open('w') as out,(E/(label+'-du.stderr')).open('w') as err:
  try:r=subprocess.run(['du','-x','-B1','--max-depth=5','--',str(root)],stdout=out,stderr=err,timeout=900);rc=r.returncode
  except subprocess.TimeoutExpired:rc=124
 errors.append({'root':str(root),'returncode':rc})
 for line in (E/(label+'-du.txt')).read_text().splitlines():
  size,path=line.split('\t',1);p=Path(path)
  try:mtime=datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat()
  except OSError:mtime='UNKNOWN'
  rows.append({'path':path,'bytes':int(size),'mtime':mtime,'measurement_root':str(root),'measurement_complete':rc==0})
 print('measured',root,'rc',rc,'rows',len(rows),flush=True)
# Existing project-attributed BUILD/GBS roots outside top-level depth are measured
# only when already enumerated in this project's old inventory; no other project traversal.
oldE=B/'tools/bolt/results/disk-cleanup-20261114'
oldrows=[json.loads(l) for l in (oldE/'inventory.jsonl').read_text().splitlines()]
extra=[]
for r in oldrows:
 p=Path(r['path'])
 if str(p).startswith(str(W)+'/') and p.is_dir() and ('BUILD-ROOTS' in p.parts or p.name in ('BUILD','cache','ccache','ThinLTOCache')):
  if not any(x['path']==str(p) for x in rows):extra.append(p)
# Query each recorded deep location once; bounded even if a directory is inaccessible.
for i,p in enumerate(sorted(set(extra))):
 if time.monotonic()-start>5400:errors.append({'root':str(p),'returncode':'UNKNOWN total budget'});continue
 try:
  r=subprocess.run(['du','-x','-s','-B1','--',str(p)],capture_output=True,text=True,timeout=120)
  (E/('deep-'+str(i)+'.txt')).write_text(r.stdout+r.stderr)
  if r.returncode==0:
   rows.append({'path':str(p),'bytes':int(r.stdout.split()[0]),'mtime':datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(),'measurement_root':str(p),'measurement_complete':True})
  else:errors.append({'root':str(p),'returncode':r.returncode})
 except subprocess.TimeoutExpired:errors.append({'root':str(p),'returncode':124})
stat=os.statvfs('/home');df={'time':datetime.datetime.now().astimezone().isoformat(),'total':stat.f_blocks*stat.f_frsize,'used':(stat.f_blocks-stat.f_bfree)*stat.f_frsize,'available':stat.f_bavail*stat.f_frsize}
(E/'df.json').write_text(json.dumps(df,indent=2)+'\n')
(E/'measurements.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(E/'measurement-errors.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2)+'\n')
print('DF',df,'ROWS',len(rows),'EXTRA',len(extra),flush=True)
print('已结束',datetime.datetime.now().astimezone().isoformat(),'A measurement')
