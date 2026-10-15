import os,sys,json,time,subprocess,hashlib,stat,shutil,lzma,signal,selectors,traceback
from pathlib import Path
E=Path(__file__).resolve().parent;W=E.parents[1];L=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';M=E/'merged';P=Path('home/abuild/rpmbuild/BUILD/llvm-22.1.8');G=1024**3
mounts=[];result={'status':'NOT RUN','started':time.time()};child=None
def interrupted(sig,frame): raise RuntimeError('signal '+str(sig))
for sig in (signal.SIGTERM,signal.SIGINT,signal.SIGHUP): signal.signal(sig,interrupted)

def save(name,v): (E/name).write_text(json.dumps(v,indent=2)+'\n')
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024**2),b''):h.update(b)
 return h.hexdigest()
def command(argv):
 with (E/'privileged-commands.jsonl').open('a') as f:f.write(json.dumps({'time':time.time(),'argv':list(map(str,argv))})+'\n')
 r=subprocess.run(list(map(str,argv)),capture_output=True,text=True)
 with (E/'mount-commands.log').open('a') as f:f.write(r.stdout+r.stderr)
 if r.returncode:raise RuntimeError('command failed rc=%s argv=%r output=%s%s'%(r.returncode,argv,r.stdout,r.stderr))
 return r.stdout

def snapshot(name):
 root=L/'home/abuild/rpmbuild/BUILD';n=0
 with lzma.open(E/(name+'-build-paths.jsonl.xz'),'wt') as f:
  for d,ds,fs in os.walk(root,onerror=lambda e:(_ for _ in ()).throw(e)):
   ds.sort();fs.sort()
   for v in sorted(ds+fs):
    p=Path(d)/v;s=p.lstat();r={'path':p.relative_to(root).as_posix(),'mode':s.st_mode,'bytes':s.st_size,'mtime_ns':s.st_mtime_ns}
    if stat.S_ISLNK(s.st_mode):r['target']=os.readlink(p)
    f.write(json.dumps(r,sort_keys=True)+'\n');n+=1
 files=['CMakeCache.txt','build.ninja','.ninja_log','.ninja_deps','bin/clang-22','lib64/libtf_xla_runtime.a'];rows=[]
 for fn in files:
  p=L/P/'build'/fn;rows.append({'path':str(p),'bytes':p.stat().st_size,'sha256':digest(p)})
 save(name+'-critical-sha.json',{'paths':n,'files':rows})
 return {'manifest':digest(E/(name+'-build-paths.jsonl.xz')),'paths':n,'files':rows}

def kill_group(p):
 try:os.killpg(p.pid,signal.SIGKILL)
 except ProcessLookupError:pass
 p.wait()
 until=time.monotonic()+10
 while True:
  live=[]
  for d in Path('/proc').iterdir():
   if d.name.isdigit():
    try:
     fields=(d/'stat').read_text().rsplit(')',1)[1].split()
     if int(fields[2])==p.pid and fields[0] not in ('Z','X'):live.append((d.name,fields[0]))
    except (OSError,ValueError,IndexError):pass
  if not live:return
  if time.monotonic()>until:raise RuntimeError('live descendants after SIGKILL '+repr(live))
  time.sleep(.1)

