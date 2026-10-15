from pathlib import Path
import subprocess as sp,os,json,time,signal,shlex,fcntl,hashlib
W=Path.cwd();E=W/'temp/hybrid-link-20261015';R=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';S=E/'source'
(E/'home').mkdir(exist_ok=True);(E/'tmp').mkdir(exist_ok=True)
(S/'mlgo_verify_assets').mkdir(exist_ok=True)
sp.run(['tar','-C',str(S/'mlgo_verify_assets'),'-xzf',str(S/'packaging/mlgo_x86_model.tar.gz')],check=True)
lock=open(W.parent/'heavy-stage.lock','a');print('Waiting for shared configuration lock',flush=True);fcntl.flock(lock,fcntl.LOCK_EX);print('Shared lock acquired',flush=True)
try:
 for label in ['b','a','c']:
  if label=='a': sp.run(['git','-C',str(S),'apply',str(E/'source-port.diff')],check=True)
  args=json.loads((E/('x86_64-'+('baseline' if label=='b' else 'hybrid')+'-cmake.json')).read_text())[:-1]
  if label=='c':args=[x.replace('-DTIZEN_HYBRID_LINK=ON','-DTIZEN_HYBRID_LINK=OFF') for x in args]
  args+=['-DLLVM_THINLTO_CACHE_PATH=/tmp/hybrid52/config-'+label+'/lto.cache']
  cmd=['/usr/bin/cmake','-S','/tmp/hybrid52/source/llvm','-B','/tmp/hybrid52/config-'+label,*args]
  (E/(label+'-configure-argv.json')).write_text(json.dumps(cmd,indent=2)+'\n')
  inner='set -eu\nexport HOME=/tmp/hybrid52/home TMPDIR=/tmp/hybrid52/tmp PYTHONDONTWRITEBYTECODE=1\ncd /tmp/hybrid52/source\nexec '+shlex.join(cmd)+'\n'
  (E/(label+'-configure.sh')).write_text(inner)
  ns='set -eu\nmount --make-rprivate /\nmount --bind "$1" "$2/tmp/hybrid52"\nexec chroot "$2" /bin/bash /tmp/hybrid52/'+label+'-configure.sh'
  argv=['systemd-run','--user','--scope','--unit=llvm52-config-'+label,'-p','MemoryMax=18G','-p','MemorySwapMax=0','nice','-n','19','ionice','-c3','unshare','-Ur','-m','sh','-c',ns,'sh',str(E),str(R)]
  (E/(label+'-outer-argv.json')).write_text(json.dumps(argv,indent=2)+'\n')
  mem=lambda:int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
  assert mem()>=6*1024**3
  t=time.monotonic();out=open(E/(label+'-configure.log'),'w');p=sp.Popen(argv,stdout=out,stderr=sp.STDOUT,start_new_session=True)
  samples=[];reason=None
  while p.poll() is None:
   st=os.statvfs(E);row={'elapsed':time.monotonic()-t,'available_memory':mem(),'available_disk':st.f_bavail*st.f_frsize};samples.append(row)
   if row['available_memory']<2*1024**3 or row['available_disk']<30*1024**3 or row['elapsed']>1800:
    reason='RESOURCE_OR_TIMEOUT';sp.run(['systemctl','--user','kill','--kill-whom=all','--signal=TERM','llvm52-config-'+label+'.scope']);p.wait();break
   time.sleep(2)
  out.close();result={'label':label,'exit':p.returncode,'wall_seconds':time.monotonic()-t,'reason':reason,'samples':samples}
  (E/(label+'-configure-result.json')).write_text(json.dumps(result,indent=2)+'\n');print(label,p.returncode,result['wall_seconds'],flush=True)
  if p.returncode or reason:raise SystemExit('CONFIGURE_FAILED_'+label)
finally:fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
