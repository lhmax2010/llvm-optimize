import hashlib,json,time,datetime
from pathlib import Path
D=Path(__file__).resolve().parent
rows=[];seen={}
for x in json.loads((D/'asset-inputs.json').read_text()):
 p=Path(x['path']);r=dict(x)
 try:
  s=p.stat();key=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns);h=seen.get(key)
  if h is None:
   v=hashlib.sha256()
   with p.open('rb') as f:
    for b in iter(lambda:f.read(4*1024*1024),b''):v.update(b)
   h=v.hexdigest();seen[key]=h
  z=p.stat();assert (z.st_dev,z.st_ino,z.st_size,z.st_mtime_ns)==key,'file changed during read'
  r.update(bytes=s.st_size,allocated_bytes=s.st_blocks*512,sha256=h,nlink=s.st_nlink,device=s.st_dev,inode=s.st_ino,read_at=datetime.datetime.now().astimezone().isoformat())
 except (OSError,AssertionError) as ex:r['error']=str(ex)
 rows.append(r);print(x['role'],r.get('bytes'),r.get('sha256',r.get('error')),flush=True)
 (D/'preserve-assets.json').write_text(json.dumps(rows,indent=2)+'\n')
