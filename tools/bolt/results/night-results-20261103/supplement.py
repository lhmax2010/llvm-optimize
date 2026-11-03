from pathlib import Path
import json,subprocess,hashlib,os,datetime
E=Path(__file__).parent;B=E.parents[3];W=Path('/home/linhao/Toolchain/development/llvm-optimize');N=W/'temp/night-20261103'
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for name in ('toolchain','basedev'):
 D=N/name;WORK=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt';O=E/name
 for src,target in [(WORK/'rewrite/bolt.log',O/'bolt-rewrite.log'),(WORK/'tool-build.txt',O/'tool-build.txt')]:
  if src.exists():target.write_bytes(src.read_bytes())
 raw=(WORK/'rewrite/bolt.log').read_text();(O/'profile-log-excerpts.txt').write_text('\n'.join(f'L{i}: {l}' for i,l in enumerate(raw.splitlines(),1) if any(x in l.lower() for x in ('profile','stale','unmatched','functions')))+'\n')
 p=WORK.parent.parent/'debugfiles.list'
 if p.exists():(O/'debugfiles.list').write_bytes(p.read_bytes())
 log=next((D/'gbs-driver/local/repos').glob('*/x86_64/logs/success/*/log.txt'));extra=[]
 for i,l in enumerate(log.open(errors='replace'),1):
  if any(x in l for x in ('BOLT_NINJA_EXIT_0','BOLT_TOOL_DRY_RUN','rm -rf /usr/lib/debug','rm -rf /home/abuild/rpmbuild/BUILDROOT')):extra.append(f'L{i}: {l.rstrip()}')
 (O/'extra-anchors.txt').write_text('\n'.join(extra)+'\n')
 for f in ('controller.stdout','controller.stderr'):
  if (D/f).exists():(O/f).write_bytes((D/f).read_bytes())
for f in ('night-result.json','night-progress.json'):
 if (N/f).exists():(E/f).write_bytes((N/f).read_bytes())
# Exact launcher source excerpt, not a changed launcher.
T=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt/tools/bolt/night-launch-20261103')
for name,lo,hi in [('launcher.py',90,120),('validate.py',94,108),('resource_report.py',20,33),('night.py',31,42)]:
 text=(T/name).read_text().splitlines();(E/(name+'.excerpt.txt')).write_text('\n'.join(f'{i+1}: {s}' for i,s in enumerate(text) if lo<=i+1<=hi)+'\n')
# Read-only metadata diff; not payload content verification.
t=json.loads((E/'toolchain/rpm-inventory.json').read_text());d=json.loads((E/'basedev/rpm-inventory.json').read_text())
def key(r):return r['query'].split('\t')[0]+(' [src]' if r['path'].endswith('.src.rpm') else '')
a={key(r):r for r in t};b={key(r):r for r in d};changes={}
for k in a.keys()&b.keys():
 onlyt=sorted(set(a[k]['files'])-set(b[k]['files']));onlyd=sorted(set(b[k]['files'])-set(a[k]['files']))
 if onlyt or onlyd:changes[k]={'only_T':onlyt,'only_D':onlyd}
save(E/'rpm-list-differences.json',dict(only_T=sorted(a.keys()-b.keys()),only_D=sorted(b.keys()-a.keys()),common_package_path_differences=changes,method='rpm -qp and rpm -qpl only; file payload bytes not compared'))
rows=[];denied=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:
  cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace');comm=(p/'comm').read_text().strip()
  paths={}
  for link in ('cwd','root'):
   try:paths[link]=os.readlink(p/link)
   except (PermissionError,FileNotFoundError,ProcessLookupError):pass
  if any(v.startswith(str(N)) for v in paths.values()) or comm in ('rpmbuild','gbs','ninja','cmake'):rows.append(dict(pid=int(p.name),comm=comm,cmd=cmd,paths=paths))
 except PermissionError:denied.append(p.name)
 except (FileNotFoundError,ProcessLookupError):pass
save(E/'processes-final.json',dict(time=datetime.datetime.now().astimezone().isoformat(),matches=rows,cmdline_permission_denied=denied,scope='readable /proc, cwd/root links may be inaccessible'))
print((E/'basedev/profile-log-excerpts.txt').read_text());print(json.dumps(json.loads((E/'rpm-list-differences.json').read_text()),ensure_ascii=False)[:1500])
