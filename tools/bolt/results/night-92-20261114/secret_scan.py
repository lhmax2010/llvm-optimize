import datetime,hashlib,io,json,re,subprocess,tarfile
from pathlib import Path
E=Path(__file__).resolve().parent
commits=['8d1137fdc9f326fba0fbd7baf27b755bf95b928d','21dcb101f7c56e00db6e0404687b0c7df3e63216']
excludes={'tools/bolt/results/night-88-20261114/package_evidence.py','tools/bolt/results/night-88-20261114/package_evidence_v2.py',str(Path(__file__).relative_to(Path.cwd()))}
patterns=[('private_key_header',re.compile(r'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----')),('credential_assignment',re.compile(r'(?i)\b(?:password|passwd|token|access_token|api_key|http_password)\s*=\s*[^\s]+')),('authorization',re.compile(r'(?i)Authorization\s*:')),('ssh_path',re.compile(r'(?:~|/home/[^/\s]+|/root)/\.ssh(?:/|\b)')),('gerrit_http_password',re.compile(r'(?i)(?:gerrit.{0,30}http.{0,10}pass(?:word)?\s*[:=]|http.{0,10}pass(?:word)?.{0,30}gerrit)'))]
seen=set(); inventory=[];hits=[];excluded=[]
def scan(label,data,commit):
 sha=hashlib.sha256(data).hexdigest();inventory.append({'file':label,'commit':commit,'bytes':len(data),'sha256':sha})
 for n,line in enumerate(data.decode('utf-8','replace').splitlines(),1):
  matched=[name for name,p in patterns if p.search(line)]
  if matched:hits.append({'file':label,'commit':commit,'line':n,'rules':matched,'line_sha256':hashlib.sha256(line.encode()).hexdigest(),'content':'REDACTED: inspect original read-only Git blob at this line; no credential values copied'})
for commit in commits:
 paths=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','--diff-filter=AM','-r',commit,'-z']).decode().split('\0')
 for path in filter(None,paths):
  oid=subprocess.check_output(['git','rev-parse',commit+':'+path],text=True).strip()
  if (path,oid) in seen:continue
  seen.add((path,oid));data=subprocess.check_output(['git','show',commit+':'+path])
  if path in excludes:excluded.append({'file':path,'commit':commit,'blob':oid,'sha256':hashlib.sha256(data).hexdigest(),'reason':'PM explicitly excludes scanner implementation from hit verdict; signature literals are intentional'});continue
  if path.endswith('.tar.gz'):
   inventory.append({'file':path,'commit':commit,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'scan':'decompressed regular-file members below; no extraction to filesystem'})
   with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tf:
    for member in tf:
     if member.isfile():scan(path+'!'+member.name,tf.extractfile(member).read(),commit)
     elif member.issym() or member.islnk():scan(path+'!'+member.name+'[link]',member.linkname.encode(),commit)
  else:scan(path,data,commit)
excluded.append({'file':str(Path(__file__).relative_to(Path.cwd())),'reason':'new scan script not in the two target commits; explicitly registered, excluded'})
result={'commits':commits,'status':'STOP' if hits else 'PASS','files_scanned_including_tar_members':len(inventory),'hits':hits,'hit_count':len(hits),'exclusions':excluded,'time':datetime.datetime.now().astimezone().isoformat(),'rule':'No quoted-signature/documentation exemption. Every match outside explicitly excluded scripts is reported; a match is not proof of a live secret.'}
(E/'secret-scan-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n');(E/'secret-scan-result.json').write_text(json.dumps(result,indent=2)+'\n')
print('STOP: secret-scan pattern matches outside the explicitly excluded scripts; no history rewritten.' if hits else 'PASS: no matches')
for hit in hits:print(hit['commit'][:8],hit['file']+':'+str(hit['line']),','.join(hit['rules']))
print('92步骤2 已结束',result['time'],'status='+result['status'])
