import json,sys,datetime
from pathlib import Path
D=Path(__file__).resolve().parent;run=sys.argv[1] if len(sys.argv)>1 else 'baseline-resume2';label=sys.argv[2] if len(sys.argv)>2 else 'baseline';E=D/run
print(datetime.datetime.now().astimezone().isoformat())
log=E/'build.log'
if log.exists():print('last_log',log.read_text(errors='replace').splitlines()[-1][:900])
p=D/(label+'-root')/'local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/native-archive-conversion/summary.json'
if p.exists():
 d=json.loads(p.read_text());print('Source1005',d.get('status'),'archives_completed',len(d.get('archives',[])),'installed',sum(bool(a.get('installed')) for a in d.get('archives',[])))
for name in ('du-root-complete.jsonl','independent-processes.jsonl'):
 p=E/name
 if p.exists():
  r=json.loads(p.read_text().splitlines()[-1])
  if name.startswith('du'):print('root_du',r['time_ns'],r['stdout'].strip(),'rc',r['rc'])
  else:print('processes',[(p['name'],p['state']) for p in r['processes']][-6:])
p=E/'result.json'
if p.exists():print('RESULT',p.read_text())
