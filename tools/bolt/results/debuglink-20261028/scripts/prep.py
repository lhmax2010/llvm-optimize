from pathlib import Path
import subprocess,json,configparser,time,shutil,threading,datetime
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/debuglink-20261028';plan=json.loads((D/'plan.json').read_text());assert json.loads((E/'export-result.json').read_text())['rc']==0
G=D/'gbs-root';R=G/'local/BUILD-ROOTS/scratch.x86_64.0'
for p in [G/'local/BUILD-ROOTS',G/'local/sources',G/'local/repos']:p.mkdir(parents=True,exist_ok=True)
c=configparser.ConfigParser();c.read(plan['config']);profile=c[c['general']['profile']];cmd=['sudo','-n','/usr/bin/build','--uid','1000:1000','--root',str(R),'--dist',profile['buildconf'],'--arch','x86_64','--target','x86_64-tizen-linux','--stage=-bp','--debug','--baselibs','--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20']
for n in ('repo.base_0','repo.base_debug_0'):cmd+=['--repo',c[n]['url']]
cmd+=[str(D/'export/llvm.spec')];unit='debuglink-prep-20261028'
argv=['systemd-run','--user','--wait','--pipe','--unit='+unit,'-p','MemoryMax='+str(plan['MemoryMax_bytes']),'-p','MemorySwapMax=0','-p','CPUQuota=1200%','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop','-p','KillMode=control-group','-p','TimeoutStopSec=120',*cmd]
(E/'prep-command.json').write_text(json.dumps(argv,indent=2)+'\n');reason='prep-unexpected-error';rc=1;start=time.time_ns()
try:
 with (E/'prep.stdout').open('wb') as o,(E/'prep.stderr').open('wb') as e:
  p=subprocess.Popen(argv,stdout=o,stderr=e)
  while p.poll() is None:
   if shutil.disk_usage('/home').free<20*1024**3:
    reason='home-below-20GiB';subprocess.run(['systemctl','--user','stop',unit]);break
   time.sleep(5)
  rc=p.wait();reason='prep-complete' if rc==0 else reason if reason=='home-below-20GiB' else 'prep-failed'
finally:
 (E/'prep-result.json').write_text(json.dumps({'rc':rc,'reason':reason,'start_ns':start,'end_ns':time.time_ns()},indent=2)+'\n')
 with (E/'debuglink.log').open('a') as f:f.write('DEBUGLINK FINISHED '+datetime.datetime.now().astimezone().isoformat()+' status='+('ok' if rc==0 else 'failed')+' reason='+reason+'\n')
print(reason,rc,flush=True);raise SystemExit(rc)
