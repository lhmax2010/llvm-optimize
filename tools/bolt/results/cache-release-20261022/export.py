import subprocess,time,json,sys
from pathlib import Path
D=Path(__file__).resolve().parent;S=D.parent/'bolt-v4-20261013/v41/llvm-source'
sha=sys.argv[1];label=sys.argv[2];out=Path(sys.argv[3]);E=D/(label+'-export');E.mkdir(exist_ok=True)
argv=['gbs','export','--spec','llvm.spec','--commit',sha,'--upstream-branch','sandbox/fangyu.he/llvm_optmize','--upstream-tag','upstream/22.1.8','--outdir-directly','-o',str(out),str(S)]
ts=time.monotonic()
with (E/'stdout').open('wb') as o,(E/'stderr').open('wb') as e:r=subprocess.run(argv,stdout=o,stderr=e)
(E/'result.json').write_text(json.dumps({'argv':argv,'rc':r.returncode,'seconds':time.monotonic()-ts},indent=2));sys.exit(r.returncode)
