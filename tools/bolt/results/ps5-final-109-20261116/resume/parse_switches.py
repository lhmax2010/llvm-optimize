
from pathlib import Path
import subprocess,os,json,re,datetime,hashlib,difflib,shlex
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt');E=Path(__file__).parent
S=W/'temp/ps5-final-109-20261116/source'
R=W/'temp/review-20261103/config-root/local/BUILD-ROOTS/scratch.x86_64.0'
M=B/'tools/bolt/results/fifth-review-20261111/rerun4/parse';N=W/'temp/hq-review-105-20261116/exports/candidate'
P=E/'parse';P.mkdir()
env=dict(os.environ,RPM_CONFIGDIR=str(R/'usr/lib/rpm'),LC_ALL='C',HOME=str(P))
loader=[str(R/'usr/lib64/ld-linux-x86-64.so.2'),'--library-path',str(R/'usr/lib64')]
def run(tag,argv):
 r=subprocess.run(argv,cwd=P,env=env,capture_output=True)
 (P/(tag+'.stdout')).write_bytes(r.stdout);(P/(tag+'.stderr')).write_bytes(r.stderr)
 (P/(tag+'.json')).write_text(json.dumps(dict(argv=argv,rc=r.returncode),indent=2))
 if r.returncode:raise RuntimeError(tag+': '+r.stderr.decode())
 return r.stdout.decode()
show=run('showrc',loader+[str(R/'usr/bin/rpmspec'),'--showrc'])
base=next(l.split(': ',1)[1] for l in show.splitlines() if l.startswith('Macro path:'))
base=':'.join(x for x in base.split(':') if x.startswith(str(R)))
rows=[]
def expand(label,spec,arch='x86_64',without=(),rollback=False,project='toolchain'):
 macro=P/(label+'.macros');key=project+'-'+('x86-debug' if arch=='x86_64' else arch)
 macro.write_bytes((M/(key+'.macros')).read_bytes())
 if rollback:
  t=spec.read_text();assert t.count('%bcond_without clang_bolt')==1
  spec=P/'rollback.spec';spec.write_text(t.replace('%bcond_without clang_bolt','%bcond_with clang_bolt',1))
 common=['--define','_topdir '+str(P/'rpm'),'--define','_builddir '+str(P/'rpm/BUILD'),'--macros',base+':'+str(macro),'--target',arch+'-tizen-linux','--define','_sourcedir '+str(N)]
 if project=='toolchain':common+=['--define','_toolchain clang']
 opts=sum((['--define','_without_'+x+' 1'] for x in without),[])
 text=run(label+'-expanded',loader+[str(R/'usr/bin/rpmspec'),'-P',*common,*opts,str(spec)])
 run(label+'-nobuild',loader+[str(R/'usr/bin/rpmbuild'),'-bp','--nodeps','--nobuild',*common,*opts,str(spec)])
 return text
def cmake(text):
 lines=text.splitlines();i=next(i for i,l in enumerate(lines) if l.strip()=='cmake \\')
 block=[]
 while True:
  line=lines[i];block.append(line);i+=1
  if not line.endswith('\\'):break
 return shlex.split('\n'.join(block).replace('\\\n',' '))
def difference(label,a,b):
 diff=''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),'baseline','candidate'))
 (P/(label+'.diff')).write_text(diff);return diff
for arch in ['x86_64','armv7l','aarch64']:
 old=expand('old-'+arch,E.parent/'baseline-spec.txt',arch)
 new=expand('default-'+arch,S/'packaging/llvm.spec',arch)
 d=difference('default-'+arch,old,new)
 row={'case':'default-'+arch,'PASS':not d,'byte_identical':not d};rows.append(row)
 (E/'parse-result.json').write_text(json.dumps(rows,indent=2))
 print(row,flush=True)
 if d:raise RuntimeError('STOP default expansion differs: '+arch+'\n'+d)
parent=expand('parent',E.parent/'parent-spec.txt')
for label,opts,rollback,hybrid,bolt in [
 ('total-off',['llvm_speedup'],False,False,False),
 ('hybrid-off',['hybrid_link'],False,False,True),
 ('bolt-off',['clang_bolt'],False,True,False),
 ('both-off',['hybrid_link','clang_bolt'],False,False,False),
 ('bcond-rollback',[],True,True,False)]:
 text=expand(label,S/'packaging/llvm.spec',without=opts,rollback=rollback)
 got_hybrid='-DTIZEN_HYBRID_LINK=ON' in text
 got_bolt=bool(re.search(r'^bolt_step\(\)',text,re.M))
 ok=got_hybrid==hybrid and got_bolt==bolt
 row={'case':label,'hybrid':got_hybrid,'bolt':got_bolt,'PASS':ok}
 if not hybrid:
  a=cmake(parent);b=cmake(text)
  (P/(label+'-cmake-argv.json')).write_text(json.dumps({'parent':a,'new':b,'equal':a==b},indent=2))
  row['cmake_argv_equals_parent']=a==b;row['PASS'] &= a==b
  row['hybrid_assertion_absent']='TIZEN_HYBRID_LINK_OK' not in text
  row['PASS'] &= row['hybrid_assertion_absent']
 if not bolt:row['PASS'] &= not any(x in text for x in ['BOLT_PIPELINE_PASS','BOLT_POST_GATE_PASS','BOLT_WORK='])
 row['fixed_flags_retained']='TIZEN_LLVM_FIXED_FLAGS' in text;row['PASS'] &= row['fixed_flags_retained']
 rows.append(row);(E/'parse-result.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
 if not row['PASS']:raise RuntimeError('STOP switch combination mismatch: '+label)
print('已结束',datetime.datetime.now().astimezone().isoformat(),'parse PASS cases='+str(len(rows)),flush=True)
