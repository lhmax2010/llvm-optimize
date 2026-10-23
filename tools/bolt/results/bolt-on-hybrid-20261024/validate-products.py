"""Run only after successful new-root build; all product inputs are read-only."""
from pathlib import Path
import json,hashlib,subprocess,time,shutil,re,sys
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/bolt-on-hybrid-20261024';R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';BUILD=R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build';WORK=BUILD/'clang-bolt';P=D/'products'
def sha(p):return hashlib.file_digest(Path(p).open('rb'),'sha256').hexdigest()
def save(name,obj):
 p=E/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def run(name,argv,timeout=300):
 start=time.time_ns();r=subprocess.run(argv,capture_output=True,text=True,timeout=timeout);j=dict(argv=argv,rc=r.returncode,stdout=r.stdout,stderr=r.stderr,start_ns=start,end_ns=time.time_ns());save(name+'.json',j);return j
assert json.loads((E/'build-result.json').read_text())['exit_code']==0
assert not (E/'gate-stop.json').exists()
log=(E/'rpm-build.log').read_text(errors='replace')
for marker in ['BOLT_PIPELINE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_POST_GATE_PASS','BOLT_CACHE_RELEASE removed']:
 assert marker in log,marker
rpms=sorted((R/'home/abuild/rpmbuild/RPMS/x86_64').glob('*.rpm'));srpms=sorted((R/'home/abuild/rpmbuild/SRPMS').glob('*.rpm'));assert len(rpms)==22 and len(srpms)==1
P.mkdir(exist_ok=True);preserved=[]
for src,rel in [(WORK/'clang.candidate','binaries/clang.candidate'),(WORK/'ordinary-clang-22','binaries/ordinary-clang-22'),(BUILD/'bin/llvm-bolt','binaries/llvm-bolt'),*[(p,'RPMS/'+p.name) for p in rpms],*[(p,'SRPMS/'+p.name) for p in srpms],*[(WORK/n,'work/'+n) for n in ['identity.json','disk-begin.json','disk-tool-built.json','disk-pipeline.json','disk-post.json','cache-release.json']]]:
 assert src.is_file(),src
 dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);assert not dest.exists(),dest;shutil.copy2(src,dest);a=sha(src);assert sha(dest)==a
 preserved.append(dict(source=str(src),retained=str(dest),sha256=a,bytes=src.stat().st_size))
save('preserved-products.json',preserved)
identity=json.loads((WORK/'identity.json').read_text());assert sha(WORK/'clang.candidate')==identity['after_sha256']
rows=[]
for p in rpms+srpms:
 q=run('rpm-headers/'+p.name,['rpm','-qp','--qf','%{NAME}\t%{NEVRA}\n',str(p)]);assert q['rc']==0
 rows.append(dict(file=p.name,bytes=p.stat().st_size,sha256=sha(p),header=q['stdout']))
save('rpm-identities.json',rows)
base=json.loads((W/'docs/53_hybrid_local_validation_evidence/rpm-identities.json').read_text());byname={x['name']:x for x in base}
save('rpm-size-comparison.json',[dict(file=x['file'],hybrid_bytes=byname[x['file']]['bytes'],hybrid_bolt_bytes=x['bytes'],delta=x['bytes']-byname[x['file']]['bytes']) for x in rows])
links=[]
for name,p in [('candidate',WORK/'clang.candidate'),('ordinary',WORK/'ordinary-clang-22'),*[(n,BUILD/'bin'/n) for n in ['clang-22','clang','clang++','clang-cl','clang-cpp','lld','ld.lld','ld64.lld','lld-link','wasm-ld','llvm-ar','llvm-ranlib','llvm-bolt']]]:
 if not p.exists():continue
 r=run('needed/'+name,['readelf','-dW',str(p)]);assert r['rc']==0;libs=re.findall(r'\(NEEDED\).*?\[([^]]+)\]',r['stdout']);assert not any(x.startswith(('libLLVM','libclang-cpp')) for x in libs),(name,libs)
 links.append(dict(name=name,path=str(p),needed=libs,sha256=sha(p)))
assert next(x['needed'] for x in links if x['name']=='candidate')==next(x['needed'] for x in links if x['name']=='ordinary')
save('linkage.json',links)
# Reuse the previously certified 90 .ii records, verify every input before copying.
units=json.loads((W/'docs/53_hybrid_local_validation_evidence/tu-inputs.json').read_text());assert len(units)==90
save('tu-inputs.json',units)
V=R/'home/abuild/bolt-hybrid-validation';V.mkdir(exist_ok=True);slot=V/'compiler/clang-22';slot.parent.mkdir(exist_ok=True);inside='/home/abuild/bolt-hybrid-validation';results={};identities=[]
for role,src in [('ordinary',WORK/'ordinary-clang-22'),('candidate',WORK/'clang.candidate')]:
 shutil.copyfile(src,slot);slot.chmod(0o755);identities.append(dict(role=role,source=str(src),sha256=sha(src),inode=slot.stat().st_ino));assert sha(slot)==sha(src)
 for u in units:
  i=u['index'];s=V/'objects'/f'{i:03d}';s.mkdir(parents=True,exist_ok=True);inp=s/'input.ii';assert sha(u['copy'])==u['sha256']
  if not inp.exists():shutil.copyfile(u['copy'],inp)
  assert sha(inp)==u['sha256'];sub=inside+'/objects/'+f'{i:03d}';args=list(u['original_argv']);args[0]=inside+'/compiler/clang-22';args.insert(1,'--no-default-config');args[args.index('-c')+1]=sub+'/input.ii';args[args.index('-o')+1]=sub+'/same.o';args=[('-resource-dir=/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/lib64/clang/22' if x.startswith('-resource-dir=') else x) for x in args]
  out=s/'same.o';out.unlink(missing_ok=True);r=run('objects/'+role+'-'+str(i),['sudo','-n','/usr/sbin/chroot',str(R),*args],600);assert r['rc']==0 and out.is_file() and out.stat().st_size>0
  value=dict(sha256=sha(out),bytes=out.stat().st_size,target=u['target'],key=u['key'],argv=args)
  if role=='ordinary':shutil.copyfile(out,s/'ordinary.o');results[i]={'ordinary':value}
  else:results[i]['candidate']=value;results[i]['byte_equal']=(s/'ordinary.o').read_bytes()==out.read_bytes();assert results[i]['byte_equal'],i
  save('objects-progress.json',dict(role=role,index=i,identities=identities,results=results));print('OBJECT',role,i+1,'/90',flush=True)
assert len({x['inode'] for x in identities})==1
save('objects-result.json',dict(total=90,passed=sum(x['byte_equal'] for x in results.values()),same_entity=True,section_filtering=False,identities=identities,results=results))
save('validation-result.json',dict(status='PASS',RPMs=22,SRPMs=1,objects=90,candidate_sha256=identity['after_sha256'],preservation=str(P)))
print('VALIDATION_PASS',flush=True)
