import collections,json,os,re,stat,sys
from pathlib import Path
from validate import W,D,E,R,V,INNER,run,root,save,sha
import check_hybrid_link_needed as needed

def executables():
 paths=(E/'rpm-paths.txt').read_text().splitlines();rows=[]
 for logical in paths:
  if logical.startswith(('/usr/lib/debug/','/usr/src/debug/')):continue
  try:p=needed.rooted_path(R,logical)
  except Exception as exc:rows.append({'path':logical,'error':str(exc),'status':'PATH_ERROR'});continue
  if not p.is_file() or not p.stat().st_mode&0o111:continue
  with p.open('rb') as f:magic=f.read(128)
  elf=magic.startswith(b'\x7fELF');script=magic.startswith(b'#!')
  if not elf and not script:continue
  if elf:
   h=run('runtime/headers-'+str(len(rows)),['readelf','-lW',str(p)])
   if 'INTERP' not in h['stdout'] and '/bin/' not in logical:continue
  row={'path':logical,'resolved':str(p),'sha256':sha(p),'elf':elf,'script':script}
  if elf:
   l=root('runtime/ldd-'+str(len(rows)),['ldd',logical]);row['ldd_rc']=l['rc'];row['missing_libraries']=bool(re.search(r'\bnot found\b',l['stdout']+l['stderr']))
  attempts=[]
  for flag in ('--version','--help'):
   try:args=[logical,'-flavor','gnu',flag] if Path(logical).name=='lld' else [logical,flag];q=root('runtime/command-'+str(len(rows))+'-'+flag[2:],args,30)
   except Exception as exc:attempts.append({'flag':flag,'error':str(exc)});continue
   attempts.append({'flag':flag,**q})
   if q['rc']==0:break
  row['attempts']=attempts;row['status']='PASS' if attempts and attempts[-1].get('rc')==0 and not row.get('missing_libraries') and row.get('ldd_rc',0)==0 else 'REVIEW_REQUIRED';rows.append(row)
  save('runtime-progress.json',rows)
 save('runtime-result.json',{'counts':dict(collections.Counter(r['status'] for r in rows)),'rows':rows})

def sdk():
 V.mkdir(exist_ok=True);p=V/'sdk';p.mkdir(exist_ok=True)
 (p/'main.cpp').write_text('#include <llvm/IR/LLVMContext.h>\n#include <llvm/IR/Module.h>\n#include <llvm/Support/raw_ostream.h>\n#include <clang/Basic/Version.h>\nint main(){llvm::LLVMContext c; llvm::Module m("hybrid-sdk",c); llvm::outs()<<clang::getClangFullVersion()<<"\\n"; m.print(llvm::outs(),nullptr); return 0;}\n')
 (p/'CMakeLists.txt').write_text('''cmake_minimum_required(VERSION 3.16)
project(HybridSDK LANGUAGES C CXX)
find_package(LLVM REQUIRED CONFIG)
find_package(Clang REQUIRED CONFIG)
add_executable(hybrid-sdk main.cpp)
target_include_directories(hybrid-sdk PRIVATE ${LLVM_INCLUDE_DIRS} ${CLANG_INCLUDE_DIRS})
target_compile_features(hybrid-sdk PRIVATE cxx_std_17)
target_link_libraries(hybrid-sdk PRIVATE LLVM clang-cpp)
get_property(imported DIRECTORY PROPERTY IMPORTED_TARGETS)
file(WRITE "${CMAKE_BINARY_DIR}/imported-files.tsv" "")
foreach(t IN LISTS imported)
  get_target_property(configs ${t} IMPORTED_CONFIGURATIONS)
  set(props IMPORTED_LOCATION IMPORTED_IMPLIB)
  foreach(c IN LISTS configs)
    string(TOUPPER "${c}" c)
    list(APPEND props IMPORTED_LOCATION_${c} IMPORTED_IMPLIB_${c})
  endforeach()
  foreach(prop IN LISTS props)
    get_target_property(f ${t} ${prop})
    if(f AND NOT f MATCHES "-NOTFOUND$")
      if(NOT EXISTS "${f}")
        message(FATAL_ERROR "Missing imported file ${t} ${prop} ${f}")
      endif()
      file(APPEND "${CMAKE_BINARY_DIR}/imported-files.tsv" "${t}\\t${prop}\\t${f}\\n")
    endif()
  endforeach()
endforeach()
''')
 args=[('configure',['cmake','-S',INNER+'/sdk','-B',INNER+'/sdk-build','-DCMAKE_C_COMPILER=/usr/bin/clang','-DCMAKE_CXX_COMPILER=/usr/bin/clang++']),('compile',['cmake','--build',INNER+'/sdk-build','--parallel','1']),('run',[INNER+'/sdk-build/hybrid-sdk']),('needed',['readelf','-dW',INNER+'/sdk-build/hybrid-sdk'])];rows=[]
 for name,argv in args:
  r=root('sdk-'+name,argv,300);rows.append({'name':name,**r})
  if r['rc']!=0:break
 if (V/'sdk-build/imported-files.tsv').exists():(E/'sdk-imported-files.tsv').write_bytes((V/'sdk-build/imported-files.tsv').read_bytes())
 save('sdk-result.json',{'pass':len(rows)==4 and all(r['rc']==0 for r in rows) and 'libLLVM.so' in rows[-1]['stdout'] and 'libclang-cpp.so' in rows[-1]['stdout'],'rows':rows})

