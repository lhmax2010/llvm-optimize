from pathlib import Path
import subprocess,json,os,tarfile,hashlib,concurrent.futures,time,xml.etree.ElementTree as X
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=W/'temp/qb-meta-switch-20261028/second-specs';E=B/'tools/bolt/results/qb-meta-switch-20261028/second-ruling';D.mkdir(exist_ok=True)
projects={p.get('name'):p.get('revision') for p in X.parse(E/'unified-standard.xml').iter('project')}
# SSH server-side archive at exact manifest revisions; packaging only, no checkout/build.
def one(item):
 project,rev=item;key=project.replace('/','__');dest=E/'specs'/key;meta=dest/'provenance.json'
 if meta.exists():return json.loads(meta.read_text())
 dest.mkdir(parents=True,exist_ok=True);tar=D/(key+'.tar')
 row=dict(project=project,revision=rev,url='ssh://review.tizen.org:29418/'+project,specs=[])
 try:
  with tar.open('wb') as o:
   r=subprocess.run(['git','archive','--remote='+row['url'],rev,'packaging'],env=dict(os.environ,GIT_SSH_COMMAND='ssh -o BatchMode=yes -o ConnectTimeout=15'),stdout=o,stderr=subprocess.PIPE,timeout=150)
  row.update(rc=r.returncode,stderr=r.stderr.decode(errors='replace'),archive_bytes=tar.stat().st_size)
  if r.returncode==0:
   with tarfile.open(tar) as t:
    for m in t:
     if m.isfile() and m.name.endswith('.spec'):
      b=t.extractfile(m).read();p=dest/m.name
      if '..' in Path(m.name).parts or Path(m.name).is_absolute():raise ValueError('unsafe path')
      p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);row['specs'].append(dict(path=str(p.relative_to(E)),source_path=m.name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 except Exception as ex:row['error']=str(ex)
 meta.write_text(json.dumps(row,indent=2)+'\n');return row
rows=[];start=time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for future in concurrent.futures.as_completed([pool.submit(one,x) for x in projects.items()]):
  row=future.result();rows.append(row)
  if len(rows)%20==0 or row.get('rc')!=0 or not row['specs']:print(len(rows),'/',len(projects),'seconds',round(time.time()-start),row['project'],'rc',row.get('rc'),'specs',len(row['specs']),flush=True)
  (E/'spec-acquisition.json').write_text(json.dumps(sorted(rows,key=lambda r:r['project']),indent=2)+'\n')
print('COMPLETE',len(rows),'specs',sum(len(r['specs']) for r in rows),'errors',sum(r.get('rc')!=0 or not r['specs'] for r in rows),flush=True)
