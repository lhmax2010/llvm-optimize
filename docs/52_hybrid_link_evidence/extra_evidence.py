from pathlib import Path
import json,csv,re,subprocess as sp,hashlib,shlex
W=Path.cwd();E=W/'temp/hybrid-link-20261015';S=E/'source';D=W/'docs/52_hybrid_link_evidence';Q=W/'docs/qb_1199098_vs_1178133/size_attribution'
rows=json.loads((E/'allrows.json').read_text());a={r['output']:r for r in rows['a']}
# Source and generated installation rules; no installation performed.
aliases={'clang':'clang-22'};proof=[]
for p in sorted((E/'config-a').rglob('cmake_install.cmake')):
 for ln,line in enumerate(p.read_text().splitlines(),1):
  m=re.search(r'install_symlink\("([^"]+)" "([^"]+)" "bin" "([^"]+)"\)',line)
  if m:aliases[m[1]]=m[2];proof.append(f'{p.relative_to(E)}:{ln}: {line.strip()}')
proof.append('source/clang/tools/driver/CMakeLists.txt:88: set_target_properties(clang PROPERTIES VERSION ${CLANG_EXECUTABLE_VERSION})')
(D/'install-aliases.txt').write_text('\n'.join(proof)+'\n');(D/'aliases.json').write_text(json.dumps(aliases,indent=2)+'\n')
p=Q/'raw/new_armv7l_clang-accel-x86_64-armv7l_files.jsonl';records=[]
for n,line in enumerate(p.read_text().splitlines(),1):
 r=json.loads(line)
 if not r['path'].startswith('/emul/usr/bin/'):continue
 name=Path(r['path']).name;canonical=name
 if name.startswith('armv7l-tizen-linux-gnueabi-'):canonical=name.removeprefix('armv7l-tizen-linux-gnueabi-')
 while canonical in aliases:canonical=aliases[canonical]
 v=a.get('bin/'+canonical)
 assert v is not None,(name,canonical)
 state=('动态 LLVM+clang-cpp' if v['libclang_cpp_so'] else '动态 LLVM') if v['libLLVM_so'] else '静态 LLVM（上游例外）' if canonical in ['llvm-tblgen','clang-tblgen','lldb-tblgen','llvm-config','llvm-exegesis'] else '静态 LLVM（三组）'
 records.append({'path':r['path'],'old_payload_type':r['type'],'canonical_target':v['output'],'after':state,'libLLVM_so':v['libLLVM_so'],'libclang_cpp_so':v['libclang_cpp_so'],'inventory_line':n,'ninja_line':v['line']})
with (D/'accel-tool-map.csv').open('w') as f:
 out=csv.DictWriter(f,fieldnames=list(records[0]));out.writeheader();out.writerows(records)
# Both snapshot ELF dependency inventories for the tools and dynamic libraries.
with (Q/'elf_all.csv').open() as f:
 raw=[r for r in csv.DictReader(f) if r['package']=='clang-accel-x86_64-armv7l']
with (D/'accel-elf-baselines.csv').open('w') as f:
 out=csv.DictWriter(f,fieldnames=['side','path','needed','readelf_evidence']);out.writeheader();out.writerows({k:r[k] for k in out.fieldnames} for r in raw)
old=[json.loads(x) for x in (Q/'raw/old_armv7l_clang-accel-x86_64-armv7l_files.jsonl').read_text().splitlines()]
new=[json.loads(x) for x in p.read_text().splitlines()]
summary={'bin_entries':len(records),'static_three_group_entries':sum(r['after']=='静态 LLVM（三组）' for r in records),'upstream_static_entries':sum('上游' in r['after'] for r in records),'dynamic_entries':sum(r['libLLVM_so'] for r in records),'old_shared_libraries':[r['path'] for r in old if 'libLLVM.so' in r['path'] or 'libclang-cpp.so' in r['path']],'new_shared_libraries':[r['path'] for r in new if 'libLLVM.so' in r['path'] or 'libclang-cpp.so' in r['path']]}
(D/'accel-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(summary)
# Source line excerpts identify private static archives and upstream exceptions.
paths=['llvm/tools/opt/CMakeLists.txt','llvm/lib/Debuginfod/CMakeLists.txt','llvm/tools/llvm-diff/CMakeLists.txt','llvm/tools/llvm-cfi-verify/CMakeLists.txt','llvm/cmake/modules/TableGen.cmake','llvm/tools/llvm-config/CMakeLists.txt','llvm/tools/llvm-exegesis/CMakeLists.txt','llvm/tools/lli/ChildTarget/CMakeLists.txt','llvm/benchmarks/CMakeLists.txt','clang-tools-extra/clang-tidy/CMakeLists.txt','clang-tools-extra/clangd/CMakeLists.txt','llvm/tools/llvm-shlib/CMakeLists.txt','clang/tools/clang-shlib/CMakeLists.txt','llvm/cmake/modules/AddLLVM.cmake','clang/cmake/modules/AddClang.cmake','lld/cmake/modules/AddLLD.cmake']
with (D/'source-evidence.txt').open('w') as f:
 for path in paths:
  for ln,line in enumerate((S/path).read_text().splitlines(),1):
   if re.search(r'add_llvm_|add_clang_|target_link_libraries|DISABLE_LLVM|LLVM_LINK_LLVM|CLANG_LINK_CLANG|TIZEN_|PRIVATE|SHARED|LINK_COMPONENTS|STATIC|LLVMOptDriver|LLVM_DYLIB_COMPONENTS|LLVM_INSTALL_UTILS',line):f.write(f'{path}:{ln}: {line}\n')
# Complete recipe has unchanged files/packages; expected baseline binary package names.
spec35=(W/'docs/35_archive_fix_v2_final.md').read_text();names=sorted(set(re.findall(r'^\| ([^| ]+)-22\.1\.8-1\.x86_64\.rpm \|',spec35,re.M)));assert len(names)==22,names
(D/'expected-rpm-names.txt').write_text('\n'.join(names)+'\n')
print('rpm',names)
