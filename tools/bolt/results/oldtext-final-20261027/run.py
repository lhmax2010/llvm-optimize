"""One isolated hybrid build; no admission, memory freeze, or timed lease rotation."""
import fcntl,json,os,shutil,subprocess,threading,time
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027');plan=json.loads((D/'plan.json').read_text());G=D/'gbs-root';R=G/'local/BUILD-ROOTS/scratch.x86_64.0';unit='oldtext-final-20261027.service';stop=threading.Event();reason=None
assert json.loads((E/'export-result.json').read_text())['rc']==0;assert all(r['PASS'] for r in json.loads((E/'five-parse/matrix.json').read_text()))
assert json.loads((E/'prep-result.json').read_text())['rc']==0;dest=G/'local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1';shutil.copytree(D/'export',dest)
cmd=['gbs','-c',plan['config'],'build','-A','x86_64','-B',str(G),'-c',plan['commit'],'--threads=30','--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20','--baselibs','--style=tar','--spec','llvm.spec',plan['source']]
(D/'build-command.json').write_text(json.dumps(cmd,indent=2)+'\n');(E/'build-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');startwait=time.monotonic();fcntl.flock(lock,fcntl.LOCK_EX);acquired=time.monotonic()
(E/'lock.json').write_text(json.dumps({'acquired_ns':time.time_ns(),'wait_seconds':acquired-startwait,'policy':'exclusive for this single build; no timed freeze per user override'},indent=2)+'\n')
def append(name,j):
 with (E/name).open('a') as f:f.write(json.dumps(j)+'\n')
def du():
 while not stop.is_set():
  stamp=time.time_ns();start=time.monotonic()
  if (R/'usr/bin/python3').exists() and (R/'usr/bin/du').exists():
   code="import subprocess,sys\ntry:\n p=subprocess.run(['/usr/bin/du','-sx','-B1','/'],capture_output=True,text=True,timeout=50);sys.stdout.write(p.stdout);sys.stderr.write(p.stderr);sys.exit(p.returncode)\nexcept subprocess.TimeoutExpired:\n print('DU_TIMEOUT_50_SECONDS',file=sys.stderr);sys.exit(124)"
   argv=['sudo','-n','/usr/sbin/chroot',str(R),'/usr/bin/python3','-B','-c',code]
   try:
    p=subprocess.run(argv,capture_output=True,text=True,timeout=58);row={'time_ns':stamp,'argv':argv,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'seconds':time.monotonic()-start}
   except subprocess.TimeoutExpired:row={'time_ns':stamp,'argv':argv,'missing':'outer timeout 58s','seconds':time.monotonic()-start}
  else:row={'time_ns':stamp,'missing':'chroot du/python not ready'}
  append('du-root.jsonl',row);stop.wait(max(0,60-(time.monotonic()-start)))
def logs():
 global reason
 position=0
 while not stop.wait(2):
  p=R/'.build.log'
  if p.exists():
   with p.open('rb') as src:
    src.seek(position);b=src.read();position+=len(b)
   if b:
    with (E/'rpm-build.log').open('ab') as out:out.write(b)
    if b'BOLT_GATE_FAILED:' in b and reason is None:
     reason='BOLT_GATE_FAILED observed; stop without bypass'
     (E/'gate-stop.json').write_text(json.dumps({'time_ns':time.time_ns(),'tail':b.decode(errors='replace')[-16000:]}))
     subprocess.run(['systemctl','--user','stop',unit],capture_output=True,text=True);return
 if (R/'.build.log').exists():shutil.copyfile(R/'.build.log',E/'rpm-build.log')
