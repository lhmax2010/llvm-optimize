from pathlib import Path
import json,hashlib,urllib.request,subprocess,gzip,datetime,traceback
from rpm_io import manifest
E=Path(__file__).resolve().parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
X=W/'temp/qb-1226850-1226851'
O=E.parent/'qb-1225393-1225395'
plan=json.loads((E/'rpm-plan.json').read_text())
oldrecords=[json.loads(p.read_text()) for p in (O/'downloads').glob('*/*/*.json')]
oldmap={(r['build'],r['arch'],r['name']):r for r in oldrecords}
mapping={'1226850':'1225393','1226851':'1225395'}
oldplan=json.loads((O/'rpm-plan.json').read_text())
for bid,oldid in mapping.items():
 for arch in ('x86_64','armv7l','aarch64'):
  names={r['name'] for r in plan if r['build']==bid and r['arch']==arch}
  previous={r['name'] for r in oldplan if r['build']==oldid and r['arch']==arch}
  assert names==previous,('RPM list differs',bid,arch,sorted(names-previous),sorted(previous-names))
def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def now():return datetime.datetime.now().astimezone().isoformat()
def fetch(row):
 p=Path(row['path']);p.parent.mkdir(parents=True,exist_ok=True)
 receipt=E/'downloads'/row['build']/row['arch']/(row['name']+'.json')
 if p.exists():
  digest=sha(p)
  expected=row.get('sha256')
  if receipt.exists():expected=json.loads(receipt.read_text())['sha256']
  assert expected and digest==expected,('existing file has no verified receipt or SHA differs',str(p))
 else:
  h=hashlib.sha256()
  with urllib.request.urlopen(row['url'],timeout=120) as src,p.open('xb') as out:
   while b:=src.read(1024*1024):out.write(b);h.update(b)
  digest=h.hexdigest()
 q=subprocess.run(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}\n',str(p)],capture_output=True,text=True)
 assert q.returncode==0,q.stderr
 rec={**row,'sha256':digest,'bytes':p.stat().st_size,'rpm_query':q.stdout,'rpm_stderr':q.stderr,'time':now()}
 save(receipt,rec)
 return rec
def getman(p,bid,arch,name):
 out=E/'manifests'/bid/arch/(name+'.json.gz');out.parent.mkdir(parents=True,exist_ok=True)
 m=manifest(p)
 with gzip.open(out,'wt') as f:json.dump(m,f,sort_keys=True)
 return m
results=[]
try:
 # Compare all binary packages first. Source RPMs are downloaded for the separate whitelist audit.
 for row in sorted(plan,key=lambda r:(r['name'].endswith('.src.rpm'),r['arch']!='x86_64',r['build'],r['arch'],r['name'])):
  oldid=mapping[row['build']]
  old=oldmap[(oldid,row['arch'],row['name'])]
  print('START',row['build'],row['arch'],row['name'],flush=True)
  a=fetch(old);b=fetch(row)
  assert '60fabc723f30c5cc04146a9dd83487ebed63f259' in a['rpm_query'],a
  assert 'fea0fe464d56e17f2c7588c557bfffd9f6ac352b' in b['rpm_query'],b
  assert a['rpm_query'].split('\t')[1]==b['rpm_query'].split('\t')[1]=='22.1.8'
  ma=getman(Path(a['path']),oldid,row['arch'],row['name']);mb=getman(Path(b['path']),row['build'],row['arch'],row['name'])
  added=sorted(mb.keys()-ma.keys());removed=sorted(ma.keys()-mb.keys())
  changes=[];times=[]
  for n in sorted(ma.keys()&mb.keys()):
   delta={k:[ma[n].get(k),mb[n].get(k)] for k in ma[n].keys()|mb[n].keys() if ma[n].get(k)!=mb[n].get(k)}
   if 'mtime' in delta:times.append({'file':n,'mtime':delta.pop('mtime')})
   if delta:changes.append({'file':n,'differences':delta})
  archives=[{'file':n,'old_sha256':ma[n]['sha256'],'new_sha256':mb[n]['sha256'],'equal':ma[n]['sha256']==mb[n]['sha256']} for n in ma.keys()&mb.keys() if n.endswith('.a')]
  source=row['name'].endswith('.src.rpm')
  result={'build':row['build'],'baseline':oldid,'arch':row['arch'],'name':row['name'],'old':a,'new':b,
    'file_count':len(mb),'added':added,'removed':removed,'changes':changes,'payload_mtime_differences':times,
    'archives':archives,'status':'SOURCE_AUDIT_PENDING' if source else ('PASS' if not(added or removed or changes) else 'FAIL')}
  results.append(result);save(E/'package-results.json',results)
  print('RESULT',result['status'],'files',len(mb),'changes',len(changes),'archives',len(archives),flush=True)
  if not source:
   assert result['status']=='PASS',result['changes'][:10]
   if row['arch']=='x86_64' and row['name'].startswith('llvm-static-devel-'):
    assert len(archives)==225 and all(x['equal'] for x in archives)
 print('PACKAGE_SCAN 已结束',now(),'status=ok',flush=True)
except BaseException:
 (E/'package-failure.txt').write_text(traceback.format_exc())
 print('PACKAGE_SCAN 已结束',now(),'status=failed',flush=True)
 raise
