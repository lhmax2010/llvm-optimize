from pathlib import Path
import subprocess,json,time,os,datetime
E=Path(__file__).parent;T=Path('/home/linhao/Toolchain/development/llvm-optimize/temp')
def stamp():return datetime.datetime.now().astimezone().isoformat()
def run(name,args,limit=45):
 start=time.monotonic()
 try:
  p=subprocess.run(args,capture_output=True,text=True,timeout=limit);rc=p.returncode;out=p.stdout;err=p.stderr
 except subprocess.TimeoutExpired as x:
  rc=124;out=(x.stdout or b'').decode(errors='replace') if isinstance(x.stdout,bytes) else x.stdout or '';err=(x.stderr or b'').decode(errors='replace') if isinstance(x.stderr,bytes) else x.stderr or ''
 (E/(name+'.stdout')).write_text(out);(E/(name+'.stderr')).write_text(err)
 return dict(argv=args,rc=rc,seconds=time.monotonic()-start,stdout=out,stderr=err,time=stamp())
def save(name,v): (E/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
save('df-before.json',run('df-before',['df','-B1','/home']))
save('mounts.json',run('mounts',['findmnt','-rn','-o','TARGET,SOURCE,FSTYPE,OPTIONS']))
save('processes.json',run('processes',['ps','-eo','pid,ppid,stat,etime,comm,args']))
rows=[]
for i,p in enumerate(sorted(T.iterdir())):
 if not p.is_dir() or p.is_symlink():continue
 r=run('du-%03d'%i,['nice','-n','19','ionice','-c3','du','-sx','-B1',str(p)],30)
 n=int(r['stdout'].split()[0]) if r['rc']!=124 and r['stdout'].strip() else None
 row=dict(path=str(p),bytes=n,size_status='UNKNOWN' if n is None else 'lower-bound' if r['rc'] else 'OK',mtime=datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(),du=r)
 rows.append(row);save('units.json',rows)
 if n is None or n>5*2**30:print(p.name, n, row['size_status'],flush=True)
save('df-after-scan.json',run('df-after-scan',['df','-B1','/home']))
print('SCAN FINISHED',stamp(),len(rows),'directories',flush=True)
