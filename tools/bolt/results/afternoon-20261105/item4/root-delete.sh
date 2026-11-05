#!/bin/sh
set -eu
cd "$(dirname "$0")"
exec python3 -B - <<'PYROOT'
from pathlib import Path
import json,os,subprocess,time,traceback
from checks import identity,process_snapshot,mount_snapshot,command,stamp
E=Path.cwd()
target='/home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full/stage-D/gbs-root'
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
state='failed';reason='precheck';assert os.geteuid()==0
try:
 old=json.loads((E/'precheck.json').read_text());new=identity(target)
 assert new==old['identity'] and new['directory'] and not new['symlink'] and not new['parent_symlink'] and new['realpath']==target,new
 mounts=mount_snapshot([target]);procs=process_snapshot([target]);save('root-precheck.json',dict(identity=new,mounts=mounts,processes=procs))
 refs=[];errors=[]
 for p in (Path(os.sep)/'proc').glob('[0-9]*/mountinfo'):
  try:refs.extend(dict(path=str(p),line=l) for l in p.read_text().splitlines() if target in l)
  except (FileNotFoundError,ProcessLookupError):pass
  except PermissionError as e:errors.append(str(e))
 save('mountinfo.json',dict(references=refs,errors=errors))
 assert not refs and not errors and mounts['rc']==0 and not mounts['matches']
 assert not procs['matches'] and not procs['errors'],procs
 save('df-before.json',command(['df','-B1',target]));start=time.monotonic();reason='rm'
 argv=['rm','-rf','--one-file-system','--',target];p=subprocess.run(argv,capture_output=True,text=True)
 save('delete.json',dict(argv=argv,rc=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=time.monotonic()-start,absent=not os.path.lexists(target)))
 save('df-after.json',command(['df','-B1',str(Path(target).parent)]))
 assert p.returncode==0 and not os.path.lexists(target)
 siblings=[dict(name=p.name,mtime_ns=p.lstat().st_mtime_ns,inode=p.lstat().st_ino,bytes=p.lstat().st_size) for p in Path(target).parent.iterdir() if p.name!='gbs-root'];save('siblings-after.json',siblings);assert sorted(siblings,key=lambda v:v['name'])==sorted(old['siblings'],key=lambda v:v['name'])
 state='ok';reason='only-approved-stage-D-root-removed-siblings-unchanged'
except BaseException:traceback.print_exc();raise
finally:
 line='ITEM4 已结束 '+stamp()+' status='+state+' reason='+reason;(E/'end.txt').write_text(line+'\n');print(line,flush=True)
PYROOT
