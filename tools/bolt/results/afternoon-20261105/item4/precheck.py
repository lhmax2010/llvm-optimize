from pathlib import Path
import json
from checks import identity,process_snapshot,mount_snapshot,command,stamp
E=Path(__file__).parent;target='/home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full/stage-D/gbs-root'
r=dict(time=stamp(),identity=identity(target),mounts=mount_snapshot([target]),process=process_snapshot([target]),du=command(['nice','-n','19','ionice','-c3','du','-sx','-B1',target],180),df=command(['df','-B1',target]))
r['siblings']=[dict(name=p.name,mtime_ns=p.lstat().st_mtime_ns,inode=p.lstat().st_ino,bytes=p.lstat().st_size) for p in Path(target).parent.iterdir() if p.name!='gbs-root']
(E/'precheck.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='process'},indent=2));print('process matches',len(r['process']['matches']),'unprivileged read errors',len(r['process']['errors']))
