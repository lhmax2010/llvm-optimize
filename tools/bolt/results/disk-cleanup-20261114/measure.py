from pathlib import Path
import os,subprocess,time,json,datetime
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')
start=time.monotonic();deadline=start+7200
roots=sorted((W/'temp').iterdir())+[p for p in W.iterdir() if p.name!='temp']+[B]
roots += sorted(p for p in Path('/var/tmp').iterdir() if p.name.startswith('llvm-optimize-'))
# Only project-named siblings; do not recurse into unrelated projects.
siblings=[p for p in W.parent.iterdir() if p.name.startswith('llvm-optimize') and p not in (W,B)]
roots+=siblings
(E/'scope.json').write_text(json.dumps({'W':str(W),'B':str(B),'home_abuild_exists':Path('/home/abuild').exists(),'roots':[str(p) for p in roots],'siblings':[str(p) for p in siblings],'time':datetime.datetime.now().astimezone().isoformat(),'limits':{'each_seconds':900,'total_seconds':7200,'fallback_levels':2}},indent=2)+'\n')
rows=[]
def measure(p,level=0):
 remaining=deadline-time.monotonic();rec={'path':str(p),'level':level,'start':datetime.datetime.now().astimezone().isoformat(),'size_bytes':None,'device':p.lstat().st_dev,'symlink':p.is_symlink(),'realpath':str(p.resolve())}
 if remaining<=0:rec.update(status='UNKNOWN',reason='total 2-hour budget exhausted');return rec
 argv=['nice','-n','19','ionice','-c','3','du','-x','-B1','--max-depth=3','--',str(p)];rec['argv']=argv;t=time.monotonic()
 try:
  q=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=min(900,remaining));out=q.stdout.decode(errors='replace');err=q.stderr.decode(errors='replace');rc=q.returncode
 except subprocess.TimeoutExpired as ex:
  out=(ex.stdout or b'').decode(errors='replace');err=(ex.stderr or b'').decode(errors='replace');rc='TIMEOUT'
 rec.update(rc=rc,elapsed_seconds=time.monotonic()-t,stderr=err,status='OK' if rc==0 else 'UNKNOWN')
 idx=len(rows);(E/f'du-{idx:03d}.txt').write_text(out);rec['raw']=f'du-{idx:03d}.txt'
 vals=[]
 for line in out.splitlines():
  a,sep,b=line.partition('\t')
  if sep and a.isdigit():
   vals.append({'path':b,'size_bytes':int(a)})
   if b==str(p) and rc==0:rec['size_bytes']=int(a)
 rec['children']=vals
 rows.append(rec)
 with (E/'measurements.jsonl').open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
 print('DU',len(rows),str(p),rec['size_bytes'],rec['status'],round(rec['elapsed_seconds'],2),flush=True)
 if rc=='TIMEOUT' and level<2 and p.is_dir() and not p.is_symlink():
  for child in sorted(p.iterdir()):
   if child.is_dir() and not child.is_symlink():measure(child,level+1)
 return rec
for root in roots:measure(root)
(E/'measurement-summary.json').write_text(json.dumps({'measurements':len(rows),'unknown':sum(r['status']!='OK' for r in rows),'elapsed_seconds':time.monotonic()-start,'root_sum_not_deduplicated':sum(r['size_bytes'] or 0 for r in rows if r['level']==0),'end':datetime.datetime.now().astimezone().isoformat()},indent=2)+'\n')
print('97测量 已结束',datetime.datetime.now().astimezone().isoformat(),'status=DONE',flush=True)
