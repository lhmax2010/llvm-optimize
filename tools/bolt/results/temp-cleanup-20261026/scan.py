from pathlib import Path
import subprocess,json,time,os,datetime
E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
def run(name,argv,timeout=None):
 t=time.time();r=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
 (E/(name+'.stdout')).write_bytes(r.stdout);(E/(name+'.stderr')).write_bytes(r.stderr)
 return dict(name=name,argv=argv,rc=r.returncode,seconds=time.time()-t,time=datetime.datetime.now().astimezone().isoformat())
records=[];units=[]
for name,argv in [('df',['df','-B1','/home','/var/tmp']),('findmnt',['findmnt','-J','-o','TARGET,SOURCE,FSTYPE,OPTIONS']),('ps',['ps','-eo','pid,ppid,user,stat,pcpu,comm,args']),('lslocks',['lslocks','--json']),('lsof',['lsof','-nP'])]:
 records.append(run(name,argv));print(name,'done',flush=True)
paths=[('W',p) for p in W.iterdir() if p.is_dir() and not p.is_symlink()]
paths += [('temp',p) for p in (W/'temp').iterdir() if p.is_dir() and not p.is_symlink()]
paths += [('var-tmp',p) for p in Path('/var/tmp').iterdir() if p.is_dir() and ('llvm' in p.name or 'gbs' in p.name or 'hybrid' in p.name or 'bolt' in p.name)]
for i,(group,p) in enumerate(paths):
 name=f'du-{i:03d}';r=run(name,['du','-sx','-B1','--time','--time-style=full-iso','--',str(p)]);records.append(r)
 text=(E/(name+'.stdout')).read_text();parts=text.rstrip().split('\t',2)
 u=dict(path=str(p),group=group,evidence=name,bytes=int(parts[0]) if parts and parts[0].isdigit() else None,du_time=parts[1] if len(parts)>1 else None,rc=r['rc'])
 units.append(u);(E/'units.json').write_text(json.dumps(units,indent=2)+'\n');(E/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
 print(group,p.name,u['bytes'],r['rc'],flush=True)
for i,u in enumerate(units):
 if u['bytes'] and u['bytes']>50*1024**3 and u['group']!='W':
  records.append(run('expand-'+str(i),['du','-x','-B1','--max-depth=1','--time','--time-style=full-iso','--',u['path']]))
(E/'commands.json').write_text(json.dumps(records,indent=2)+'\n');(E/'scan-complete.json').write_text(json.dumps(dict(time=datetime.datetime.now().astimezone().isoformat(),units=len(units)))+'\n')
