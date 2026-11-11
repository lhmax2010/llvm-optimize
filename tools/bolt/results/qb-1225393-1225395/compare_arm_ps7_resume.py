from package_utils import *
from rpm_extract import extract_selected
import re,sys,traceback,difflib,xml.etree.ElementTree as ET
S=W/'temp/rebase-359934-20261106/source'
def git(*args):return subprocess.check_output(['git','-C',str(S),*args],timeout=30)
log=(E/'arm-baseline-resume.stdout').open('x')
def emit(*args):
 text=' '.join(map(str,args));print(text,flush=True);log.write(text+'\n');log.flush()
base={
 '1225393':('1216401','Tizen-Base-Toolchain','tizen-base-toolchain_20261103.084003'),
 '1225395':('1216400','Tizen-Base-Dev','tizen-base-dev_20261103.083743')}
rows=json.loads((E/'package-results.json').read_text());results=json.loads((E/'arm-baseline-results.json').read_text());identities=json.loads((E/'arm-baseline-identities.json').read_text())
done={(r['build'],r['arch'],r['name']) for r in results}
allowed={'usr/lib/cmake/llvm/AddLLVM.cmake':'llvm/cmake/modules/AddLLVM.cmake','usr/lib/cmake/clang/AddClang.cmake':'clang/cmake/modules/AddClang.cmake'}
# Paths may be usr/lib64 in RPMs; identify exact suffix then verify full bytes from Git.
def module_source(p):
 for suffix,src in [('cmake/llvm/AddLLVM.cmake','llvm/cmake/modules/AddLLVM.cmake'),('cmake/clang/AddClang.cmake','clang/cmake/modules/AddClang.cmake')]:
  if p.endswith('/'+suffix):return src
 return None
