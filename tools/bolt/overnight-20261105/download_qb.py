from pathlib import Path
import urllib.request,urllib.parse,json,hashlib,subprocess,shutil,datetime,traceback
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/baseline-attribution-20261105';O=W/'temp/qb-1216409-1216410/full-rpms';O.mkdir(exist_ok=False)
known={r['url']:r for r in json.loads((B/'tools/bolt/results/qb-1216409-1216410/rpm-downloads.json').read_text())};rows=[]
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(): (E/'rpm-downloads.json').write_text(json.dumps(rows,indent=2)+'\n')
try:
 for bid,project,snap,rel,label,n in [(1216409,'Tizen-Base-Toolchain','tizen-base-toolchain_20261103.085926','2.1','toolchain',23),(1216410,'Tizen-Base-Dev','tizen-base-dev_20261103.090039','5.1','basedev',13)]:
  local=sorted((W/'temp/night-20261103'/label/'gbs-driver/local/repos').glob('**/*.rpm'));assert len(local)==n,(label,len(local));(O/str(bid)).mkdir()
  for p in local:
   vals=subprocess.check_output(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{ARCH}',str(p)],text=True).strip().split('\t');name,version,arch=vals;source=p.name.endswith('.src.rpm');arch='src' if source else arch
   repo='debug' if ('debuginfo' in name or 'debugsource' in name) else 'packages/'+arch
   fname=f'{name}-{version}-{rel}.{arch}.rpm';url=f'https://download.tizen.org/RBS/TIZEN/Tizen/{project}/{snap}/repos/standard/{repo}/{fname}';dest=O/str(bid)/fname
   if url in known:
    old=known[url];assert sha(Path(old['path']))==old['sha256'];shutil.copyfile(old['path'],dest);mode='verified-existing-copy'
   else:
    with urllib.request.urlopen(url,timeout=120) as r:
     assert urllib.parse.urlparse(r.url).hostname=='download.tizen.org';assert 'text/html' not in r.headers.get('Content-Type',''),'HTML/login response'
     with dest.open('xb') as f:
      while block:=r.read(1024*1024):
       s=__import__('os').statvfs('/home');assert s.f_bavail*s.f_frsize>=30*1024**3,'home-below-30GiB';f.write(block)
    mode='public-no-credentials'
   q=subprocess.run(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}\t%{BUILDTIME}\t%{BUILDHOST}',str(dest)],capture_output=True,text=True);assert q.returncode==0,q.stderr
   row={'build':bid,'project':label,'url':url,'path':str(dest),'bytes':dest.stat().st_size,'sha256':sha(dest),'metadata':q.stdout,'local_rpm':str(p),'local_sha256':sha(p),'reuse':mode};rows.append(row);save();print('DOWNLOAD_OK',bid,fname,row['bytes'],flush=True)
 (E/'downloads-result.json').write_text(json.dumps({'status':'ok','count':len(rows)},indent=2)+'\n')
except Exception as ex:
 (E/'downloads-result.json').write_text(json.dumps({'status':'stopped','reason':str(ex),'completed':len(rows)},indent=2)+'\n');traceback.print_exc();raise
finally:print('DOWNLOAD 已结束',datetime.datetime.now().astimezone().isoformat(),flush=True)
