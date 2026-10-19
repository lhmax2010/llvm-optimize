from pathlib import Path
import json,subprocess,time
E=Path(__file__).parent;S=E.parent/'bolt-v4-20261013/v41/llvm-source';sha=json.loads((E/'release.json').read_text())['commit']
a=['gbs','export','--spec','llvm.spec','--commit',sha,'--upstream-branch','sandbox/fangyu.he/llvm_optmize','--upstream-tag','upstream/22.1.8','--outdir-directly','-o',str(E/'export'),str(S)]
v=subprocess.run(['gbs','--version'],capture_output=True,text=True);(E/'gbs-version.txt').write_text(v.stdout+v.stderr)
t=time.monotonic()
with (E/'gbs-export.stdout').open('wb') as out,(E/'gbs-export.stderr').open('wb') as err:r=subprocess.run(a,stdout=out,stderr=err)
(E/'gbs-export.json').write_text(json.dumps({'argv':a,'rc':r.returncode,'seconds':time.monotonic()-t},indent=2)+'\n');print(r.returncode);assert r.returncode==0
