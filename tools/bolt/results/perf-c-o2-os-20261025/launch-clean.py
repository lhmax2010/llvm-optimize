from pathlib import Path
import json,subprocess
E=Path(__file__).resolve().parent
assert json.loads((E/'finished.json').read_text())['status']=='COMPLETE'
assert subprocess.run(['systemctl','--user','is-active','--quiet','bolt-perf-c-o2-os-20261025-v2.service']).returncode!=0
C=E/'clean-c';assert not (C/'samples.jsonl').exists()
old=json.loads((E/'launch.json').read_text());argv=old['argv'].copy()
argv=[x.replace('bolt-perf-c-o2-os-20261025-v2','bolt-perf-c-o2-os-20261025-clean-c').replace(str(E/'measure.stdout'),str(C/'measure.stdout')).replace(str(E/'measure.stderr'),str(C/'measure.stderr')).replace(str(E/'measure.py'),str(C/'measure.py')) for x in argv]
r=subprocess.run(argv,text=True,capture_output=True)
(C/'launch.json').write_text(json.dumps(dict(argv=argv,rc=r.returncode,stdout=r.stdout,stderr=r.stderr,memmax=old['memmax']),indent=2)+'\n')
print(r.stdout,r.stderr);assert r.returncode==0
