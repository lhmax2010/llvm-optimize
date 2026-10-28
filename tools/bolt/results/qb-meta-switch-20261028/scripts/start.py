from pathlib import Path
import subprocess,json,hashlib,urllib.request,xml.etree.ElementTree as X,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=Path(__file__).resolve().parent;E=B/'tools/bolt/results/qb-meta-switch-20261028';R=W/'temp/qb-meta-20261028/repo'
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
head=git('rev-parse','origin/master').decode().strip();(E/'master.txt').write_bytes(git('show','-s','--format=fuller',head));prov=[]
for name in ['Tizen-Base-Toolchain','Tizen-Base-Dev','Tizen-Unified-Toolchain','Tizen-Unified']:
 prefix='TIZEN/Tizen/'+name+'/'
 for p in git('ls-tree','-r','--name-only',head,'--',prefix).decode().splitlines():
  data=git('show',head+':'+p);out=E/'metadata'/name/p[len(prefix):];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data);prov.append(dict(file=str(out.relative_to(E)),git_commit=head,git_path=p,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
(E/'metadata-provenance.json').write_text(json.dumps(prov,indent=2)+'\n')
urls={
 'unified-reference':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/reference/',
 'unified-fixed':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified/tizen-unified_20261027.231956/',
 'unified-toolchain-fixed':'https://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Unified-Toolchain/tizen-unified-toolchain_20261016.052151/'}
rows=[]
for label,url in urls.items():
 try:
  with urllib.request.urlopen(url,timeout=60) as r:data=r.read();row=dict(url=url,final_url=r.url,status=r.status)
  p=E/(label+'.html');p.write_bytes(data);row.update(file=p.name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
 except Exception as ex:row=dict(url=url,error=str(ex))
 rows.append(row);print(label,row.get('status'),row.get('bytes'),row.get('error'),flush=True)
(E/'public-provenance.json').write_text(json.dumps(rows,indent=2)+'\n')
