from pathlib import Path
import json,time,subprocess,shutil
D=Path(__file__).resolve().parent
E=D.parent.parent.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027'
R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
while True:
 time.sleep(50)
 print(time.strftime('%H:%M:%S'), 'home_free_GiB',round(shutil.disk_usage('/home').free/1024**3,1),flush=True)
 for n in ('controller-result.json','validation-result.json','rss-accepted.json'):
  if (E/n).exists():
   v=json.loads((E/n).read_text());print(n,{k:v[k] for k in ('rc','status','reason','label') if k in v},flush=True)
 if not (E/'controller-result.json').exists():
  try:
   with (R/'.build.log').open('rb') as f:f.seek(max(0,(R/'.build.log').stat().st_size-3000));a=f.read().decode(errors='replace').splitlines()
   print('\n'.join(a[-2:]),flush=True)
  except OSError:pass
 else:
  for p in sorted((E/'validation').glob('*/progress.json')):
   v=json.loads(p.read_text());print(p.parent.name,v.get('completed'),v.get('total'),flush=True)
 if (E/'validation-controller-result.json').exists():break
