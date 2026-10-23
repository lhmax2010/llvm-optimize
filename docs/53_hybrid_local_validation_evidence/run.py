"""One isolated hybrid build; no admission, memory freeze, or timed lease rotation."""
import fcntl,json,os,shutil,subprocess,threading,time
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W/'docs/53_hybrid_local_validation_evidence';plan=json.loads((D/'plan.json').read_text());G=D/'gbs-root';R=G/'local/BUILD-ROOTS/scratch.x86_64.0';unit='hybrid-local-20261023.service';stop=threading.Event();reason=None
assert json.loads((E/'export-result.json').read_text())['rc']==0;assert all(r['pass'] for r in json.loads((E/'export-checks.json').read_text()))
assert not G.exists();dest=G/'local/sources/tizen_base_toolchain_standard/llvm-22.1.8-1';shutil.copytree(D/'export',dest)
cmd=['gbs','-c',plan['config'],'build','-A','x86_64','-B',str(G),'-c',plan['commit'],'--threads=30','--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20','--baselibs','--clean-once','--style=tar','--spec','llvm.spec',plan['source']]
(D/'build-command.json').write_text(json.dumps(cmd,indent=2)+'\n');(E/'build-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');startwait=time.monotonic();fcntl.flock(lock,fcntl.LOCK_EX);acquired=time.monotonic()
(E/'lock.json').write_text(json.dumps({'acquired_ns':time.time_ns(),'wait_seconds':acquired-startwait,'policy':'exclusive for this single build; no timed freeze per user override'},indent=2)+'\n')
def append(name,j):
 with (E/name).open('a') as f:f.write(json.dumps(j)+'\n')
def du():
 while not stop.is_set():
  stamp=time.time_ns();start=time.monotonic()
  if (R/'usr/bin/timeout').exists() and (R/'bin/du').exists():
   argv=['sudo','-n','/usr/sbin/chroot',str(R),'/usr/bin/timeout','-k','5','50','/bin/du','-sx','-B1','/']
   try:
    p=subprocess.run(argv,capture_output=True,text=True,timeout=58);row={'time_ns':stamp,'argv':argv,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'seconds':time.monotonic()-start}
   except subprocess.TimeoutExpired:row={'time_ns':stamp,'argv':argv,'missing':'outer timeout 58s','seconds':time.monotonic()-start}
  else:row={'time_ns':stamp,'missing':'chroot du/timeout not ready'}
  append('du-root.jsonl',row);stop.wait(max(0,60-(time.monotonic()-start)))
def logs():
 position=0
 while not stop.wait(2):
  p=R/'.build.log'
  if p.exists():
   with p.open('rb') as src:
    src.seek(position);b=src.read();position+=len(b)
   if b:
    with (E/'rpm-build.log').open('ab') as out:out.write(b)
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
  append('resources.jsonl',row)
  if free<20*1024**3 and reason is None:
   reason='home available below 20 GiB';(E/'disk-stop.json').write_text(json.dumps(row,indent=2)+'\n')
   subprocess.run(['systemctl','--user','stop',unit],capture_output=True,text=True);return
argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax='+str(plan['MemoryMax_bytes']),'-p','MemorySwapMax=0','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=120','-p','WorkingDirectory='+plan['source'],'--setenv=TMPDIR='+str(D/'tmp'),'--setenv=PYTHONDONTWRITEBYTECODE=1','python3','-B',str(D/'build-runner.py')]
(E/'service-command.json').write_text(json.dumps(argv,indent=2)+'\n');start=time.time_ns()
threads=[]
try:
 with (E/'service.stdout').open('wb') as out,(E/'service.stderr').open('wb') as err:
  p=subprocess.Popen(argv,stdout=out,stderr=err)
  for fn in (du,logs,resources):
   t=threading.Thread(target=fn);t.start();threads.append(t)
  rc=p.wait()
finally:
 stop.set()
 for t in threads:t.join(timeout=65)
 fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
(E/'controller-result.json').write_text(json.dumps({'rc':rc,'reason':reason,'start_ns':start,'end_ns':time.time_ns(),'held_seconds':time.monotonic()-acquired},indent=2)+'\n')
print('BUILD_EXIT',rc,'reason',reason,flush=True)
