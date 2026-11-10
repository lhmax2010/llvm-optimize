from pathlib import Path
import json,urllib.request,hashlib,subprocess,datetime
E=Path(__file__).resolve().parent
rows=json.loads((E/'rpm-plan.json').read_text())
done=[]
for r in rows:
 p=Path(r['path']);p.parent.mkdir(parents=True,exist_ok=True);h=hashlib.sha256()
 if p.exists(): raise RuntimeError('Refusing to overwrite unverified download '+str(p))
 with urllib.request.urlopen(r['url'],timeout=180) as response,p.open('xb') as f:
  for b in iter(lambda:response.read(1048576),b''):f.write(b);h.update(b)
 r.update(bytes=p.stat().st_size,sha256=h.hexdigest(),time=datetime.datetime.now().astimezone().isoformat())
 q=subprocess.run(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}\t%{SOURCERPM}\t%{BUILDTIME}\n',str(p)],text=True,capture_output=True);assert q.returncode==0,q.stderr
 r.update(query=q.stdout,query_stderr=q.stderr)
 assert 'fa4f9978c9162d3c6cd2113d0cfe1173f04881c8' in q.stdout,q.stdout
 done.append(r)
 (E/'rpm-downloads.json').write_text(json.dumps(done,indent=2)+'\n')
 print(r['build'],p.name,r['bytes'],r['sha256'],flush=True)
