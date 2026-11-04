"""Separate A/B/C/D systemd services; established physical-root / gbs-driver layout."""
from common import *
from monitor import Monitor
import sys,shutil,configparser,shlex,datetime,traceback,fcntl

def service(d,name,argv,tree,log=None):
 out=d/'evidence'/name;out.mkdir(parents=True);save(out/'command.json',argv)
 unit='pgo-'+d.parent.name+'-'+d.name+'-'+name+'-20261102.service'
 args=['systemd-run','--user','--wait','--pipe','--unit='+unit,*props(),'--setenv=PYTHONDONTWRITEBYTECODE=1','/usr/bin/python3','-B',str(T/'service.py'),str(out),str(out/'command.json')]
 save(out/'systemd-command.json',args);m=Monitor(unit,out,tree,log);m.phase=name if name!='D' else 'setup'
 with (out/'stdout').open('wb') as o,(out/'stderr').open('wb') as e:
  p=subprocess.Popen(args,stdout=o,stderr=e);m.start()
  try:
   while p.poll() is None and not (out/'service-result.json').exists():time.sleep(.5)
   m.finish()
  except BaseException:
   subprocess.run(['systemctl','--user','stop',unit],capture_output=True);p.wait();raise
  finally:(out/'monitor-release').write_text('monitor-finished\n')
  rc=p.wait()
 save(out/'controller.json',{'rc':rc,'reason':m.reason})
 if rc or m.reason:raise RuntimeError(f'{name}: rc={rc} reason={m.reason}; see {out}')
 result=json.loads((out/'service-result.json').read_text())
 ev=dict(l.split() for l in result['stats']['memory.events'].splitlines())
 assert int(ev.get('oom',0))==0 and int(ev.get('oom_kill',0))==0,'OOM'

def cleanup(d):
 r=root(d);rows=[]
 while True:
  mounts=subprocess.check_output(['findmnt','-rn','-o','TARGET'],text=True).splitlines();ours=[x for x in mounts if x.startswith(str(r)+'/')]
  if not ours:break
  x=sorted(ours,key=len,reverse=True)[0];rel=x[len(str(r)):];assert rel in ['/proc','/dev/pts','/dev/shm','/sys','/proc/sys/fs/binfmt_misc'],x
  p=subprocess.run(['sudo','-n','/usr/sbin/chroot',str(r),'/bin/umount','-n',rel],capture_output=True,text=True);rows.append({'target':x,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr});save(d/'evidence/cleanup.json',rows)
  if p.returncode:raise RuntimeError('ordinary umount failed '+x)
 save(d/'evidence/cleanup.json',rows)

def prepare_root(d,which):
 d.mkdir();(d/'evidence').mkdir();(d/'tmp').mkdir();r=root(d)
 for s in ['BUILD-ROOTS','sources','repos']:(d/'gbs-root/local'/s).mkdir(parents=True,exist_ok=True)
 driver=d/'gbs-driver/local';driver.mkdir(parents=True)
 (driver/'BUILD-ROOTS').symlink_to(d/'gbs-root/local/BUILD-ROOTS',target_is_directory=True)
 for s in ['sources','repos']:(driver/s).mkdir()
 shutil.copytree(P/('export-'+which),d/'export')
 c=configparser.ConfigParser();c.read(CONFIG);profile=c[c['general']['profile']]
 argv=['sudo','-n','/usr/bin/build','--uid','1000:1000','--root',str(r),'--dist',profile['buildconf'],'--arch','x86_64','--target','x86_64-tizen-linux','--stage=-bp','--debug','--baselibs',*MACROS]
 for n in ['repo.base_0','repo.base_debug_0']:argv+=['--repo',c[n]['url']]
 argv+=[str(d/'export/llvm.spec')]
 service(d,'prepare',argv,r);cleanup(d)
 dest=driver/'sources/tizen_base_toolchain_standard/llvm-22.1.8-1';shutil.copytree(d/'export',dest)
 return r