try:
 assert (E/'ps7-to-ps10.stat').exists()
 # Previously completed aarch64 proof ties both CMake byte streams to all five Git objects.
 reference={}
 for r in results:
  for c in r['changes']:
   assert c['reason'].startswith('exact hybrid change')
   d=X/'ps7-module-proof'/r['build']/r['arch']/r['name']
   reference[c['source']]=((d/'old'/c['file']).read_bytes(),(d/'new'/c['file']).read_bytes())
 assert len(reference)==2
 for newbid,(oldbid,project,snap) in base.items():
  url='https://download.tizen.org/snapshots/TIZEN/Tizen/'+project+'/'+snap+'/'
  manifest_url=url+'builddata/manifest/'+snap+'_standard.xml'
  data=urllib.request.urlopen(manifest_url,timeout=120).read()
  out=E/'baseline'/oldbid;out.mkdir(parents=True,exist_ok=True);(out/'manifest.xml').write_bytes(data)
  projects=[x.attrib for x in ET.fromstring(data).iter('project') if x.get('name')=='platform/upstream/llvm']
  assert len(projects)==1 and projects[0].get('revision')=='463c9a133a6dfea9adf1e6c8e07ab705cbf2a587',projects
  identities.append({'build':oldbid,'url':manifest_url,'sha256':hashlib.sha256(data).hexdigest(),'project':projects[0]})
  for arch in ['aarch64','armv7l']:
   logurl=url+'builddata/buildlogs/standard/'+arch+'/succeeded/llvm.buildlog.txt'
   logpath=out/(arch+'-llvm.buildlog.txt.gz')
   names=set();h=hashlib.sha256();linecount=0;success=[]
   with urllib.request.urlopen(logurl,timeout=120) as inp,gzip.open(logpath,'wb') as dst:
    for raw in inp:
     dst.write(raw);h.update(raw);linecount+=1;text=raw.decode(errors='replace')
     if 'Wrote:' in text:names.add(text.split('Wrote:',1)[1].strip().split('/')[-1])
     if 'finished "build llvm.spec"' in text:success.append({'line':linecount,'text':text.strip()})
   newrows=[r for r in rows if r['build']==newbid and r['arch']==arch]
   expected={r['name'] for r in newrows}
   assert {n for n in names if not n.endswith('.src.rpm')}==expected,(oldbid,arch,names,expected)
   assert success
   save(out/(arch+'-log-meta.json'),{'url':logurl,'sha256':h.hexdigest(),'lines':linecount,'success':success,'rpms':sorted(names)})
   for r in newrows:
    if (r['build'],r['arch'],r['name']) in done:continue
    emit('START',oldbid,'->',newbid,arch,r['name'])
    nrec=r['new'];oldurl=url+'repos/'+nrec['url'].split('/repos/',1)[1]
    old=fetch({'build':oldbid,'project':project,'arch':arch,'name':r['name'],'url':oldurl,'path':str(X/oldbid/arch/'rpms'/r['name'])})
    assert '463c9a133a6dfea9adf1e6c8e07ab705cbf2a587' in old['rpm_query'],old
    a=getman(Path(old['path']),oldbid,arch,r['name'])
    with gzip.open(E/'manifests'/newbid/arch/(r['name']+'.json.gz'),'rt') as f:b=json.load(f)
    assert sha(Path(nrec['path']))==nrec['sha256']
    added=sorted(b.keys()-a.keys());removed=sorted(a.keys()-b.keys());changes=[];times=[]
    for name in sorted(a.keys()&b.keys()):
     delta={k:[a[name].get(k),b[name].get(k)] for k in a[name].keys()|b[name].keys() if a[name].get(k)!=b[name].get(k)}
     if 'mtime' in delta:times.append({'file':name,'mtime':delta.pop('mtime')})
     if delta:changes.append({'file':name,'differences':delta})
    result={'build':newbid,'baseline':oldbid,'arch':arch,'name':r['name'],'old':old,'new':nrec,
     'file_count':len(b),'added':added,'removed':removed,'changes':changes,'payload_mtime_differences':times,'status':'PASS'}
    if added or removed:result['status']='FAIL'
    for c in changes:
     source=module_source(c['file'])
     if not source or set(c['differences'])-{'bytes','sha256'}:
      c['reason']='outside the two allowed installed CMake modules';result['status']='FAIL';continue
     scratch=X/'ps7-module-proof'/newbid/arch/r['name']
     if not (scratch/'old').exists():extract_selected(old['path'],{c['file']},scratch/'old')
     if not (scratch/'new').exists():extract_selected(nrec['path'],{c['file']},scratch/'new')
     aa=(scratch/'old'/c['file']).read_bytes();bb=(scratch/'new'/c['file']).read_bytes()
     assert hashlib.sha256(aa).hexdigest()==a[c['file']]['sha256']
     assert hashlib.sha256(bb).hexdigest()==b[c['file']]['sha256']
     assert (aa,bb)==reference[source], 'module differs from previously Git-verified byte streams'
     diff=''.join(difflib.unified_diff(aa.decode().splitlines(True),bb.decode().splitlines(True),fromfile='PS7/'+source,tofile='hybrid/'+source))
     dp=E/'baseline'/oldbid/(newbid+'-'+arch+'-'+Path(source).name+'.diff');dp.write_text(diff)
     c.update(reason='exact hybrid change; old=PS7=PS10=hybrid parent, new=hybrid=60fabc',source=source,proof_diff=str(dp.relative_to(E)))
    results.append(result);save(E/'arm-baseline-results.json',results);save(E/'arm-baseline-identities.json',identities)
    emit('RESULT',result['status'],'changes',len(changes),'files',len(b))
    assert result['status']=='PASS',result['changes']
 end='ITEM3 已结束 '+now()+' status=ok reason=all_ARM_payloads_equal_except_exact_hybrid_CMake_changes'
 (E/'item3-resume-ending.txt').write_text(end+'\n');emit(end)
except BaseException:
 (E/'arm-baseline-resume-failure.txt').write_text(traceback.format_exc())
 end='ITEM3 已结束 '+now()+' status=failed'
 (E/'item3-resume-ending.txt').write_text(end+'\n');emit(end)
 raise
