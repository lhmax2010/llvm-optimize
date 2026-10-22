#!/usr/bin/env python3
"""Read-only filesystem inventory. No chmod, sudo, mount, build or deletion."""
import datetime,json,os,subprocess,time
from pathlib import Path
D=Path(__file__).resolve().parent
stamp=lambda:datetime.datetime.now().astimezone().isoformat()
def run(name,argv,timeout=1200):
 start=stamp();t=time.monotonic()
 with (D/(name+'.stdout')).open('w') as out,(D/(name+'.stderr')).open('w') as err:
  p=subprocess.run(argv,stdout=out,stderr=err,text=True,timeout=timeout)
 meta={'start':start,'end':stamp(),'argv':argv,'returncode':p.returncode,'elapsed_seconds':time.monotonic()-t}
 (D/(name+'.json')).write_text(json.dumps(meta,indent=2)+'\n')
 print(name,meta['returncode'],round(meta['elapsed_seconds'],3),flush=True)
 return meta
run('findmnt',['findmnt','-J','-o','TARGET,SOURCE,FSTYPE,OPTIONS'])
run('df-before',['df','-B1','-T'])
run('lslocks-before',['lslocks','-o','PID,COMMAND,TYPE,MODE,PATH'])
run('ps-before',['ps','-eo','pid,ppid,uid,lstart,stat,comm'])
(D/'mountinfo-before.txt').write_text(Path('/proc/self/mountinfo').read_text())
(D/'meminfo-before.txt').write_text(Path('/proc/meminfo').read_text())
# Enumerate separately mounted local disks; skip virtual filesystems, loop/snap images.
fs=json.loads((D/'findmnt.stdout').read_text())['filesystems'];flat=[]
def visit(items):
 for x in items:
  flat.append(x);visit(x.get('children',[]))
visit(fs)
local=[x for x in flat if x['fstype'] in {'ext2','ext3','ext4','xfs','btrfs','zfs','vfat','ntfs','ntfs3','exfat'} and not x['source'].startswith('/dev/loop')]
(D/'local-filesystems.json').write_text(json.dumps(local,indent=2)+'\n')
for i,x in enumerate(local):
 run('du-filesystem-'+str(i),['du','-x','-B1','--threshold=5368709121','--time','--time-style=full-iso','--',x['target']],3600)
run('df-after-discovery',['df','-B1','-T'])