def stage_a(d,rehearsal):
 r=root(d);inner=r/INNER.lstrip('/');build=inner/'build';build.mkdir(exist_ok=True)
 # Bootstrap runtime is absent from the fixed snapshot's installed compiler.
 # Copy its same-version, previously-built profile runtime into this fresh root only.
 runtime=H/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'/INNER.lstrip('/')/'build/lib64/clang/22/lib/linux/libclang_rt.profile-x86_64.a'
 local=r/'home/abuild/pgo-resource';local.mkdir(exist_ok=True);shutil.copyfile(runtime,local/runtime.name)
 code="from pathlib import Path;import shutil;p=Path('/usr/lib64/clang/22/lib/linux/libclang_rt.profile-x86_64.a');assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile('/home/abuild/pgo-resource/libclang_rt.profile-x86_64.a',p)"
 call(['sudo','-n','/usr/sbin/chroot',str(r),'/usr/bin/python3','-B','-c',code],d/'evidence/bootstrap-runtime.stdout')
 save(d/'evidence/bootstrap-runtime.json',{'source':str(runtime),'sha256':sha(runtime),'note':'existing same-version runtime, provisioned only in fresh test root; own profile target built at night'})
 args=json.loads((E/'cmake-A.json').read_text());env=json.loads((E/'rpm-environment.json').read_text())
 script='#!/bin/sh\nset -eu\ncd '+shlex.quote(INNER+'/build')+'\nprintf "PATH=%s\\n" "$PATH"\ncommand -v clang\ncommand -v clang++\n'+shlex.join(args)+'\nprintf "%s\\n" PGO_A_CONFIGURE_PASS\n'
 if not rehearsal:script+='ninja -j6 clang_rt.profile-x86_64\nninja -j6 clang\nprintf "%s\\n" PGO_A_BUILD_PASS\n'
 (local/'stage-A.sh').write_text(script);save(d/'evidence/cmake-argv.json',args)
 service(d,'A',prefix(r)+[k+'='+v for k,v in env.items()]+['/bin/sh','/home/abuild/pgo-resource/stage-A.sh'],r)
 assert (build/'build.ninja').exists();assert 'PGO_A_CONFIGURE_PASS' in (d/'evidence/A/stdout').read_text()
 # Verify configured compiler identities and IR option without invoking ninja.
 cache=(build/'CMakeCache.txt').read_text();assert 'LLVM_BUILD_INSTRUMENTED:STRING=IR' in cache
 save(d/'evidence/configure-proof.json',{'PASS':True,'cache_sha256':sha(build/'CMakeCache.txt'),'build_ninja_sha256':sha(build/'build.ninja'),'rehearsal_no_ninja':rehearsal})

