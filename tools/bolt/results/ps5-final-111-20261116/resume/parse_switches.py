
from pathlib import Path
import subprocess,os,json,re,datetime,hashlib,difflib,shlex
from post_macro_gate import check_post
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt');E=Path(__file__).parent
S=W/'temp/ps5-final-111-20261116/source'
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
 # rpm -P omits the implicit install-post hook: explicitly expand it in
 # a temporary verification section and inspect that body, not the main text.
 probe=P/(label+'-post-probe.spec')
 probe.write_text(spec.read_text()+'\n%verifyscript\n# POST_PROBE_BEGIN\n%{__spec_install_post}\n# POST_PROBE_END\n')
 expanded=run(label+'-post-probe',loader+[str(R/'usr/bin/rpmspec'),'-P',*common,*opts,str(probe)])
 body=expanded.split('# POST_PROBE_BEGIN\n',1)[1].split('# POST_PROBE_END',1)[0]
 expected=(label!='parent' and arch=='x86_64' and not rollback and
           not any(x in without for x in ('llvm_speedup','clang_bolt')))
 counts=check_post(body,expected)
 (P/(label+'-post-result.json')).write_text(json.dumps({'enabled':expected,'counts':counts,'body':body},indent=2))
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
 old=expand('old-'+arch,E/'baseline-spec.txt',arch)
 new=expand('default-'+arch,S/'packaging/llvm.spec',arch)
 rawdiff=difference('default-'+arch,old,new)
 old_lines=old.splitlines(True);new_lines=new.splitlines(True)
 old_blanks=[i+1 for i,x in enumerate(old_lines) if not x.strip()]
 new_blanks=[i+1 for i,x in enumerate(new_lines) if not x.strip()]
 old_body=''.join(x for x in old_lines if x.strip())
 new_body=''.join(x for x in new_lines if x.strip())
 accepted_macro_prefix=old_body==new_body
 d='' if accepted_macro_prefix else rawdiff
 row={'case':'default-'+arch,'PASS':accepted_macro_prefix,
      'byte_identical':not rawdiff,'baseline_blank_line_positions':old_blanks,
      'candidate_blank_line_positions':new_blanks,
      'baseline_blank_count':len(old_blanks),'candidate_blank_count':len(new_blanks),
      'nonblank_byte_identical':old_body==new_body,
      'python_minimum_present':bool(re.search(r'^BuildRequires:\s*python3\s*>=\s*3[.]9\s*$',new,re.M))};rows.append(row)
 row['PASS'] &= row['python_minimum_present']==(arch=='x86_64')
 (E/'parse-result.json').write_text(json.dumps(rows,indent=2))
 print(row,flush=True)
 if d:raise RuntimeError('STOP default expansion differs: '+arch+'\n'+d)
parent=expand('parent',E/'parent-spec.txt')
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
  resets=['-DTIZEN_HYBRID_LINK=OFF','-UBUILD_SHARED_LIBS','-ULLVM_TOOL_LLVM_DRIVER_BUILD']
  reset_counts={x:b.count(x) for x in resets}
  restored=[x for x in b if x not in resets]
  row['reset_counts']=reset_counts
  row['cmake_argv_equals_parent_after_three_resets']=restored==a
  row['PASS'] &= restored==a and all(n==1 for n in reset_counts.values())
  (P/(label+'-cmake-reset-proof.json')).write_text(json.dumps({'parent':a,'new':b,'resets':resets,'counts':reset_counts,'without_resets':restored,'equal':restored==a},indent=2))
  row['hybrid_assertion_absent']='TIZEN_HYBRID_LINK_OK' not in text
  row['PASS'] &= row['hybrid_assertion_absent']
 if not bolt:row['PASS'] &= not any(x in text for x in ['BOLT_PIPELINE_PASS','BOLT_WORK='])
 row['python_minimum_retained']=bool(re.search(r'^BuildRequires:\s*python3\s*>=\s*3[.]9\s*$',text,re.M))
 row['bolt_dependencies_correct']=('BuildRequires: xz elfutils' in text)==bolt
 row['PASS'] &= row['python_minimum_retained'] and row['bolt_dependencies_correct']
 row['fixed_flags_retained']='TIZEN_LLVM_FIXED_FLAGS' in text;row['PASS'] &= row['fixed_flags_retained']
 rows.append(row);(E/'parse-result.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
 if not row['PASS']:raise RuntimeError('STOP switch combination mismatch: '+label)
print('已结束',datetime.datetime.now().astimezone().isoformat(),'parse PASS cases='+str(len(rows)),flush=True)
