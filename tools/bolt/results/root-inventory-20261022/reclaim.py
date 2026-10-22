#!/usr/bin/env python3
"""Compute a conservative deletion scenario; never remove/copy source files."""
from pathlib import Path
import os,stat,json,datetime,hashlib
D=Path(__file__).resolve().parent
T=Path('/home/linhao/Toolchain/development/llvm-optimize/temp')
roots=[T/'bolt-v4-20261015-review3/payload-merged',T/'bolt-v4-20261015-review4b/payload-merged',T/'bolt-v4-20261015-validation/baseline-extract',T/'bolt-v4-20261015-install-rehearsal/upper']
assets=json.loads((D/'preserve-assets.json').read_text()); keep={x['path'] for x in assets if x['path'].startswith(str(roots[-1])+'/')}
records={}; errors=[]; totals=[]
for root in roots:
 count=0; blocks=0; local=set()
 def err(e):errors.append({'path':e.filename,'error':str(e)})
 for base,dirs,files in os.walk(root,followlinks=False,onerror=err):
  for p in [Path(base)]+[Path(base)/n for n in files]+[Path(base)/n for n in dirs if (Path(base)/n).is_symlink()]:
   try:s=p.lstat()
   except OSError as e:err(e);continue
   key=(s.st_dev,s.st_ino); count+=1
   if key not in local: blocks+=s.st_blocks*512; local.add(key)
   r=records.setdefault(key,{'blocks':s.st_blocks*512,'bytes':s.st_size,'nlink':s.st_nlink,'dir':stat.S_ISDIR(s.st_mode),'names':[]})
   r['names'].append(str(p))
   if str(root)==str(roots[-1]) and '/clang-bolt/' in str(p) and stat.S_ISREG(s.st_mode) and s.st_size<=10*1024**2 and p.suffix in {'.json','.jsonl','.log','.txt','.sh','.py','.tsv'}:keep.add(str(p))
 totals.append({'path':str(root),'allocated_bytes':blocks,'paths':count,'du_unit':'st_blocks * 512, unique inode per root'})
 print(str(root),blocks,count,flush=True)
external=[]; eligible=0; preserve=[]
for k,r in records.items():
 if not r['dir'] and r['nlink']>len(set(r['names'])):external.append({'device':k[0],'inode':k[1],**r});continue
 eligible+=r['blocks']
 for n in r['names']:
  if n in keep:
   preserve.append({'path':n,'bytes':r['bytes'],'allocated_bytes':r['blocks'],'reserve_copy_bytes':((r['bytes']+4095)//4096)*4096});break
known={x['path']:x['sha256'] for x in assets if 'sha256' in x}
for x in preserve:
 x['sha256']=known.get(x['path']) or hashlib.sha256(Path(x['path']).read_bytes()).hexdigest()
reserve=sum(x['reserve_copy_bytes'] for x in preserve)
out={'time':datetime.datetime.now().astimezone().isoformat(),'roots':totals,'errors':errors,'gross_unique_allocated':sum(r['blocks'] for r in records.values()),'external_hardlink_inodes':external,'reclaimable_before_preservation':eligible,'preserve_files':preserve,'preserve_copy_reservation':reserve,'net_reclaim_scenario':eligible-reserve,'note':'Proposal only. No source writes/deletion/copy. Copy reserve rounds logical size to 4096; excludes new directory metadata. Free space is not a guarantee.'}
(D/'reclaim-scenario.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('NET',eligible-reserve,'external',len(external),'errors',len(errors),'preserve',len(preserve),flush=True)
