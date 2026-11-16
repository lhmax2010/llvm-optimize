
from pathlib import Path
import subprocess,json,os,datetime
W=Path('/home/linhao/Toolchain/development/llvm-optimize'); B=Path(str(W)+'-bolt'); E=B/'tools/bolt/results/hq-review-361395/round3/resume3'
D=W/'temp/hq-review-105-20261116/link-probe'; tools=D/'tools'
root=W/'temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
pairs=[('candidate',W/'temp/hq-review-104-20261116/361395-ps4'),('with-361624',W/'temp/hq-review-105-20261116/trial-361624')]
out=[]
for label,source in pairs:
 build=D/label
 cmd=[str(tools/'cmake'),'-G','Ninja','-S',str(source/'llvm'),'-B',str(build),
 '-DCMAKE_BUILD_TYPE=Release','-DLLVM_ENABLE_PROJECTS=bolt','-DLLVM_TARGETS_TO_BUILD=X86',
 '-DLLVM_BUILD_LLVM_DYLIB=ON','-DLLVM_LINK_LLVM_DYLIB=ON','-DTIZEN_HYBRID_LINK=ON','-DBUILD_SHARED_LIBS=OFF',
 '-DLLVM_LIBDIR_SUFFIX=64','-DLLVM_ENABLE_RTTI=ON','-DLLVM_INCLUDE_TESTS=OFF','-DLLVM_INCLUDE_BENCHMARKS=OFF','-DLLVM_INCLUDE_EXAMPLES=OFF','-DLLVM_ENABLE_BINDINGS=OFF',
 '-DBOLT_ENABLE_RUNTIME=OFF','-DBOLT_BUILD_TOOLS=OFF','-DBOLT_INCLUDE_TESTS=OFF','-DBOLT_TARGETS_TO_BUILD=X86',
 '-DLLVM_ENABLE_ZSTD=OFF','-DLLVM_ENABLE_LIBEDIT=OFF','-DLLVM_ENABLE_LIBXML2=OFF','-DLLVM_ENABLE_TERMINFO=OFF','-DLLVM_ENABLE_CURL=OFF','-DLLVM_ENABLE_ZLIB=OFF',
 '-DCMAKE_C_COMPILER='+str(tools/'clang'),'-DCMAKE_CXX_COMPILER='+str(tools/'clang++'),
 '-DCMAKE_MAKE_PROGRAM='+str(tools/'ninja'),'-DCMAKE_AR='+str(tools/'llvm-ar'),'-DCMAKE_RANLIB='+str(tools/'llvm-ranlib'),
 '-DCMAKE_SYSROOT='+str(root)]
 (E/(label+'-cmake-command.json')).write_text(json.dumps(cmd,indent=2)+'\n')
 with (E/(label+'-cmake.log')).open('w') as log:
  p=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=900)
 print(label,'configure',p.returncode,flush=True)
 if p.returncode:
  print((E/(label+'-cmake.log')).read_text()[-6000:]);raise SystemExit(p.returncode)
 cmd=[str(tools/'ninja'),'-C',str(build),'-t','commands','-s','bin/llvm-bolt']
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=120)
 (E/(label+'-llvm-bolt-link.txt')).write_text(p.stdout)
 (E/(label+'-ninja.stderr')).write_text(p.stderr)
 if p.returncode:raise SystemExit(p.returncode)
 link=p.stdout
 record={'label':label,'configure_rc':0,'ninja_commands_rc':0,'link_has_libLLVM_so':'libLLVM.so' in link,'command_count':len(link.splitlines()),'scope':'link-policy configure probe, not complete product configuration; no LLVM target built'}
 out.append(record)
 print(record,flush=True)
(E/'link-probe-result.json').write_text(json.dumps(out,indent=2)+'\n')
print('已结束',datetime.datetime.now().astimezone().isoformat(),'link-probe PASS')
