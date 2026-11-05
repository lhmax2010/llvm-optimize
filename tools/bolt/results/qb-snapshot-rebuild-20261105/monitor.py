from pathlib import Path
import datetime,json,os,subprocess,time
E=Path(__file__).resolve().parent;D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain');start=json.loads((E.parent/'disk-cleanup-20261105c/launch-service.json').read_text())['time'];due=datetime.datetime.fromisoformat(start).timestamp()+1800
units=['night-toolchain-full-controller-20261105.service','night-toolchain-full-20261105.service','night-toolchain-full-prep-20261105.service']
def tail(p,n=65536):
 try:
  with p.open('rb') as f:f.seek(max(0,p.stat().st_size-n));return f.read().decode(errors='replace')
 except FileNotFoundError:return 'MISSING'
while True:
 while time.time()<due:time.sleep(min(60,due-time.time()))
 now=datetime.datetime.now().astimezone().isoformat();sv={}
 for unit in units:
  r=subprocess.run(['systemctl','--user','show',unit,'-p','ActiveState','-p','SubState','-p','Result','-p','ExecMainStatus','-p','MemoryCurrent','-p','MemoryPeak','-p','CPUUsageNSec','-p','ControlGroup'],capture_output=True,text=True,timeout=20);sv[unit]={'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
 fs=os.statvfs('/home');rec={'time':now,'units':sv,'available_bytes':fs.f_bavail*fs.f_frsize,'controller_stdout_tail':tail(D/'controller.stdout'),'controller_stderr_tail':tail(D/'controller.stderr'),'samples':{}}
 for n in ['resources.jsonl','du-root.jsonl','bolt-process.jsonl','phase-events.jsonl','build-result.json','result.json']:
  rec['samples'][n]=tail(D/'evidence'/n,8192)
 with (E/'monitor.jsonl').open('a') as f:f.write(json.dumps(rec,ensure_ascii=False)+'\n')
 ended=[l for l in rec['controller_stdout_tail'].splitlines() if l.startswith('NIGHT_PROJECT 已结束')]
 state=sv[units[0]]['stdout'];print('MONITOR',now,'available_GiB',round(rec['available_bytes']/2**30,3),'controller',state.replace('\n',' '),flush=True)
 if ended:
  (E/'observed-end.txt').write_text('\n'.join(ended)+'\n');print(ended[-1],flush=True);break
 if 'ActiveState=failed' in state or 'ActiveState=inactive' in state:
  (E/'missing-end.txt').write_text('MONITOR 已结束 '+now+' status=failed reason=controller-inactive-without-end-marker\n');print((E/'missing-end.txt').read_text(),flush=True);break
 due+=1800
