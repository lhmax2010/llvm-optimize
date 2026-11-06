"""Run retained-product checks serially in two independent 16-GiB services.
No build, cleanup, mount, sudo, or mutation of original evidence.
"""
from pathlib import Path
import subprocess,json,sys,time,datetime,traceback
from checks import save
from resource_report import report,critical_stop
W=Path('/home/linhao/Toolchain/development/llvm-optimize');N=W/'temp/night-20261103';T=Path(__file__).parent

def main():
 status='failed';reason='unexpected';projects=[]
 try:
  for project in ('toolchain','basedev'):assert not (N/project/'validation-02').exists(),('existing output refused',project)
  for project in ('toolchain','basedev'):
   D=N/project;O=D/'validation-02';unit='night-revalidation-'+project+'-20261104.service'
   argv=['systemd-run','--user','--unit='+unit,'-p','MemoryMax=16G','-p','MemorySwapMax=0','-p','OOMPolicy=stop','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','CPUQuota=200%','-p','StandardOutput=journal','-p','StandardError=journal',sys.executable,'-B',str(T/'validate.py'),'--project',project,'--root',str(D),'--peer',str(N/'toolchain'),'--output',str(O)]
   print('START',project,json.dumps(argv),flush=True);subprocess.run(argv,check=True)
   peak=0;events='';memory_current=0
   while True:
    props=subprocess.check_output(['systemctl','--user','show',unit,'-p','ActiveState','-p','Result','-p','MemoryPeak','-p','ControlGroup','-p','ExecMainStatus'],text=True)
    fields=dict(line.split('=',1) for line in props.splitlines() if '=' in line)
    cg=Path('/sys/fs/cgroup')/fields.get('ControlGroup','').lstrip('/')
    try:
     peak=max(peak,int((cg/'memory.peak').read_text()));events=(cg/'memory.events').read_text();memory_current=int((cg/'memory.current').read_text())
    except (OSError,ValueError):pass
    if O.exists():save(O/'service-sampling.json',dict(peak=peak,memory_current=memory_current,memory_events=events,service=fields))
    if fields.get('ActiveState') in ('inactive','failed'):break
    time.sleep(5)
   O.mkdir(exist_ok=True);save(O/'service-command.json',argv);save(O/'service-result.json',dict(fields,observed_memory_peak=peak,memory_events=events))
   journal=subprocess.run(['journalctl','--user','-u',unit,'--no-pager','-o','cat'],capture_output=True,text=True);(O/'service-journal.txt').write_text(journal.stdout);(O/'service-journal.stderr').write_text(journal.stderr)
   if fields.get('Result')=='oom-kill':save(O/'result.json',dict(status='stopped',reason='memory-oom-stop'))
   if not (O/'result.json').exists():save(O/'result.json',dict(status='failed',reason='service-ended-without-result'))
   result=json.loads((O/'result.json').read_text());report(D,output=O)
   ended='REVALIDATION_PROJECT 已结束 '+datetime.datetime.now().astimezone().isoformat()+' '+project+' status='+result['status']+' reason='+result.get('reason','see-result.json')
   (O/'ended.txt').write_text(ended+'\n');print(ended,flush=True);projects.append(dict(project=project,status=result['status']))
   # Do not inherit the previous night's OOM: only THIS new validation stops
   # this serial queue. No D after MemoryError or service OOM.
   failure=(O/'failure.txt').read_text() if (O/'failure.txt').exists() else ''
   if fields.get('Result')=='oom-kill' or result.get('reason') in ('memory-stop','memory-oom-stop') or 'MemoryError' in failure:
    status='stopped';reason='memory-stop';break
  else:status='ok' if all(p['status']=='ok' for p in projects) else 'failed';reason='both-validations-finished'
 except BaseException:traceback.print_exc();reason='controller-error'
 finally:print('REVALIDATION 已结束',datetime.datetime.now().astimezone().isoformat(),'status='+status,'reason='+reason,flush=True)
 return 0 if status=='ok' else 1
if __name__=='__main__':sys.exit(main())
