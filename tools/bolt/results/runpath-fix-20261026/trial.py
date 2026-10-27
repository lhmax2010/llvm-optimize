from pathlib import Path
import json,subprocess,shutil,time,hashlib
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';Q=R/'home/abuild/runpath-pretrial';Q.mkdir(exist_ok=True)
assert json.loads((E/'prep-result.json').read_text())['rc']==0
shutil.copyfile(D/'source/packaging/clang-bolt-helper.py',Q/'helper.py')
ordinary=W/'temp/bolt-on-hybrid-20261024/products/binaries/ordinary-clang-22'
with ordinary.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
assert sha=='d5090159915657b235b96f1202c058e1efd1647d6a2225ac8fdb2906aeaa501d'
shutil.copy2(ordinary,Q/'ordinary-clang-22')
script='''import os,json,subprocess,time,hashlib,sys
from pathlib import Path
import helper as h
base=Path('/home/abuild/rpmbuild/BUILD/llvm-22.1.8');build=base/'pretrial-include';work=Path('/home/abuild/runpath-pretrial')
report={'PATH':os.environ['PATH'],'clang':subprocess.check_output(['which','clang'],text=True).strip(),'clang++':subprocess.check_output(['which','clang++'],text=True).strip(),'ordinary_sha256':h.digest(work/'ordinary-clang-22'),'configuration':'preparation only; generated LLVM headers; no compiler build'}
argv=['cmake','-S',str(base/'llvm'),'-B',str(build),'-G','Ninja','-DCMAKE_C_COMPILER=clang','-DCMAKE_CXX_COMPILER=clang++','-DCMAKE_BUILD_TYPE=Release','-DLLVM_ENABLE_PROJECTS=clang','-DLLVM_TARGETS_TO_BUILD=X86','-DLLVM_INCLUDE_TESTS=OFF','-DLLVM_INCLUDE_BENCHMARKS=OFF']
p=subprocess.run(argv,stdout=(work/'configure.stdout').open('w'),stderr=(work/'configure.stderr').open('w'));report.update(configure_argv=argv,configure_rc=p.returncode)
if p.returncode: (work/'result.json').write_text(json.dumps(report,indent=2));sys.exit(1)
rows=[]
for n,(source,target,args) in enumerate(h.real_commands(build,'/usr/lib64/clang/22')):
    argv=[str(work/'ordinary-clang-22'),*args,'-o',str(work/('trial-%d.o'%n))];start=time.monotonic()
    p=subprocess.run(argv,stdout=(work/('trial-%d.stdout'%n)).open('w'),stderr=(work/('trial-%d.stderr'%n)).open('w'))
    row={'source':source,'source_sha256':h.digest(base/source),'target':target,'argv':argv,'rc':p.returncode,'seconds':time.monotonic()-start};rows.append(row)
    report['trials']=rows;(work/'result.json').write_text(json.dumps(report,indent=2))
    if p.returncode:sys.exit(1)
report['PASS']=True;(work/'result.json').write_text(json.dumps(report,indent=2));print('REAL_PRETRIAL_PASS',len(rows),sum(x['seconds'] for x in rows))
'''
(Q/'trial.py').write_text(script)
cmd=['sudo','-n','/usr/sbin/chroot','--userspec=1000:1000',str(R),'/usr/bin/env','-i','HOME=/home/abuild','USER=abuild','LOGNAME=abuild','SHELL=/bin/sh','PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin','LC_ALL=C','LANG=C','/bin/sh','-c','cd /home/abuild/runpath-pretrial && python3 -B trial.py']
with (E/'real-pretrial.stdout').open('wb') as o,(E/'real-pretrial.stderr').open('wb') as e:p=subprocess.run(cmd,stdout=o,stderr=e)
(E/'real-pretrial-command.json').write_text(json.dumps({'argv':cmd,'rc':p.returncode},indent=2))
for f in Q.iterdir():
 if f.suffix in ('.json','.stdout','.stderr'):shutil.copyfile(f,E/('pretrial-'+f.name))
print('REAL_PRETRIAL_EXIT',p.returncode,flush=True)
