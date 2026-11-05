from pathlib import Path
import json,subprocess
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize')
rows=[]
for name in ('gbs-root-x86_64-debuginfo-j4-v2','gbs-root-x86_64-archivefix-v2'):
 base=W/'temp'/name/'local'
 choices=[base/'repos',base/'SRPMS',base/'BUILD-ROOTS']
 r=base/'BUILD-ROOTS/scratch.x86_64.0'
 for tail in ['usr','lib64','home/abuild/rpmbuild/RPMS','home/abuild/rpmbuild/SRPMS','home/abuild/rpmbuild/SOURCES','home/abuild/rpmbuild/BUILDROOT','home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/bin','home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64','home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lto.cache','home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/tools','home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib']:choices.append(r/tail)
 for p in choices:
  if not p.exists():rows.append({'path':str(p),'exists':False});continue
  r1=subprocess.run(['timeout','60','nice','-n','19','ionice','-c3','du','-sx','-B1','--',str(p)],capture_output=True,text=True)
  rows.append({'path':str(p),'rc':r1.returncode,'stdout':r1.stdout,'stderr':r1.stderr})
  (E/'deep-sizes.json').write_text(json.dumps(rows,indent=2))
print('deep sizes complete',len(rows))
