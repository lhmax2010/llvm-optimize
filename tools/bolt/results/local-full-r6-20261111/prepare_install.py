from pathlib import Path,PurePosixPath
import sys,json,os,shutil,stat,hashlib,subprocess,re,posixpath
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).parent/'install';E.mkdir(exist_ok=False);C=W/'temp/local-full-r6-20261111-install/root';R=W/'temp/rebase-359934-20261111-r6/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
identities=json.loads((Path(__file__).parent/'toolchain/comparison/rpm-identities.json').read_text())
P={k:Path(v['local']['path']) for k,v in identities.items() if 'local' in v}
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261105'));from rpm_io import manifest
from rpm_extract import extract_selected
assert json.loads((R.parents[3]/'evidence/build-result.json').read_text())['exit_code']==0
assert not C.exists();C.mkdir(parents=True);rows=[]
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def resolve(root,rel):
 todo=list(PurePosixPath(rel).parts);parts=[];n=0
 while todo:
  a=todo.pop(0)
  if a in ('/','','.'):continue
  if a=='..':
   if parts:parts.pop()
   continue
  p=root.joinpath(*parts,a)
  if p.is_symlink():
   n+=1;assert n<40;v=os.readlink(p)
   if v.startswith('/'):parts=[]
   todo=list(PurePosixPath(v).parts)+todo
  else:parts.append(a)
 return root.joinpath(*parts)
def copy(rel):
 rel=rel.lstrip('/');src=R/rel;dest=C/rel
 if dest.exists() or dest.is_symlink():return
 dest.parent.mkdir(parents=True,exist_ok=True)
 if src.is_symlink():
  v=os.readlink(src);dest.symlink_to(v);rows.append(dict(path=rel,source=str(src),symlink=v));nextrel=posixpath.normpath(v if v.startswith('/') else '/'+posixpath.dirname(rel)+'/'+v);copy(nextrel)
 elif src.is_file():
  shutil.copy2(src,dest);rows.append(dict(path=rel,source=str(src),bytes=src.stat().st_size,sha256=sha(src),copy_sha256=sha(dest)));assert rows[-1]['sha256']==rows[-1]['copy_sha256']
 else:raise AssertionError(('missing fixed-snapshot source',src))
# Packaged platform LLDB, symbolizer and libLLVM from the same QB run, in fresh C.
for name in ['libllvm','llvm','lldb']:
 rpm=P[name];m=manifest(rpm);rpmsha=sha(rpm);names={k for k,v in m.items() if stat.S_ISREG(v['mode'])};extract_selected(rpm,names,C)
 for k,v in m.items():
  p=C/k
  if stat.S_ISREG(v['mode']):p.chmod(v['mode']&0o777);rows.append(dict(path=k,source_rpm=str(rpm),rpm_sha256=rpmsha,bytes=p.stat().st_size,sha256=sha(p)))
  elif stat.S_ISDIR(v['mode']):p.mkdir(parents=True,exist_ok=True)
  elif stat.S_ISLNK(v['mode']):
   p.parent.mkdir(parents=True,exist_ok=True)
   if not p.is_symlink():p.symlink_to(v['target'])
   rows.append(dict(path=k,source_rpm=str(rpm),symlink=v['target']))
(C/'usr/bin/lldb-server').symlink_to('/home/owner/share/tmp/sdk_tools/lldb/bin/lldb-server')
rows.append(dict(path='usr/bin/lldb-server',symlink='/home/owner/share/tmp/sdk_tools/lldb/bin/lldb-server',purpose='test-only alias to locally built packaged platform server'))
for rel in ['/usr/bin/rpm','/usr/bin/rpmdb','/usr/bin/rpmkeys','/usr/bin/rpmsign','/usr/bin/rpmspec','/sbin/ldconfig','/bin/sh','/bin/mount','/bin/umount','/usr/bin/env','/usr/bin/sha256sum']:copy(rel)
for rel in ['/etc/passwd','/etc/group','/etc/nsswitch.conf','/etc/hosts','/etc/ld.so.conf']:
 if (R/rel.lstrip('/')).is_file():copy(rel)
for sub in ['usr/lib/rpm','etc/rpm']:
 if (R/sub).exists():
  for p in (R/sub).rglob('*'):
   if p.is_file() or p.is_symlink():copy(str(p.relative_to(R)))
for sub in ['usr/lib/python3.14','usr/lib64/python3.14']:
 if (R/sub).exists():
  for p in (R/sub).rglob('*'):
   if p.is_file() or p.is_symlink():copy(str(p.relative_to(R)))
