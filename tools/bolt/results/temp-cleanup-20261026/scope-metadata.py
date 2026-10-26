from pathlib import Path
import json,os,stat
E=Path(__file__).resolve().parent;p=json.loads((E/'scenarios.json').read_text());roots=sorted(set(r for fs in p.values() for v in fs.values() for r in v['paths']));rows=[]
for root in roots:
 row=dict(path=root,newest_file_ns=0,newest_file=None,files=0,root_owned_dirs=0,nonwritable_dirs=0,errors=[])
 for d,ds,fs in os.walk(root,followlinks=False,onerror=lambda e:row['errors'].append(str(e))):
  s=Path(d).stat();row['root_owned_dirs']+=s.st_uid==0;row['nonwritable_dirs']+=not os.access(d,os.W_OK|os.X_OK)
  for name in fs:
   q=Path(d)/name
   try:s=q.lstat()
   except OSError as e:row['errors'].append(str(e));continue
   if stat.S_ISREG(s.st_mode):
    row['files']+=1
    if s.st_mtime_ns>row['newest_file_ns']:row['newest_file_ns']=s.st_mtime_ns;row['newest_file']=str(q)
 rows.append(row);print(root,row['files'],flush=True)
(E/'scope-metadata.json').write_text(json.dumps(rows,indent=2)+'\n')