def stage_b(d):
 r=root(d);b=r/INNER.lstrip('/')/'build';profiles=d/'profiles';profiles.mkdir();objects=d/'objects';objects.mkdir()
 rows=json.loads((E/'training.json').read_text());commands=[]
 loader=r/'lib64/ld-linux-x86-64.so.2';libpath=str(b/'lib64')+':'+str(r/'usr/lib64')+':'+str(r/'lib64')
 for i,row in enumerate(rows):
  assert sha(row['path'])==row['sha256']
  commands.append({'name':row['name'],'argv':[str(loader),'--library-path',libpath,str(b/'bin/clang-22'),'--driver-mode=g++',*row['compiler_args'],'-c',row['path'],'-o',str(objects/(str(i)+'.o'))],'LLVM_PROFILE_FILE':str(profiles/(str(i)+'-%m-%p.profraw'))})
 save(d/'training-commands.json',commands)
 service(d,'B',['/usr/bin/python3','-B',str(T/'train.py'),str(d)],r)
 raws=sorted(profiles.glob('*.profraw'));assert raws and all(p.stat().st_size for p in raws)
 save(d/'evidence/profraw.json',{'count':len(raws),'total_bytes':sum(p.stat().st_size for p in raws),'files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in raws]})

def stage_c(d):
 hr=root(H);hb=hr/INNER.lstrip('/')/'build';tool=hb/'bin/llvm-profdata';profile=d/'profiles/clang.profdata'
 argv=[str(hr/'lib64/ld-linux-x86-64.so.2'),'--library-path',str(hb/'lib64')+':'+str(hr/'usr/lib64')+':'+str(hr/'lib64'),str(tool),'merge','-o',str(profile),*[str(p) for p in sorted((d/'profiles').glob('*.profraw'))]]
 service(d,'C',argv,root(d));assert profile.stat().st_size
 save(d/'evidence/profdata.json',{'path':str(profile),'bytes':profile.stat().st_size,'sha256':sha(profile),'llvm_profdata':str(tool),'tool_sha256':sha(tool),'tool_source':'same 3ee2d847 full-20261030 build; no additional LLVM target built'})
 return profile

def stage_d(d,profile):
 r=prepare_root(d,'PGO');p=r/PROFDATA.lstrip('/');p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(profile,p);assert sha(p)==sha(profile)
 source=json.loads((E/'source.json').read_text());argv=['gbs','-c',str(CONFIG),'build','-A','x86_64','-B',str(d/'gbs-driver'),'-c',source['experiment_commit'],'--threads=30',*MACROS,'--baselibs','--style=tar','--spec','llvm.spec',source['source_D']]
 # No old expected identity check: PGO changes the input. Packaged helper gates stay unchanged.
 service(d,'D',argv,r,r/'.build.log')
 if (r/'.build.log').exists():shutil.copyfile(r/'.build.log',d/'evidence/rpm-build.log')

def worker(mode,d):
 status='failed';reason='unexpected';roots=[]
 try:
  budget=disk_budget();save(d/'disk-budget-at-worker.json',budget)
  if budget.get('BUDGET_MARGIN_WARNING'):print(budget['BUDGET_MARGIN_WARNING'],flush=True)
  assert json.loads((E/'prepare.json').read_text())['PASS'];assert budget['PASS']
  with (W.parent/'heavy-stage.lock').open('a+') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX)
   ad=d/'stage-A';roots.append(ad);prepare_root(ad,'baseline');stage_a(ad,mode=='rehearsal')
   if mode=='full':
    stage_b(ad);profile=stage_c(ad);dd=d/'stage-D';roots.append(dd);stage_d(dd,profile)
   status='ok';reason='configure-only-no-ninja' if mode=='rehearsal' else 'A-B-C-D-complete'
 except BaseException as exc:
  reason=' '.join(str(exc).split()) or type(exc).__name__
  (d/'failure.txt').write_text(traceback.format_exc());traceback.print_exc()
 finally:
  for x in roots:
   try:
    cleanup(x)
    if (root(x)/'.build.log').exists():shutil.copyfile(root(x)/'.build.log',x/'evidence/rpm-build.log')
   except BaseException:status='failed';reason='cleanup-failed';(d/(x.name+'-cleanup-failure.txt')).write_text(traceback.format_exc())
  mounts=[l for l in Path('/proc/self/mountinfo').read_text().splitlines() if str(d)+'/' in l]
  units=subprocess.run(['systemctl','--user','list-units','--all','--no-pager','pgo-*20261102.service'],capture_output=True,text=True)
  residual=[]
  for p in Path('/proc').glob('[0-9]*'):
   try:
    cg=(p/'cgroup').read_text()
    if 'pgo-'+d.name+'-stage-' in cg:residual.append({'pid':p.name,'cgroup':cg,'argv':(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')})
   except OSError:pass
  save(d/'audit.json',{'mounts':mounts,'remaining_stage_processes':residual,'systemd':units.stdout})
  if residual:status='failed';reason='residual-stage-process'
  if mounts:status='failed';reason='residual-mount'
  save(d/'result.json',{'status':status,'reason':reason})
  print('PGO_RESOURCE 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+status,'reason='+reason,flush=True)
 return 0 if status=='ok' else 1

def launch(mode):
 assert mode in ['rehearsal','full']
 if mode=='full':assert json.loads((E/'ready.json').read_text())['PASS'],'daytime preflight/rehearsal not certified'
 budget=disk_budget();save(E/'disk-budget-at-launch.json',budget);assert budget['PASS']
 if mode=='rehearsal':
  n=1
  while (P/f'rehearsal-{n:02}').exists():n+=1
  d=P/f'rehearsal-{n:02}'
 else:d=P/'full';assert not d.exists()
 d.mkdir();unit='pgo-controller-'+d.name+'-20261102.service'
 argv=['systemd-run','--user','--unit='+unit,*props(),'-p','StandardOutput=append:'+str(d/'controller.stdout'),'-p','StandardError=append:'+str(d/'controller.stderr'),'/usr/bin/python3','-B',str(T/'driver.py'),'--worker',mode,str(d)]
 save(d/'launch.json',argv);subprocess.run(argv,check=True)
 print('Started:',unit);print('tail -f '+str(d/'controller.stdout'))
if __name__=='__main__':
 if sys.argv[1]=='--worker':sys.exit(worker(sys.argv[2],Path(sys.argv[3])))
 launch(sys.argv[1])
