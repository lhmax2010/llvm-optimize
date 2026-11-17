
from pathlib import Path
import subprocess,os,json,re,datetime,hashlib,difflib,shlex
from post_macro_gate import check_post
W=Path('/home/linhao/Toolchain/development/llvm-optimize');B=Path(str(W)+'-bolt');E=Path(__file__).parent
S=W/'temp/ps5-helper-118/source'
R=W/'temp/review-20261103/config-root/local/BUILD-ROOTS/scratch.x86_64.0'
M=B/'tools/bolt/results/fifth-review-20261111/rerun4/parse';N=W/'temp/hq-review-105-20261116/exports/candidate'
P=E/'truth-table-final';P.mkdir()
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

import itertools,unittest,ast,sys
# Admission controlled by the task118 service resource limits.
cases={}
for speed,hybrid,bolt in itertools.product((False,True),repeat=3):
 label='switch-'+''.join(str(int(x)) for x in (speed,hybrid,bolt))
 without=[name for name,value in zip(('llvm_speedup','hybrid_link','clang_bolt'),(speed,hybrid,bolt)) if not value]
 text=expand(label,S/'packaging/llvm.spec',without=without)
 cases[label]=(speed,hybrid,bolt,text)
class P1P2Tests(unittest.TestCase):
 def test_p1_off_matches_parent_except_three_resets(self):
  old=cmake((E/'parse/parent-expanded.stdout').read_text())
  new=cmake(cases['switch-000'][3])
  resets=['-DTIZEN_HYBRID_LINK=OFF','-UBUILD_SHARED_LIBS','-ULLVM_TOOL_LLVM_DRIVER_BUILD']
  self.assertEqual([new.count(x) for x in resets],[1,1,1])
  self.assertEqual([x for x in new if x not in resets],old)
 def test_p1_reset_order(self):
  args=cmake(cases['switch-101'][3])
  i=args.index('-DTIZEN_HYBRID_LINK=OFF')
  self.assertEqual(args[i:i+5],['-DTIZEN_HYBRID_LINK=OFF','-UBUILD_SHARED_LIBS','-ULLVM_TOOL_LLVM_DRIVER_BUILD','-DLLVM_LINK_LLVM_DYLIB=OFF','-DCLANG_LINK_CLANG_DYLIB=OFF'])
 def test_p1_no_resets_with_hybrid_enabled(self):
  args=cmake(cases['switch-111'][3])
  for x in ['-DTIZEN_HYBRID_LINK=OFF','-UBUILD_SHARED_LIBS','-ULLVM_TOOL_LLVM_DRIVER_BUILD']:
   self.assertNotIn(x,args)
 def test_p2_python_when_bolt_disabled(self):
  for label in ['switch-000','switch-100','switch-110']:
   text=cases[label][3]
   self.assertRegex(text,r'BuildRequires:\s*python3\s*>=\s*3[.]9')
   self.assertNotIn('BuildRequires: xz elfutils',text)
 def test_p2_arm_expansion_unchanged_without_python_requirement(self):
  for arch in ['armv7l','aarch64']:
   old=(E/('parse/old-'+arch+'-expanded.stdout')).read_text()
   new=(E/('parse/default-'+arch+'-expanded.stdout')).read_text()
   self.assertEqual(''.join(x for x in old.splitlines(True) if x.strip()),''.join(x for x in new.splitlines(True) if x.strip()))
   self.assertNotRegex(new,r'BuildRequires:\s*python3\s*>=\s*3[.]9')
 def test_s2_comment_only_helper_change(self):
  old=subprocess.check_output(['git','-C',str(S),'show','56902c58ba8fc2d3a4216e69ed3acb3d2cb6f8a3:packaging/clang-bolt-helper.py']).decode()
  # Historical S2 assertion stays scoped to H; task114 intentionally changes AST.
  new=subprocess.check_output(['git','-C',str(S),'show','378f8d5c94aeadd2a8618d04ad39a531529c726c:packaging/clang-bolt-helper.py']).decode()
  self.assertEqual(ast.dump(ast.parse(old)),ast.dump(ast.parse(new)))
def make_case(label):
 def check(self):
  speed,hybrid,bolt,text=cases[label];h=speed and hybrid;b=speed and bolt
  self.assertEqual('-DTIZEN_HYBRID_LINK=ON' in text,h)
  self.assertEqual('-DTIZEN_HYBRID_LINK=OFF' in text,not h)
  self.assertEqual(bool(re.search(r'^bolt_step\(\)',text,re.M)),b)
  self.assertEqual('BuildRequires: xz elfutils' in text,b)
  self.assertRegex(text,r'BuildRequires:\s*python3\s*>=\s*3[.]9')
  self.assertIn('TIZEN_LLVM_FIXED_FLAGS',text)
  post=json.loads((P/(label+'-post-result.json')).read_text())
  self.assertEqual(post['enabled'],b)
 return check
for label in cases:setattr(P1P2Tests,'test_'+label.replace('-','_'),make_case(label))
r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(P1P2Tests))
result={'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'PASS':r.wasSuccessful(),'combinations':list(cases)}
(E/'p1p2-result.json').write_text(json.dumps(result,indent=2));print(result)
print('已结束',datetime.datetime.now().astimezone().isoformat(),'P1/P2',result['PASS'])
sys.exit(0 if r.wasSuccessful() else 1)
