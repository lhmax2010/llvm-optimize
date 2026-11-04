from pathlib import Path
import json,tarfile,hashlib,difflib,datetime
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=B/'tools/bolt/results/baseline-attribution-20261105'
rows=json.loads((E/'qb-changed-file-paths.json').read_text());out=[]
def entries(p):
 r=[]
 with tarfile.open(p) as t:
  for m in t:
   f=t.extractfile(m) if m.isfile() else None;r.append({'name':m.name,'mode':m.mode,'uid':m.uid,'gid':m.gid,'uname':m.uname,'gname':m.gname,'mtime':m.mtime,'type':str(m.type),'link':m.linkname,'sha256':hashlib.file_digest(f,'sha256').hexdigest() if f else None})
 return r
try:
 for row in rows:
  if not row['package'].endswith('\tsrc'):continue
  a,b=Path(row['old']),Path(row['new']);z={k:row[k] for k in ('project','path','old_sha','new_sha')}
  if row['path'].startswith('mlgo_') and tarfile.is_tarfile(a) and tarfile.is_tarfile(b):
   x,y=entries(a),entries(b);z['old_members']=x;z['new_members']=y;z['member_content_names_order_equal']=[(m['name'],m['sha256']) for m in x]==[(m['name'],m['sha256']) for m in y]
  elif row['path'].endswith('.spec'):
   z['diff']=''.join(difflib.unified_diff(a.read_text().splitlines(True),b.read_text().splitlines(True),fromfile=str(a),tofile=str(b)));(E/(row['project']+'-source-spec.diff')).write_text(z['diff'])
  out.append(z)
finally:
 (E/'source-difference-details.json').write_text(json.dumps(out,indent=2)+'\n');print('SOURCE_DETAILS 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok',flush=True)
