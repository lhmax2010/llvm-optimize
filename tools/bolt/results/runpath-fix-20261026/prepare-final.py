from pathlib import Path
import subprocess,json,hashlib,configparser,shutil,os,time
D=Path(__file__).resolve().parent;W=D.parent.parent;B=W.parent/'llvm-optimize-bolt';E=B/'tools/bolt/results/runpath-fix-20261026';S=D/'source';C=W/'temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf'
def git(*args):return subprocess.check_output(['git','-C',str(S),*args],text=True).strip()
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert json.loads((E/'pretrial-result.json').read_text())['PASS']
assert git('rev-parse','HEAD')=='aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7'
assert git('diff','--name-only').splitlines()==['packaging/clang-bolt-helper.py','packaging/llvm.spec']
msg=git('log','-1','--format=%B');addition='Match the BOLT candidate RUNPATH to the ordinary CMake-installed clang\nusing an in-place CMake RPATH_CHANGE and preserve all other ELF bytes.\nBuild llvm-bolt in parallel with the existing build job limit and verify\nthe exact task set independently of completion order. Check real LLVM C\nand C++ objects before strip, before install and after RPM processing.\n'
pos=msg.index('Change-Id:');msg=msg[:pos]+addition+'\n'+msg[pos:];(D/'commit-message.txt').write_text(msg+'\n')
subprocess.run(['git','-C',str(S),'add','packaging/clang-bolt-helper.py','packaging/llvm.spec'],check=True)
subprocess.run(['git','-C',str(S),'-c','user.name=Hao Lin','-c','user.email=hao.lin@samsung.com','commit','--amend','--reset-author','-F',str(D/'commit-message.txt')],check=True)
assert git('rev-parse','HEAD^')=='6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2';assert not git('status','--porcelain')
c=configparser.ConfigParser();c.read(C);bc=Path(c[c['general']['profile']]['buildconf']);assert sha(bc)=='e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945'
mem=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemTotal:')))*1024
plan=dict(source=str(S),commit=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}'),config=str(C),config_sha256=sha(C),buildconf=str(bc),buildconf_sha256=sha(bc),MemoryMax_bytes=mem-8*1024**3,MemTotal_bytes=mem,MemorySwapMax=0,nice=10,io_class=2,io_priority=7,home_available=shutil.disk_usage('/home').free,gbs_version=subprocess.check_output(['gbs','--version'],text=True).strip())
(D/'plan.json').write_text(json.dumps(plan,indent=2));(E/'preflight.json').write_text(json.dumps(plan,indent=2));shutil.copyfile(C,E/'gbs.conf');shutil.copyfile(bc,E/'build.conf')
(E/'source.patch').write_bytes(subprocess.check_output(['git','-C',str(S),'diff','aa637c1','HEAD','--','packaging']))
for n in ('llvm.spec','clang-bolt-helper.py'):shutil.copyfile(S/'packaging'/n,E/n)
argv=['gbs','-c',str(C),'export','--spec','llvm.spec','--commit',plan['commit'],'--upstream-branch','sandbox/fangyu.he/llvm_optmize','--upstream-tag','upstream/22.1.8','--outdir-directly','-o',str(D/'export'),str(S)]
start=time.time_ns()
with (E/'export.stdout').open('wb') as out,(E/'export.stderr').open('wb') as err:p=subprocess.run(argv,stdout=out,stderr=err,env={**os.environ,'TMPDIR':str(D/'tmp')})
(E/'export-result.json').write_text(json.dumps(dict(argv=argv,rc=p.returncode,start_ns=start,end_ns=time.time_ns()),indent=2));assert p.returncode==0
shutil.copyfile(D/'export/llvm.spec',E/'exported.spec');print('EXPORT_PASS',plan['commit'])
