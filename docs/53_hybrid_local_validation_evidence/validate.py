"""Validation runs only against this task's new root and copied inputs."""
import collections,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W/'docs/53_hybrid_local_validation_evidence';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';V=R/'home/abuild/hybrid-validation';INNER='/home/abuild/hybrid-validation'
sys.path.insert(0,str(W/'tools'));import check_hybrid_link_needed as needed

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def save(name,obj):
 p=E/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def run(name,argv,timeout=300):
 start=time.time_ns();p=subprocess.run(argv,capture_output=True,text=True,timeout=timeout);r={'argv':argv,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'start_ns':start,'end_ns':time.time_ns()};save(name+'.json',r);return r
def root(name,args,timeout=300):return run(name,['sudo','-n','/usr/sbin/chroot',str(R),*args],timeout)
def linkage():
 table=json.loads((W/'docs/52_hybrid_link_evidence/needed-expectations-v2.json').read_text());rows=[]
 for t in table['targets']:
  p=BUILD/t['build_output'];r=run('linkage/raw-'+str(len(rows)),['readelf','-dW',str(p)])
  libs=re.findall(r'\(NEEDED\).*?\[([^]]+)\]',r['stdout']);state=needed.needed_status(t['expected_needed'],libs)
  rows.append({**t,'exists':p.exists(),'needed':libs,'status':state['status'] if r['rc']==0 else 'INSPECTION_ERROR','needed_comparison':state,'rc':r['rc']})
 save('linkage-188.json',{'total':len(rows),'counts':dict(collections.Counter(str(x['status']) for x in rows)),'rows':rows})
 return rows

def sizes():
 paths={'root':R,'cache':BUILD/'lto.cache','build':BUILD,'BUILDROOT':R/'home/abuild/rpmbuild/BUILDROOT','binary_rpms':R/'home/abuild/rpmbuild/RPMS','source_rpms':R/'home/abuild/rpmbuild/SRPMS'};rows=[]
 for name,path in paths.items():
  inner='/'+str(path.relative_to(R));r=root('final-size-'+name,['/bin/du','-sx','-B1',inner],600);rows.append({'name':name,'path':str(path),**r})
 save('final-sizes.json',rows)

def install():
 rpms=sorted((R/'home/abuild/rpmbuild/RPMS/x86_64').glob('*.rpm'));srpms=sorted((R/'home/abuild/rpmbuild/SRPMS').glob('*.rpm'));assert len(rpms)==22 and len(srpms)==1
 rows=[];paths=set()
 for p in rpms+srpms:
  q=run('rpm-header/'+p.name,['rpm','-qp','--qf','%{NAME}\t%{NEVRA}\t%{BUILDTIME}\n',str(p)]);assert q['rc']==0
  f=run('rpm-files/'+p.name,['rpm','-qpl',str(p)]);assert f['rc']==0
  if p in rpms:paths.update(f['stdout'].splitlines())
  rows.append({'file':str(p),'name':p.name,'bytes':p.stat().st_size,'sha256':sha(p),'header':q['stdout']})
 save('rpm-identities.json',rows);expected=sorted((W/'docs/52_hybrid_link_evidence/expected-rpm-names.txt').read_text().splitlines());actual=sorted(r['header'].split('\t',1)[0] for r in rows if not r['name'].endswith('.src.rpm'));save('rpm-name-check.json',{'expected':expected,'actual':actual,'pass':actual==expected});assert actual==expected
 (E/'rpm-paths.txt').write_text('\n'.join(sorted(paths))+'\n')
 root('installed-before',['rpm','-qa'])
 r=root('install-rpms',['/bin/sh','-ec','rpm -Uvh --oldpackage --replacepkgs /home/abuild/rpmbuild/RPMS/x86_64/*.rpm'],1200);assert r['rc']==0,r
 root('installed-after',['rpm','-qa']);return paths

