import subprocess,json,datetime
from pathlib import Path
D=Path(__file__).resolve().parent
out=[]
for p in ['/home/linhao/lld_base_1193909_work','/home/linhao/Toolchain/development/MLGO','/home/linhao/Toolchain/development/llvm_inline_development']:
 r=subprocess.run(['du','-sx','-B1','--time','--time-style=full-iso','--',p],capture_output=True,text=True,timeout=300)
 out.append({'path':p,'argv':r.args,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'bytes':int(r.stdout.split('\t')[0]),'time':datetime.datetime.now().astimezone().isoformat()})
 (D/'du-additional.json').write_text(json.dumps(out,indent=2)+'\n');print(p,r.stdout.strip(),flush=True)
