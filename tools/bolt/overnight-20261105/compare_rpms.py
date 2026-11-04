"""QB/local comparison. Only new scratch/output writes; reuse verified BUILDROOT files."""
from pathlib import Path
import sys,json,subprocess,stat,hashlib,datetime,traceback,tarfile,difflib
from compare_rules import file_proof,debuglink_name,debuglink_proof
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize'
sys.path.append(str(B/'tools/bolt/night-launch-20261103'))
from rpm_io import manifest
from rpm_extract import extract_selected
E=B/'tools/bolt/results/baseline-attribution-20261105';P=W/'temp/qb-full-compare-20261105';P.mkdir(exist_ok=False)
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def source_archive(a,b):
 def entries(p):
  rows=[]
  with tarfile.open(p,'r:*') as t:
   for m in t:
    f=t.extractfile(m) if m.isfile() else None
    rows.append({'name':m.name,'mode':m.mode,'type':m.type.decode(),'link':m.linkname,'uid':m.uid,'gid':m.gid,'mtime':m.mtime,'sha256':hashlib.file_digest(f,'sha256').hexdigest() if f else None})
  return rows
 aa,bb=entries(a),entries(b);assert len(aa)==len(bb),'source tar member count changed';meta=[]
 for x,y in zip(aa,bb):
  at=x.pop('mtime');bt=y.pop('mtime')
  if at!=bt:meta.append({'path':x['name'],'old':at,'new':bt})
  assert x==y,('source tar content changed',x['name'])
 return {'classification':'source-tar-metadata-only','mtime_changes':meta}
rows=json.loads((E/'rpm-downloads.json').read_text());assert len(rows)==36
summary=[];manifest_sets={};filemap=[]
try:
 for label in ['toolchain','basedev']:
  subset=[r for r in rows if r['project']==label];m={};paths={};root=W/'temp/night-20261103'/label/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';roots=list((root/'home/abuild/rpmbuild/BUILDROOT').glob('llvm-*'))
  for r in subset:
   key=r['metadata'].split('\t')[0]+'\t'+('src' if r['path'].endswith('.src.rpm') else r['metadata'].split('\t')[3]);paths[key]={'old':Path(r['local_rpm']),'new':Path(r['path'])};m[key]={}
   for side in ['old','new']:
    mm=manifest(paths[key][side]);m[key][side]=mm;save(E/'manifests'/label/(key.replace('\t','-')+'-'+side+'.json'),mm)
   print('MANIFEST',label,key,flush=True)
  save(E/(label+'-rpm-paths.json'),{k:{s:str(p) for s,p in v.items()} for k,v in paths.items()})
  # Both packaged payloads are needed: rpmbuild has removed BUILDROOT.
  for key,mm in m.items():
   for side,other in [('old','new'),('new','old')]:
    names={n for n,v in mm[side].items() if stat.S_ISREG(v['mode']) and (n not in mm[other] or v['sha256']!=mm[other][n]['sha256'])}
    if names:extract_selected(paths[key][side],names,P/label/key.replace('\t','-')/side)
  cache={}
  def getfile(side,key,name):
   ident=(side,key,name)
   if ident in cache:return cache[ident]
   row=m[key][side][name];expected=row['sha256'];target=P/label/key.replace('\t','-')/side/name
   if target.is_file() and not target.is_symlink():assert sha(target)==expected;cache[ident]=target;return target
   native=(roots[0]/name) if roots else P/'nonexistent-root-file'
   if native.is_file() and not native.is_symlink() and sha(native)==expected:
    cache[ident]=native;return native
   dest=P/label/key.replace('\t','-')/(side+'-extra-'+hashlib.sha256(name.encode()).hexdigest()[:12])
   target=dest/name
   if not target.exists():extract_selected(paths[key][side],{name},dest)
   assert sha(target)==expected;cache[ident]=target;return target
  def symbol(side,binary_name,filename):
   name=str(Path('usr/lib/debug')/Path(binary_name).parent/filename);owners=[k for k in m if name in m[k][side]];assert owners,('debug file missing from RPM set',name)
   assert len({m[k][side][name]['sha256'] for k in owners})==1;return getfile(side,owners[0],name)
  for key,mm in m.items():
   aa,bb=mm['old'],mm['new'];diffs=[];mt=[];added=sorted(set(bb)-set(aa));removed=sorted(set(aa)-set(bb))
   oldmeta=subprocess.check_output(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}\t%{BUILDTIME}\t%{BUILDHOST}',str(paths[key]['old'])],text=True)
   newmeta=subprocess.check_output(['rpm','-qp','--qf','%{NAME}\t%{VERSION}\t%{RELEASE}\t%{ARCH}\t%{VCS}\t%{BUILDTIME}\t%{BUILDHOST}',str(paths[key]['new'])],text=True)
   for name in sorted(set(aa)&set(bb)):
    a,b=aa[name],bb[name]
    if a['mtime']!=b['mtime']:mt.append({'path':name,'old':a['mtime'],'new':b['mtime']})
    same=all(a.get(k)==b.get(k) for k in ('mode','uid','gid','target','bytes','sha256'))
    if same:continue
    proof={};x=y=None
    try:
     assert all(a.get(k)==b.get(k) for k in ('mode','uid','gid','target')),'payload permission/owner/type/link changed'
     x=getfile('old',key,name);y=getfile('new',key,name);filemap.append({'project':label,'package':key,'path':name,'old':str(x),'new':str(y),'old_sha':a['sha256'],'new_sha':b['sha256']})
     dl=debuglink_name(x)
     if dl:proof=debuglink_proof(x,y,symbol('old',name,dl),symbol('new',name,debuglink_name(y)))
     elif key.endswith('\tsrc') and tarfile.is_tarfile(x) and tarfile.is_tarfile(y):proof=source_archive(x,y)
     else:proof=file_proof(x,y)
    except Exception as ex:proof={'classification':'FAIL','error':str(ex)}
    diffs.append({'path':name,'old_sha':a['sha256'],'new_sha':b['sha256'],**proof})
    print('FILE',label,key,name,proof['classification'],flush=True)
   r={'project':label,'package':key,'PASS':not added and not removed and all(v['classification']!='FAIL' for v in diffs),'metadata_old':oldmeta,'metadata_new':newmeta,'file_count':len(aa),'added':added,'removed':removed,'content_changes':diffs,'payload_mtime_changes':mt}
   summary.append(r);save(E/'qb-rpm-comparison.json',summary);save(E/'qb-changed-file-paths.json',filemap);print('PACKAGE',label,key,r['PASS'],flush=True)
 save(E/'item2-result.json',{'status':'ok' if all(r['PASS'] for r in summary) else 'differences','packages':len(summary),'passed':sum(r['PASS'] for r in summary),'failed':sum(not r['PASS'] for r in summary)})
except BaseException as ex:
 save(E/'item2-result.json',{'status':'stopped','reason':str(ex),'completed_packages':len(summary)});traceback.print_exc();raise
finally:
 result=json.loads((E/'item2-result.json').read_text());line='ITEM2 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status='+result['status']+' reason='+str(result.get('reason','comparison-complete'));(E/'item2-end.txt').write_text(line+'\n');print(line,flush=True)
