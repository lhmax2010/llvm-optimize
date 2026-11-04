"""Copy text evidence only, preserving all products and original evidence."""
from pathlib import Path
import os,json,hashlib,gzip,shutil,subprocess,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=Path(__file__).parent;rows=[]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
for project in ('toolchain','basedev'):
 O=W/'temp/night-20261103'/project/'validation-02';assert (O/'ended.txt').exists(),('validation not finished',project)
 dest=E/project;dest.mkdir(exist_ok=False)
 for base,dirs,files in os.walk(O):
  dirs[:]=[d for d in dirs if d not in ('rpm-bytes','payload')]
  for name in sorted(files):
   p=Path(base)/name
   if p.is_symlink():continue
   if p.suffix not in ('.json','.jsonl','.log','.txt','.stdout','.stderr','.md','.py','.sh','.ll'):
    if 'tools' not in p.relative_to(O).parts:continue
    with p.open('rb') as f:
     if not f.read(2)==b'#!':continue
   rel=p.relative_to(O);q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);compressed=p.stat().st_size>1048576
   if compressed:
    q=Path(str(q)+'.gz')
    with p.open('rb') as src,q.open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as out:shutil.copyfileobj(src,out)
   else:shutil.copyfile(p,q)
   rows.append(dict(source=str(p),source_bytes=p.stat().st_size,source_sha256=sha(p),evidence=str(q.relative_to(E)),evidence_bytes=q.stat().st_size,evidence_sha256=sha(q),gzip=compressed))
(E/'validation-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
p=subprocess.run(['df','-B1','/home'],capture_output=True,text=True);(E/'df-final.txt').write_text(p.stdout);(E/'collected-at.txt').write_text(datetime.datetime.now().astimezone().isoformat()+'\n');print('COLLECTED',len(rows))
