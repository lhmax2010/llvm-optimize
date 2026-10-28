from common import *
import re
C=D/'scratch.debug-probe';C.mkdir(exist_ok=True);copied={}
def copy(src,dest):
 dst=C/dest.lstrip('/');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);dst.chmod(src.stat().st_mode&0o777);copied[dest]={'source':str(src),'bytes':dst.stat().st_size,'sha256':sha(dst)}
def exe(src,dest):
 copy(src,dest);q=run('chroot-deps/'+Path(dest).name,[*LD,'--list',src]);assert q['rc']==0
 for s in re.findall(r'(/[^\s]+) \(0x', (E/('chroot-deps/'+Path(dest).name+'.stdout')).read_text()):
  p=Path(s)
  if p.is_file():
   rel='/'+str(p.relative_to(R)) if str(p).startswith(str(R)+'/') else s
   copy(p,rel)
exe(R/'usr/bin/lldb-instr','/usr/bin/lldb-instr')
exe(BUILD/'bin/lldb-server','/usr/bin/lldb-server')
exe(D/'scheme-a/clang-22','/usr/bin/clang-22')
for name in ['sh','mount','umount']:
 exe(R/'bin'/name,'/bin/'+name)
exe(R/'usr/bin/env','/usr/bin/env')
copy(R/'lib64/ld-linux-x86-64.so.2','/lib64/ld-linux-x86-64.so.2')
copy(D/'scheme-a/clang-22.debug','/usr/lib/debug/usr/bin/clang-22.debug')
(C/'probe').mkdir(exist_ok=True);(C/'proc').mkdir(exist_ok=True);(C/'tmp').mkdir(exist_ok=True);(C/'dev').mkdir(exist_ok=True)
(C/'dev/null').touch();(C/'probe/crash.c').write_text('#pragma clang __debug crash\n')
cmds=['settings set target.disable-aslr false','settings set target.disable-stdio true','target create /usr/bin/clang-22','image list -v','image lookup -n clang::ParseAST','settings set target.run-args --no-default-config -fno-crash-diagnostics -fsyntax-only /probe/crash.c','run','bt all','quit']
(C/'probe/probe.lldb').write_text('\n'.join(cmds)+'\n');save('chroot-files.json',copied)
# Use only existing sudo chroot authorization; no writes to historical roots.
argv=['sudo','-n','/usr/sbin/chroot',C,'/usr/bin/env','LLVM_PROFILE_FILE=/probe/lldb.profraw','LLDB_DEBUGSERVER_PATH=/usr/bin/lldb-server','/usr/bin/lldb-instr','--no-lldbinit','--batch','-s','/probe/probe.lldb']
print(run('chroot-lldb-no-proc',argv,timeout=90),flush=True)
