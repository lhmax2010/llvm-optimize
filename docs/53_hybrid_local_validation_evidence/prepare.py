import configparser,hashlib,json,os,re,subprocess,time
from pathlib import Path
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=Path(__file__).resolve().parent;E=W/'docs/53_hybrid_local_validation_evidence';S=W/'temp/llvm-optimize-intranet-20261020/llvm';C=W/'temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(S),*a],text=True).strip()
head='6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2';assert git('rev-parse','HEAD')==head;assert not git('status','--porcelain');assert git('rev-parse','HEAD^{tree}')=='80a6fd231c4564a3b762f4ec288cf2c41f9d2e20';assert git('config','--get','core.abbrev')=='12'
c=configparser.ConfigParser();c.read(C);profile=c['general']['profile'];assert c[profile]['repos'].replace(' ','')=='repo.base_0,repo.base_debug_0';bc=Path(c[profile]['buildconf']);assert sha(bc)=='e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945'
base='http://download.tizen.org/snapshots/TIZEN/Tizen/Tizen-Base-Toolchain/tizen-base-toolchain_20261013.024319/repos/standard/'
assert c['repo.base_0']['url']==base+'packages/';assert c['repo.base_debug_0']['url']==base+'debug/'
mem=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:')))*1024
j={'source':str(S),'commit':head,'tree':git('rev-parse','HEAD^{tree}'),'upstream':git('rev-parse','upstream'),'clean':True,'config':str(C),'config_sha256':sha(C),'buildconf':str(bc),'buildconf_sha256':sha(bc),'repos':{k:dict(c[k]) for k in ('repo.base_0','repo.base_debug_0')},'MemTotal_bytes':mem,'MemoryMax_bytes':mem-8*1024**3,'MemorySwapMax':0,'nice':10,'io_class':2,'io_priority':7,'only_active_stop':'/home available <20 GiB','no_memory_admission_or_freeze':True,'gbs_version':subprocess.check_output(['gbs','--version'],text=True).strip(),'baseline_worktree_status':subprocess.check_output(['git','-C',str(W),'status','--short'],text=True)}
(E/'preflight.json').write_text(json.dumps(j,indent=2)+'\n');(D/'plan.json').write_text(json.dumps(j,indent=2)+'\n');(E/'build.conf').write_bytes(bc.read_bytes());(E/'gbs.conf').write_bytes(C.read_bytes())
(D/'tmp').mkdir();out=D/'export';argv=['gbs','-c',str(C),'export','--spec','llvm.spec','--commit',head,'--outdir-directly','--outdir',str(out),str(S)];start=time.time_ns()
with (E/'export.stdout').open('w') as o,(E/'export.stderr').open('w') as e:r=subprocess.run(argv,stdout=o,stderr=e,env={**os.environ,'TMPDIR':str(D/'tmp'),'PYTHONDONTWRITEBYTECODE':'1'})
(E/'export-result.json').write_text(json.dumps({'argv':argv,'rc':r.returncode,'start_ns':start,'end_ns':time.time_ns()},indent=2)+'\n');assert r.returncode==0
text=(W/'docs/llvm_optimize_intranet_fetch.md').read_text();expected=re.findall(r'\| `((?:000[1-8]-[^`]+\.patch)|llvm\.spec)` \| [\d,]+ \| `([0-9a-f]{64})`',text);assert len(expected)==9
checks=[]
for name,want in expected:
 p=out/name;got=sha(p);checks.append({'file':name,'expected':want,'actual':got,'pass':got==want});assert got==want,(name,got,want)
(E/'export-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
for p in out.iterdir():
 if p.suffix in ('.spec','.patch'):(E/p.name).write_bytes(p.read_bytes())
print('PREFLIGHT_AND_EXPORT_PASS',flush=True)
