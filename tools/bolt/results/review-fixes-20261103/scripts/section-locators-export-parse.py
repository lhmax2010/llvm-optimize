from pathlib import Path
import subprocess,json,time,shutil,re,difflib
W=Path('/home/linhao/Toolchain/development/llvm-optimize');D=W/'temp/review-20261103';E=D/'evidence';S=W/'temp/review-20261102/source';R=D/'config-root/local/BUILD-ROOTS/scratch.x86_64.0';C=W/'temp/bolt-v4-20261021-disk-footprint/gbs_llvm_qb1202084.conf'
sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip();P=R/'home/abuild/review-parse';P.mkdir(exist_ok=True);X=D/('export-'+sha[:12]);PE=E/('section-locators-parse-'+sha[:12]);PE.mkdir(exist_ok=True)
def run(name,args):
 t=time.monotonic();p=subprocess.run(args,capture_output=True,text=True);(PE/(name+'.stdout')).write_text(p.stdout);(PE/(name+'.stderr')).write_text(p.stderr);r={'argv':args,'rc':p.returncode,'seconds':time.monotonic()-t};(PE/(name+'.json')).write_text(json.dumps(r,indent=2)+'\n');return r,p.stdout
r,_=run('gbs-export',['gbs','-c',str(C),'export','--spec','llvm.spec','--commit',sha,'--upstream-branch','sandbox/fangyu.he/llvm_optmize','--upstream-tag','upstream/22.1.8','--outdir-directly','-o',str(X),str(S)]);assert r['rc']==0
shutil.copytree(X,P/sha,dirs_exist_ok=True);spec=(X/'llvm.spec').read_text();(P/sha/'rollback.spec').write_text(spec.replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
prefix=['sudo','-n','chroot','--userspec=1000:1000',str(R),'/usr/bin/env','-i','HOME=/home/abuild','USER=abuild','LOGNAME=abuild','SHELL=/bin/sh','PATH=/bin:/usr/bin:/usr/local/sbin','LC_ALL=C','LANG=C']
r,o=run('rpm-version',prefix+['rpm','-q','--qf','%{NAME} %{VERSION}-%{RELEASE}\n','rpm','rpm-build']);assert r['rc']==0 and all(x.split()[1].startswith('4.14.1.1-') for x in o.splitlines())
rows=[]
for name,target,off,rollback in [('x86-on','x86_64-tizen-linux',False,False),('x86-off','x86_64-tizen-linux',True,False),('x86-rollback','x86_64-tizen-linux',False,True),('armv7l','armv7l-tizen-linux',False,False),('aarch64','aarch64-tizen-linux',False,False)]:
 path='/home/abuild/review-parse/'+sha+'/'+('rollback.spec' if rollback else 'llvm.spec')
 common=['--target',target,'--define','_sourcedir /home/abuild/review-parse/'+sha,'--define','_toolchain clang']
 r,_=run(name,prefix+['rpmbuild','-bp','--nodeps','--nobuild']+common+(['--without','clang_bolt'] if off else [])+[path]);rr,tt=run(name+'-expanded',prefix+['rpmspec','-P']+common+(['--define','_without_clang_bolt 1'] if off else [])+[path]);rows.append({'case':name,'rc':r['rc'],'expanded_rc':rr['rc'],'patches':[l for l in tt.splitlines() if re.match(r'^Patch\d+:',l)]});assert r['rc']==rr['rc']==0 and len(rows[-1]['patches'])==8,rows[-1]
(PE/'five-parse.json').write_text(json.dumps(rows,indent=2)+'\n')
parent=subprocess.check_output(['git','rev-parse','HEAD^'],cwd=S,text=True).strip();sources={'new':sha,'hybrid':parent,'previous':'3ee2d84719e4bd358c0b2366161f70f2eb788313'}
for label,commit in sources.items():(P/(label+'.spec')).write_bytes(subprocess.check_output(['git','show',commit+':packaging/llvm.spec'],cwd=S))
summary=[]
for mode,defs in [('debug',['--define','_toolchain clang']),('release',['--undefine','_toolchain'])]:
 outputs={}
 for label in sources:
  r,t=run('off-'+mode+'-'+label,prefix+['rpmspec','-P','--target','x86_64-tizen-linux','--define','_without_clang_bolt 1']+defs+['/home/abuild/review-parse/'+label+'.spec']);assert r['rc']==0;outputs[label]=t
 for other in ['hybrid','previous']:
  diff=''.join(difflib.unified_diff(outputs[other].splitlines(True),outputs['new'].splitlines(True),fromfile=other,tofile='new'));(PE/('off-'+mode+'-vs-'+other+'.diff')).write_text(diff);summary.append({'mode':mode,'against':other,'diff_lines':len(diff.splitlines())})
(PE/'off-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('FIVE_PARSE_PASS',sha,summary)
