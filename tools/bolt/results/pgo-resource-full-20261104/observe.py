"""Read-only experiment observation; no stop, restart, cleanup or privilege calls."""
from pathlib import Path
import subprocess,time,json,datetime
D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/pgo-resource-20261102/full');E=Path(__file__).parent
UNIT='pgo-controller-full-20261102.service'
def tail(p,limit=12000):
 if not p.exists():return ''
 with p.open('rb') as f:f.seek(max(0,p.stat().st_size-limit));return f.read().decode(errors='replace')
def inspect(status):
 row=dict(time=datetime.datetime.now().astimezone().isoformat(),service=status,controller_stdout=tail(D/'controller.stdout'),controller_stderr=tail(D/'controller.stderr'),stages=[])
 for out in sorted(D.glob('stage-*/evidence/*')):
  if out.is_dir():row['stages'].append(dict(path=str(out),stdout_tail=tail(out/'stdout',3000),stderr_tail=tail(out/'stderr',3000),cgroup_tail=tail(out/'cgroup.jsonl',3000),filesystem_tail=tail(out/'filesystem.jsonl',1000)))
 with (E/'observation.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 print('PGO_OBSERVE',row['time'],status.replace('\n',';'),flush=True)
 print(row['controller_stdout'],flush=True)
 return 'PGO_RESOURCE 已结束' in row['controller_stdout']
nextread=time.monotonic()+1800
while True:
 p=subprocess.run(['systemctl','--user','show',UNIT,'-p','ActiveState','-p','SubState','-p','Result','-p','MainPID'],capture_output=True,text=True)
 stopped='ActiveState=active' not in p.stdout and 'ActiveState=activating' not in p.stdout
 if stopped or time.monotonic()>=nextread:
  ended=inspect(p.stdout);nextread=time.monotonic()+1800
  if ended or stopped:
   print('OBSERVER 已结束',datetime.datetime.now().astimezone().isoformat(),'reason='+('controller-ended' if ended else 'inactive-without-end-marker'),flush=True);break
 time.sleep(30)
