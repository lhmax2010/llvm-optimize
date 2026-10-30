"""Local-only build child; no production changes."""
import json,subprocess,time,sys
from pathlib import Path
D=Path(__file__).resolve().parent;E=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/debuglink-20261028/rehearsal-20261030/evidence');argv=json.loads((D/'build-command.json').read_text());start=time.time_ns()
r=subprocess.run(argv)
cgroup=next(l.split(':',2)[2] for l in Path('/proc/self/cgroup').read_text().splitlines() if l.startswith('0::'))
base=Path('/sys/fs/cgroup')/cgroup.lstrip('/');stats={}
for name in ('memory.events','memory.peak','memory.swap.peak','memory.max','memory.swap.max'):
 try:stats[name]=(base/name).read_text()
 except OSError as exc:stats[name]=str(exc)
(E/'build-result.json').write_text(json.dumps({'exit_code':r.returncode,'start_ns':start,'end_ns':time.time_ns(),'seconds':(time.time_ns()-start)/1e9,'cgroup':cgroup,'stats':stats},indent=2)+'\n');sys.exit(r.returncode)
