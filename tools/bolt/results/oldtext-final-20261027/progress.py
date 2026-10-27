from pathlib import Path
import json, datetime
E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027')
print(datetime.datetime.now().astimezone().isoformat())
for label in ['rss']+sorted(p.name for p in (E/'validation').glob('rss-repeat-*') if p.is_dir()):
 p=E/'validation'/label/'progress.json'
 if p.exists():
  j=json.loads(p.read_text());r=j['last'];print(label,j['completed'],'/',j['total'],r['role'],r['language'],r['target'],'rc',r['rc'],'equal',r['byte_equal'])
for f in ['validation-result.json','resume-result.json','validation-failure.txt']:
 p=E/f
 if p.exists():print(f,p.read_text()[:1600])
p=E/'external-load.jsonl'
if p.exists():
 with p.open('rb') as f:
  f.seek(max(0,p.stat().st_size-16000));lines=f.read().splitlines();j=json.loads(lines[-1]);print('external heavy:',j.get('sustained_heavy'))
