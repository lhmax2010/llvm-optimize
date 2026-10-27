from pathlib import Path
import time,json,subprocess
D=Path(__file__).resolve().parent;E=D.parent.parent.parent/'llvm-optimize-bolt/tools/bolt/results/oldtext-final-20261027'
while True:
 time.sleep(50)
 print(time.strftime('%H:%M:%S'),subprocess.check_output(['systemctl','--user','show','oldtext-final-resume-20261027.service','-p','ActiveState','-p','MemoryCurrent'],text=True).strip().replace('\n',' '),flush=True)
 p=E/'resume-rpm.log'
 if p.exists():
  with p.open('rb') as f:f.seek(max(0,p.stat().st_size-4000));rows=f.read().decode(errors='replace').splitlines()
  print('\n'.join(x[:250] for x in rows[-2:]),flush=True)
 if (E/'validation-steps.json').exists():print('validation',[(s['step'],s['rc']) for s in json.loads((E/'validation-steps.json').read_text())],flush=True)
 for p in sorted((E/'validation').glob('*/progress.json')):
  x=json.loads(p.read_text());print(p.parent.name,x.get('completed'),x.get('total'),flush=True)
 if (E/'resume-result.json').exists():print((E/'resume-result.json').read_text(),flush=True);break
