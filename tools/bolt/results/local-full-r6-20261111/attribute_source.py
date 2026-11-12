from pathlib import Path
import tarfile,hashlib,json,subprocess,gzip,datetime,re,difflib
W=Path('/home/linhao/Toolchain/development/llvm-optimize'); E=Path(__file__).parent
P=W/'temp/local-full-r6-20261111-compare/toolchain/payload/llvm-src'
O=W/'temp/local-full-r6-20261111-source-attribution';O.mkdir(exist_ok=False)
patches=sorted((P/'qb').glob('*.patch'))
targets=set()
for p in patches:
 for l in p.read_text().splitlines():
  if l.startswith('+++ b/'):targets.add(l[6:])
def inventory(label):
 out={};ex=O/label;ex.mkdir()
 with tarfile.open(P/label/'llvm-22.1.8.tar.gz','r|gz') as t:
  for m in t:
   n=m.name.removeprefix('llvm-22.1.8/').rstrip('/')
   row=dict(type=m.type.decode(),size=m.size,mode=m.mode,link=m.linkname)
   if m.isfile():
    f=t.extractfile(m);h=hashlib.sha256();buf=bytearray() if n in targets else None
    while b:=f.read(1<<20):
     h.update(b)
     if buf is not None:buf.extend(b)
    row['sha256']=h.hexdigest()
    if buf is not None:
     d=ex/n;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(buf)
   out[n]=row
 with gzip.open(E/('source-'+label+'-tar-manifest.json.gz'),'wt') as f:json.dump(out,f,sort_keys=True)
 return out
a=inventory('local');b=inventory('qb')
for p in patches:
 cmd=['patch','--batch','--forward','-p1','-i',str(p)]
 q=subprocess.run(cmd,cwd=O/'qb',capture_output=True,text=True)
 (E/('source-apply-'+p.name+'.txt')).write_text('argv='+repr(cmd)+'\n'+q.stdout+q.stderr+'\nrc='+str(q.returncode)+'\n')
 assert q.returncode==0,(p,q.stdout,q.stderr)
 for n in targets:
  f=O/'qb'/n
  if f.exists() and n in b:b[n]['sha256']=hashlib.sha256(f.read_bytes()).hexdigest();b[n]['size']=f.stat().st_size
changes=[]
for n in sorted(a.keys()|b.keys()):
 x,y=a.get(n),b.get(n)
 if x!=y:changes.append(dict(file=n,local=x,qb_patched=y))
result=dict(local_entries=len(a),qb_entries=len(b),patches=[p.name for p in patches],patched_files=sorted(targets),differences=changes,status='PASS' if not changes else 'DIFFERENCES',workspace=str(O))
(E/'source-attribution.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(result, differences=changes[:12]),indent=2))
print('SOURCE_ATTRIBUTION 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+result['status'])
