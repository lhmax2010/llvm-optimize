import os,sys,json,time,subprocess,hashlib,stat,shutil,lzma,signal,fcntl,traceback
from pathlib import Path
E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged';G=1024**3
mounts=[];result={'status':'NOT RUN','matrix':[],'prep':[]};lock=None;project=None;child=None;started=time.monotonic()
def save(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024**2),b''):h.update(b)
 return h.hexdigest()
def cmd(a):
 r=subprocess.run(list(map(str,a)),capture_output=True,text=True)
 with (E/'mount-commands.jsonl').open('a') as f:f.write(json.dumps({'argv':list(map(str,a)),'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr})+'\n')
 if r.returncode:raise RuntimeError(repr(a)+' '+r.stderr)
 return r.stdout
def snapshot(label):
 root=L/'home/abuild/rpmbuild/BUILD';n=0
 with lzma.open(E/(label+'-build.jsonl.xz'),'wt') as f:
  for d,ds,fs in os.walk(root,onerror=lambda x:(_ for _ in ()).throw(x)):
   ds.sort();fs.sort()
   for v in sorted(ds+fs):
    p=Path(d)/v;s=p.lstat();row={'path':p.relative_to(root).as_posix(),'mode':s.st_mode,'bytes':s.st_size,'mtime_ns':s.st_mtime_ns}
    if stat.S_ISLNK(s.st_mode):row['target']=os.readlink(p)
    f.write(json.dumps(row,sort_keys=True)+'\n');n+=1
 build=root/'llvm-22.1.8/build';files=[]
 for name in ['CMakeCache.txt','build.ninja','.ninja_log','.ninja_deps','bin/clang-22','lib64/libtf_xla_runtime.a']:
  p=build/name;files.append({'path':name,'bytes':p.stat().st_size,'sha256':sha(p)})
 value={'paths':n,'manifest_sha256':sha(E/(label+'-build.jsonl.xz')),'files':files};save(label+'-snapshot.json',value);return value
prefix=['/usr/sbin/chroot','--userspec=1000:1000',str(M),'/usr/bin/env','-i','HOME=/home/abuild','USER=abuild','LOGNAME=abuild','SHELL=/bin/sh','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LC_ALL=C','LANG=C']
def kill(p):
 try:os.killpg(p.pid,signal.SIGKILL)
 except ProcessLookupError:pass
 p.wait()
def run(name,a,timeout=120):
 global child
 ts=time.monotonic();timed=False;guard=None
 with (E/(name+'.stdout')).open('wb') as out,(E/(name+'.stderr')).open('wb') as err:
  child=subprocess.Popen(prefix+a,stdout=out,stderr=err,start_new_session=True)
  while child.poll() is None:
   avail=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
   if time.monotonic()-ts>timeout:timed=True;kill(child);break
   if avail<3*G or shutil.disk_usage(E).free<30*G or time.monotonic()-started>3200:
    guard='resource admission/runtime guard';kill(child);break
   time.sleep(.1)
  rc=child.wait();child=None
 row={'name':name,'argv':prefix+a,'rc':rc,'seconds':time.monotonic()-ts,'timeout':timed,'resource_abort':guard}
 save(name+'-result.json',row)
 if guard:raise RuntimeError(guard)
 return row
try:
 assert os.geteuid()==0
 save('root-entry.json',{'time':time.time(),'pid':os.getpid()})
 lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+')
 waitstart=time.monotonic()
 while True:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
  except BlockingIOError:
   if time.monotonic()-waitstart>7200:raise TimeoutError('shared lock wait >2h')
   time.sleep(1)
 started=time.monotonic();save('locks.json',{'shared_lock_acquired':time.time(),'wait_seconds':started-waitstart})
 project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
 fd=os.open(project,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o644);os.write(fd,json.dumps({'pid':os.getpid(),'evidence':str(E)}).encode());os.close(fd)
 avail=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
 assert avail>=6*G
 free=shutil.disk_usage(E).free;save('admission.json',{'MemAvailable':avail,'disk_free':free,'max_write_budget':20*G,'projected_free':free-20*G,'minimum_free':30*G,'memory_cap':4*G,'swap_cap':0,'nice':19,'ionice':3})
 assert free-20*G>=30*G
 before=snapshot('lower-before')
 for name in ['upper','work','merged']:(E/name).mkdir()
 (E/'mountinfo-before.txt').write_text(Path('/proc/self/mountinfo').read_text())
 cmd(['mount','-t','overlay','overlay','-o',f'lowerdir={L},upperdir={E}/upper,workdir={E}/work',M]);mounts.append(M)
 cmd(['mount','-t','proc','proc',M/'proc']);mounts.append(M/'proc')
 cmd(['mount','-t','tmpfs','-o','mode=755,nosuid','bolt26-dev',M/'dev']);mounts.append(M/'dev')
 for n,major,minor in [('null',1,3),('zero',1,5),('full',1,7),('random',1,8),('urandom',1,9),('tty',5,0)]:
  os.mknod(M/'dev'/n,stat.S_IFCHR|0o666,os.makedev(major,minor));os.chmod(M/'dev'/n,0o666)
 for n,target in [('fd','/proc/self/fd'),('stdin','/proc/self/fd/0'),('stdout','/proc/self/fd/1'),('stderr','/proc/self/fd/2')]:os.symlink(target,M/'dev'/n)
 (M/'dev/shm').mkdir(mode=0o1777);os.chmod(M/'dev/shm',0o1777)
 # Fresh device nodes only; no host bind mounts.
 (E/'mountinfo-during.txt').write_text(Path('/proc/self/mountinfo').read_text())
 D=M/'home/abuild/bolt26';D.mkdir()
 for label in ['before','after']:
  shutil.copytree(E/('export-'+label),D/('export-'+label))
  p=D/('export-'+label)/'llvm.spec';rollback=p.read_text().replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1)
  (p.parent/'llvm-rollback.spec').write_text(rollback)
 for name in ['BUILD','BUILDROOT','RPMS','SRPMS','SPECS']:(D/name).mkdir()
 for d,ds,fs in os.walk(D):
  os.chown(d,1000,1000)
  for n in fs:os.chown(Path(d)/n,1000,1000)
 version=run('tizen-rpm-version',['/usr/bin/rpm','--version']);assert version['rc']==0
 assert '4.14.1.1' in (E/'tizen-rpm-version.stdout').read_text()
 run('rpm-environment',['/bin/sh','-c','printf "PATH=%s\\n" "$PATH"; command -v clang; command -v clang++; rpm --eval "%{_toolchain} %{_target_cpu} %{_target_os}"'])
 cases=[('x86-default','x86_64-tizen-linux',[],False),('x86-without','x86_64-tizen-linux',['--without','clang_bolt'],False),('x86-rollback','x86_64-tizen-linux',[],True),('armv7l','armv7l-tizen-linux',[],False),('aarch64','aarch64-tizen-linux',[],False)]
 for label in ['before','after']:
  for case,target,extra,rollback in cases:
   name=label+'-'+case;spec=f'/home/abuild/bolt26/export-{label}/'+('llvm-rollback.spec' if rollback else 'llvm.spec')
   common=['--target',target,'--define',f'_sourcedir /home/abuild/bolt26/export-{label}','--define','_builddir /home/abuild/bolt26/BUILD','--define','_buildrootdir /home/abuild/bolt26/BUILDROOT']+extra
   row=run(name,['/usr/bin/rpmspec','-P']+common+[spec]);stderr=(E/(name+'.stderr')).read_text();stdout=(E/(name+'.stdout')).read_text()
   import re
   row['source_patch_list']=[l for l in stdout.splitlines() if re.match(r'^(Source|Patch)\d*:',l)]
   if label=='before' and case in ['armv7l','aarch64'] and 'No patch number 0' not in stderr:
    fallback=run(name+'-bp-fallback',['/usr/bin/rpmbuild','-bp','--nodeps']+common+[spec]);stderr=(E/(name+'-bp-fallback.stderr')).read_text();row['bp_fallback']=fallback
   expected_fail=label=='before' and case!='x86-default'
   row['PASS']=('No patch number 0' in stderr and row['rc']!=0) if expected_fail else row['rc']==0 and len([l for l in row['source_patch_list'] if l.startswith('Patch')])==7
   result['matrix'].append(row);save('parse-results.json',result)
   if not row['PASS']:raise RuntimeError('PRODUCT GATE '+name+': '+stderr)
 # Optional %prep only: 20-minute total budget, both targets use the x86 RPM executable.
 prepstart=time.monotonic()
 for target in ['armv7l-tizen-linux','aarch64-tizen-linux']:
  name='prep-'+target.split('-')[0];remaining=1200-(time.monotonic()-prepstart)
  if remaining<=0:result['prep'].append({'name':name,'status':'NOT RUN','reason':'20-minute time budget exhausted'});continue
  row=run(name,['/usr/bin/rpmbuild','-bp','--nodeps','--target',target,'--define','_sourcedir /home/abuild/bolt26/export-after','--define','_builddir /home/abuild/bolt26/BUILD','--define','_buildrootdir /home/abuild/bolt26/BUILDROOT','/home/abuild/bolt26/export-after/llvm.spec'],remaining)
  text=(E/(name+'.stdout')).read_text()+(E/(name+'.stderr')).read_text()
  row['applied_patch_numbers']=re.findall(r'Patch #(\d+)',text)
  row['status']='NOT RUN' if row['timeout'] else ('PASS' if row['rc']==0 and row['applied_patch_numbers']==list(map(str,range(7))) else 'FAIL')
  result['prep'].append(row);save('parse-results.json',result)
  if row['status']=='FAIL':raise RuntimeError('PRODUCT GATE optional prep failed: '+name+' '+text[-2500:])
 result['status']='PASS'
except Exception as exc:
 result.update(status='STOP',reason=str(exc));(E/'root-exception.txt').write_text(traceback.format_exc())
finally:
 if child is not None and child.poll() is None:kill(child)
 errors=[]
 for mount in reversed(mounts):
  try:cmd(['umount',mount])
  except Exception as exc:errors.append(str(exc))
 result['unmount_errors']=errors
 (E/'mountinfo-after.txt').write_text(Path('/proc/self/mountinfo').read_text())
 if 'before' in globals():
  try:result['lower_unchanged']=before==snapshot('lower-after')
  except Exception as exc:result['lower_audit_error']=str(exc)
 if project and project.exists():
  try:
   if json.loads(project.read_text()).get('pid')==os.getpid():project.unlink()
  except Exception:pass
 result['lock_held_seconds']=time.monotonic()-started
 if lock:fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
 result['disk_free_after']=shutil.disk_usage(E).free
 if errors or result.get('lower_unchanged') is False:result['status']='STOP'
 save('parse-results.json',result)
 for d,ds,fs in os.walk(E):
  if Path(d)==E/'upper' or Path(d)==E/'work' or Path(d)==E/'merged':ds[:]=[];continue
  os.chown(d,1000,1000)
  for n in fs:os.chown(Path(d)/n,1000,1000)
sys.exit(0 if result['status']=='PASS' else 1)
