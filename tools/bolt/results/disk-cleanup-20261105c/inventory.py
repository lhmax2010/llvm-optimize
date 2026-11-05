from pathlib import Path
import os,json,subprocess,time,stat
from checks import command,identity,mount_snapshot,process_snapshot,user_services,stamp
E=Path(__file__).resolve().parent;R=Path('/home/linhao/qb_analysis')
def save(n,o):(E/n).write_text(json.dumps(o,ensure_ascii=False,indent=2))
a={'time':stamp(),'identity':identity(str(R)),'top':[]}
for p in sorted(R.iterdir()):
 s=p.lstat();a['top'].append({'name':p.name,'mode':stat.filemode(s.st_mode),'bytes':s.st_size})
a['du']=command(['timeout','180','nice','-n','19','ionice','-c3','du','-sx','-B1','--',str(R)],190);save('inventory.json',a)
save('df-before.json',command(['df','-B1','/home']));save('mounts-user.json',mount_snapshot([str(R)]));save('processes-user.json',process_snapshot([str(R)]));save('services-user.json',user_services())
repos=[];errors=[]
for base,ds,fs in os.walk(R,followlinks=False,onerror=lambda e:errors.append(str(e))):
 if '.git' in ds or '.git' in fs:repos.append(base)
 if 'HEAD' in fs and 'objects' in ds and 'refs' in ds:repos.append(base);ds[:]=[];continue
 ds[:]=[d for d in ds if d not in ('.git','proc','sys','dev')]
rows=[]
for p in repos:
 args=['git','--no-optional-locks','-c','safe.directory='+p,'-C',p]
 row={'path':p,'head':command(args+['rev-parse','--verify','HEAD'],20),'unpublished_remote_tracking':command(args+['rev-list','--count','HEAD','--branches','--tags','--not','--remotes'],30)}
 row['interpretation']='local remote-tracking refs only; missing/stale remote refs do not prove unpublished on server'
 rows.append(row);save('repositories.json',{'rows':rows,'walk_errors':errors})
print('inventory complete',len(rows),'repositories',flush=True)
