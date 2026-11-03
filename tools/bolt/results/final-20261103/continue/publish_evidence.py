from pathlib import Path
import json,shutil,hashlib,gzip,subprocess,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=W/'temp/final-20261103';E=D/'continue-20261103';O=B/'tools/bolt/results/final-20261103/continue'
assert not O.exists(), 'do not overwrite a published result directory'
O.mkdir(parents=True)
def copy(src,dest):
 dest.parent.mkdir(parents=True,exist_ok=True)
 if src.stat().st_size>1024**2 and src.suffix in ('.txt','.log','.stdout','.stderr','.jsonl'):
  dest=dest.with_name(dest.name+'.gz')
  with src.open('rb') as a,gzip.GzipFile(filename=str(dest),mode='wb',mtime=0) as out:shutil.copyfileobj(a,out)
 else:shutil.copyfile(src,dest)
for p in E.rglob('*'):
 if p.is_file() and not p.relative_to(E).parts[0] in ('export',):copy(p,O/p.relative_to(E))
for project in ('toolchain','basedev','basedev/retry-02'):
 r=D/(project.split('/')[0]+'-rehearsal')
 if '/' in project:r=r/'retry-02'
 for p in (r/'evidence').rglob('*'):
  if p.is_file():copy(p,O/'rehearsals'/project/'evidence'/p.relative_to(r/'evidence'))
 for p in r.iterdir():
  if p.is_file():copy(p,O/'rehearsals'/project/p.name)
 if '/' not in project:
  for p in (D/'configs'/project).iterdir():
   if p.is_file():copy(p,O/'configs'/project/p.name)
files=[]
for p in sorted(O.rglob('*')):
 if p.is_file():files.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(O)))
(O/'SHA256SUMS').write_text('\n'.join(files)+'\n')
print('EVIDENCE_FILES',len(files),'BYTES',sum(p.stat().st_size for p in O.rglob('*') if p.is_file()))
