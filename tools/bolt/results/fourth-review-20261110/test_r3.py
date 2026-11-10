from pathlib import Path
import importlib.util,sys,os,signal,time,struct,json,subprocess,unittest,shlex,re
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
E=Path(__file__).parent
W=Path('/home/linhao/Toolchain/development/llvm-optimize')
B=W.with_name('llvm-optimize-bolt');S=W/'temp/rebase-359934-20261106/source'
X=Path(os.environ['TEST_SCRATCH'])/'cases';X.mkdir()
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

class R4(unittest.TestCase):
 def test_pic_absolute_8_16_and_abs_exception(self):
  for kind in (12,14):
   for flags in (6,3):
    b=rel_fixture(kind);section_set(b,1,2,flags)
    self.assertEqual(len(a.pic_relocations(b)['forbidden']),1)
    b=rel_fixture(kind,True);section_set(b,1,2,flags)
    self.assertEqual(a.pic_relocations(b)['forbidden'],[])
 def test_pic_offsets_and_widths(self):
  for kind,width in ((1,8),(10,4),(11,4),(12,2),(14,1),(2,1)):
   for offset in (8,2**64-1,9-width):
    b=rel_fixture(kind,True);struct.pack_into('<Q',b,400,offset)
    with self.subTest(kind=kind,offset=offset),self.assertRaises(ValueError):a.pic_relocations(b)
   b=rel_fixture(kind,True);struct.pack_into('<Q',b,400,8-width)
   self.assertEqual(a.pic_relocations(b)['forbidden'],[])
 def test_pic_section_table_invalid(self):
  for off in (0,2**64-1):
   b=rel_fixture();struct.pack_into('<Q',b,40,off)
   with self.assertRaises(ValueError):a.pic_relocations(b)
  for stride in (0,40):
   b=rel_fixture();struct.pack_into('<H',b,58,stride)
   with self.assertRaises(ValueError):a.pic_relocations(b)
  for field in (6,7):
   b=rel_fixture();section_set(b,3,field,4)
   with self.assertRaises(ValueError):a.pic_relocations(b)
  for n in (0,16,63,64,255,319):
   with self.assertRaises(ValueError):a.pic_relocations(rel_fixture()[:n])
 def test_elf_details_name_index(self):
  b=bytearray(native());count=struct.unpack_from('<H',b,60)[0]
  struct.pack_into('<H',b,62,count)
  with self.assertRaises(ValueError):a.elf_details(b)
 def test_ar_size_syntax_and_longname_boundary(self):
  for text in ('1_0','+4',' 4','-1','-60'):
   p=X/('bad-size-'+text.replace(' ','space')+'.a')
   p.write_bytes(b'!<arch>\n'+ar_header('x/',text)+b'abcd')
   with self.assertRaisesRegex(ValueError,'size'):a.inspect(p)
  for off in (1,4):
   p=X/('bad-long-'+str(off)+'.a');p.write_bytes(b'!<arch>\n'+member('//',b'first.o/\nsecond.o/\n')+member('/'+str(off),b'BC\xc0\xde'))
   with self.assertRaises(ValueError):a.inspect(p)
  p=X/'good-long-second.a';p.write_bytes(b'!<arch>\n'+member('//',b'first.o/\nsecond.o/\n')+member('/9',b'BC\xc0\xde'))
  self.assertEqual(a.inspect(p)['members'][0]['name'],'second.o')
 @classmethod
 def real(cls):
  if hasattr(cls,'real_data'):return cls.real_data
  sys.path.insert(0,str(B/'tools/bolt/night-launch-20261103'))
  import validate
  R,BUILD,WORK=validate.rootpaths(W/'temp/night-20261103/basedev')
  d=X/'real';d.mkdir();wr=d/'tools';wr.mkdir()
  tools={}
  for name in ('clang-22','llvm-dis','llvm-nm','llvm-as'):
   p=wr/name;p.write_text('#!/bin/sh\nexec '+shlex.join([str(x) for x in validate.loader(R,R/'usr/bin'/name)])+' "$@"\n');p.chmod(0o755);tools[name]=p
  summary=json.loads((BUILD/'native-archive-conversion/summary.json').read_text())
  record=next(r for r in summary['archives'] if r['converted'])
  orig=BUILD/'lib64'/Path(record['path']).name
  m=next(m for m in a.inspect(orig)['members'] if m['kind']=='bitcode')
  with orig.open('rb') as f:f.seek(m['offset']);bc=f.read(m['size'])
  (d/'real-release.bc').write_bytes(bc)
  (d/'source.json').write_text(json.dumps(dict(path=str(orig),member=m),indent=2))
  cls.real_data=d,tools,bc
  return cls.real_data
 def run_real_convert(self,label,bc,converter=a):
  d,tools,_=self.real();p=d/label;p.mkdir();root=p/'root';root.mkdir();build=p/'build';build.mkdir()
  (build/'CMakeCache.txt').write_text('# test input, no CMake execution\n')
  (root/'fixture.a').write_bytes(archive([('member.bc',bc)]))
  answer=converter.convert(root,build/'evidence',tools['clang-22'],tools['llvm-dis'],tools['llvm-nm'],build,jobs=1,debug_info='no')
  return answer,build/'evidence/archives/fixture.a'
 def test_real_module_asm_short_byte_rejected(self):
  d,tools,bc=self.real()
  ll=subprocess.check_output([str(tools['llvm-dis']),str(d/'real-release.bc'),'-o','-'],text=True)
  for directive in ('short','byte'):
   source=d/(directive+'.ll');output=d/(directive+'.bc')
   source.write_text('module asm ".text\\0A.'+directive+' external_symbol"\n'+ll)
   p=subprocess.run([str(tools['llvm-as']),str(source),'-o',str(output)],capture_output=True,text=True)
   self.assertEqual(p.returncode,0,p.stderr)
   with self.assertRaisesRegex(ValueError,'non-PIC relocation'):self.run_real_convert('asm-'+directive,output.read_bytes())
 def test_old_new_real_conversion_bytes(self):
  d,tools,bc=self.real()
  rows=[]
  for label,converter in [('old',old),('new',a)]:
   answer,path=self.run_real_convert('bytes-'+label,bc,converter)
   info=converter.inspect(path);rows.append(dict(label=label,path=str(path),sha256=info['sha256'],members=info['members']))
   self.assertEqual(answer['status'],'CONVERTED')
  self.assertEqual(rows[0]['sha256'],rows[1]['sha256'])
  self.assertEqual([m['sha256'] for m in rows[0]['members']],[m['sha256'] for m in rows[1]['members']])
  observed.append(dict(case='old-new-real-conversion',rows=rows))
 def cli(self,label,mode,sig=0,ignore=False):
  d,tools,bc=self.real();p=d/label;p.mkdir();root=p/'root';root.mkdir();build=p/'build';build.mkdir();keep=p/'preserved';keep.mkdir()
  (build/'CMakeCache.txt').write_text('# no CMake\n')
  # A real release bitcode input, used also by the ignored-SIGCHLD exec probe.
  (root/'fixture.a').write_bytes(archive([('member.bc',bc)]))
  launcher=p/'probe.py'
  launcher.write_text("""import importlib.util,sys,signal,os,shutil,json
from pathlib import Path
source=SOURCE; mode=MODE; sig=SIGNAL; root=Path(ROOT); keep=root/'preserved'
sp=importlib.util.spec_from_file_location('a',source);a=importlib.util.module_from_spec(sp);sp.loader.exec_module(a)
moves=[]
def preserve(path,*args,**kwargs):
 path=Path(path)
 if not path.exists():
  if kwargs.get('missing_ok') or kwargs.get('ignore_errors'):return
  raise FileNotFoundError(str(path))
 assert path.resolve().is_relative_to(root)
 dest=keep/(str(len(moves))+'-'+path.name);path.rename(dest);moves.append(dict(source=str(path),saved=str(dest)))
Path.unlink=preserve;shutil.rmtree=preserve
real_install=a.install
if mode=='late':
 def install(*args,**kwargs):
  result=real_install(*args,**kwargs);os.kill(os.getpid(),sig);return result
 a.install=install
elif mode=='during':
 original_run=a.Commands.run
 def run(self,argv,prefix,stdout=None):
  if str(prefix).endswith('disassemble'):os.kill(os.getpid(),sig);self.check()
  return original_run(self,argv,prefix,stdout)
 a.Commands.run=run
try:sys.exit(a.install_main())
finally:(root/'preserved.json').write_text(json.dumps(moves,indent=2))
""".replace('SOURCE',repr(str(S/'packaging/llvm-static-archives-native.py'))).replace('MODE',repr(mode)).replace('SIGNAL',str(int(sig))).replace('ROOT',repr(str(p))))
  argv=[sys.executable,'-B',str(launcher),'--root',str(root),'--build',str(build),'--evidence',str(build/'evidence'),'--arch','x86_64','--debug-info','no','--jobs','1','--compiler',str(tools['clang-22']),'--disassembler',str(tools['llvm-dis']),'--nm',str(tools['llvm-nm'])]
  if ignore:
   argv=[sys.executable,'-B','-c','import signal,os,sys;signal.signal(signal.SIGCHLD,signal.SIG_IGN);os.execv(sys.argv[1],sys.argv[1:])',*argv]
  result=subprocess.run(argv,capture_output=True,text=True,timeout=60)
  (p/'stdout').write_text(result.stdout);(p/'stderr').write_text(result.stderr)
  observed.append(dict(case=label,argv=argv,rc=result.returncode,stdout=result.stdout,stderr=result.stderr))
  return result,p
 def test_cli_mid_conversion_signals(self):
  for sig in (signal.SIGTERM,signal.SIGHUP,signal.SIGINT):
   result,p=self.cli('during-'+str(sig),'during',sig)
   self.assertEqual(result.returncode,128+sig,result.stderr);self.assertIn('Traceback',result.stderr)
 def test_cli_after_last_check_signals(self):
  for sig in (signal.SIGTERM,signal.SIGHUP,signal.SIGINT):
   result,p=self.cli('late-'+str(sig),'late',sig)
   self.assertEqual(result.returncode,128+sig,result.stderr);self.assertIn('NATIVE_ARCHIVES_CANCELLED after completion',result.stdout)
 def test_cli_normal_versions_after_cleanup(self):
  result,p=self.cli('normal','normal')
  self.assertEqual(result.returncode,0,result.stderr)
  summary=json.loads((p/'build/evidence/summary.json').read_text())
  self.assertEqual(summary['tools']['tool_versions'],{'compiler':'22.1.8','disassembler':'22.1.8','nm':'22.1.8'})
  self.assertEqual(set(summary['tools']['version_texts']),{'compiler','disassembler','nm'})
  self.assertIn('NATIVE_ARCHIVES_TOOLS',result.stdout)
  self.assertTrue(all(v.strip() for v in summary['tools']['version_texts'].values()))
  self.assertFalse(list((p/'build/evidence').rglob('*.txt')))
  self.assertTrue(list((p/'preserved').iterdir()))
 def test_sigchld_ignore_exec_real_archive(self):
  result,p=self.cli('sigchld','normal',ignore=True)
  self.assertEqual(result.returncode,0,result.stderr);self.assertIn('NATIVE_ARCHIVES_SIGCHLD_RESET',result.stdout)
  self.assertIn('NATIVE_ARCHIVES_END',result.stdout);self.assertIn('PASS 1',result.stdout)
 def test_version_mismatch_before_archive(self):
  d,tools,bc=self.real();p=d/'version-negative';p.mkdir();root=p/'root';root.mkdir();build=p/'build';build.mkdir();(build/'CMakeCache.txt').write_text('fixture')
  wr=p/'bin';wr.mkdir();cl=wr/'clang';cl.write_text('#!/bin/sh\nprintf "clang version 22.1.8\n"\n');cl.chmod(0o755)
  dis=wr/'llvm-dis';dis.write_text('#!/bin/sh\nprintf "LLVM version 22.1.7\n"\n');dis.chmod(0o755)
  nm=wr/'llvm-nm';nm.write_text('#!/bin/sh\nprintf "LLVM version 22.1.8\n"\n');nm.chmod(0o755)
  (root/'fixture.a').write_bytes(archive([('member.bc',bc)]))
  with patch.object(a,'validate_archive') as scan:
   with self.assertRaisesRegex(ValueError,'version mismatch'):a.convert(root,build/'evidence',cl,dis,nm,build,jobs=1,debug_info='no')
   scan.assert_not_called()
 def test_shell_status_matrix(self):
  text=(E/'post-expanded.stdout').read_text()
  functions=text[text.index('bolt_fail() {'):text.index('bolt_step() {')]
  # Only the diagnostic command is replaced by a fixture; all three functions
  # under review are taken verbatim from the expanded production spec.
  functions=re.sub(r'python3 -B \S+ disk-diagnose[^\n]*','true',functions)
  results=[]
  for shell in ('/bin/sh','/bin/dash','/bin/bash'):
   for fn in ('bolt_checked','bolt_optional','bolt_status_exit'):
    for code in (0,1,2,129,130,143,137):
     cmd='/bin/sh -c '+shlex.quote('exit '+str(code))
     call=('bolt_checked fixture - '+cmd if fn=='bolt_checked' else 'bolt_optional '+cmd if fn=='bolt_optional' else cmd+' || bolt_status_exit $?')
     result=subprocess.run([shell,'-e','-c',functions+'\n'+call+'\necho CONTINUED\n'],capture_output=True,text=True)
     expect=0 if code==0 or (fn=='bolt_optional' and code not in (129,130,143)) else code if code in (129,130,143) else 1
     self.assertEqual(result.returncode,expect,(shell,fn,code,result.stderr))
     self.assertEqual('CONTINUED' in result.stdout,expect==0)
     results.append(dict(shell=shell,function=fn,input=code,returncode=result.returncode,continued='CONTINUED' in result.stdout))
    for sig in (signal.SIGTERM,signal.SIGHUP,signal.SIGINT):
     # The executable receives a real signal and dies with that signal. Its
     # parent shell converts wait status to 128+signal before function handling.
     cmd=shlex.join([sys.executable,'-B','-c','import os,signal;signal.signal('+str(int(sig))+',signal.SIG_DFL);os.kill(os.getpid(),'+str(int(sig))+')'])
     call=('bolt_checked fixture - '+cmd if fn=='bolt_checked' else 'bolt_optional '+cmd if fn=='bolt_optional' else cmd+' || bolt_status_exit $?')
     result=subprocess.run([shell,'-e','-c',functions+'\n'+call+'\necho CONTINUED\n'],capture_output=True,text=True)
     self.assertEqual(result.returncode,128+sig,(shell,fn,sig,result.stderr));self.assertNotIn('CONTINUED',result.stdout)
     results.append(dict(shell=shell,function=fn,real_signal=int(sig),returncode=result.returncode,continued=False))
  observed.append(dict(case='shell-status-matrix',rows=results))
 def test_process_states_at_run_return(self):
  p=X/'process-states';p.mkdir();script=p/'spawn.py'
  script.write_text("""import os,time,signal
from pathlib import Path
p=Path(ROOT);p.joinpath('direct').write_text(str(os.getpid()))
child=os.fork()
if child==0:
 signal.signal(signal.SIGTERM,signal.SIG_IGN);p.joinpath('grandchild').write_text(str(os.getpid()))
 while True:time.sleep(.01)
while not p.joinpath('grandchild').exists():time.sleep(.01)
""".replace('ROOT',repr(str(p))))
  command=a.Commands(timeout=10)
  command.run([sys.executable,'-B',str(script)],p/'run')
  def state(pid):
   try:
    fields=Path('/proc',str(pid),'stat').read_text().split(') ',1)[1].split()
    return dict(pid=pid,state='zombie' if fields[0]=='Z' else 'running',kernel_state=fields[0],pgrp=int(fields[2]))
   except FileNotFoundError:return dict(pid=pid,state='gone')
  direct=int((p/'direct').read_text());grandchild=int((p/'grandchild').read_text())
  rows=[state(direct),state(grandchild)]
  self.assertEqual(rows[0]['state'],'gone')
  self.assertNotEqual(rows[1]['state'],'running')
  group=[]
  for statfile in Path('/proc').glob('[0-9]*/stat'):
   try:
    fields=statfile.read_text().split(') ',1)[1].split()
    if int(fields[2])==direct:group.append(state(int(statfile.parent.name)))
   except (FileNotFoundError,PermissionError):pass
  self.assertFalse(any(row['state']=='running' for row in group))
  observed.append(dict(case='process-states-immediate',rows=rows,group=group))

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(R3),unittest.defaultTestLoader.loadTestsFromTestCase(R4)]))
 (E/'r3-observed.json').write_text(json.dumps(observed,indent=2)+'\n')
 (E/'r3-result.json').write_text(json.dumps(dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),PASS=result.wasSuccessful()),indent=2)+'\n')
 sys.exit(not result.wasSuccessful())
