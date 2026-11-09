from pathlib import Path
import importlib.util,sys,os,signal,time,struct,json,subprocess,unittest,shlex,re
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
E=Path(__file__).parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=W.with_name('llvm-optimize-bolt');S=W/'temp/rebase-359934-20261106/source'
X=W/'temp/third-code-review-20261109/resume/r3-tests';X.mkdir()
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
a=load('converter',S/'packaging/llvm-static-archives-native.py')
old=load('old_converter',E/'baseline-llvm-static-archives-native.py')
sys.path.insert(0,str(B/'tools'))
from test_inspect_llvm_archives import archive,member,native
observed=[]
def ar_header(name,size):
 return f'{name:<16}{0:<12}{0:<6}{0:<6}{100644:<8}{size:<10}\x60\n'.encode()
def rel_fixture(kind=2,abs_symbol=False,rela=True):
 # Four ELF64 section headers; trailing fake SHN_ABS symbol lies in-file,
 # but deliberately beyond the symbol table's declared two entries.
 header=b'\x7fELF'+bytes([2,1,1])+b'\0'*9+struct.pack('<HHIQQQIHHHHHH',1,62,1,0,0,64,0,64,0,0,64,4,0)
 syms=b'\0'*24+struct.pack('<IBBHQQ',0,0x10,0,0xfff1 if abs_symbol else 1,0,8)
 fake=struct.pack('<IBBHQQ',0,0x10,0,0xfff1,0,0)
 rel=struct.pack('<QQ',0,(1<<32)|kind)+(struct.pack('<q',0) if rela else b'')
 sh=lambda typ,flags,offset,size,link=0,info=0,entsize=0:struct.pack('<IIQQQQIIQQ',0,typ,flags,0,offset,size,link,info,8,entsize)
 return bytearray(header+b'\0'*64+sh(1,6,320,8)+sh(2,0,328,48,entsize=24)+sh(4 if rela else 9,0,400,len(rel),2,1,len(rel))+b'\x90'*8+syms+fake+rel)
def section_set(b,idx,field,value):
 p=64+64*idx
 row=list(struct.unpack_from('<IIQQQQIIQQ',b,p));row[field]=value
 struct.pack_into('<IIQQQQIIQQ',b,p,*row)
def alive(pid):
 try:return Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()[0]!='Z'
 except FileNotFoundError:return False
