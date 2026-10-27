"""Local resource-limited continuation, retaining interrupted evidence."""
from pathlib import Path
import os,json,subprocess,time,threading,shutil,datetime,fcntl,signal,traceback,ast
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';WORK=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt';C=R/'home/abuild/oldtext-resume-20261027';unit='oldtext-final-resume-20261027.service';stop=threading.Event();reason=None;status='stopped';p=None;validation_proc=None
origin=datetime.datetime(2026,10,27,12,8,30,tzinfo=datetime.timezone.utc).timestamp()
lock=open('/home/linhao/Toolchain/development/heavy-stage.lock','a+');fcntl.flock(lock,fcntl.LOCK_EX)
start=time.time_ns();cg=next(l.split(':',2)[2] for l in Path('/proc/self/cgroup').read_text().splitlines() if l.startswith('0::'));CG=Path('/sys/fs/cgroup')/cg.lstrip('/')
def append(name,row):
 with (E/name).open('a') as f:f.write(json.dumps(row)+'\n')
def mark(sig,frame):
 global reason
 reason='service-signal-'+str(sig);(C/'STOP').write_text(reason)
signal.signal(signal.SIGTERM,mark);signal.signal(signal.SIGINT,mark)
def guard():
 global reason
 while not stop.wait(3):
  row={'time_ns':time.time_ns(),'home_available_bytes':shutil.disk_usage('/home').free,'meminfo':Path('/proc/meminfo').read_text(),'loadavg':Path('/proc/loadavg').read_text()}
  for n in ['memory.current','memory.peak','memory.events','memory.swap.current','cpu.stat','io.stat']:row[n]=(CG/n).read_text()
  append('resume-resources.jsonl',row)
  if row['home_available_bytes']<20*1024**3:reason='home-below-20GiB'
  if 'oom_kill 0\n' not in row['memory.events']:reason='cgroup-OOM'
  for file,field in [(WORK/'rewrite/rewrite-result.json','counts'),(WORK/'identity.json','identity')]:
   if file.exists() and reason is None:
    try:v=json.loads(file.read_text())
    except (OSError,json.JSONDecodeError):continue
    expected={'N':23592,'M':144032,'S':0,'U':1,'Q':383,'R':4.238545331242318e-05,'S_over_N':0.0}
    bad=v['counts']!=expected if field=='counts' else v.get('strip_all_sha256',v.get('after_sha256'))!='13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8'
    if bad:reason='identity-or-profile-mismatch';(E/'identity-stop.json').write_text(json.dumps({'file':str(file),'data':v},indent=2)+'\n')
  if reason:
   (C/'STOP').write_text(reason)
   if validation_proc is not None and validation_proc.poll() is None:os.killpg(validation_proc.pid,signal.SIGTERM)
# Preserve the original observer implementation, no production instrumentation.
module=ast.parse((D/'run.py').read_text());fn=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='bolt_observer');exec(compile(ast.Module(body=[fn],type_ignores=[]),str(D/'run.py'),'exec'))
threads=[]
try:
 assert not (C/'STOP').exists() and not (C/'result.json').exists()
 cmd=['sudo','-n','/usr/sbin/chroot',str(R),'/usr/bin/python3','-B','/home/abuild/oldtext-resume-20261027/resume-root.py'];(E/'resume-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
 for fn in [guard,bolt_observer]:
  t=threading.Thread(target=fn);t.start();threads.append(t)
 p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 with (E/'resume-rpm.log').open('wb') as out:
  for raw in iter(p.stdout.readline,b''):
   prefix=('[%5ds] '%int(time.time()-origin)).encode();out.write(prefix+raw);out.flush()
   if b'BOLT_GATE_FAILED:' in raw:reason='BOLT_GATE_FAILED';(C/'STOP').write_text(reason)
 rc=p.wait();stats={n:(CG/n).read_text() for n in ['memory.events','memory.peak','memory.max','memory.swap.max','cpu.max']}
 (E/'build-result.json').write_text(json.dumps({'exit_code':rc,'start_ns':start,'end_ns':time.time_ns(),'seconds':(time.time_ns()-start)/1e9,'stats':stats,'method':'normal rpmbuild -ba --noprep after host reboot; completed prep reused; same macros and spec'},indent=2)+'\n')
 with (E/'resumed-rpm-build.log').open('wb') as out:
  for src in [E/'pre-reboot/.build.log',E/'resume-rpm.log']:
   with src.open('rb') as inp:shutil.copyfileobj(inp,out)
 (E/'controller-result.json').write_text(json.dumps({'rc':rc,'reason':reason,'start_ns':start,'end_ns':time.time_ns()},indent=2)+'\n')
 if rc or reason:raise RuntimeError(reason or 'resumed-build-failed')
 # Keep resource guard but stop compiler-specific observer automatically after it exits.
 with (E/'validation-service.stdout').open('wb') as out,(E/'validation-service.stderr').open('wb') as err:
  validation_proc=subprocess.Popen(['python3','-B',str(D/'validate-runner.py')],stdout=out,stderr=err,start_new_session=True);validation_proc.wait()
 result=json.loads((E/'validation-result.json').read_text()) if (E/'validation-result.json').exists() else {}
 if validation_proc.returncode or result.get('status')!='ok':raise RuntimeError(result.get('reason','validation-failed'))
 status='ok';reason='build-and-all-local-validations-complete'
except BaseException as exc:
 reason=reason or str(exc);(E/'resume-failure.txt').write_text(traceback.format_exc())
finally:
 stop.set()
 for t in threads:t.join(timeout=10)
 fcntl.flock(lock,fcntl.LOCK_UN);lock.close()
 result={'status':status,'reason':reason,'end':datetime.datetime.now().astimezone().isoformat()};(E/'resume-result.json').write_text(json.dumps(result,indent=2)+'\n')
 with (E/'oldtext-final.log').open('a') as out:out.write('OLDTEXT_FINAL FINISHED '+result['end']+' status='+status+' reason='+str(reason).replace(' ','-')+'\n')
 print(json.dumps(result),flush=True)
raise SystemExit(0 if status=='ok' else 1)
