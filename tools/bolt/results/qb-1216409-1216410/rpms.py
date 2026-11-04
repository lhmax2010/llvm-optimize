from common import *
import subprocess,shutil
rows=[]
for bid,project,snap,rel in [(1216409,'Tizen-Base-Toolchain','tizen-base-toolchain_20261103.085926','2.1'),(1216410,'Tizen-Base-Dev','tizen-base-dev_20261103.090039','5.1')]:
 base=f'https://download.tizen.org/RBS/TIZEN/Tizen/{project}/{snap}/'
 for name,repo,member in [('clang','packages/x86_64','./usr/bin/clang-22')]+([('clang-debuginfo','debug','./usr/lib/debug/usr/bin/clang-22.debug')] if bid==1216409 else []):
  file=f'{name}-22.1.8-{rel}.x86_64.rpm';u=base+'repos/standard/'+repo+'/'+file;p=D/str(bid)/'rpms'/file;p.parent.mkdir(parents=True,exist_ok=True)
  h=hashlib.sha256();size=0
  with urllib.request.urlopen(u,timeout=120) as r,p.open('xb') as f:
   while data:=r.read(1048576):f.write(data);h.update(data);size+=len(data)
  row={'build':bid,'url':u,'path':str(p),'bytes':size,'sha256':h.hexdigest()};save(f'{bid}/{file}.json',json.dumps(row,indent=2)+'\n',u)
  for tag,args in [('query',['rpm','-qp','--qf','%{NAME}\n%{VERSION}-%{RELEASE}\n%{ARCH}\n%{VCS}\n%{SOURCERPM}\n',str(p)]),('files',['rpm','-qpl',str(p)])]:
   r=subprocess.run(args,capture_output=True);save(f'{bid}/{file}-{tag}.txt',r.stdout+r.stderr);assert r.returncode==0
  root=D/str(bid)/'extracted';root.mkdir(exist_ok=True)
  x=subprocess.Popen(['rpm2cpio',str(p)],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  y=subprocess.run(['cpio','-idm','--no-absolute-filenames',member],stdin=x.stdout,capture_output=True,cwd=root)
  x.stdout.close();err=x.stderr.read();rc=x.wait();save(f'{bid}/{name}-extraction.txt',y.stdout+y.stderr+err);assert rc==0 and y.returncode==0
  f=root/member[2:];h=hashlib.sha256()
  with f.open('rb') as s:
   for data in iter(lambda:s.read(1048576),b''):h.update(data)
  row['extracted']={'path':str(f),'bytes':f.stat().st_size,'sha256':h.hexdigest()};rows.append(row);print(row,flush=True)
(E/'rpm-downloads.json').write_text(json.dumps(rows,indent=2)+'\n')