def archives():
 sys.path.insert(0,str(W/'tools'));from inspect_llvm_archives import inspect
 expected=(W/'docs/52_hybrid_sandbox_evidence/expected-static-devel-archives.txt').read_text().splitlines()
 rpm=list((R/'home/abuild/rpmbuild/RPMS/x86_64').glob('llvm-static-devel-*.rpm'));assert len(rpm)==1
 q=run('static-devel-files',['rpm','-qpl',str(rpm[0])]);actual=sorted(x for x in q['stdout'].splitlines() if x.endswith('.a'));assert actual==sorted(expected) and len(actual)==225
 rows=[]
 for path in actual:
  archive=R/path.lstrip('/');r=inspect(archive)
  with archive.open('rb') as f:head=f.read(68)
  r['index_header_present']=head[8:24].rstrip() in (b'/',b'/SYM64/');passed=r['index_header_present'] and not r['thin'] and r['bitcode']==0 and r['other']==0 and r['machine']==r['member_count'] and r['index_equals_machine_symbols']
  row={k:v for k,v in r.items() if k not in ('members','index','machine_symbols','native_symbols','native_map')};row['pass']=passed;rows.append(row)
  with (E/'archive-inspection.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 save('archives-result.json',{'count':len(rows),'passed':sum(r['pass'] for r in rows),'rows':rows})


def native_smoke():
 V.mkdir(exist_ok=True);p=V/'native-smoke';p.mkdir(exist_ok=True)
 (p/'hello.c').write_text('#include <stdio.h>\nint main(void){puts("hello");return 0;}\n')
 (p/'hello.cc').write_text('#include <iostream>\nint main(){std::cout<<"hello\\n";}\n')
 (p/'answer.c').write_text('int answer(void){return 42;}\n')
 script='cd '+INNER+'/native-smoke; clang -c hello.c -o hello.o; clang++ -c hello.cc -o hello-cxx.o; clang -fuse-ld=lld hello.o -o hello; clang++ -fuse-ld=lld hello-cxx.o -o hello-cxx; test "$(./hello)" = hello; test "$(./hello-cxx)" = hello; clang -c answer.c -o answer.o; llvm-ar rcs libanswer.a answer.o; llvm-ar t libanswer.a; llvm-nm --print-armap libanswer.a; ld.lld -r answer.o -o answer-linked.o; readelf -h answer-linked.o; opt --version; llc --version; clang-tidy --version'
 r=root('native-smoke',['/bin/sh','-exc',script],300);save('native-smoke-result.json',{'pass':r['rc']==0,'files':{f.name:sha(f) for f in p.iterdir() if f.is_file()},'result':r})

if __name__=='__main__':globals()[sys.argv[1]]()
