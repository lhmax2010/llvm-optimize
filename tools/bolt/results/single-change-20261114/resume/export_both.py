from pathlib import Path
import subprocess,json,datetime
E=Path(__file__).resolve().parent
N=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/single-change-20261114/source')
new=json.loads((E/'created-commits.json').read_text())[-1]['sha']
for label,rev in [('PS3',new),('old','2cdd37ff747765e99c2befa3e6e8a88663ab77fe')]:
 out=N.parent/('export-'+label)
 assert not out.exists(),str(out)
 argv=['gbs','export','--commit',rev,'--outdir',str(out),'--outdir-directly',str(N)]
 with (E/(label+'-export.stdout')).open('wb') as so,(E/(label+'-export.stderr')).open('wb') as se:
  p=subprocess.run(argv,cwd=N,stdout=so,stderr=se)
 (E/(label+'-export.json')).write_text(json.dumps({'argv':argv,'cwd':str(N),'rc':p.returncode,'time':datetime.datetime.now().astimezone().isoformat()},indent=2)+'\n')
 assert p.returncode==0,label
 print(label,'export PASS',flush=True)
