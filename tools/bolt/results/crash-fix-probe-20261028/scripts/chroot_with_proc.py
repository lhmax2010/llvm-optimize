from common import *
C=D/'scratch.debug-probe'
run('chroot-mountinfo-before',['findmnt','-R',str(C)])
m=run('chroot-proc-mount',['sudo','-n','/usr/sbin/chroot',C,'/bin/mount','-n','-t','proc','none','/proc'])
try:
 if m['rc']==0:
  run('chroot-mountinfo-during',['findmnt','-t','proc'])
  x=run('chroot-lldb-with-proc',['sudo','-n','/usr/sbin/chroot',C,'/usr/bin/env','LLDB_DEBUGSERVER_PATH=/usr/bin/lldb-server','/usr/bin/lldb','--no-lldbinit','--batch','-s','/probe/probe.lldb'],timeout=90);print(x,flush=True)
finally:
 if m['rc']==0:print(run('chroot-proc-umount',['sudo','-n','/usr/sbin/chroot',C,'/bin/umount','/proc']),flush=True)
 run('chroot-mountinfo-after',['findmnt','-R',str(C)])
