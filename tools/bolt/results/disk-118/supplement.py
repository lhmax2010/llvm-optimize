from pathlib import Path
import subprocess,json,datetime,os
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.with_name('llvm-optimize-bolt');E=B/'tools/bolt/results/disk-118'
rows=json.loads((E/'measurements.json').read_text());seen={r['path'] for r in rows};missing=[]
for parent in [W,W/'temp']:
 for p in sorted(parent.iterdir()):
  if p.is_dir() and not p.is_symlink() and str(p) not in seen and p.name!='temp':missing.append(p)
print('missing directories',len(missing),flush=True)
for i,p in enumerate(missing):
 try:
  r=subprocess.run(['du','-x','-s','-B1','--',str(p)],capture_output=True,text=True,timeout=120)
  (E/('supplement-'+str(i)+'.txt')).write_text(r.stdout+r.stderr)
  size=int(r.stdout.split('\t',1)[0]) if r.stdout else None
  row={'path':str(p),'bytes':size,'mtime':datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(),'measurement_root':str(p),'measurement_complete':r.returncode==0,'rc':r.returncode}
 except subprocess.TimeoutExpired as e:
  row={'path':str(p),'bytes':None,'mtime':datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(),'measurement_root':str(p),'measurement_complete':False,'rc':124}
  (E/('supplement-'+str(i)+'.txt')).write_bytes((e.stdout or b'')+(e.stderr or b''))
 rows.append(row);print(i,p.name,row['bytes'],row['rc'],flush=True)
(E/'measurements-combined.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('已结束',datetime.datetime.now().astimezone().isoformat(),'A supplement')
