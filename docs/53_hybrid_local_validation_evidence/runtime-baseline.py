"""Read-only RPM header comparison for runtime script failures."""
import json,subprocess
from pathlib import Path
from validate import W,D,E,R,run,save
B=W/'temp/bolt-v4-20261022-cache-release/baseline-products/RPMS/x86_64';N=R/'home/abuild/rpmbuild/RPMS/x86_64';maps={}
for role,folder in [('baseline',B),('hybrid',N)]:
 entries={}
 for pkg in ['clang','llvm','clang-devel','llvm-devel']:
  p=folder/(pkg+'-22.1.8-1.x86_64.rpm');r=run('runtime-baseline/'+role+'-'+pkg,['rpm','-qp','--qf','[%{FILENAMES}\t%{FILEDIGESTS}\n]',str(p)]);assert r['rc']==0
  entries.update(line.split('\t',1) for line in r['stdout'].splitlines() if '\t' in line)
 maps[role]=entries
rows=[]
for r in json.loads((E/'runtime-result.json').read_text())['rows']:
 if r['status']=='PASS' or not r['script']:continue
 p=r['path'];a=maps['baseline'].get(p);b=maps['hybrid'].get(p);rows.append({'path':p,'baseline_file_digest':a,'hybrid_file_digest':b,'same':bool(a) and a==b})
save('runtime-baseline-comparison.json',{'scripts':rows,'libscanbuild_paths':{k:[p for p in v if 'libscanbuild' in p] for k,v in maps.items()},'scope':'clang/llvm and their devel RPM payload headers; same script bytes do not prove all runtime environment dependencies equivalent'})
