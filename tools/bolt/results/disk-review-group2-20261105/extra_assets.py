from pathlib import Path
import json,subprocess,gzip,os
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');T=W/'temp';cache={};rows=[]
def sha(p):
 s=p.stat();k=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)
 if k not in cache:
  r=subprocess.run(['timeout','120','nice','-n','19','ionice','-c3','sha256sum','--',str(p)],capture_output=True,text=True)
  cache[k]={'rc':r.returncode,'sha256':r.stdout.split()[0] if r.returncode==0 else None,'stderr':r.stderr}
 return cache[k]
# Probe binaries are named unlike installed clang: include every matrix product.
for name in ('crash-probe-20261028','crash-fix-probe-20261028'):
 for line in gzip.open(E/name/'files.jsonl.gz','rt'):
  x=json.loads(line);p=Path(x['path'])
  if x['size']<1024*1024 or x.get('link'):continue
  x['hash']=sha(p);rows.append(x)
  (E/'probe-binary-hashes.json').write_text(json.dumps(rows,indent=2))
comparisons=[]
for f in ['clang.final','clang.ordinary','clang.symbols','same-clang']:
 a=T/'crash-probe-20261028'/f
 if not a.exists():continue
 ds=[]
 for product in ['oldtext-final-20261027/products','debuglink-20261028/full-20261030/products','bolt-on-hybrid-20261024/products','bolt-v4-20261022-cache-release/baseline-products','bolt-v4-20261022-cache-release/revised-products']:
  for p in (T/product).rglob('*'):
   if p.is_file() and p.stat().st_size==a.stat().st_size:
    h=sha(p)
    if h.get('sha256') and h['sha256']==sha(a)['sha256']:ds.append(str(p))
 comparisons.append({'file':str(a),'hash':sha(a),'same_sha_retained_products':ds})
(E/'probe-external-duplicates.json').write_text(json.dumps(comparisons,indent=2))
print('probe assets complete',len(rows),flush=True)
# Verify copied RPM-derived compiler-rt payload provenance without extracting or modifying.