# RPM payload used for preflight; clang is installed by rpm later, not copied to C.
clang=P['clang'];extract_selected(clang,{'usr/bin/clang-22'},C.parent/'rpm-probe');probe=C.parent/'rpm-probe/usr/bin/clang-22';probe.chmod(0o755)
programs=['/usr/bin/rpm','/usr/bin/rpmdb','/usr/bin/rpmkeys','/usr/bin/rpmsign','/usr/bin/rpmspec','/sbin/ldconfig','/bin/sh','/bin/mount','/bin/umount','/usr/bin/env','/usr/bin/sha256sum','/usr/bin/lldb','/usr/bin/lldb-server','/usr/bin/llvm-symbolizer','/usr/bin/clang-22']
seen=set();deps=[]
def visit(rel,physical=None):
 rel=posixpath.normpath(rel)
 if rel in seen:return
 seen.add(rel);p=physical or resolve(C,rel)
 if not p.exists():copy(rel);p=resolve(C,rel)
 assert p.is_file(),p
 if p.open('rb').read(4)!=b'\x7fELF':
  line=p.open('rb').readline().decode(errors='replace');assert line.startswith('#!'),(p,'not ELF or script');visit(line[2:].strip().split()[0]);return
 t=subprocess.check_output(['readelf','-W','-l','-d',str(p)],text=True,stderr=subprocess.STDOUT);interp=re.search(r'Requesting program interpreter: (.*?)\]',t);needed=re.findall(r'\(NEEDED\).*?\[(.*?)\]',t);origin=posixpath.dirname('/'+str(p.relative_to(C))) if physical is None else posixpath.dirname(rel);search=[]
 for tags in re.findall(r'\((?:RUNPATH|RPATH)\).*?\[(.*?)\]',t):search +=[x.replace('${ORIGIN}',origin).replace('$ORIGIN',origin) for x in tags.split(':')]
 search += ['/lib64','/usr/lib64','/lib','/usr/lib'];record=dict(program=rel,physical=str(p),needed=needed,resolved=[]);deps.append(record)
 if interp:visit(interp[1])
 for lib in needed:
  choices=[posixpath.normpath(d+'/'+lib) for d in search];chosen=next((v for v in choices if resolve(C,v).is_file()),None)
  if chosen is None:chosen=next((v for v in choices if resolve(R,v).is_file()),None);assert chosen,(rel,lib);copy(chosen)
  record['resolved'].append(dict(library=lib,path=chosen));visit(chosen)
for p in programs:visit(p,probe if p=='/usr/bin/clang-22' else None)
# Every rpmpopt exec target is included, including programs not used by installation.
import shlex
execs=[]
for p in C.rglob('rpmpopt*'):
 if not p.is_file():continue
 for i,line in enumerate(p.read_text().splitlines(),1):
  if not re.match(r'^\s*\S+\s+exec\s+',line):continue
  a=shlex.split(line,comments=True)
  if len(a)>=4 and a[1]=='exec':
   x=a[3];rel=x if x.startswith('/') else next(v for v in ['/usr/bin/'+x,'/bin/'+x,'/usr/sbin/'+x,'/sbin/'+x] if resolve(C,v).is_file() or resolve(R,v).is_file());visit(rel);execs.append(dict(file=str(p.relative_to(C)),line=i,text=line,target=rel))
for sub in ['dev','proc','tmp','var/lib/rpm','var/cache/ldconfig','rpms','probe/install-r6','opt/symbolizer']: (C/sub).mkdir(parents=True,exist_ok=True)
(C/'opt/symbolizer/llvm-symbolizer').symlink_to('/usr/bin/llvm-symbolizer')
for n in ['clang','clang-debuginfo']:
 p=P[n];shutil.copy2(p,C/'rpms'/p.name);rows.append(dict(path='rpms/'+p.name,source=str(p),sha256=sha(p),copy_sha256=sha(C/'rpms'/p.name)))
old=W/'temp/debuglink-20261028/full-20261030/install-test-root/probe/install-20261102'
for n in ['crash.c','probe.lldb']:
 s=(old/n).read_text().replace('/probe/install-20261102/','/probe/install-r6/');(C/'probe/install-r6'/n).write_text(s)
shutil.copyfile(B/'tools/bolt/results/debuglink-20261028/install-test-20261102-resume3/symbol-samples.json',E/'symbol-samples.json')
(E/'copied-files.json').write_text(json.dumps(rows,indent=2)+'\n');(E/'dependency-preflight.json').write_text(json.dumps(dict(PASS=True,programs=programs,closure=deps,rpmpopt=execs,snapshot='20261030.061318',isolation='rootless bwrap user/PID/mount namespaces; no sudo',source_root=str(R)),indent=2)+'\n');print('INSTALL_PREPARATION_PASS',len(rows),len(deps),'execs',len(execs))
