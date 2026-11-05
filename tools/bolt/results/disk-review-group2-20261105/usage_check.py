from pathlib import Path
import os,json,datetime
E=Path(__file__).resolve().parent;W=Path('/home/linhao/Toolchain/development/llvm-optimize');N=json.loads((E/'targets.json').read_text());paths=[str(W/'temp'/n) for n in N];hits=[];blind=[]
for p in Path('/proc').glob('[0-9]*'):
 try:cmd=(p/'cmdline').read_bytes().replace(b'\0',b' ').decode(errors='replace')
 except OSError:cmd='UNKNOWN'
 try:fd=list((p/'fd').iterdir())
 except (PermissionError,OSError) as x:blind.append({'pid':p.name,'path':str(p/'fd'),'error':str(x)});fd=[]
 for q in [p/'cwd',p/'root',p/'exe']+fd:
  try:v=os.readlink(q)
  except PermissionError as x:blind.append({'pid':p.name,'path':str(q),'error':str(x)});continue
  except OSError:continue
  for n,t in zip(N,paths):
   if v==t or v.startswith(t+'/'):
    hits.append({'directory':n,'pid':p.name,'link':str(q),'target':v,'command':cmd,'own_audit':('disk-review-group2-20261105' in cmd or cmd.startswith('sha256sum -- ') or cmd.startswith('du -sx -B1'))})
(E/'usage.json').write_text(json.dumps({'time':datetime.datetime.now().astimezone().isoformat(),'hits':hits,'permission_blind_spots':blind},ensure_ascii=False,indent=2))
