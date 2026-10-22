#!/usr/bin/env python3
import json,os,subprocess,time,datetime
from pathlib import Path
D=Path(__file__).resolve().parent;H=Path('/home/linhao');W=H/'Toolchain/development/llvm-optimize'
units=set(json.loads((D/'initial-units.json').read_text()))
for base in [H,H/'Toolchain/development/llvm_inline_development/tmp',Path('/var/tmp'),Path('/tmp')]:
 for p in base.iterdir():
  if p.is_dir() and ('gbs' in p.name.lower() or 'llvm' in p.name.lower()):units.add(str(p))
units.update(map(str,[H/'temp/llvm',H/'clang-toolchains',H/'Toolchain/LLVM_Upgrade/llvm',H/'Toolchain/tizen-docs-release',H/'Toolchain/development/llvm',H/'Toolchain/development/llvm_inline_development/tmp',H/'Toolchain/development/llvm_inline_development/codes/llvm',H/'Toolchain/development/llvm_inline_development/docs/llvm_optimize_docs/verification/port22/artifacts',H/'Toolchain/development/llvm_inline_development_second/codes/llvm',H/'Toolchain/development/llvm_image_analysis/work/sparse',H/'Toolchain/development/llvm_image_analysis/work/signature']))
(D/'all-unit-paths.json').write_text(json.dumps(sorted(units),indent=2)+'\n')
results=[]
with (D/'du-units.stdout').open('w') as out,(D/'du-units.stderr').open('w') as err:
 for root in sorted(units):
  t=time.monotonic();arg=['du','-sx','-B1','--time','--time-style=full-iso','--',root]
  try:
   p=subprocess.run(arg,capture_output=True,text=True,timeout=180)
   out.write(p.stdout);out.flush();err.write(p.stderr);err.flush()
   r={'path':root,'argv':arg,'rc':p.returncode,'seconds':time.monotonic()-t,'stdout':p.stdout,'stderr':p.stderr,'time':datetime.datetime.now().astimezone().isoformat()}
   if p.stdout:r['bytes']=int(p.stdout.split('\t')[0])
  except subprocess.TimeoutExpired:r={'path':root,'timeout':180}
  results.append(r);(D/'du-units.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
  print(root,r.get('bytes'),r.get('rc'),flush=True)
locks=[]
for root in units|{str(W),str(W.parent)}:
 p=Path(root)
 for loc in [p,p/'local',p/'local/BUILD-ROOTS']:
  try:
   for c in loc.iterdir():
    if 'lock' in c.name.lower() and not c.is_dir():
     s=c.lstat();locks.append({'path':str(c),'bytes':s.st_size,'mtime':s.st_mtime,'symlink':c.is_symlink()})
  except OSError:pass
(D/'local-lock-file-metadata.json').write_text(json.dumps(locks,indent=2)+'\n')
