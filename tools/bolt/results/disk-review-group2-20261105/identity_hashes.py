from pathlib import Path
import json,subprocess
E=Path(__file__).resolve().parent;out=[]
for n in json.loads((E/'targets.json').read_text()):
 for x in json.loads((E/n/'inventory.json').read_text())['special']:
  if x.get('link') or Path(x['path']).name not in ('identity.json','build.conf'):continue
  r=subprocess.run(['timeout','30','nice','-n','19','ionice','-c3','sha256sum','--',x['path']],capture_output=True,text=True)
  out.append(dict(x,hash={'rc':r.returncode,'sha256':r.stdout.split()[0] if r.returncode==0 else None,'stderr':r.stderr}))
(E/'identity-hashes.json').write_text(json.dumps(out,indent=2));print(len(out))
