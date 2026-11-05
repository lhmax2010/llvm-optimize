from pathlib import Path
import json,hashlib,os
from checks import identity,parent_snapshot,command,stamp
E=Path(__file__).parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
rows=json.loads((E/'inventory.json').read_text());results=json.loads((E/'execution-results.json').read_text())
post=dict(time=stamp(),paths=[dict(number=r['number'],path=r['path'],exists=os.path.lexists(r['path']),result=next((x['status'] for x in results if x['number']==r['number']),'not-run')) for r in rows])
restored=E/'alternates-restoration.json'
if restored.exists():
 recovery=json.loads(restored.read_text());post['restoration']=recovery
 for row in post['paths']:
  if Path(recovery['target']).is_relative_to(row['path']):row['original_result']=row['result'];row['result']='retained-object-store'
parents=parent_snapshot([r['path'] for r in rows[:3]]);save('parents-after.json',parents);post['parents_unchanged']=parents==json.loads((E/'parents-before.json').read_text())
protected=json.loads((E/'protected-before.json').read_text());after=[dict(path=x['path'],identity=identity(x['path'])) for x in protected];save('protected-after.json',after);post['protected_unchanged']=after==protected
keep=W/'temp/pgo-profiles-keep-20261102';files=[]
for p in sorted(keep.rglob('*')):
 assert not p.is_symlink()
 if p.is_file():
  with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
  files.append(dict(path=str(p.relative_to(keep)),bytes=p.stat().st_size,sha256=h))
save('profiles-final.json',files);post['profiles_unchanged']=files==json.loads((E/'profiles-before.json').read_text());post['night_not_started']=not (W/'temp/night-20261105/toolchain').exists()
source_paths=['bolt-on-hybrid-20261024/source','debuglink-tb20261026/source','review-20261102/source','oldtext-final-20261027/source','runpath-fix-20261026/source','hq-463c9a13/repo']
source_checks=[dict(path=str(W/'temp'/p),head=command(['git','-C',str(W/'temp'/p),'rev-parse','HEAD'])) for p in source_paths]
for row in source_checks:row['head_object']=command(['git','-C',row['path'],'cat-file','-e','HEAD^{commit}'])
save('protected-source-heads.json',source_checks);post['protected_source_repositories_readable']=all(x['head']['rc']==0 and x['head_object']['rc']==0 for x in source_checks)
save('df-after.json',command(['df','-B1','/home']));save('postcheck.json',post)
print(json.dumps({k:v for k,v in post.items() if k!='paths'},ensure_ascii=False))
assert post['parents_unchanged'] and post['protected_unchanged'] and post['profiles_unchanged'] and post['night_not_started']
assert all(not x['exists'] for x in post['paths'] if x['result']=='deleted')
print('POSTCHECK 已结束',stamp(),'status=ok')
