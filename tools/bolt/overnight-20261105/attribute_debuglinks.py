from pathlib import Path
import sys,json,hashlib,datetime,traceback
from compare_rules import *
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=B/'tools/bolt/results/baseline-attribution-20261105';O=W/'temp/attribution-20261105';sys.path.append(str(B/'tools/bolt/night-launch-20261103'))
from rpm_extract import extract_selected
from rpm_io import manifest
rows=json.loads((E/'attribution-files.json').read_text());mans={};rpms={'new':{},'old':{}}
for p in (E/'cert-manifests').glob('*-old.json'):
 k=p.name.removesuffix('-old.json');mans[k]={'old':json.loads(p.read_text()),'new':json.loads(p.with_name(k+'-new.json').read_text())}
import subprocess
for side,root in [('old',W/'temp/debuglink-20261028/full-20261030/products'),('new',W/'temp/night-20261103/toolchain/gbs-driver/local/repos')]:
 for p in root.glob('**/*.rpm'):
  if p.name.endswith('.src.rpm'):continue
  key=subprocess.check_output(['rpm','-qp','--qf','%{NAME}-%{ARCH}',str(p)],text=True);rpms[side][key]=p
for k in rpms['old'].keys() & rpms['new'].keys():
 if k not in mans:
  mans[k]={side:manifest(rpms[side][k]) for side in ['old','new']}
  for side in ['old','new']:(E/'cert-manifests'/(k+'-'+side+'.json')).write_text(json.dumps(mans[k][side],indent=2)+'\n')
needed={}
for r in rows:
 for side in ['old','new']:
  filename=debuglink_name(r[side])
  if not filename:continue
  name=str(Path('usr/lib/debug')/Path(r['path']).parent/filename)
  owners=[k for k in mans if name in mans[k][side]]
  if owners and not (O/'payload'/owners[0]/side/name).exists() and not (side=='new' and (W/'temp/qb-full-compare-20261105/toolchain'/owners[0]/'old'/name).exists()):needed.setdefault((owners[0],side),set()).add(name)
for (k,side),names in needed.items():extract_selected(rpms[side][k],names,O/'debuglink-extra'/k/side)
result=[]
def symbol(side,path,filename):
 name=str(Path('usr/lib/debug')/Path(path).parent/filename);owners=[k for k in mans if name in mans[k][side]];assert owners,('symbol package not among audited manifests',name)
 k=owners[0];p=O/'payload'/k/side/name
 if not p.exists() and side=='new':p=W/'temp/qb-full-compare-20261105/toolchain'/k/'old'/name
 if not p.exists():p=O/'debuglink-extra'/k/side/name
 with p.open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==mans[k][side][name]['sha256']
 return p
try:
 for r in rows:
  name=debuglink_name(r['old'])
  if not name:continue
  q={k:r[k] for k in ('path','package','old','new')}
  try:q['proof']=debuglink_proof(r['old'],r['new'],symbol('old',r['path'],name),symbol('new',r['path'],debuglink_name(r['new'])));q['PASS']=True
  except Exception as ex:q.update(PASS=False,error=str(ex))
  result.append(q);print('DEBUGLINK_RECHECK',r['package'],r['path'],q['PASS'],flush=True)
finally:
 (E/'cert-debuglink-recheck.json').write_text(json.dumps(result,indent=2)+'\n');line='DEBUGLINK_RECHECK 已结束 '+datetime.datetime.now().astimezone().isoformat()+f' checked={len(result)} passed={sum(r["PASS"] for r in result)}';(E/'debuglink-recheck-end.txt').write_text(line+'\n');print(line,flush=True)
