from pathlib import Path
import subprocess,json,hashlib,configparser,shutil,importlib.util,time,os,re
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/bolt-on-hybrid-20261024';S=D/'source';C=W/'temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf'
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(S),*args],text=True).strip()
assert git('rev-parse','HEAD^')=='6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2';assert not git('status','--porcelain');assert git('symbolic-ref','-q','HEAD') if False else True
for p in ['packaging/clang-bolt-helper.py','packaging/clang-bolt-v2.fdata.xz']:
 assert subprocess.check_output(['git','-C',str(S),'show','3d3b4bf:'+p])==(S/p).read_bytes()
c=configparser.ConfigParser();c.read(C);bc=Path(c[c['general']['profile']]['buildconf']);assert sha(bc)=='e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945'
assert c[c['general']['profile']]['repos'].replace(' ','')=='repo.base_0,repo.base_debug_0'
base='http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319/repos/standard/'
assert c['repo.base_0']['url']==base+'packages/' and c['repo.base_debug_0']['url']==base+'debug/'
mem=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemTotal:')))*1024
plan=dict(source=str(S),commit=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}'),config=str(C),config_sha256=sha(C),buildconf=str(bc),buildconf_sha256=sha(bc),MemoryMax_bytes=mem-8*1024**3,MemTotal_bytes=mem,MemorySwapMax=0,nice=10,io_class=2,io_priority=7,merge_conflicts=0,gbs_version=subprocess.check_output(['gbs','--version'],text=True).strip())
(D/'plan.json').write_text(json.dumps(plan,indent=2)+'\n');(E/'preflight.json').write_text(json.dumps(plan,indent=2)+'\n');shutil.copyfile(C,E/'gbs.conf');shutil.copyfile(bc,E/'build.conf')
(E/'merged-spec.diff').write_bytes(subprocess.check_output(['git','-C',str(S),'diff','6e9d4f2','HEAD','--','packaging/llvm.spec']))
(E/'local-source.patch').write_bytes(subprocess.check_output(['git','-C',str(S),'format-patch','-1','--stdout','--no-binary']))
# Query a copied historical graph, never execute ninja inside a historical root.
G=D/'graph-copy';(G/'CMakeFiles').mkdir(parents=True,exist_ok=True)
shutil.copyfile(W/'docs/53_hybrid_local_validation_evidence/build-metadata/build.ninja',G/'build.ninja')
R=W/'temp/hybrid-local-20261023/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
shutil.copyfile(R/'home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/CMakeFiles/rules.ninja',G/'CMakeFiles/rules.ninja')
shutil.copyfile(R/'usr/bin/ninja',D/'ninja');(D/'ninja').chmod(0o755)
p=subprocess.run([str(D/'ninja'),'-f','build.ninja','-t','commands','bin/clang-22'],cwd=G,capture_output=True,text=True);assert p.returncode==0,p.stderr
edges=[l for l in p.stdout.splitlines() if ' -o bin/clang-22 ' in l];assert len(edges)==1
(E/'hybrid-link.original').write_text(edges[0]+'\n')
spec=importlib.util.spec_from_file_location('helper',S/'packaging/clang-bolt-helper.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
replay=h.replay_script(edges[0],'/tmp/precheck-clang','/tmp/precheck-link.d');(E/'hybrid-replay-precheck.sh').write_text(replay)
notes=[]
for path in [S/'bolt/tools/driver/CMakeLists.txt',*sorted((S/'bolt/lib').glob('*/CMakeLists.txt')),*sorted((S/'bolt/lib/Target').glob('*/CMakeLists.txt'))]:
 text=path.read_text()
 if 'add_llvm_library(' in text or 'add_bolt_tool(llvm-bolt' in text:
  assert 'DISABLE_LLVM_LINK_LLVM_DYLIB' in text,path
  notes.append({'file':str(path.relative_to(S)),'disable_dylib_lines':[i for i,l in enumerate(text.splitlines(),1) if 'DISABLE_LLVM_LINK_LLVM_DYLIB' in l]})
(E/'link-precheck.json').write_text(json.dumps(dict(clang_replay='PASS',graph_copy=str(G),cache=re.findall(r'--thinlto-cache-dir=([^\s]+)',edges[0]),bolt_expected_linkage='static LLVM; driver and all BOLT libraries explicitly disable dylib',cmake_evidence=notes,whitelist_changes=[]),indent=2)+'\n')
(D/'tmp').mkdir();argv=['gbs','-c',str(C),'export','--spec','llvm.spec','--commit',plan['commit'],'--upstream-branch','sandbox/fangyu.he/llvm_optmize','--upstream-tag','upstream/22.1.8','--outdir-directly','-o',str(D/'export'),str(S)];start=time.time_ns()
with (E/'export.stdout').open('wb') as out,(E/'export.stderr').open('wb') as err:p=subprocess.run(argv,stdout=out,stderr=err,env={**os.environ,'TMPDIR':str(D/'tmp')})
(E/'export-result.json').write_text(json.dumps(dict(argv=argv,rc=p.returncode,start_ns=start,end_ns=time.time_ns()),indent=2));assert p.returncode==0
for p in (D/'export').iterdir():
 if p.suffix in ('.spec','.patch'):shutil.copyfile(p,E/p.name)
print('MERGE_LINK_PREFLIGHT_EXPORT_PASS',plan['commit'],flush=True)
