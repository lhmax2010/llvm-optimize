"""Local-only validation wrapper: one graphical authentication; read-only lower."""
import os,sys,json,time,subprocess,hashlib,stat,shutil,lzma,signal,fcntl,traceback,re
from pathlib import Path
E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged-rpm';G=1024**3
mounts=[];result={'status':'NOT RUN','matrix':[],'real_full':'NOT RUN'};lock=None;project=None;child=None;started=time.monotonic();before=None
S=W/'temp/bolt-v4-20261013/v41/llvm-source';helper=S/'packaging/clang-bolt-helper.py'
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
def run(name,a,timeout=120,host=False,env=None):
 global child
 ts=time.monotonic();timed=False;guard=None;argv=a if host else prefix+a
 with (E/(name+'.stdout')).open('wb') as out,(E/(name+'.stderr')).open('wb') as err:
  def drop():os.setgroups([]);os.setgid(1000);os.setuid(1000)
  child=subprocess.Popen(argv,stdout=out,stderr=err,start_new_session=True,env=env,preexec_fn=drop if host else None)
  while child.poll() is None:
   avail=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
   if time.monotonic()-ts>timeout:timed=True;kill(child);break
   if avail<3*G or shutil.disk_usage(E).free<30*G or time.monotonic()-started>3200:
    guard='local resource runtime guard';kill(child);break
   time.sleep(.1)
  rc=child.wait();child=None
 row={'name':name,'argv':argv,'rc':rc,'seconds':time.monotonic()-ts,'timeout':timed,'resource_abort':guard}
 save(name+'-result.json',row)
 if guard:raise RuntimeError(guard)
 return row
