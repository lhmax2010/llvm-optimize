from pathlib import Path
import os,sys,json,subprocess,gzip,hashlib,stat,mmap,difflib,datetime,traceback
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize';E=Path(__file__).resolve().parent
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261105'))
from rpm_io import manifest
from rpm_extract import extract_selected
from compare_rules import file_proof,debuglink_name,debuglink_proof
def now():return datetime.datetime.now().astimezone().isoformat()
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def query(p):
 s=subprocess.check_output(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}\t%{BUILDTIME}\t%{BUILDHOST}',str(p)],text=True)
 x=s.split('\t');assert len(x)==7;return dict(zip(['name','version','release','arch','vcs','buildtime','buildhost'],x))
def members(p):
 out=[];names=b'';index=0
 with p.open('rb') as f,mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as mm:
  assert mm[:8]==b'!<arch>\n';at=8
  while at<len(mm):
   hd=mm[at:at+60];assert len(hd)==60 and hd[58:60]==bytes([96,10])
   size=int(hd[48:58]);start=at+60;end=start+size;assert end<=len(mm)
   raw=hd[:16].strip();name=raw.decode()
   if raw==b'//':names=mm[start:end]
   elif raw.startswith(b'/') and raw[1:].isdigit():
    no=int(raw[1:]);ne=names.find(b'/\n',no);assert ne>=no;name=names[no:ne].decode()
   elif raw.startswith(b'#1/'):
    nn=int(raw[3:]);name=mm[start:start+nn].rstrip(b'\0').decode();start+=nn
   elif raw not in (b'/',b'/SYM64/'):name=name.rstrip('/')
   h=hashlib.sha256()
   for pos in range(start,end,1024*1024):h.update(mm[pos:min(end,pos+1024*1024)])
   out.append(dict(index=index,name=name,bytes=end-start,sha256=h.hexdigest(),date=hd[16:28].decode().strip(),uid=hd[28:34].decode().strip(),gid=hd[34:40].decode().strip(),mode=hd[40:48].decode().strip()))
   index+=1;at=end+(size%2)
  assert at==len(mm)
 return out