def installed_linkage():
 table=json.loads((W/'docs/52_hybrid_link_evidence/needed-expectations-v2.json').read_text());paths=(E/'rpm-paths.txt').read_text().splitlines();paths=[p for p in paths if p.startswith('/usr/bin/') or re.match(r'/usr/lib64/.*\.so',p) or re.search(r'/sdk_tools/lldb/(bin|lib64)/',p)]
 j=needed.inspect_paths(table,R,paths,require_declared=True);save('installed-needed.json',j);return j

def objects():
 V.mkdir(exist_ok=True);slot=V/'compiler/clang-22';slot.parent.mkdir(exist_ok=True);units=json.loads((E/'tu-inputs.json').read_text());results={};identities=[]
 for label,source,want in [('ordinary',W/'temp/bolt-v4-20261022-cache-release/baseline-products/binaries/ordinary-clang-22','06c940726269210ce3655e17366820a080bfe236a3adc24622958e6a6709e309'),('hybrid',R/'usr/bin/clang-22',None)]:
  actual=sha(source);assert want is None or actual==want;shutil.copyfile(source,slot);slot.chmod(0o755);assert sha(slot)==actual;identities.append({'role':label,'source':str(source),'sha256':actual,'slot':INNER+'/compiler/clang-22','inode':slot.stat().st_ino})
  for u in units:
   i=u['index'];sub=V/'objects'/f'{i:03d}';sub.mkdir(parents=True,exist_ok=True);input_path=sub/'input.ii'
   if not input_path.exists():shutil.copyfile(u['copy'],input_path)
   assert sha(input_path)==u['sha256'];inside=INNER+'/objects/'+f'{i:03d}';a=list(u['original_argv']);a[0]=INNER+'/compiler/clang-22';a.insert(1,'--no-default-config');a[a.index('-c')+1]=inside+'/input.ii';a[a.index('-o')+1]=inside+'/same.o';a=[('-resource-dir=/usr/lib64/clang/22' if x.startswith('-resource-dir=') else x) for x in a]
   (sub/'same.o').unlink(missing_ok=True);r=root('objects/'+label+'-'+f'{i:03d}',a,600);assert r['rc']==0,(label,i,r);p=sub/'same.o';assert p.is_file() and p.stat().st_size>0;shutil.copyfile(p,sub/(label+'.o'));value={'key':u['key'],'target':u['target'],'input_sha256':u['sha256'],'sha256':sha(p),'bytes':p.stat().st_size,'argv':a}
   if label=='ordinary':results[i]={'ordinary':value}
   else:results[i]['hybrid']=value;results[i]['byte_equal']=(sub/'ordinary.o').read_bytes()==p.read_bytes()
   save('objects-progress.json',{'role':label,'index':i,'identities':identities,'results':results})
   print('OBJECT',label,i+1,'/90',flush=True)
 assert len({x['inode'] for x in identities})==1
 save('objects-result.json',{'total':90,'passed':sum(r.get('byte_equal',False) for r in results.values()),'same_entity':True,'section_filtering':False,'identities':identities,'results':results})

def arm_parse():
 V.mkdir(exist_ok=True);shutil.copyfile(D/'export/llvm.spec',V/'llvm.spec');rows=[]
 r=root('rpm-version',['rpm','--version']);assert r['rc']==0
 for arch in ('armv7l','aarch64'):
  r=root('parse-'+arch,['rpmspec','--target='+arch+'-tizen-linux','--define','_toolchain 1','-P',INNER+'/llvm.spec']);rows.append({'arch':arch,'rc':r['rc'],'patch_commands':len(re.findall(r'^%patch\b[^\n]*',r['stdout'],re.M))})
 save('arm-parse-result.json',rows)

if __name__=='__main__':
 assert sys.argv[1] in ('linkage','sizes','install','installed_linkage','objects','arm_parse')
 result=globals()[sys.argv[1]]();print('DONE',sys.argv[1],flush=True)
