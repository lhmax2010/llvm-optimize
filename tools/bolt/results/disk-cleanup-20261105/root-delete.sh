#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec python3 -B - <<'PYROOT'
from pathlib import Path
import json,os,subprocess,time
from checks import identity,process_snapshot,mount_snapshot,command,stamp
E=Path.cwd()
target='/home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full/stage-A/gbs-root'
def save(n,v):(E/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
assert os.geteuid()==0
assert not (E/'root-entered.json').exists()
save('root-entered.json',{'time':stamp()})
try:
 old=json.loads((E/'precheck-2.json').read_text())['identity']; ident=identity(target)
 assert ident==old and ident['directory'] and not ident['symlink'] and not ident['parent_symlink'] and ident['realpath']==target,ident
 mounts=mount_snapshot([target]);process=process_snapshot([target]);save('root-check.json',{'mounts':mounts,'process':process,'identity':ident})
 refs=[];errors=[]
 for info in (Path(os.sep)/'proc').glob('[0-9]*/mountinfo'):
  try:
   refs += [{'path':str(info),'line':l} for l in info.read_text().splitlines() if target in l]
  except (FileNotFoundError,ProcessLookupError):pass
  except PermissionError as e:errors.append(str(e))
 save('mountinfo-root.json',{'references':refs,'errors':errors})
 assert not refs and not errors
 assert mounts['rc']==0 and not mounts['matches'],mounts
 assert not process['matches'] and not process['errors'],process
 # Read-only check of the ordinary-user target; only target above may be removed here.
 other=json.loads((E/'precheck-1.json').read_text())['identity']['realpath']
 save('payload-root-readonly-process.json',process_snapshot([other]))
 save('df-stage-A-before.json',command(['df','-B1',target]))
 start=time.monotonic();argv=['rm','-rf','--one-file-system','--',target]
 p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 save('stage-A-deletion.json',{'argv':argv,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'seconds':time.monotonic()-start,'absent':not os.path.lexists(target)})
 save('df-stage-A-after.json',command(['df','-B1',str(Path(target).parent)]))
 assert p.returncode==0 and not os.path.lexists(target)
 print('CLEANUP_STAGE_A 已结束',stamp(),'status=ok',flush=True)
except BaseException as e:
 print('CLEANUP_STAGE_A 已结束',stamp(),'status=failed reason='+str(e),flush=True)
 raise
PYROOT