class R3(unittest.TestCase):
 def inspect_data(self,name,data):
  p=X/(name+'.a');p.write_bytes(data)
  before=time.monotonic()
  def expired(*_):raise TimeoutError('ar exceeded one second')
  old_handler=signal.signal(signal.SIGALRM,expired);signal.setitimer(signal.ITIMER_REAL,1)
  try:return a.inspect(p)
  finally:
   signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old_handler)
   observed.append(dict(case=name,seconds=time.monotonic()-before))
 def test_ar_bad_lengths_and_names(self):
  bad={'size-minus60':b'!<arch>\n'+ar_header('x/',-60),'size-minus1':b'!<arch>\n'+ar_header('x/',-1),
   'bsd-negative':b'!<arch>\n'+member('#1/-1',b'ab'),'bsd-too-long':b'!<arch>\n'+member('#1/3',b'ab'),
   'gnu-negative':b'!<arch>\n'+member('//',b'long-name.o/\n')+member('/-1',b'ab'),
   'gnu-too-long':b'!<arch>\n'+member('//',b'name/\n')+member('/6',b'ab'),
   'missing-padding':b'!<arch>\n'+member('x/',b'a')[:-1],
   'stored-too-long':b'!<arch>\n'+ar_header('x/',8)+b'ab',
   'thin-negative-stored':b'!<thin>\n'+ar_header('#1/-1',1)}
  for label,data in bad.items():
   with self.subTest(case=label),self.assertRaises(ValueError):self.inspect_data(label,data)
 def test_ar_positive_duplicate_longnames_indexes(self):
  r=self.inspect_data('duplicates',archive([('same.o',native('a')),('same.o',native('b'))],[('a',0),('b',1)]))
  self.assertEqual([m['occurrence'] for m in r['members']],[1,2]);self.assertTrue(r['index_equals_machine_symbols'])
  for wide in [False,True]:
   self.assertTrue(self.inspect_data('index-'+str(wide),archive([('x.o',native())],[('foo',0)],wide))['index_equals_machine_symbols'])
  r=self.inspect_data('gnu-good',b'!<arch>\n'+member('//',b'very-long-name.o/\n')+member('/0',b'BC\xc0\xde'))
  self.assertEqual(r['members'][0]['name'],'very-long-name.o')
  name=b'very-long-bsd-name.o'
  r=self.inspect_data('bsd-good',b'!<arch>\n'+member('#1/'+str(len(name)),name+b'BC\xc0\xde'))
  self.assertEqual(r['members'][0]['name'],name.decode());self.assertEqual(r['bitcode'],1)
 def test_pic_legal(self):
  for rela in (False,True):
   for kind,absolute in [(10,True),(1,True),(2,False),(9,False)]:
    self.assertEqual(a.pic_relocations(rel_fixture(kind,absolute,rela)),{'checked':1,'forbidden':[]})
  self.assertEqual(len(a.pic_relocations(rel_fixture(10))['forbidden']),1)
 def test_pic_invalid_symbol_indexes(self):
  for index in (2,9999):
   b=rel_fixture();struct.pack_into('<Q',b,408,(index<<32)|10)
   with self.assertRaisesRegex(ValueError,'symbol index outside'):a.pic_relocations(b)
 def test_pic_invalid_symbol_tables(self):
  for field,value in [(1,3),(9,0),(9,16),(5,47),(4,10000),(5,24000)]:
   b=rel_fixture();section_set(b,2,field,value)
   with self.subTest(field=field,value=value),self.assertRaises(ValueError):a.pic_relocations(b)
 def test_pic_invalid_relocation_tables(self):
  for rela in (False,True):
   for field,value in [(9,0),(9,8),(5,1),(4,10000),(5,24000)]:
    b=rel_fixture(rela=rela);section_set(b,3,field,value)
    with self.subTest(rela=rela,field=field,value=value),self.assertRaises(ValueError):a.pic_relocations(b)
   with self.assertRaises(ValueError):a.pic_relocations(rel_fixture(rela=rela)[:-1])
 def versions(self,tag,other=False):
  d=X/tag;d.mkdir();(d/'bin').mkdir();(d/'other').mkdir();(d/'CMakeCache.txt').write_text('fixture')
  tools=[]
  for name in ('clang','llvm-dis','llvm-nm'):
   p=d/('other' if other and name=='llvm-nm' else 'bin')/name;p.write_text('fixture');p.chmod(0o755);tools.append(p)
  class Commands:
   def run(self,argv,prefix,stdout):
    stdout.write(('clang version 22.1.8\n' if Path(argv[0]).name=='clang' else 'LLVM version 22.1.8\n').encode())
  return a.validate_tools(d,*tools,Commands(),d)
 def test_tools_same_build_bin(self):self.assertIn('compiler_sha256',self.versions('same-bin'))
 def test_tools_other_nm_directory(self):
  with self.assertRaisesRegex(ValueError,'nm directory differs'):self.versions('other-bin',True)
 def test_messages(self):
  ids=subprocess.check_output(['git','rev-list','--reverse','13c3e223..HEAD'],cwd=S,text=True).splitlines()
  self.assertEqual(len(ids),3)
  for c in ids:
   msg=subprocess.check_output(['git','show','-s','--format=%B',c],cwd=S,text=True).strip()
   self.assertLessEqual(max(map(len,msg.splitlines())),72)
   trailers=subprocess.check_output(['git','interpret-trailers','--parse'],cwd=S,input=msg,text=True).splitlines()
   self.assertEqual(sorted(x.split(':',1)[0] for x in trailers),['Change-Id','Signed-off-by'])
   self.assertEqual(msg.rsplit('\n\n',1)[-1].splitlines(),trailers)
 def test_required_step_signals_and_failure(self):
  text=(E/'post-expanded.stdout').read_text()
  functions=text[text.index('bolt_fail() {'):text.index('bolt_optional python3 -B ')]
  for sig in (signal.SIGTERM,signal.SIGHUP,signal.SIGINT,None):
   d=X/('required-'+str(sig));d.mkdir();ready=d/'ready';after=d/'after'
   wrapper=d/'helper.py'
   wrapper.write_text("""from pathlib import Path
import importlib.util,sys,os,time
spec=importlib.util.spec_from_file_location('h',HELPER);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
def diagnose(*a,**kw):print('BOLT_DISK_DIAGNOSIS fixture')
h.disk_diagnose=diagnose
def step(*a,**kw):
 Path(READY).write_text(str(os.getpid()))
 if NORMAL:raise h.GateError('ordinary step failure')
 while True:h.check_cancel();time.sleep(.01)
h.run_step=step
sys.exit(h.cli())
""".replace('HELPER',repr(str(S/'packaging/clang-bolt-helper.py'))).replace('READY',repr(str(ready))).replace('NORMAL',repr(sig is None)))
   body=re.sub(r'python3 -B \S+',shlex.join([sys.executable,'-B',str(wrapper)]),functions)
   script=d/'test.sh';script.write_text('BOLT_WORK='+shlex.quote(str(d))+'\n'+body+'\nbolt_step probe /bin/true\nprintf after > '+shlex.quote(str(after))+'\n')
   p=subprocess.Popen(['/bin/sh','-e',str(script)],cwd=d,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   try:
    end=time.monotonic()+10
    while not ready.exists() and p.poll() is None and time.monotonic()<end:time.sleep(.01)
    self.assertTrue(ready.exists())
    if sig:os.kill(int(ready.read_text()),sig)
    out,err=p.communicate(timeout=10)
    self.assertEqual(p.returncode,128+sig if sig else 1,(out,err));self.assertFalse(after.exists())
    if sig:self.assertNotIn('BOLT_DISK_DIAGNOSIS',out+err)
    else:self.assertIn('BOLT_DISK_DIAGNOSIS',out+err)
    observed.append(dict(case='required-step',signal=int(sig) if sig else None,rc=p.returncode,stdout=out,stderr=err))
   finally:
    if p.poll() is None:p.kill();p.wait()
 def command_probe(self,tag,scenario):
  d=X/tag;d.mkdir();script=d/'worker.py'
  # Every probe creates a fresh session only through Commands.run.
  script.write_text("""import os,signal,time,sys
from pathlib import Path
mode=sys.argv[1];root=Path(sys.argv[2])
if mode=='normal':
 for i in range(500000):pass
 sys.exit(0)
if mode=='fail':
 while not (root/'other-ready').exists():time.sleep(.01)
 sys.exit(1)
if mode=='other':
 child=os.fork()
 if not child:
  signal.signal(signal.SIGTERM,signal.SIG_IGN)
  (root/'grandchild').write_text(str(os.getpid()))
  (root/'other-ready').write_text('ready')
  while True:time.sleep(.02)
 while True:time.sleep(.02)
if mode=='leader':
 child=os.fork()
 if not child:
  signal.signal(signal.SIGTERM,signal.SIG_IGN)
  (root/'grandchild').write_text(str(os.getpid()))
  while True:time.sleep(.02)
 while not (root/'grandchild').exists():time.sleep(.01)
 sys.exit(0)
if mode=='hup':
 (root/'ready').write_text('ready')
 while True:time.sleep(.02)
""")
  events=[];cmd=a.Commands(timeout=10);real_kill=os.killpg;real_wait=os.wait4
  def kill(pid,sig):
   events.append(['signal',pid,int(sig)])
   return real_kill(pid,sig)
  def reap(pid,flags):
   events.append(['reap',pid,flags,cmd.lock.locked()])
   return real_wait(pid,flags)
  with patch.object(a.os,'killpg',kill),patch.object(a.os,'wait4',reap):
   if scenario=='workers':
    with ThreadPoolExecutor(max_workers=2) as pool:
     futures=[pool.submit(cmd.run,[sys.executable,'-B',str(script),mode,str(d)],d/mode) for mode in ('other','fail')]
     for f in futures:
      with self.assertRaises(RuntimeError):f.result(timeout=15)
   elif scenario=='hup':
    oldhandler=signal.signal(signal.SIGHUP,cmd.interrupted)
    try:
     with ThreadPoolExecutor(max_workers=1) as pool:
      future=pool.submit(cmd.run,[sys.executable,'-B',str(script),'hup',str(d)],d/'hup')
      end=time.monotonic()+10
      while not (d/'ready').exists() and time.monotonic()<end:time.sleep(.01)
      self.assertTrue((d/'ready').exists());os.kill(os.getpid(),signal.SIGHUP)
      with self.assertRaises(RuntimeError):future.result(timeout=15)
    finally:signal.signal(signal.SIGHUP,oldhandler)
   else:
    result=cmd.run([sys.executable,'-B',str(script),scenario,str(d)],d/scenario)
    self.assertEqual(result['exit'],0);self.assertGreater(result['max_rss_kib'],0)
    self.assertGreaterEqual(result['user'],0);self.assertGreaterEqual(result['sys'],0)
    if scenario=='normal':
     before=old.Commands(timeout=10).run([sys.executable,'-B',str(script),'normal',str(d)],d/'old-normal')
     self.assertEqual(result['exit'],before['exit'])
     for key in ('user','sys','max_rss_kib'):
      self.assertIsInstance(result[key],type(before[key]))
     # Different executions have different usage; both must expose actual wait4 fields.
     observed.append(dict(case='normal-accounting',new=result,old=before))
  # Ignore the old implementation's separate normal probe for this order check.
  reaps=[(i,e) for i,e in enumerate(events) if e[0]=='reap' and e[3]]
  self.assertTrue(reaps)
  for i,event in reaps:
   pid=event[1];kills=[j for j,e in enumerate(events) if e[:3]==['signal',pid,int(signal.SIGKILL)]]
   self.assertTrue(kills,(pid,events));self.assertLess(max(kills),i);self.assertEqual(event[2],0)
   self.assertFalse(any(e[0]=='signal' and e[1]==pid for e in events[i+1:]))
  self.assertEqual(cmd.children,set())
  if (d/'grandchild').exists():
   pid=int((d/'grandchild').read_text());end=time.monotonic()+2
   while alive(pid) and time.monotonic()<end:time.sleep(.01)
   self.assertFalse(alive(pid),pid)
  observed.append(dict(case=scenario,events=events))
 def test_converter_sighup(self):
  source=(S/'packaging/llvm-static-archives-native.py').read_text()
  self.assertEqual(source.count('for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)'),2)
  self.command_probe('cancel-hup','hup')
 def test_converter_exited_leader_descendant(self):self.command_probe('exited-leader','leader')
 def test_converter_worker_failure(self):self.command_probe('worker-failure','workers')
 def test_converter_normal_wait4(self):self.command_probe('normal-wait4','normal')
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(R3))
 (E/'r3-observed.json').write_text(json.dumps(observed,indent=2)+'\n')
 (E/'r3-result.json').write_text(json.dumps(dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),PASS=result.wasSuccessful()),indent=2)+'\n')
 sys.exit(not result.wasSuccessful())