try:
 assert os.geteuid()==0
 while not (E/"release-ready").exists():time.sleep(.2)
 save('root-entry.json',{'time':time.time(),'pid':os.getpid()})
 lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+')
 waitstart=time.monotonic()
 while True:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
  except BlockingIOError:
   save('lock-wait.json',{'waiting':True,'seconds':time.monotonic()-waitstart})
   if time.monotonic()-waitstart>7200:raise TimeoutError('shared lock wait >2h')
   time.sleep(1)
 started=time.monotonic();save('locks.json',{'shared_lock_acquired':time.time(),'wait_seconds':started-waitstart})
 project=W/'temp/gbs-root-x86_64-archivefix-v2/.llvm-optimize-exclusive.lock'
 fd=os.open(project,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o644);os.write(fd,json.dumps({'pid':os.getpid(),'evidence':str(E)}).encode());os.close(fd)
 avail=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemAvailable:')))*1024
 assert avail>=6*G
 free=shutil.disk_usage(E).free
 save('admission.json',{'local_only':True,'MemAvailable':avail,'disk_free':free,'bounded_write_estimate':G,'memory_cap':4*G,'swap_cap':0,'nice':19,'ionice':3})
 assert free-G>=30*G
 before=snapshot('lower-before')
 for name in ['upper-rpm','work-rpm','merged-rpm']:(E/name).mkdir()
 (E/'mountinfo-before.txt').write_text(Path('/proc/self/mountinfo').read_text())
 cmd(['mount','-t','overlay','overlay','-o',f'lowerdir={L},upperdir={E}/upper-rpm,workdir={E}/work-rpm',M]);mounts.append(M)
 cmd(['mount','-t','proc','proc',M/'proc']);mounts.append(M/'proc')
 cmd(['mount','-t','tmpfs','-o','mode=755,nosuid','bolt27-dev',M/'dev']);mounts.append(M/'dev')
 for n,major,minor in [('null',1,3),('zero',1,5),('full',1,7),('random',1,8),('urandom',1,9),('tty',5,0)]:
  os.mknod(M/'dev'/n,stat.S_IFCHR|0o666,os.makedev(major,minor));os.chmod(M/'dev'/n,0o666)
 for n,target in [('fd','/proc/self/fd'),('stdin','/proc/self/fd/0'),('stdout','/proc/self/fd/1'),('stderr','/proc/self/fd/2')]:os.symlink(target,M/'dev'/n)
 (M/'dev/shm').mkdir(mode=0o1777);os.chmod(M/'dev/shm',0o1777)
 (E/'mountinfo-during.txt').write_text(Path('/proc/self/mountinfo').read_text())
 D=M/'home/abuild/bolt27';D.mkdir();shutil.copytree(E/'export',D/'export')
 p=D/'export/llvm.spec';assert '%bcond_without clang_bolt' in p.read_text()
 (p.parent/'llvm-rollback.spec').write_text(p.read_text().replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
 for name in ['BUILD','BUILDROOT','RPMS','SRPMS','SPECS','tmp']:(D/name).mkdir()
 # This wrapper copies RPM's generated script and never executes it.
 capture=D/'copy-shell.sh';capture.write_text('#!/bin/sh\nset -eu\nfor script do :; done\ncp "$script" /home/abuild/bolt27/captured-install.sh\n');capture.chmod(0o755)
 for d,ds,fs in os.walk(D):
  os.chown(d,1000,1000)
  for n in fs:os.chown(Path(d)/n,1000,1000)
 version=run('tizen-rpm-version',['/usr/bin/rpm','--version']);assert version['rc']==0
 pkg=run('tizen-rpm-package-version',['/usr/bin/rpm','-q','--qf','%{NAME} %{VERSION}-%{RELEASE}\n','rpm','rpm-build']);assert pkg['rc']==0
 assert all(line.split()[1].startswith('4.14.1.1-') for line in (E/'tizen-rpm-package-version.stdout').read_text().splitlines())
 run('rpm-environment',['/bin/sh','-c','printf "PATH=%s\\n" "$PATH"; command -v clang; command -v clang++; rpm --eval "%{_toolchain} %{_target_cpu} %{_target_os}"'])
 cases=[('x86-default','x86_64-tizen-linux',[],False),('x86-without','x86_64-tizen-linux',['--without','clang_bolt'],False),('x86-rollback','x86_64-tizen-linux',[],True),('armv7l','armv7l-tizen-linux',[],False),('aarch64','aarch64-tizen-linux',[],False)]
 for case,target,extra,rollback in cases:
  spec='/home/abuild/bolt27/export/'+('llvm-rollback.spec' if rollback else 'llvm.spec')
  common=['--target',target,'--define','_sourcedir /home/abuild/bolt27/export','--define','_builddir /home/abuild/bolt27/BUILD','--define','_buildrootdir /home/abuild/bolt27/BUILDROOT','--define','_tmppath /home/abuild/bolt27/tmp','--define','_toolchain clang']+extra
  row=run(case,['/usr/bin/rpmbuild','-bp','--nodeps','--nobuild']+common+[spec])
  expand_common=common[:-len(extra)] if extra else common.copy()
  if extra:expand_common+=['--define','_without_clang_bolt 1']
  expansion=run(case+'-expanded',['/usr/bin/rpmspec','-P']+expand_common+[spec]);row['source_patch_expansion']=expansion
  stdout=(E/(case+'-expanded.stdout')).read_text();row['source_patch_list']=[l for l in stdout.splitlines() if re.match(r'^(Source|Patch)\d*:',l)]
  row['PASS']=row['rc']==0 and expansion['rc']==0 and len([l for l in row['source_patch_list'] if l.startswith('Patch')])==7
  result['matrix'].append(row);save('parse-results.json',result)
  if not row['PASS']:raise RuntimeError('PRODUCT GATE '+case+': '+(E/(case+'.stderr')).read_text())
 # Capture the actual Tizen macro-chain script, without running install/cmake/ninja.
 cap=run('tizen-install-capture',['/usr/bin/rpmbuild','-bi','--short-circuit','--nodeps','--target','x86_64-tizen-linux','--define','_toolchain clang','--define','_sourcedir /home/abuild/bolt27/export','--define','_builddir /home/abuild/bolt27/BUILD','--define','_buildrootdir /home/abuild/bolt27/BUILDROOT','--define','_tmppath /home/abuild/bolt27/tmp','--define','__spec_install_cmd /home/abuild/bolt27/copy-shell.sh %{___build_args}','/home/abuild/bolt27/export/llvm.spec'])
 script=D/'captured-install.sh';assert script.is_file() and script.stat().st_size>0
 shutil.copyfile(script,E/'tizen-captured-install.sh')
 syntax=run('tizen-install-syntax',['/bin/sh','-n','/home/abuild/bolt27/captured-install.sh']);assert syntax['rc']==0
 result['tizen_script_syntax']='PASS';result['capture_exit_expected_filelist']=cap['rc']
 # Optional real ENOSPC, bounded to a 1 MiB tmpfs. Host logs stay outside it.
 F=E/'real-full';F.mkdir();cmd(['mount','-t','tmpfs','-o','size=1m,mode=1777,nosuid,nodev','bolt27-full',F]);mounts.append(F)
 build=F/'build';work=build/'clang-bolt';(build/'bin').mkdir(parents=True);work.mkdir()
 (build/'bin/clang-22').write_bytes(b'x'*16384);(work/'ordinary-clang-22').write_bytes(b'x'*16384)
 (work/'link.original').write_text('--thinlto-cache-dir='+str(E/'real-source'))
 for d,ds,fs in os.walk(F):
  os.chown(d,1000,1000)
  for n in fs:os.chown(Path(d)/n,1000,1000)
 env=os.environ.copy();env.update(BOLT_BUILD=str(build),BOLT_WORK=str(work));env.pop('BOLT_PROFILE_SOURCE',None);env.pop('BOLT_INSTALL_ROOT',None)
 report=run('real-full-report',['/usr/bin/python3','-B',str(helper),'disk-report','begin'],host=True,env=env);assert report['rc']==0
 full=run('real-full-copy',['/usr/bin/python3','-B',str(helper),'cache-copy',str(work/'link.original'),str(work/'copy'),str(work/'copy.json')],host=True,env=env)
 transcript=(E/'real-full-copy.stdout').read_text();diags=[json.loads(l.split(' ',1)[1]) for l in transcript.splitlines() if l.startswith('BOLT_DISK_DIAGNOSIS ')]
 assert full['rc']==1 and diags and diags[-1]['cause']=='disk' and all(k in diags[-1] for k in ['used_bytes','free_bytes','estimated_total_bytes','estimated_remaining_bytes','shortfall_bytes'])
 result['real_full']={'status':'PASS','rc':full['rc'],'diagnosis':diags[-1]};result['status']='PASS'
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
 if before is not None:
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
 # Only this wrapper's top-level evidence files; never walk the overlay upper.
 for p in E.iterdir():
  if p.is_file():os.chown(p,1000,1000)
sys.exit(0 if result['status']=='PASS' else 1)
