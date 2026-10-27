from pathlib import Path
import subprocess,json,hashlib,configparser,os,time
D=Path(__file__).resolve().parent;W=D.parent.parent;E=W.parent/'llvm-optimize-bolt/tools/bolt/results/runpath-fix-20261026';S=D/'source';C=W/'temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf'
c=configparser.ConfigParser();c.read(C);profile=c[c['general']['profile']];bc=Path(profile['buildconf'])
assert hashlib.sha256(bc.read_bytes()).hexdigest()=='e5187fd758a663eec273a434090aaab9f8e32f80a036e3bca2cf0352dd286945'
assert profile['repos'].replace(' ','')=='repo.base_0,repo.base_debug_0'
urls=[c[n]['url'] for n in ('repo.base_0','repo.base_debug_0')];assert all('tizen-base-toolchain_20261013.024319' in u for u in urls)
(D/'tmp').mkdir(exist_ok=True)
cmd=['gbs','-c',str(C),'export','--spec','llvm.spec','--commit','aa637c1b4a0f9ea9f6f0317cf035126eba85aeb7','--upstream-branch','sandbox/fangyu.he/llvm_optmize','--upstream-tag','upstream/22.1.8','--outdir-directly','-o',str(D/'prep-export'),str(S)]
with (E/'prep-export.stdout').open('wb') as o,(E/'prep-export.stderr').open('wb') as e:p=subprocess.run(cmd,stdout=o,stderr=e,env={**os.environ,'TMPDIR':str(D/'tmp')})
(E/'prep-export.json').write_text(json.dumps({'argv':cmd,'rc':p.returncode},indent=2));assert p.returncode==0
R=D/'gbs-root/local/BUILD-ROOTS/scratch.x86_64.0'
cmd=['sudo','-n','/usr/bin/build','--uid','1000:1000','--root',str(R),'--dist',str(bc),'--arch','x86_64','--target','x86_64-tizen-linux','--stage=-bp','--debug','--baselibs','--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20']
for u in urls:cmd+=['--repo',u]
cmd+=[str(D/'prep-export/llvm.spec')]
(E/'prep-command.json').write_text(json.dumps(cmd,indent=2))
mem=int(next(l.split()[1] for l in Path('/proc/meminfo').read_text().splitlines() if l.startswith('MemTotal:')))*1024
argv=['systemd-run','--user','--wait','--pipe','--unit=runpath-fix-prep-20261026','-p','MemoryMax='+str(mem-8*1024**3),'-p','MemorySwapMax=0','-p','Nice=10','-p','IOSchedulingClass=best-effort','-p','IOSchedulingPriority=7','-p','OOMPolicy=stop',*cmd]
with (E/'prep.stdout').open('wb') as o,(E/'prep.stderr').open('wb') as e:p=subprocess.run(argv,stdout=o,stderr=e)
(E/'prep-result.json').write_text(json.dumps({'argv':argv,'rc':p.returncode},indent=2));print('PREP_EXIT',p.returncode,flush=True)
