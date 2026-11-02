"""Prepare experiment copies and evidence; no LLVM compilation."""
from common import *
import shlex,re,difflib,importlib.util,shutil
P.mkdir(exist_ok=True);E.mkdir(exist_ok=True)
assert sha(CONFIG.parent/'build.conf')==BUILD_SHA
save(E/'disk-budget.json',disk_budget());assert disk_budget()['PASS'],'insufficient space; stop'
log=(H/'evidence/rpm-build.log').read_text().splitlines()
idx,line=next((i,l) for i,l in enumerate(log,1) if '+ cmake -G Ninja' in l)
argv=shlex.split(line.split('+ ',1)[1]);assert argv[-1]=='../llvm'
(E/'configure-original.txt').write_text(f'L{idx}: {line}\n')
save(E/'cmake-base.json',argv)
a=argv[:-1]+['-DLLVM_BUILD_INSTRUMENTED=IR',argv[-1]]
d=argv[:-1]+['-DLLVM_PROFDATA_FILE='+PROFDATA,argv[-1]]
save(E/'cmake-A.json',a);save(E/'cmake-D.json',d)
assert a[:-2]+a[-1:]==argv and d[:-2]+d[-1:]==argv
save(E/'cmake-differences.json',{'A_added':a[-2],'D_added':d[-2],'other_argv_byte_equal':True,'origin_line':idx})
(E/'cmake-A.txt').write_text(shlex.join(a)+'\n');(E/'cmake-D.txt').write_text(shlex.join(d)+'\n')
baseenv={'CFLAGS':next(x.split('=',1)[1] for x in argv if x.startswith('-DCMAKE_C_FLAGS=')),'CXXFLAGS':next(x.split('=',1)[1] for x in argv if x.startswith('-DCMAKE_CXX_FLAGS=')),'LDFLAGS':'-Wl,-z,relro,--as-needed','AR':'llvm-ar','RANLIB':'llvm-ranlib'}
save(E/'rpm-environment.json',baseenv)
manifest=W/'temp/bolt-aarch64-v2-20260921/profile-v2-manifest.json';m=json.loads(manifest.read_text())
genpath=W/'tools/bench_inputs/generate_synthetic.py';spec=importlib.util.spec_from_file_location('synth',genpath);gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
rows=[]
for c in m['corpora']:
 actual={x['name']:x for x in c['real_inputs']}
 for item in c['inputs_flags_manifest']:
  name=item['name']
  if name in 'ABC' and len(name)==1:
   dest=P/'inputs'/name;assert not dest.exists();gen.generate(dest,item['scale'],c['seed']);path=dest/(name+'.cpp')
  else:
   # AArch64 flags manifest uses real_aarch64_ prefix; paths are in real_inputs.
   match=[x for x in c['real_inputs'] if x['sha256']==item['sha256']];assert len(match)==1;path=Path(match[0]['path'])
  assert path.is_file() and sha(path)==item['sha256'],str(path)
  target=c['target'];sysroot=c['sysroot'];resource=m['resource_dir'];assert Path(sysroot).is_dir() and Path(resource).is_dir()
  flags=['--target='+target,'--sysroot='+sysroot,'-resource-dir='+resource]+item['flags']
  if path.suffix=='.ii':flags+=['-x','c++-cpp-output']
  rows.append({'name':name,'target':target,'path':str(path),'sha256':sha(path),'bytes':path.stat().st_size,'compiler_args':flags,'synthetic':name in ['A','B','C']})
assert len(rows)==23 and sum(x['target'].startswith('armv7l') for x in rows)==13
save(E/'training.json',rows);save(E/'training-provenance.json',{'manifest':str(manifest),'sha256':sha(manifest),'generator':str(genpath),'generator_sha256':sha(genpath),'count':len(rows)})
# Isolated detached source copy. Original source and all Source files stay untouched.
copy=P/'source-D';assert not copy.exists()
call(['git','clone','--shared','--no-checkout',str(S),str(copy)],E/'clone.stdout')
call(['git','checkout','--detach',COMMIT],E/'checkout.stdout',cwd=copy)
specfile=copy/'packaging/llvm.spec';before=specfile.read_text();needle='    ../llvm\n';assert before.count(needle)==1
after=before.replace(needle,'    -DLLVM_PROFDATA_FILE='+PROFDATA+' \\\n'+needle)
specfile.write_text(after);(E/'spec-PGO.diff').write_text(''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='original/packaging/llvm.spec',tofile='experiment/packaging/llvm.spec')))
call(['git','-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','-am','experiment: measure PGO resource use (local only)'],E/'local-experiment-commit.stdout',cwd=copy)
commit=subprocess.check_output(['git','-C',str(copy),'rev-parse','HEAD'],text=True).strip()
save(E/'source.json',{'base_commit':COMMIT,'experiment_commit':commit,'source_D':str(copy),'published_source_unchanged':True,'spec_sha256':sha(specfile)})
export=json.loads((H/'export-command.json').read_text())
for label,source,rev in [('baseline',S,COMMIT),('PGO',copy,commit)]:
 out=P/('export-'+label);args=[str(out) if x==str(H/'export') else str(source) if x==str(S) else rev if x==COMMIT else x for x in export]
 call(args,E/('export-'+label+'.stdout'))
# Only PGO line plus GBS VCS header can differ in the exports.
old=(P/'export-baseline/llvm.spec').read_text();new=(P/'export-PGO/llvm.spec').read_text();(E/'export-spec.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True))))
save(E/'prepare.json',{'PASS':True,'training_count':23,'source_D_commit':commit,'buildconf_sha256':BUILD_SHA})
print('PREPARE PASS',flush=True)
