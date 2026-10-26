from pathlib import Path
import os,json,subprocess,time
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=E.parents[3]
names=[p.name for p in (W/'temp').iterdir() if p.is_dir()]+[p.name for p in Path('/var/tmp').glob('*llvm*') if p.is_dir()]
refs={x:[] for x in names}
for repo in [W,B]:
 for p in (repo/'docs').rglob('*.md'):
  if p==B/'docs/bolt/38_temp_cleanup_inventory.md':continue
  try:lines=p.read_text(errors='replace').splitlines()
  except OSError:continue
  for i,line in enumerate(lines,1):
   for name in names:
    if name in line:refs[name].append(dict(repo='main' if repo==W else 'bolt-v4',file=str(p.relative_to(repo)),line=i,text=line))
(E/'doc-references.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n')
mounts={};errors=[];process=[]
for p in Path('/proc').glob('[0-9]*'):
 try:
  for line in (p/'mountinfo').read_text().splitlines():
   if str(W) in line or '/var/tmp/llvm' in line:mounts.setdefault(line,[]).append(int(p.name))
 except OSError as x:errors.append(dict(pid=int(p.name),item='mountinfo',error=str(x)))
 for item in ['cwd','root']:
  try:
   target=os.readlink(p/item)
   if str(W) in target or '/var/tmp/llvm' in target:process.append(dict(pid=int(p.name),item=item,path=target))
  except OSError:pass
(E/'proc-mount-references.json').write_text(json.dumps(dict(mounts=mounts,errors=errors,cwd_root=process),indent=2)+'\n')
lines=(E/'lsof.stdout').read_text(errors='replace').splitlines()
(E/'lsof-project.txt').write_text('\n'.join(x for x in lines if str(W) in x or '/var/tmp/llvm' in x)+'\n')
(E/'lsof-visibility.txt').write_text('\n'.join(x for x in lines if 'NOFD' in x)+'\n')
print('references',sum(map(len,refs.values())),'mounts',len(mounts),'mountinfo errors',len(errors))
