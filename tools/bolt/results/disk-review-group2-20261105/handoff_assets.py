from pathlib import Path
import json,subprocess
E=Path(__file__).resolve().parent;R=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/llvm-optimize-intranet-20261020/assets');out=[]
expected={}
for l in (R/'SHA256SUMS').read_text().splitlines():
 h,n=l.split(None,1);expected[n.lstrip('*')]=h
for p in sorted(R.iterdir()):
 if not p.is_file():continue
 r=subprocess.run(['timeout','120','nice','-n','19','ionice','-c3','sha256sum','--',str(p)],capture_output=True,text=True);h=r.stdout.split()[0] if r.returncode==0 else None
 out.append({'path':str(p),'size':p.stat().st_size,'hash':{'rc':r.returncode,'sha256':h,'stderr':r.stderr},'expected':expected.get(p.name),'match':h==expected[p.name] if p.name in expected else None})
 (E/'handoff-assets.json').write_text(json.dumps(out,indent=2))
print('assets',len(out),'checked',sum(x['match'] is True for x in out),'fail',sum(x['match'] is False for x in out),flush=True)