def resources():
 global reason
 while not stop.wait(2):
  now=time.time_ns();free=shutil.disk_usage('/home').free
  r=subprocess.run(['systemctl','--user','show',unit,'--property=ControlGroup','--value'],capture_output=True,text=True);cg=r.stdout.strip();row={'time_ns':now,'home_available_bytes':free,'meminfo':Path('/proc/meminfo').read_text(),'cgroup':cg}
  if cg:
   for n in ('memory.current','memory.peak','memory.events','memory.swap.current','cpu.stat','io.stat'):
    try:row[n]=(Path('/sys/fs/cgroup')/cg.lstrip('/')/n).read_text()
    except OSError as exc:row[n]=str(exc)
  work=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
  for file,field in [(work/'rewrite/rewrite-result.json','counts'),(work/'identity.json','identity')]:
   if file.exists() and reason is None:
    try:data=json.loads(file.read_text())
    except (OSError,json.JSONDecodeError):continue
    expected={'N':23592,'M':144032,'S':0,'U':1,'Q':383,'R':4.238545331242318e-05,'S_over_N':0.0}
    mismatch=(data['counts']!=expected) if field=='counts' else data.get('strip_all_sha256',data.get('after_sha256'))!='13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8'
    if mismatch:
     reason='identity-or-profile-mismatch';(E/'identity-stop.json').write_text(json.dumps({'file':str(file),'data':data},indent=2)+'\n');subprocess.run(['systemctl','--user','stop',unit],capture_output=True,text=True);return
  append('resources.jsonl',row)
  if free<20*1024**3 and reason is None:
   reason='home available below 20 GiB';(E/'disk-stop.json').write_text(json.dumps(row,indent=2)+'\n')
   subprocess.run(['systemctl','--user','stop',unit],capture_output=True,text=True);return
def bolt_observer():
 target=None;first=None;seen=set()
 while not stop.is_set():
  work=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
  if not (work/'rewrite/bolt.log.argv.json').exists():stop.wait(.5);continue
  if target is None:
   for entry in Path('/proc').iterdir():
    if not entry.name.isdigit() or int(entry.name) in seen:continue
    try:
     args=entry.joinpath('cmdline').read_bytes().split(b'\0')
     if args and args[0].endswith(b'/bin/llvm-bolt') and any(a.startswith(b'-data=') for a in args):
      # Ensure the process belongs to this new build's cgroup.
      if unit.removesuffix('.service') not in entry.joinpath('cgroup').read_text():continue
      target=entry;first=time.time_ns();append('bolt-process.jsonl',{'event':'found','time_ns':first,'pid':int(entry.name),'argv':[a.decode(errors='replace') for a in args if a],'stat':entry.joinpath('stat').read_text()});break
    except (OSError,ProcessLookupError):pass
   if target is None:
    if (work/'rewrite/rewrite-result.json').exists():break
    stop.wait(.02);continue
  try:
   text=target.joinpath('status').read_text();vm={l.split(':',1)[0]:l.split(':',1)[1].strip() for l in text.splitlines() if l.startswith(('VmHWM:','VmRSS:','State:'))}
   append('bolt-process.jsonl',{'event':'sample','time_ns':time.time_ns(),'pid':int(target.name),**vm})
  except OSError:
   append('bolt-process.jsonl',{'event':'gone','time_ns':time.time_ns(),'pid':int(target.name)});break
  stop.wait(.01)
argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax='+str(plan['MemoryMax_bytes']),'-p','MemorySwapMax=0','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=120','-p','WorkingDirectory='+plan['source'],'--setenv=TMPDIR='+str(D/'tmp'),'--setenv=PYTHONDONTWRITEBYTECODE=1','python3','-B',str(D/'build-runner.py')]
(E/'service-command.json').write_text(json.dumps(argv,indent=2)+'\n');start=time.time_ns()
threads=[]
try:
 with (E/'service.stdout').open('wb') as out,(E/'service.stderr').open('wb') as err:
  p=subprocess.Popen(argv,stdout=out,stderr=err)
  for fn in (du,logs,resources,bolt_observer):
   t=threading.Thread(target=fn);t.start();threads.append(t)
  rc=p.wait()
finally:
 stop.set()
 for t in threads:t.join(timeout=65)
 fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
(E/'controller-result.json').write_text(json.dumps({'rc':rc,'reason':reason,'start_ns':start,'end_ns':time.time_ns(),'held_seconds':time.monotonic()-acquired},indent=2)+'\n')
print('BUILD_EXIT',rc,'reason',reason,flush=True)

from datetime import datetime
status='ok' if rc==0 and reason is None else 'stopped' if reason else 'failed'
with (E/'oldtext-final.log').open('a') as f:f.write('OLDTEXT_FINAL FINISHED '+datetime.now().astimezone().isoformat()+' status='+status+' reason='+str(reason or ('build-complete' if rc==0 else 'build-failed'))+'\n')
