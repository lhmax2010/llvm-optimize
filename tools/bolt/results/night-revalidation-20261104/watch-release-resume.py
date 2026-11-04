from pathlib import Path
import subprocess,json,time,datetime
D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261103/basedev');O=D/'validation-02';E=O/'release-check-resume';unit='night-revalidation-release-resume-20261104.service';main='night-revalidation-basedev-20261104.service';peak=0;combined=0;events=''
def props(u):
 s=subprocess.check_output(['systemctl','--user','show',u,'-p','ActiveState','-p','Result','-p','MemoryCurrent','-p','MemoryPeak','-p','ControlGroup'],text=True);return dict(l.split('=',1) for l in s.splitlines() if '=' in l)
def number(s):
 try:return int(s)
 except (ValueError,TypeError):return 0
while True:
 r=props(unit);m=props(main);peak=max(peak,number(r.get('MemoryPeak')));combined=max(combined,number(r.get('MemoryCurrent'))+number(m.get('MemoryCurrent')))
 try:events=(Path('/sys/fs/cgroup')/r['ControlGroup'].lstrip('/')/'memory.events').read_text()
 except OSError:pass
 (E/'service-sampling.json').write_text(json.dumps(dict(service=r,main=m,observed_memory_peak=peak,observed_combined_current_peak=combined,memory_events=events,time=datetime.datetime.now().astimezone().isoformat()),indent=2)+'\n')
 if r['ActiveState'] in ('inactive','failed'):break
 time.sleep(5)
(E/'service-journal.txt').write_text(subprocess.check_output(['journalctl','--user','-u',unit,'--no-pager','-o','cat'],text=True));(E/'service-result.json').write_text(json.dumps(dict(r,observed_memory_peak=peak,observed_combined_current_peak=combined,memory_events=events),indent=2)+'\n')
if r.get('Result')=='oom-kill' or ((E/'failure.txt').exists() and 'MemoryError' in (E/'failure.txt').read_text()):
 with (O/'failure.txt').open('a') as f:f.write('MemoryError: supplementary release validation OOM; stop all validation\n')
 subprocess.run(['systemctl','--user','stop',main],check=True)
print('RELEASE_RESUME_WATCH_END',r['Result'],'peak',peak,'combined_sampled_peak',combined,flush=True)
