"""Daytime negative copies and release fixtures; never writes historical products."""
from pathlib import Path
import json,shutil,ctypes,subprocess,hashlib,sys,os
from checks import *
from test_checks import elf
from release_checks import ninja_modules
from resource_report import critical_stop,report
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';X=W/'temp/night-20261103/scratch-checks';X.mkdir();out=B/'tools/bolt/results/night-prep-20261103';results=[]
original=W/'temp/debuglink-20261028/full-20261030/products/binaries/clang.candidate';copy=X/'corrupt-clang';shutil.copyfile(original,copy)
with original.open('rb') as f:
 import mmap
 with mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as b:offset=sections(b)['.text']['offset']+17
with copy.open('r+b') as f:f.seek(offset);v=f.read(1);f.seek(offset);f.write(bytes([v[0]^1]))
try:content_proof(original.read_bytes(),copy.read_bytes())
except AssertionError as e:results.append(dict(case='real clang one code byte changed',PASS=True,rejected=str(e),offset=offset,old_sha=sha(original),new_sha=sha(copy)))
else:raise AssertionError('corrupt clang accepted')
p=X/'recorded-option.o';p.write_bytes(elf(b'-O3 -fno-inline-functions\0'))
try:no_dropped(p.read_bytes())
except AssertionError as e:results.append(dict(case='DROPPED token inserted',PASS=True,rejected=str(e),sha256=sha(p)))
else:raise AssertionError('dropped token accepted')
# Offline Ninja parser fixture: exactly the rule kind used by real CMake MODULEs.
N=X/'module-build';(N/'CMakeFiles').mkdir(parents=True)
(N/'CMakeFiles/rules.ninja').write_text('rule CXX_MODULE_LIBRARY_LINKER__fixture_Release\n  command = $PRE_LINK clang $LINK_FLAGS -shared $in -o $TARGET_FILE $LINK_LIBRARIES && $POST_BUILD\n')
(N/'build.ninja').write_text('build lib64/fixture.so: CXX_MODULE_LIBRARY_LINKER__fixture_Release object.o | lib64/libLLVM.so || fixture\n  LINK_FLAGS = -Wl,-z,relro,--as-needed -Wl,--gc-sections\n  TARGET_FILE = lib64/fixture.so\n  PRE_LINK = : &&\n  POST_BUILD = :\n  LINK_LIBRARIES = lib64/libLLVM.so\n')
r=ninja_modules(N);assert len(r)==1 and '-Wl,-z,relro,--as-needed' in r[0]['command'] and 'object.o' in r[0]['command'];results.append(dict(case='MODULE rule expansion fixture',PASS=True,result=r))
# Actual dlopen positive + negative, no compilation or package installation.
ctypes.CDLL('libm.so.6',mode=os.RTLD_NOW);results.append(dict(case='dlopen known shared library',PASS=True))
try:ctypes.CDLL(str(copy),mode=os.RTLD_NOW)
except OSError as e:results.append(dict(case='dlopen invalid library',PASS=True,rejected=str(e)))
else:raise AssertionError('dlopen executable accepted')
# Serial policy fixtures use exactly the classifier used by the night coordinator.
for name,event,expected in [('ordinary-failure',None,None),('disk-failure','disk-stop.json','disk-stop'),('oom-failure','resources.jsonl','memory-oom-stop')]:
 d=X/name;(d/'evidence').mkdir(parents=True)
 if event=='disk-stop.json':save(d/'evidence'/event,{'reason':'fixture'})
 if event=='resources.jsonl':(d/'evidence'/event).write_text(json.dumps({'memory.events':'oom 1\noom_kill 1\n'})+'\n')
 actual=critical_stop(d,{'mounts':{'stdout':''},'remaining_build_processes':[]});assert actual==expected;results.append(dict(case=name,PASS=True,critical=actual,D_permitted=actual is None))
save(out/'integration.json',results);print('INTEGRATION_PASS',len(results))
