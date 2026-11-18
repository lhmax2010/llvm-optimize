from pathlib import Path
import json,os,re,resource,subprocess
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
T=W/'temp/task133-d'; E=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt')/'tools/bolt/results/task133-d'
R=W/'temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
tools=T/'tizen-tools/bin'; out=T/'D-fixtures/truth-retry'; out.mkdir()
env=dict(os.environ, LD_LIBRARY_PATH=f'{R}/usr/lib64:{R}/lib64')
resource.setrlimit(resource.RLIMIT_CORE,(0,0))
calls=[]
def run(tool,*args):
 p=subprocess.run([str(tools/tool),*map(str,args)],cwd=out,env=env,text=True,capture_output=True,timeout=30)
 calls.append({'argv':[tool,*map(str,args)],'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 (E/'D-commands-retry.json').write_text(json.dumps(calls,indent=2)+'\n')
 return p
def ir(path,*fs):
 path.write_text(f'source_filename = "{path.stem}.c"\ntarget triple = "x86_64-tizen-linux-gnu"\n'+'\n'.join(fs)+'\n')
 return path
def fn(name,kind='normal',shape=0):
 attr={'normal':('', ''),'local':('internal ',''),
       'odr':('linkonce_odr ', ' comdat')}[kind]
 prefix=chr(36)+f'{name} = comdat any\n' if kind=='odr' else ''
 body=('switch i32 %x, label %n [i32 0, label %y i32 1, label %z]\ny: ret i32 1\nz: ret i32 2\nn: ret i32 3' if shape else
       '%b = icmp eq i32 %x, 0\n br i1 %b, label %y, label %n\ny: ret i32 1\nn: ret i32 2')
 return f'{prefix}define {attr[0]}i32 @{name}(i32 %x){attr[1]} {{\nentry:\n {body}\n}}'
def instrument(path):
 target=out/(path.stem+'.instrumented.ll')
 assert run('opt','--passes=pgo-instr-gen','-S',path,'-o',target).returncode==0
 data=target.read_text()
 keys=dict(re.findall(r'^(@[^ ]+) = private constant \[\d+ x i8\] c"([^"\n]*)"',data,re.M))
 entries={}
 for m in re.finditer(r'^define .*?@([^ (]+)\([^\n]*\{\n(.*?)^}',data,re.M|re.S):
  insts=re.findall(r'@llvm\.instrprof\.increment\(ptr (\S+), i64 (-?\d+), i32 (\d+), i32 \d+\)',m[2])
  if insts:
   (key,hash,count),=set(insts)
   entries[m[1]]=(keys[key],int(hash)%(1<<64),int(count))
 return entries
def textprofile(path,entries):
 text=':ir\n'+''.join(f'{name}\n{hash}\n{len(counts)}\n'+'\n'.join(map(str,counts))+'\n\n' for (name,hash),counts in entries.items())
 path.write_text(text)
 target=path.with_suffix('.profdata')
 assert run('llvm-profdata','merge',path,'-o',target).returncode==0
 return target
def blockcount(data):
 metas={m[1]:int(m[2]) for m in re.finditer(r'^!(\d+) = !\{!"function_entry_count", i64 (\d+)\}',data,re.M)}
 return {m[1]:metas[m[2]] for m in re.finditer(r'^define [^\n]*?@([^ (]+)\([^\n]* !prof !(\d+) \{',data,re.M) if m[2] in metas}
records=[]
def fixture(tag,units,profiles,truth, *,zero=False,after=None):
 modules=[ir(out/f'{tag}-{n}.ll',*f) for n,f in enumerate(units)]
 queries=[instrument(m) for m in modules]
 supply={}
 for n,name,count in profiles:
  key,hash,width=queries[n][name]
  supply[key,hash]=[count]*width
 if not supply: supply['unrelated',1]=[1]
 prof=textprofile(out/f'{tag}.txt',supply)
 result=[]
 for n,mod in enumerate(modules):
  dest=out/f'{mod.stem}.used.ll'
  p=run('opt','--passes=pgo-instr-use','-pgo-test-profile-file='+str(prof),'-pgo-warn-missing-function','-no-pgo-warn-mismatch=false','-no-pgo-warn-mismatch-comdat-weak=false','-stats','-S',mod,'-o',dest)
  assert p.returncode==0,p.stderr
  diag=p.stderr.splitlines()
  annotated=blockcount(dest.read_text())
  found={}
  for name,(key,hash,width) in queries[n].items():
   destline=next((l for l in diag if key in l),None)
   if name in annotated:
    found[name]='matched'
   elif destline and re.search(r'mismatch',destline,re.I):
    found[name]='mismatched'
   elif destline and re.search(r'no profile|missing|not found',destline,re.I):
    found[name]='missing'
   else:
    found[name]='unverified'
  entry={'truth':truth[n],'observed':found,'queries':queries[n],'entry_counts':annotated,'diagnostics':diag,'pass':found==truth[n]}
  if zero: entry['pass'] &= annotated.get('zero')==0
  if after:
   passes,want=after
   post=out/f'{mod.stem}.post.ll'
   pr=run('opt','--passes='+passes,'-S',dest,'-o',post)
   post_text=post.read_text() if pr.returncode==0 else ''
   entry['post_transformation']={'pass':pr.returncode==0 and want(post_text),'IR':post_text}
   entry['pass'] &= entry['post_transformation']['pass']
  result.append(entry)
 records.append({'fixture':tag,'units':result,'pass':all(x['pass'] for x in result)})
 (E/'D-fixtures-retry.json').write_text(json.dumps(records,indent=2)+'\n')
m='matched'; u='missing'; x='mismatched'; n=fn
fixture('full',[[n('a'),n('b')]],[(0,'a',3),(0,'b',4)],[{'a':m,'b':m}])
fixture('healthy',[[n('a')]],[(0,'a',3)],[{'a':m}])
fixture('missing',[[n('a'),n('b')]],[],[{'a':u,'b':u}])
fixture('mixed-hash',[[n('a'),n('b',shape=1)],[n('b')]],[(0,'a',3),(1,'b',4)],[{'a':m,'b':x},{'b':m}])
fixture('comdat',[[n('a','odr',1)],[n('a','odr')]],[(1,'a',4)],[{'a':x},{'a':m}])
fixture('cross-unit-repeat',[[n('a','odr')],[n('a','odr')]],[(0,'a',2)],[{'a':m},{'a':m}])
fixture('zero',[[n('zero'),n('a')]],[(0,'zero',0),(0,'a',3)],[{'zero':m,'a':m}],zero=True)
fixture('local-same-name',[[n('a','local')],[n('a','local')]],[(0,'a',3)],[{'a':m},{'a':u}])
fixture('odr-distinct-hash',[[n('a','odr')],[n('a','odr',1)]],[(0,'a',2),(1,'a',3)],[{'a':m},{'a':m}])
fixture('post-match-deletion',[[n('a','local')]],[(0,'a',3)],[{'a':m}],after=('globaldce',lambda s:not re.search(r'^define .*@a\(',s,re.M)))
clone_source='''define internal i32 @special(ptr %fp, i32 %x) noinline {
entry:
 %v = call i32 %fp(i32 %x)
 %a = add i32 %v, 1
 ret i32 %a
}
define dso_local i32 @impl1(i32 %x) noinline {
entry:
 %v = mul i32 %x, 3
 ret i32 %v
}
define dso_local i32 @impl2(i32 %x) noinline {
entry:
 %v = mul i32 %x, 5
 ret i32 %v
}
define i32 @caller(i32 %x) {
entry:
 %a = call i32 @special(ptr @impl1, i32 %x)
 %b = call i32 @special(ptr @impl2, i32 %x)
 %s = add i32 %a, %b
 ret i32 %s
}
'''
fixture('post-match-clone',[[clone_source]],[(0,k,3) for k in ('special','impl1','impl2','caller')],
        [dict.fromkeys(('special','impl1','impl2','caller'),m)],
        after=('ipsccp<func-spec>',lambda s:bool(re.search(r'^define [^\n]*@special\.[^ (]+\(',s,re.M))))
for row in records:
 print(row['fixture'],row['pass'],[u['observed'] for u in row['units']])
