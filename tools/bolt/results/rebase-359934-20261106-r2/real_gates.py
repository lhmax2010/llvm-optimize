from pathlib import Path
import ast,copy,hashlib,importlib.util,json,os,shutil,struct,subprocess,time
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt')
E=B/'tools/bolt/results/rebase-359934-20261106-r2'; X=W/'temp/rebase-359934-20261106-r2/real-gates'
S=W/'temp/rebase-359934-20261106/source'
R=W/'temp/night-20261105/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
oldbuild=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build'; oldwork=oldbuild/'clang-bolt'
spec=importlib.util.spec_from_file_location('h',S/'packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
X.mkdir(exist_ok=False);build=X/'source/build';work=build/'clang-bolt';work.mkdir(parents=True)
(build/'bin').mkdir()
rows=[]
def cp(a,b):
 b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b);shutil.copymode(a,b)
 rows.append(dict(source=str(a),copy=str(b),bytes=b.stat().st_size,sha256=h.digest(b),source_sha256=h.digest(a)))
 assert rows[-1]['sha256']==rows[-1]['source_sha256']
for n in ['clang.bolt','ordinary-clang-22','clang-22.debug','installed-baseline.json']:cp(oldwork/n,work/n)
cp(oldbuild.parent/'debugfiles.list',build.parent/'debugfiles.list')
for n in ['llvm-strip','llvm-objcopy']:(build/'bin'/n).symlink_to(oldbuild/'bin'/n)
for rel in h.REAL_C_SOURCES+h.REAL_CXX_SOURCES:cp(oldbuild.parent/rel,build.parent/rel)
shutil.copytree(oldbuild.parent/'llvm/include',build.parent/'llvm/include',symlinks=True)
shutil.copytree(oldbuild/'include',build/'include',symlinks=True)
(E/'real-gates-copies.json').write_text(json.dumps(rows,indent=2)+'\n')
loader=R/'usr/lib64/ld-linux-x86-64.so.2'
assert loader.is_file()
library=':'.join(str(p) for p in [R/'usr/lib64',R/'lib64',oldbuild/'lib64'])
prefix=[str(loader),'--library-path',library]
real_call=h.call
calls=[]
def call(argv,*a,**kw):
 argv=list(map(str,argv));original=argv[:]
 p=Path(argv[0])
 if p.is_file():
  with p.open('rb') as f:elf=f.read(4)==b'\x7fELF'
  if elf:argv=prefix+argv
 calls.append({'requested':original,'executed':argv})
 return real_call(argv,*a,**kw)
h.call=call
os.environ['PATH']=str(W/'temp/review-20261103/host-tools')+':'+os.environ['PATH']
candidate=work/'clang.candidate';cp(work/'clang.bolt',candidate)
call([build/'bin/llvm-strip','--strip-all',candidate],work/'strip.log',timeout=600)
strip=h.verify_strip_layout(work/'clang.bolt',candidate)
oldid=json.loads((oldwork/'identity.json').read_text())
assert h.digest(candidate)==oldid['strip_all_sha256']
identity={k:copy.deepcopy(oldid[k]) for k in ['before_sha256','bolt_note_before','bolt_sections_before']}
identity.update(before_path=str(work/'clang.bolt'),after_path=str(candidate),after_sha256=h.digest(candidate))
identity=h.adjust_rpath(candidate,work/'installed-baseline.json',work,identity)
assert h.digest(candidate)==oldid['rpath_adjusted_sha256']
before=h.debuglink_layout(candidate)
di=copy.deepcopy(oldid['debug_file']);di['path']=str(work/'clang-22.debug')
identity=h.add_debuglink(build,work,identity,di)
assert h.digest(candidate)==oldid['after_sha256']
assert before==h.debuglink_layout(candidate)
elf=h.ELF(candidate)
sections=[(s[4],s[4]+s[5]) for s in elf.sections if s[1]!=8 and s[5]]
occupied=sections+[(0,64),(elf.header[5],elf.header[5]+elf.header[9]*elf.header[10])] if hasattr(elf,'header') else sections+[(0,64)]
# Parse the ELF64 header directly so program-header bytes are never chosen as padding.
with candidate.open('rb') as f:eh=f.read(64)
po=struct.unpack_from('<Q',eh,32)[0];pe,pn=struct.unpack_from('<HH',eh,54)
occupied=sections+[(0,64),(po,po+pe*pn)]
gap=None
for load in elf.loads:
 for off in range(load[2]+64,min(load[2]+load[5],load[2]+1000000)):
  if not any(a<=off<b for a,b in occupied):gap=off;break
 if gap is not None:break
text=elf.sections[elf.names.index('.text')][4];elf.close()
assert gap is not None
neg=[]
for name,off in [('e_entry',24),('e_flags',48),('LOAD_padding',gap),('text',text)]:
 p=X/('bad-'+name);cp(candidate,p)
 with p.open('r+b') as f:f.seek(off);v=f.read(1);f.seek(off);f.write(bytes([v[0]^1]))
 try:h.require(h.debuglink_layout(p)==before,'debuglink changed program headers or ELF content/layout')
 except h.GateError as ex:neg.append(dict(case=name,offset=off,rejected=True,error=str(ex)))
 else:raise AssertionError(name+' accepted')
(E/'debuglink-real-cases.json').write_text(json.dumps({'positive':True,'negative':neg},indent=2)+'\n')
root=X/'installed';entity=root/'usr/bin/clang-22';cp(candidate,entity)
debug=root/h.DEBUG_INSTALL_PATH;cp(work/'clang-22.debug',debug);debug.chmod(0o644)
state=json.loads((oldwork/'install-state.json').read_text());state['identity']=identity;state['installed_sha256']=h.digest(entity)
for row in state['alias_changes']:
 p=root/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to('clang-22')
retained=X/'retained';retained.mkdir()
seq=0;real_unlink=Path.unlink;real_copy=shutil.copyfile
def keep(p):
 global seq
 p=Path(p)
 if p.exists() or p.is_symlink():
  assert p.is_relative_to(X),p
  seq+=1;p.rename(retained/(str(seq)+'-'+p.name))
def unlink(p,missing_ok=False):
 if not p.exists() and not p.is_symlink():
  if missing_ok:return
  raise FileNotFoundError(p)
 keep(p)
def preserving_copy(a,b,*args,**kw):
 if Path(b).exists():keep(b)
 return real_copy(a,b,*args,**kw)
Path.unlink=unlink;shutil.copyfile=preserving_copy
post=h.post_gate(root,state,str(work/'ordinary-clang-22'),str(X/'post'),str(oldbuild/'lib64/clang/22'))
(E/'real-post-result.json').write_text(json.dumps(post,indent=2)+'\n')
(E/'real-gates-calls.json').write_text(json.dumps(calls,indent=2)+'\n')
summary={'strip':True,'RUNPATH':True,'debuglink':True,'post':True,'negative_cases':neg,'strip_sha':identity['strip_all_sha256'],'RUNPATH_sha':identity['rpath_adjusted_sha256'],'final_sha':identity['after_sha256'],'equals_retained_candidate':h.digest(candidate)==h.digest(oldwork/'clang.candidate'),'real_cases':len(post['real']['cases']),'tiny_cases':len(post['tiny'])}
(E/'real-gates-result.json').write_text(json.dumps(summary,indent=2)+'\n')
print('REAL_GATES_PASS '+json.dumps(summary))
