from pathlib import Path
import json,hashlib,time
E=Path(__file__).resolve().parent
rows=json.loads((E/'asset-hashes.json').read_text());found=json.loads((E/'assets-found.json').read_text());known={r['path']:r for r in rows};cache={(r['dev'],r['ino'],r['bytes'],r['mtime_ns']):r['sha256'] for r in rows if 'sha256' in r};extra=[];read=0
for a in found:
 raw=a['path'];p=Path(raw);key=(a['dev'],a['ino'],a['bytes'],a['mtime_ns'])
 if raw in known:continue
 needed=raw.endswith('.rpm') and any(k in raw for k in ['/rpmbuild/RPMS/','/rpmbuild/SRPMS/','/rpms-docs35/','/products/','-products/'])
 if not needed and key not in cache:continue
 row=dict(a,reason='all generated/preserved RPMs; or inode identity with hashed asset')
 try:
  s=p.stat()
  if key not in cache:
   with p.open('rb') as f:cache[key]=hashlib.file_digest(f,'sha256').hexdigest()
   read+=s.st_size
  row['sha256']=cache[key];row['stable_during_read']=p.stat().st_mtime_ns==a['mtime_ns'] and p.stat().st_size==a['bytes']
 except OSError as x:row['error']=str(x)
 extra.append(row)
 if len(extra)%20==0:print(len(extra),'read GiB',round(read/2**30,2),flush=True)
(E/'asset-hashes-supplement.json').write_text(json.dumps(extra,indent=2)+'\n');(E/'hash-supplement-complete.json').write_text(json.dumps(dict(files=len(extra),bytes_read=read,time=time.time()))+'\n')
