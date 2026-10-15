from pathlib import Path
import re,json,subprocess as sp,shlex,csv,hashlib
W=Path.cwd();E=W/'temp/hybrid-link-20261015';R=W/'temp/gbs-root-x86_64-archivefix-v2/local/BUILD-ROOTS/scratch.x86_64.0';S=E/'source';D=W/'docs/52_hybrid_link_evidence';D.mkdir(exist_ok=True)
want={'clang':'bin/clang-22','lld':'bin/lld','llvm-ar':'bin/llvm-ar','clang-repl':'bin/clang-repl','clang-check':'bin/clang-check','clang-tidy':'bin/clang-tidy','clangd':'bin/clangd','opt':'bin/opt','llc':'bin/llc','lli':'bin/lli','llvm-objcopy':'bin/llvm-objcopy','llvm-nm':'bin/llvm-nm','llvm-strip':'bin/llvm-objcopy','libLTO.so':'lib64/libLTO.so.22.1','LLVMgold.so':'lib64/LLVMgold.so','lldb':'bin/lldb','liblldb':'lib64/liblldb.so.22.1.8'}
allrows={};selected={}
for label in ['a','b','c']:
 text=(E/('config-'+label)/'build.ninja').read_text();rows=[]
 for m in re.finditer(r'^build ([^\n:]+): (\w+_(?:EXECUTABLE|SHARED_LIBRARY|MODULE_LIBRARY)_LINKER[^\s]*)[^\n]*\n((?:  [^\n]*\n)*)',text,re.M):
  output=m[1].split(' | ')[0];vars=dict(re.findall(r'^  (\w+) = (.*)$',m[3],re.M));libs=vars.get('LINK_LIBRARIES','')
  archives=list(dict.fromkeys(re.findall(r'(?:\S*/)?lib(?:LLVM|clang|lld)[^\s$;]*\.a',libs)))
  llvm_a=[x for x in archives if Path(x).name.startswith('libLLVM')];clang_a=[x for x in archives if Path(x).name.startswith('libclang')];lld_a=[x for x in archives if Path(x).name.startswith('liblld')]
  rows.append(dict(output=output,rule=m[2],line=text.count('\n',0,m.start())+1,libLLVM_so=bool(re.search(r'libLLVM\.so',libs)),libclang_cpp_so=bool(re.search(r'libclang-cpp\.so',libs)),llvm_archives=llvm_a,clang_archives=clang_a,lld_archives=lld_a,link_libraries=libs))
 allrows[label]=rows
 (D/(label+'-all-link-targets.json')).write_text(json.dumps(rows,indent=2)+'\n')
 (D/(label+'-component-archive-consumers.txt')).write_text('\n'.join(r['output']+'\tLLVM='+str(len(r['llvm_archives']))+' clang='+str(len(r['clang_archives']))+' lld='+str(len(r['lld_archives'])) for r in rows if any(r[k] for k in ['llvm_archives','clang_archives','lld_archives']))+'\n')
 sel=[]
 for name,out in want.items():
  match=[r for r in rows if r['output']==out]
  if name=='liblldb' and not match: match=[r for r in rows if r['output'].startswith('lib64/liblldb.so.')]
  assert len(match)==1,(label,name,[r['output'] for r in rows if name in r['output']])
  r=dict(match[0],name=name);out=r['output'];cmd='/usr/bin/ninja -C /tmp/hybrid52/config-'+label+' -t commands -s '+shlex.quote(out)
  ns='mount --make-rprivate / && mount --bind "$1" "$2/tmp/hybrid52" && exec chroot "$2" /bin/sh -c '+shlex.quote(cmd)
  p=sp.run(['unshare','-Ur','-m','sh','-c',ns,'sh',str(E),str(R)],capture_output=True,text=True,check=True)
  r['command']=p.stdout.strip();r['extraction_command']=cmd;sel.append(r)
 selected[label]=sel
 (D/(label+'-selected-commands.json')).write_text(json.dumps(sel,indent=2)+'\n')
 print(label,'all links',len(rows),'LLVM archives:',[r['output'] for r in rows if r['llvm_archives']],flush=True)
for n in want:
 print(n,[(l,next((r['libLLVM_so'],r['libclang_cpp_so'],len(r['llvm_archives']),len(r['clang_archives']),len(r['lld_archives'])) for r in selected[l] if r['name']==n)) for l in 'abc'])
for p in ['macro-comparison.json','x86_64-build.diff','x86_64-install.diff','armv7l-build.diff','armv7l-install.diff','aarch64-build.diff','aarch64-install.diff','gerrit-356627.json','gerrit-356949.json']:
 (D/p).write_bytes((E/p).read_bytes())
for arch in ['x86_64','armv7l','aarch64']:
 for label in ['baseline','hybrid']:
  for suf in ['build.txt','install.txt','cmake.json']:
   p=arch+'-'+label+'-'+suf;(D/p).write_bytes((E/p).read_bytes())
for l in 'abc':
 for suf in ['configure-argv.json','configure.log','configure-result.json']:
  p=l+'-'+suf;(D/p).write_bytes((E/p).read_bytes())
(E/'selected.json').write_text(json.dumps(selected,indent=2));(E/'allrows.json').write_text(json.dumps(allrows,indent=2))
