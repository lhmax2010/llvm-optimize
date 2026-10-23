"""Archive evidence only; never modifies source/build/protected roots."""
import hashlib,json,shutil,subprocess,time
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W/'docs/53_hybrid_local_validation_evidence'
for p in D.glob('*.py'):shutil.copyfile(p,E/p.name)
plan=json.loads((D/'plan.json').read_text());audit={'time_ns':time.time_ns()}
for name,args in [('source_status',['git','-C',plan['source'],'status','--porcelain']),('source_identity',['git','-C',plan['source'],'show','-s','--format=%H%n%T%n%P']),('df_home',['df','-B1','/home']),('services',['systemctl','--user','show','hybrid-local-20261023.service','hybrid-local-du-20261023.service','hybrid-verify-20261023.service','hybrid-followup-20261023.service','hybrid-plugin-20261023.service','hybrid-plugin-corrected-20261023.service','-p','Id','-p','ActiveState','-p','Result'])]:
 r=subprocess.run(args,capture_output=True,text=True);audit[name]={'argv':args,'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
for key in ['config','buildconf']:audit[key]={'path':plan[key],'sha256':hashlib.sha256(Path(plan[key]).read_bytes()).hexdigest(),'same_as_preflight':hashlib.sha256(Path(plan[key]).read_bytes()).hexdigest()==plan[key+'_sha256']}
(E/'final-input-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
assert audit['source_status']['rc']==0 and not audit['source_status']['stdout'];assert all(audit[k]['same_as_preflight'] for k in ['config','buildconf'])
assert 'ActiveState=active' not in audit['services']['stdout']
# Read-only provenance for actual source excerpt.
root=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0';base=root/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/clang/examples/AnnotateFunctions';proof=[]
for name in ['AnnotateFunctions.cpp','CMakeLists.txt']:
 p=base/name;q=E/('annotate-source-'+name);q.write_bytes(p.read_bytes());proof.append({'source':str(p),'copy':q.name,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
(E/'annotate-source-provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
excluded={'native-archive-summary.json','resources.jsonl','archive-inspection.jsonl'}
files=[]
for p in sorted(E.rglob('*')):
 if not p.is_file() or p.name=='evidence-manifest.json' or str(p.relative_to(E)) in excluded:continue
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 files.append({'path':str(p.relative_to(E)),'bytes':p.stat().st_size,'sha256':h.hexdigest()})
manifest={'created_ns':time.time_ns(),'source_commit':plan['commit'],'primary_build_exit':0,'overall_validation':'PARTIAL_NOT_ALL_PASS','root_retained':str(root),'published_files':files,'raw_preserved_locally_compressed_for_publication':json.loads((E/'compression-provenance.json').read_text())}
(E/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('published',len(files),'files',sum(r['bytes'] for r in files),'bytes','raw excludes',excluded)
