from pathlib import Path
import json,subprocess,time
E=Path(__file__).resolve().parent
units=json.loads((E/'units.json').read_text());special=json.loads((E/'special-directories.json').read_text());rows=[];paths=set()
for u in units:
 if u['group']!='W' and u['bytes'] and u['bytes']>5*1024**3:
  for p in Path(u['path']).iterdir():
   if p.is_dir() and not p.is_symlink():paths.add(str(p))
for u in special:
 p=u['path']
 if u['name']=='lto.cache' or p.endswith('/rpmbuild/BUILD/llvm-22.1.8/build') or (u['name'] in ['RPMS','SRPMS','BUILDROOT'] and '/rpmbuild/' in p):paths.add(p)
paths.add('/home/linhao/Toolchain/development/llvm-optimize')
for i,p in enumerate(sorted(paths)):
 start=time.time();r=subprocess.run(['du','-sx','-B1','--',p],text=True,capture_output=True);parts=r.stdout.split('\t',1)
 row=dict(path=p,bytes=int(parts[0]) if parts[0].isdigit() else None,rc=r.returncode,stdout=r.stdout,stderr=r.stderr,seconds=time.time()-start)
 rows.append(row);(E/'subunits.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(i,p,row['bytes'],flush=True)
(E/'subunits-complete.json').write_text(json.dumps(dict(paths=len(rows),time=time.time()))+'\n')
