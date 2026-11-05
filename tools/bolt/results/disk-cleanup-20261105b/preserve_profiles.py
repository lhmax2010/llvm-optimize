from pathlib import Path
import os,hashlib,json,datetime
E=Path(__file__).parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');src=W/'temp/pgo-resource-20261102/full/stage-A/profiles';dst=W/'temp/pgo-profiles-keep-20261102'
def inventory(root):
 out=[]
 for p in sorted(root.rglob('*')):
  assert not p.is_symlink(),p
  if p.is_file():
   with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
   out.append(dict(path=str(p.relative_to(root)),bytes=p.stat().st_size,sha256=h))
 return out
assert src.is_dir() and not src.is_symlink() and src.resolve()==src;assert not dst.exists() and not dst.is_symlink();before=inventory(src);assert before
(E/'profiles-before.json').write_text(json.dumps(before,indent=2)+'\n');os.rename(src,dst);after=inventory(dst);assert before==after
(E/'profiles-after.json').write_text(json.dumps(after,indent=2)+'\n');(E/'profiles-move.json').write_text(json.dumps(dict(source=str(src),destination=str(dst),method='os.rename same filesystem; files directly under destination',files=len(before),bytes=sum(r['bytes'] for r in before),PASS=True,time=datetime.datetime.now().astimezone().isoformat()),indent=2)+'\n');print('PROFILES_MOVED_SHA_PASS',len(before),sum(r['bytes'] for r in before))
