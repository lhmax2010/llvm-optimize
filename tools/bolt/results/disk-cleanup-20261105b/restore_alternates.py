from pathlib import Path
import os,json,hashlib,shutil,datetime,subprocess
E=Path(__file__).parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W/'temp/deleted-repo-backup-20261105'
source=B/'10-archive-followup-review-20261014/submit-work-4512d286/verified.git/objects'
target=W/'temp/archive-followup-review-20261014/submit-work/.git/objects'
stage=B/'_alternates-restoration-10';stage.mkdir(exist_ok=False)
def stamp():return datetime.datetime.now().astimezone().isoformat()
def digest(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
r=dict(start=stamp(),reason='restore object store required by approved but skipped alternate-dependent clones; do not edit their configs',source=str(source),target=str(target),files=[])
assert source.is_dir() and not target.exists()
shutil.copytree(source,stage/'objects',symlinks=True)
for p in sorted(source.rglob('*')):
 assert not p.is_symlink()
 if p.is_file():
  q=stage/'objects'/p.relative_to(source);a=digest(p);b=digest(q);assert a==b
  r['files'].append(dict(path=str(p.relative_to(source)),bytes=p.stat().st_size,source_sha256=a,restored_sha256=b))
target.parent.mkdir(parents=True,exist_ok=True);os.rename(stage/'objects',target)
r.update(end=stamp(),status='object-store-restored',bytes=sum(x['bytes'] for x in r['files']))
(E/'alternates-restoration.json').write_text(json.dumps(r,indent=2)+'\n')
print('ALTERNATES_RESTORATION 已结束',stamp(),'status=ok bytes='+str(r['bytes']),flush=True)
