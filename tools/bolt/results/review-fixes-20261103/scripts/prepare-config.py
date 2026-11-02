from pathlib import Path
import subprocess,json,configparser,shutil,time
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=W.parent/'llvm-optimize-bolt';D=W/'temp/review-20261103';E=D/'evidence';S=W/'temp/review-20261102/source';C=W/'temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf';R=D/'config-root/local/BUILD-ROOTS/scratch.x86_64.0'
def run(name,args):
 (E/(name+'.argv.json')).write_text(json.dumps(args,indent=2)+'\n');t=time.time()
 with (E/(name+'.stdout')).open('wb') as o,(E/(name+'.stderr')).open('wb') as e:r=subprocess.run(args,stdout=o,stderr=e)
 (E/(name+'.result.json')).write_text(json.dumps({'rc':r.returncode,'seconds':time.time()-t})+'\n');assert r.returncode==0,name
run('export-hybrid',['gbs','-c',str(C),'export','--spec','llvm.spec','--commit','6e9d4f2bc77e20ba96d586680bb4f4c25eace7d2','--upstream-branch','sandbox/fangyu.he/llvm_optmize','--upstream-tag','upstream/22.1.8','--outdir-directly','-o',str(D/'export-hybrid'),str(S)])
c=configparser.ConfigParser();c.read(C);prof=c[c['general']['profile']]
args=['sudo','-n','/usr/bin/build','--uid','1000:1000','--root',str(R),'--dist',prof['buildconf'],'--arch','x86_64','--target','x86_64-tizen-linux','--stage=-bp','--debug','--baselibs','--define','jobs 8','--define','_smp_mflags -j8','--define','_costomized_smp_mflags -j20']
for n in ['repo.base_0','repo.base_debug_0']:args+=['--repo',c[n]['url']]
args+=[str(D/'export-hybrid/llvm.spec')];run('prepare-root',args)
print('PREPARE_DONE',flush=True)