def sample(cg,phase):
 row={'time':time.time(),'phase':phase,'free_bytes':shutil.disk_usage(E).free,'available_bytes':int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024,'processes':[]}
 for k in ['memory.current','memory.peak','memory.events','memory.max','memory.swap.max']:
  try:row[k]=(cg/k).read_text().strip()
  except OSError:pass
 try:pids=(cg/'cgroup.procs').read_text().split()
 except OSError:pids=[]
 for pid in pids:
  try:
   st=Path('/proc/'+pid+'/status').read_text().splitlines();row['processes'].append({'pid':int(pid),'name':st[0],'VmHWM_kB':int(next((x.split()[1] for x in st if x.startswith('VmHWM:')),'0')),'cmdline':Path('/proc/'+pid+'/cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')[:1200]})
  except OSError:pass
 with (E/'samples.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 return row

def run_rpm(cg):
 global child
 argv=['/usr/sbin/chroot','--userspec=1000:1000',str(M),'/usr/bin/env','-i','HOME=/home/abuild','USER=abuild','LOGNAME=abuild','SHELL=/bin/sh','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LANG=C','LC_ALL=C','/bin/sh','/home/abuild/bolt-rehearsal/abuild.sh']
 save('rpmbuild-argv.json',argv);start=time.monotonic();phase='ordinary-install';last=0;buf=b''
 child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
 sel=selectors.DefaultSelector();sel.register(child.stdout,selectors.EVENT_READ)
 with (E/'rpmbuild.log').open('wb') as raw,(E/'timeline.jsonl').open('a') as timeline:
  while sel.get_map():
   for key,_ in sel.select(.25):
    chunk=os.read(key.fd,131072)
    if not chunk:sel.unregister(key.fileobj);continue
    raw.write(chunk);raw.flush();buf+=chunk
    while b'\n' in buf:
     line,buf=buf.split(b'\n',1);text=line.decode(errors='replace')
     if text.startswith('+ ') or 'BOLT_' in text or text.startswith('error:'):
      timeline.write(json.dumps({'time':time.time(),'line':text})+'\n');timeline.flush()
     if text.startswith('+ '):
      for token,newphase in [('cmake -DCMAKE_INSTALL_PREFIX','ordinary-install'),(' snapshot ','snapshot'),('cmake -S','bolt-configure'),('ninja -n llvm-bolt','tool-dry-run'),('ninja -j 1 llvm-bolt','tool-build'),(' pipeline ','pipeline'),(' compare-root ','compare-root'),('llvm-static-archives-native.py','archive-conversion'),(' install /home/abuild/rpmbuild/BUILDROOT','candidate-install'),('find-debuginfo.sh','find-debuginfo'),(' post ','post-gate')]:
       if token in text:phase=newphase
   now=time.monotonic()
   if now-last>=.5:
    row=sample(cg,phase);last=now
    reason=None
    if row['available_bytes']<3*G:reason='host MemAvailable <3 GiB'
    if row['free_bytes']<30*G:reason='filesystem free <30 GiB'
    if now-float((E/'lock-start-monotonic').read_text())>3500:reason='shared lock 3500-second safety deadline'
    if reason:kill_group(child);raise RuntimeError(reason)
   if child.poll() is not None and not sel.get_map():break
  if buf:raw.write(buf)
 rc=child.wait();child=None
 save('rpmbuild-result.json',{'rc':rc,'wall_seconds':time.monotonic()-start})
 return rc

def copy_evidence():
 b=M/P/'build';work=b/'clang-bolt';out=E/'actual';out.mkdir(exist_ok=True)
 if work.is_dir():
  for d,ds,fs in os.walk(work):
   for f in fs:
    p=Path(d)/f
    if p.suffix in ('.json','.txt','.log','.sh') or p.name=='link.original':
     dest=out/p.relative_to(work);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 for f in ['install_manifest.txt','CMakeCache.txt','build.ninja','CMakeFiles/rules.ninja','native-archive-conversion/summary.json']:
  p=b/f
  if p.is_file():dest=out/('build-'+f.replace('/','_'));shutil.copy2(p,dest)
 for label,p in [('tree-llvm-bolt',b/'bin/llvm-bolt'),('candidate',work/'clang.candidate'),('tf-after',b/'lib64/libtf_xla_runtime.a')]:
  if p.is_file():save(label+'-sha.json',{'path':str(p),'sha256':digest(p),'bytes':p.stat().st_size})
 if (b/'bin/llvm-bolt').is_file():
  argv=['/usr/sbin/chroot','--userspec=1000:1000',str(M),'/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin/llvm-bolt','--version'];r=subprocess.run(argv,capture_output=True,text=True);(E/'tree-llvm-bolt-version.txt').write_text(r.stdout+r.stderr)

try:
 assert os.getuid()==0
 os.setpriority(os.PRIO_PROCESS,0,15)
 command(['ionice','-c','3','-p',str(os.getpid())])
 # Root visibility permits checking writable descriptors in all sessions.
 writers=[]
 for d in Path('/proc').iterdir():
  if not d.name.isdigit():continue
  try:
   for fd in (d/'fd').iterdir():
    try:
     target=os.readlink(fd)
     if target.startswith(str(L)+'/'):
      flags=int(next(x.split()[1] for x in (d/'fdinfo'/fd.name).read_text().splitlines() if x.startswith('flags:')),8)
      if flags & os.O_ACCMODE: writers.append({'pid':d.name,'fd':fd.name,'path':target,'flags':flags})
    except (OSError,StopIteration):pass
  except OSError:pass
 save('lower-writer-scan.json',{'writers':writers})
 assert not writers,'other session has writable lower descriptors'
 save('root-entry.json',{'uid':os.getuid(),'cgroup':Path('/proc/self/cgroup').read_text(),'nice':os.getpriority(os.PRIO_PROCESS,0),'ionice':command(['ionice','-p',str(os.getpid())])})
 cg=Path('/sys/fs/cgroup'+Path('/proc/self/cgroup').read_text().strip().split('::')[1]);assert (cg/'memory.max').read_text().strip()==str(18*G);assert (cg/'memory.swap.max').read_text().strip()=='0'
 assert json.loads((E/'disk-plan.json').read_text())['pass']
 (E/'mountinfo-before.txt').write_text(Path('/proc/self/mountinfo').read_text())
 before=snapshot('lower-before');save('tf-before-sha.json',before['files'][-1])
 for n in ['upper','work','merged']:(E/n).mkdir(exist_ok=False)
 command(['mount','-t','overlay','overlay','-o','lowerdir='+str(L)+',upperdir='+str(E/'upper')+',workdir='+str(E/'work'),M]);mounts.append(M)
 command(['mount','-t','proc','proc',M/'proc']);mounts.append(M/'proc')
 command(['mount','-t','tmpfs','-o','mode=755','tmpfs',M/'dev']);mounts.append(M/'dev')
 for name,major,minor in [('null',1,3),('zero',1,5),('full',1,7),('random',1,8),('urandom',1,9),('tty',5,0)]:os.mknod(M/'dev'/name,stat.S_IFCHR|0o666,os.makedev(major,minor));os.chmod(M/'dev'/name,0o666)
 (M/'dev/shm').mkdir(mode=0o1777);os.chmod(M/'dev/shm',0o1777)
 for name,target in [('fd','/proc/self/fd'),('stdin','fd/0'),('stdout','fd/1'),('stderr','fd/2')]:os.symlink(target,M/'dev'/name)
 (E/'mountinfo-during.txt').write_text(Path('/proc/self/mountinfo').read_text())
 sources=M/'home/abuild/rpmbuild/SOURCES'
 for row in json.loads((E/'source-inputs.json').read_text()):
  if not row.get('reuse_existing_lower'):shutil.copyfile(E/'inputs'/row['name'],sources/row['name'])
  assert digest(sources/row['name'])==row['sha256'],row['name']
 stage=M/'home/abuild/bolt-rehearsal';stage.mkdir();os.chown(stage,1000,1000);shutil.copy2(E/'abuild.sh',stage/'abuild.sh');os.chown(stage/'abuild.sh',1000,1000)
 result['started_install']=time.time();rc=run_rpm(cg);result['rpmbuild_rc']=rc
 copy_evidence()
 text=(E/'rpmbuild.log').read_text(errors='replace')
 if rc!=0:result.update(status='发现问题',reason='rpmbuild %install/post exited nonzero; inspect raw log');print('B_REHEARSAL_PRODUCT_FAILURE',rc,flush=True)
 else:
  assert 'BOLT_POST_GATE_PASS' in text,'missing final post gate'
  cmd=['/usr/sbin/chroot','--userspec=1000:1000',str(M),'/usr/bin/env','-i','HOME=/home/abuild','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LC_ALL=C','/bin/sh','-c',"cd /home/abuild/rpmbuild/BUILD/llvm-22.1.8/build && command -v clang && command -v clang++ && printf 'PATH=%s\\n' \"$PATH\" && NINJA_STATUS='[%f/%t] ' ninja -n llvm-bolt"]
  r=subprocess.run(cmd,capture_output=True,text=True);(E/'final-ninja-no-work.txt').write_text(r.stdout+r.stderr);assert r.returncode==0 and 'ninja: no work to do.' in r.stdout
  result['status']='PASS'
except BaseException as exc:
 if child is not None:
  try:kill_group(child)
  except BaseException:traceback.print_exc()
 result.update(status='发现问题' if result.get('started_install') else 'NOT RUN',exception=repr(exc));(E/'exception.txt').write_text(traceback.format_exc())
 try:
  if mounts:copy_evidence()
 except BaseException:traceback.print_exc()
finally:
 failures=[]
 for p in reversed(mounts):
  try:command(['umount',p])
  except BaseException as exc:failures.append(str(exc))
 (E/'mountinfo-after.txt').write_text(Path('/proc/self/mountinfo').read_text())
 result['unmount_failures']=failures
 if not failures:
  try:
   after=snapshot('lower-after');result['lower_unchanged']=before==after;save('lower-comparison.json',{'same':before==after,'before':before,'after':after})
   if before!=after:result.update(status='发现问题',reason='lower BUILD changed')
  except BaseException as exc:result['lower_audit_error']=repr(exc)
 else:result['status']='发现问题'
 result['ended']=time.time();save('rehearsal-result.json',result)
 for d,ds,fs in os.walk(E):
  # Preserve overlay upper/work ownership and contents; chown only standalone evidence.
  ds[:]=[x for x in ds if x not in ('upper','work','merged')]
  for fn in fs:
   try:os.chown(Path(d)/fn,1000,1000)
   except OSError:pass
 print(json.dumps(result,ensure_ascii=False),flush=True)
 sys.exit(0 if result['status']=='PASS' else 1)
