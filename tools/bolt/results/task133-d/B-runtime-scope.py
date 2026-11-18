from pathlib import Path
import collections,importlib.util,json,re,subprocess
w=Path('/home/linhao/Toolchain/development/llvm-optimize'); b=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt'); t=w/'temp/task133-d'; e=b/'tools/bolt/results/task133-d'; s=w/'temp/task131/pgo-dev'
spec=importlib.util.spec_from_file_location("helper",s/'packaging/clang-bolt-helper.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
data=json.loads((b/'tools/bolt/results/task131/historical-scope-sampled.json').read_text())
matches=collections.defaultdict(list)
other=[]
for r in data['matched']:
 seen=helper.pgo_runtime_target(r['object'])
 if r['category']=='runtime': matches[r['target']].append((r['object'],seen))
 elif seen: other.append((r['target'],r['category'],r['object']))
rows={k:{'edges':len(values),'accepted_runtime':sum(bool(r[1]) for r in values),'example':values[0][0]} for k,values in sorted(matches.items())}
miss=[k for k,r in rows.items() if r['edges']!=r['accepted_runtime']]
assert len(matches)==37 and not miss,miss
links={}
root=w/'temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
profile=w/'temp/pgo-profiles-keep-20261102/clang.profdata'
dirs=('compiler-rt','openmp')
vars=('CMAKE_C_FLAGS','CMAKE_CXX_FLAGS','CMAKE_ASM_FLAGS','CMAKE_EXE_LINKER_FLAGS','CMAKE_MODULE_LINKER_FLAGS','CMAKE_SHARED_LINKER_FLAGS')
for area in dirs:
 data=(s/area/'CMakeLists.txt').read_text()
 first=data.index('if(TIZEN_PGO_EXCLUDE_RUNTIMES')
 last=data.index('\nendif()',first)+len('\nendif()')
 guard=data[first:last]
 src=t/f'B-runtime-{area}.cmake'
 state='\n'.join(f'set({key} "-O3 -fprofile-instr-use=\\"{profile}\\" -g")' for key in vars)
 checks='\n'.join(f'if(NOT {key} STREQUAL "-O3  -g")\n message(FATAL_ERROR "{key} exclusion failed")\nendif()' for key in vars)
 src.write_text(f'set(TIZEN_PGO_EXCLUDE_RUNTIMES ON)\nset(LLVM_PROFDATA_FILE "{profile}")\n{state}\n{guard}\n{checks}\nif(LLVM_PROFDATA_FILE)\n message(FATAL_ERROR "profile path still set")\nendif()\n')
 p=subprocess.run([str(t/'tizen-tools/bin/cmake'),'-P',str(src)],capture_output=True,text=True)
 links[area]={'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'cmake':src.read_text()}
(e/'B-runtime-scope.json').write_text(json.dumps({'historical_targets':rows,'unexpected_categories':other,'cmake_script_checks':links},indent=2)+'\n')
assert all(r['rc']==0 for r in links.values()),links
assert not other,other
print('runtime',len(matches),sum(len(x) for x in matches.values()),'CMake',links.keys())
