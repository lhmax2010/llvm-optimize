from common import *
import re
C=D/'scratch.debug-probe';copied={}
def cp(src,dest):
 dst=C/dest.lstrip('/');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);dst.chmod(src.stat().st_mode&0o777);copied[dest]={'source':str(src),'bytes':dst.stat().st_size,'sha256':sha(dst)}
cp(BUILD/'bin/lldb','/usr/bin/lldb')
for p in re.findall(r'(/[^\s]+) \(0x',(E/'build-lldb-deps.stdout').read_text()):
 p=Path(p)
 if p.is_file():cp(p,'/lib64/'+p.name)
save('chroot-lldb-files.json',copied)
# platform-installed lldb-instr is instrumentation utility, not debugger; use existing built LLDB, no rebuild.
argv=['sudo','-n','/usr/sbin/chroot',C,'/usr/bin/env','LLDB_DEBUGSERVER_PATH=/usr/bin/lldb-server','/usr/bin/lldb','--no-lldbinit','--batch','-s','/probe/probe.lldb']
print(run('chroot-lldb-built-no-proc',argv,timeout=90),flush=True)
