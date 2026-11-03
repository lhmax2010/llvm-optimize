from pathlib import Path
import os,json,time,datetime
E=Path(__file__).parent;T=Path('/home/linhao/Toolchain/development/llvm-optimize/temp');rows=[]
for top in sorted(T.iterdir()):
 if not top.is_dir() or top.is_symlink():continue
 start=time.monotonic();marks=[];errors=[];bounded=False
 for root,ds,fs in os.walk(top,followlinks=False,onerror=lambda e:errors.append(str(e))):
  r=Path(root);depth=len(r.relative_to(top).parts)
  if time.monotonic()-start>5:bounded=True;break
  if '.git' in ds or '.git' in fs:marks.append({'kind':'git-worktree','path':str(r)})
  for name in ds:
   if name=='products' or name.endswith('-products') or name in ('preserved-before-delete','preserved-from-upper','perf-runtime','profiles','RPMS','SRPMS','evidence','gbs-root','baseline-root','revised-root'):
    marks.append({'kind':name,'path':str(r/name)})
  for name in fs:
   if name in ('SHA256SUMS','identity.json','build.conf','gbs_llvm_qb1202084.conf'):
    try:s=(r/name).stat();marks.append({'kind':name,'path':str(r/name),'bytes':s.st_size})
    except OSError as e:errors.append(str(e))
  ds[:]=[n for n in ds if n not in ('.git','proc','sys','dev') and not (r/n).is_symlink()] if depth<3 else []
 rows.append({'path':str(top),'markers':marks,'errors':errors,'bounded':bounded,'depth_limit':4})
(E/'local-assets-shallow.json').write_text(json.dumps(rows,indent=2)+'\n');print('INSPECT DONE',len(rows))