project=sys.argv[1];bid={'toolchain':'1225393','basedev':'1225395'}[project]
D=W/'temp/rebase-359934-20261111-r6'/project
V=W/'temp/local-full-r6-20261111-compare'/project;V.mkdir(parents=True,exist_ok=False)
O=E/project/'comparison';O.mkdir(parents=True,exist_ok=False)
os.environ['DWARF_PROOF_DIR']=str(V/'dwarf-proofs')
summary=[];archiveresults=[]
try:
 local=list((D/'gbs-driver/local/repos').glob('**/*.rpm'))
 qb=[Path(r['path']) for r in json.loads((B/'tools/bolt/results/qb-1225393-1225395/rpm-plan.json').read_text()) if r['build']==bid and r['arch']=='x86_64']
 if not local:raise RuntimeError('NOT RUN: no local RPM products')
 maps={};meta={};paths={}
 for side,rr in [('local',local),('qb',qb)]:
  for p in sorted(rr):
   if side=='qb':
    receipt=json.loads((B/f'tools/bolt/results/qb-1225393-1225395/downloads/{bid}/x86_64'/(p.name+'.json')).read_text())
    assert sha(p)==receipt['sha256'],('QB receipt SHA mismatch',str(p))
   z=query(p);key=z['name']+('-src' if p.name.endswith('.src.rpm') else '')
   if z['arch'] not in ('x86_64','noarch','src') and not p.name.endswith('.src.rpm'):continue
   if key in paths and side in paths[key]:
    assert sha(paths[key][side])==sha(p),'duplicate different RPM '+key;continue
   paths.setdefault(key,{})[side]=p;meta.setdefault(key,{})[side]=z
   print('MANIFEST',project,side,key,flush=True)
   m=manifest(p);maps.setdefault(key,{})[side]=m
   with gzip.open(O/(key+'-'+side+'-manifest.json.gz'),'wt') as f:json.dump(m,f)
 save(O/'rpm-identities.json',{k:{s:dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size,metadata=meta[k][s]) for s,p in pp.items()} for k,pp in paths.items()})
 extracted={}
 def get(side,key,name):
  ident=(side,key,name)
  if ident in extracted:return extracted[ident]
  dest=V/'payload'/key/side
  if not dest.exists():
   a=maps[key][side];other=maps[key].get('qb' if side=='local' else 'local',{})
   selected={n for n,r in a.items() if stat.S_ISREG(r['mode']) and (n.endswith(('.a','.debug')) or n not in other or r['sha256']!=other[n]['sha256'])}
   selected.add(name);extract_selected(paths[key][side],selected,dest)
   for n in selected:
    p=dest/n;assert sha(p)==a[n]['sha256'],('extracted SHA mismatch',key,side,n)
    extracted[(side,key,n)]=p
  if ident not in extracted:
   dest=V/'extra'/key/side/hashlib.sha256(name.encode()).hexdigest()
   extract_selected(paths[key][side],{name},dest);p=dest/name;assert sha(p)==maps[key][side][name]['sha256'];extracted[ident]=p
  return extracted[ident]
 def symbol(side,n,dl):
  name=str(Path('usr/lib/debug')/Path(n).parent/dl);owners=[k for k,mm in maps.items() if name in mm.get(side,{})]
  assert owners,('missing matching debug RPM payload',side,name)
  assert len({maps[k][side][name]['sha256'] for k in owners})==1
  return get(side,owners[0],name)
 for key in sorted(paths):
  print('COMPARE',project,key,flush=True)
  if set(paths[key])!={'local','qb'}:
   rr=dict(package=key,status='FAIL',reason='missing package side',sides=list(paths[key]));summary.append(rr);save(O/'packages.json',summary);continue
  aa,bb=maps[key]['local'],maps[key]['qb'];source=key.endswith('-src');debugsource='debugsource' in key
  a_release=meta[key]['local']['release'];b_release=meta[key]['qb']['release'];version=meta[key]['local']['version']
  ap='usr/src/debug/llvm-'+version+'-'+a_release+'.x86_64';bp='usr/src/debug/llvm-'+version+'-'+b_release+'.x86_64'
  lookup={n.replace(ap,bp) if debugsource else n:n for n in aa};assert len(lookup)==len(aa)
  added=sorted(bb.keys()-lookup.keys());removed=sorted(lookup.keys()-bb.keys());changes=[];mtime=[]
  for normalized in sorted(lookup.keys()&bb.keys()):
   n=lookup[normalized];a,b=aa[n],bb[normalized]
   if a['mtime']!=b['mtime']:mtime.append(dict(path=n,local=a['mtime'],qb=b['mtime']))
   fields=[k for k in ('mode','uid','gid','target','bytes','sha256') if a.get(k)!=b.get(k)]
   if n.endswith('.a') and stat.S_ISREG(a['mode']):
    x,y=get('local',key,n),get('qb',key,normalized);am,bm=members(x),members(y);ardiff=[];dates=[]
    if len(am)!=len(bm):ardiff.append({'reason':'member count','local':len(am),'qb':len(bm)})
    for u,v in zip(am,bm):
     dd={f:[u[f],v[f]] for f in u if f!='date' and u[f]!=v[f]}
     if dd:ardiff.append({'index':u['index'],'name':u['name'],'differences':dd})
     if u['date']!=v['date']:dates.append({'index':u['index'],'name':u['name'],'local':u['date'],'qb':v['date']})
    archiveresults.append(dict(package=key,path=n,local_archive_sha256=a['sha256'],qb_archive_sha256=b['sha256'],local_members=am,qb_members=bm,differences=ardiff,date_differences=dates,content_members=sum(x['name'] not in ('/','//','/SYM64/') for x in am),PASS=not ardiff))
   if not fields:continue
   row=dict(path=n,qb_path=normalized,changed_fields=fields,local=a,qb=b)
   try:
    if source:
     known_mode=a['mode']&0o777==0o664 and b['mode']&0o777==0o644
     assert all(a.get(f)==b.get(f) for f in ('uid','gid','target')),'source owner/link changed'
     assert a['mode']==b['mode'] or known_mode,'unapproved source permission change'
     if a['sha256']==b['sha256']:row['classification']='known-source-permissions'
     elif Path(n).name in ('llvm.spec','clang-bolt-helper.py','llvm-static-archives-native.py'):
      x,y=get('local',key,n),get('qb',key,normalized)
      diff=''.join(difflib.unified_diff(x.read_text().splitlines(True),y.read_text().splitlines(True),fromfile='local/'+n,tofile='QB/'+normalized))
      dest=O/(key+'-'+Path(n).name+'.diff');dest.write_text(diff);row.update(classification='allowed-source-change',diff=str(dest))
     else:raise AssertionError('source content outside three-file/VCS whitelist')
    else:
     assert all(a.get(f)==b.get(f) for f in ('mode','uid','gid','target')),'payload mode/owner/link changed'
     x,y=get('local',key,n),get('qb',key,normalized);dl=debuglink_name(x)
     if dl:proof=debuglink_proof(x,y,symbol('local',n,dl),symbol('qb',normalized,debuglink_name(y)))
     else:proof=file_proof(x,y)
     row.update(proof)
   except MemoryError:raise
   except TimeoutError as ex:row.update(classification='UNKNOWN',error=str(ex))
   except Exception as ex:row.update(classification='FAIL',error=str(ex))
   changes.append(row);print('FILE',project,key,n,row['classification'],flush=True)
  rr=dict(package=key,status='PASS' if not added and not removed and all(x['classification'] not in ('FAIL','UNKNOWN') for x in changes) else 'FAIL',file_count=len(aa),added=added,removed=removed,content_changes=changes,payload_mtime_changes=mtime,release_path_mapping={'local':ap,'qb':bp} if debugsource else None,metadata=meta[key])
  summary.append(rr);save(O/'packages.json',summary)
  with gzip.open(O/'static-members.json.gz','wt') as f:json.dump(archiveresults,f)
  print('PACKAGE',project,key,rr['status'],flush=True)
 result=dict(status='ok' if all(x['status']=='PASS' for x in summary) and all(x['PASS'] for x in archiveresults) else 'differences',packages=len(summary),passed=sum(x['status']=='PASS' for x in summary),archives=len(archiveresults),archive_members=sum(x['content_members'] for x in archiveresults),archives_passed=sum(x['PASS'] for x in archiveresults))
 save(O/'result.json',result)
except BaseException as ex:
 (O/'failure.txt').write_text(traceback.format_exc());save(O/'result.json',dict(status='UNKNOWN' if isinstance(ex,MemoryError) else 'failed',reason=str(ex),completed_packages=len(summary)));raise
finally:
 line='COMPARE 已结束 '+now()+' project='+project+' result='+json.dumps(json.loads((O/'result.json').read_text()),ensure_ascii=False)
 (O/'end.txt').write_text(line+'\n');print(line,flush=True)
