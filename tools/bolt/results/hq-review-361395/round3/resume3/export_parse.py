from pathlib import Path
import subprocess,os,json,re,datetime,hashlib
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.with_name('llvm-optimize');E=Path(__file__).parent
N=W/'temp/hq-review-105-20261116/exports/candidate';R=W/'temp/review-20261103/config-root/local/BUILD-ROOTS/scratch.x86_64.0';M=B/'tools/bolt/results/fifth-review-20261111/rerun4/parse'
P=E/'native-parse';P.mkdir()
env=dict(os.environ,RPM_CONFIGDIR=str(R/'usr/lib/rpm'),LC_ALL='C',HOME=str(P))
loader=[str(R/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'usr/lib64')]
def run(tag,argv):
 r=subprocess.run(argv,cwd=P,env=env,capture_output=True)
 (P/(tag+'.stdout')).write_bytes(r.stdout);(P/(tag+'.stderr')).write_bytes(r.stderr)
 (P/(tag+'.json')).write_text(json.dumps(dict(argv=argv,rc=r.returncode),indent=2))
 assert r.returncode==0,(tag,r.stderr.decode())
 return r.stdout.decode()
show=run('showrc',loader+[str(R/'usr/bin/rpmspec'),'--showrc'])
base=next(l.split(': ',1)[1] for l in show.splitlines() if l.startswith('Macro path:'));base=':'.join(x for x in base.split(':') if x.startswith(str(R)));assert base
rows=[]
for name,arch,off,rollback in [('x86-on','x86_64',False,False),('x86-off','x86_64',True,False),('armv7l','armv7l',False,False),('aarch64','aarch64',False,False),('x86-rollback','x86_64',False,True)]:
 macro=P/(name+'.macros');key='toolchain-'+('x86-debug' if arch=='x86_64' else arch)
 macro.write_bytes((M/(key+'.macros')).read_bytes())
 spec=N/'llvm.spec'
 if rollback:
  t=spec.read_text();assert t.count('%bcond_without clang_bolt')==1
  spec=P/'rollback.spec';spec.write_text(t.replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
 common=['--define','_topdir '+str(P/name),'--define','_builddir '+str(P/name/'BUILD'),'--macros',base+':'+str(macro),'--target',arch+'-tizen-linux','--define','_sourcedir '+str(N),'--define','_toolchain clang']
 run(name+'-nobuild',loader+[str(R/'usr/bin/rpmbuild'),'-bp','--nodeps','--nobuild',*common,*(['--without','clang_bolt'] if off else []),str(spec)])
 txt=run(name+'-expanded',loader+[str(R/'usr/bin/rpmspec'),'-P',*common,*(['--define','_without_clang_bolt 1'] if off else []),str(spec)])
 patches=re.findall(r'^Patch\d*\s*:',txt,re.M)
 assert not patches,(name,patches)
 assert not re.search(r'^%patch\b',txt,re.M),name
 enabled=bool(re.search(r'^\s*bolt_step\(\)',txt,re.M))
 expected=(name=='x86-on')
 assert enabled==expected,(name,enabled,expected)
 srcs=re.findall(r'^Source\d*\s*:\s*(\S+)',txt,re.M)
 missing=[x for x in srcs if not (N/x).is_file()];assert not missing,(name,missing)
 row=dict(case=name,arch=arch,nobuild_rc=0,parse_rc=0,mode='native',patch_count=len(patches),bolt_enabled=enabled,sources=srcs,missing_sources=missing,expanded_sha256=hashlib.sha256(txt.encode()).hexdigest(),PASS=True)
 rows.append(row);print(row,flush=True)
(E/'five-parse-result.json').write_text(json.dumps(dict(PASS=True,cases=rows),indent=2))
print('105续三R3(e) 已结束 '+datetime.datetime.now().astimezone().isoformat()+' status=PASS',flush=True)
