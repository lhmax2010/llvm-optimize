import json,subprocess,time
from pathlib import Path
E=Path(__file__).resolve().parent;T=Path('/home/linhao/Toolchain/development/llvm-optimize/temp')
base=T/'arm-archive-tls-thumb-20261010'
pairs=[(T/'arm-source-root-probes-20261010'/p/'archives',base/p/'archives') for p in ('x86-final-conversion','armv7l-conversion','aarch64-conversion')]
pairs.append((T/'arm-archive-stage1-20261010/x86-conversion/archives',base/'x86-final-conversion/archives'))
cache={};out=[]
def sha(p):
 s=p.stat();k=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)
 if k not in cache:
  r=subprocess.run(['timeout','120','nice','-n','19','ionice','-c3','sha256sum','--',str(p)],capture_output=True,text=True);cache[k]={'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'sha256':r.stdout.split()[0] if r.returncode==0 else None}
 return cache[k]
for old,new in pairs:
 r={'candidate_duplicate':str(old),'retained_copy':str(new),'files':[],'all_equal':True};start=time.monotonic()
 a=sorted(old.rglob('*.a'));b=sorted(new.rglob('*.a'));r['same_names']=set(p.relative_to(old) for p in a)==set(p.relative_to(new) for p in b)
 for p in a:
  if time.monotonic()-start>480:r['timeout']='UNKNOWN after 480s';r['all_equal']=False;break
  q=new/p.relative_to(old);x={'path':str(p),'other':str(q),'size':p.stat().st_size,'hash':sha(p)}
  if q.exists():x['other_hash']=sha(q)
  x['equal']=x['hash'].get('sha256') is not None and x['hash'].get('sha256')==x.get('other_hash',{}).get('sha256');r['files'].append(x);r['all_equal']&=x['equal']
 r['all_equal']&=r['same_names'];out.append(r);(E/'archive-copy-comparison.json').write_text(json.dumps(out,indent=2));print(old,len(r['files']),r['all_equal'],flush=True)
