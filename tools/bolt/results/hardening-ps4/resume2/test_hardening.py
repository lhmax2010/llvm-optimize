import importlib.util,unittest,struct,io,contextlib,json,os,signal,sys
from pathlib import Path
from unittest.mock import patch
P=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/hardening-ps4-20261114/source/packaging/llvm-static-archives-native.py')
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
a=load('new',P);old=load('old',Path(__file__).resolve().parent.parent/'baseline-converter.py')
def fixture(kind=2,offset=0,compressed=False,typ=1,alignment=1,size=24):
 header=b'\x7fELF'+bytes([2,1,1])+b'\0'*9+struct.pack('<HHIQQQIHHHHHH',1,62,1,0,0,64,0,64,0,0,64,4,0)
 sh=lambda t,f,o,n,l=0,i=0,e=0:struct.pack('<IIQQQQIIQQ',0,t,f,0,o,n,l,i,8,e)
 target=struct.pack('<IIQQ',typ,0,100,alignment) if compressed else b'\x90'*8
 syms=b'\0'*24+struct.pack('<IBBHQQ',0,0x10,0,0xfff1,0,8)
 rel=struct.pack('<QQq',offset,(1<<32)|kind,0)
 return bytearray(header+b'\0'*64+sh(1,0x800 if compressed else 6,320,size if compressed else 8)+sh(2,0,344,48,0,0,24)+sh(4,0,392,24,2,1,24)+target+b'\0'*(24-len(target))+syms+rel)
class Hardening(unittest.TestCase):
 def test_chdr_known_types_alignment(self):
  for typ in (1,2):
   for align in (0,1,2,8,2**63):
    with self.subTest(typ=typ,align=align):
     b=fixture(compressed=True,typ=typ,alignment=align,offset=96);self.assertEqual(a.pic_relocations(b),old.pic_relocations(b))
 def test_chdr_unknown_types(self):
  for typ in (0,3,0xffffffff):
   with self.subTest(typ=typ),self.assertRaisesRegex(ValueError,'unsupported ELF compression type'):
    a.pic_relocations(fixture(compressed=True,typ=typ))
 def test_chdr_short(self):
  with self.assertRaisesRegex(ValueError,'short compressed'):a.pic_relocations(fixture(compressed=True,size=23))
 def test_chdr_bad_alignment(self):
  for align in (3,6,2**64-1):
   with self.subTest(align=align),self.assertRaisesRegex(ValueError,'invalid compressed ELF section alignment'):
    a.pic_relocations(fixture(compressed=True,alignment=align))
 def test_chdr_declared_boundary(self):
  self.assertEqual(a.pic_relocations(fixture(compressed=True,offset=96)),dict(checked=0,forbidden=[]))
  with self.assertRaisesRegex(ValueError,'offset outside'):a.pic_relocations(fixture(compressed=True,offset=97))
 def test_zero_width_inside(self):
  for off in (0,7):self.assertEqual(a.pic_relocations(fixture(35,off)),old.pic_relocations(fixture(35,off)))
 def test_zero_width_end_and_beyond(self):
  for off in (8,9):
   with self.subTest(offset=off),self.assertRaisesRegex(ValueError,'offset outside'):a.pic_relocations(fixture(35,off))
 def test_zero_width_compressed_boundary(self):
  self.assertEqual(a.pic_relocations(fixture(35,99,True)),dict(checked=0,forbidden=[]))
  with self.assertRaisesRegex(ValueError,'offset outside'):a.pic_relocations(fixture(35,100,True))
 def test_none_unchanged(self):
  for off in (0,8,9,2**64-1):self.assertEqual(a.pic_relocations(fixture(0,off)),old.pic_relocations(fixture(0,off)))
 def test_relr_rejected_even_empty(self):
  for idx in (0,1,3):
   b=fixture();struct.pack_into('<I',b,64+64*idx+4,19)
   with self.subTest(section=idx),self.assertRaisesRegex(ValueError,'unsupported RELR'):a.pic_relocations(b)
 def test_regular_relocations_unchanged(self):
  for kind in (1,2,10,11,12,14,35):self.assertEqual(a.pic_relocations(fixture(kind)),old.pic_relocations(fixture(kind)))
 def context(self,env,states):
  out=io.StringIO()
  with patch.dict(os.environ,env,clear=True),patch.object(a.signal,'getsignal',side_effect=lambda s:states[s]),contextlib.redirect_stdout(out):a.log_startup_context()
  lines=out.getvalue().splitlines();self.assertEqual(len(lines),1);self.assertTrue(lines[0].startswith('NATIVE_ARCHIVES_STARTUP '));return json.loads(lines[0].split(' ',1)[1])
 def test_startup_architecture_and_states(self):
  handler=lambda *_:None
  s={signal.SIGTERM:signal.SIG_IGN,signal.SIGINT:signal.SIG_DFL,signal.SIGHUP:handler}
  r=self.context({'CFLAGS':'-O3 -m64 -march=old -march=nehalem -msse4.2 -mfpmath=sse -g','CXXFLAGS':'-O3 -mtune=generic -DSECRET=omitted'},s)
  self.assertEqual(r,{'architecture_parameters':{'CFLAGS':['-m64','-march=old','-march=nehalem','-msse4.2','-mfpmath=sse'],'CXXFLAGS':['-mtune=generic']},'signals':{'SIGTERM':'ignored','SIGINT':'default','SIGHUP':'handler'}})
 def test_startup_all_signal_states(self):
  for state,name in ((signal.SIG_IGN,'ignored'),(signal.SIG_DFL,'default'),(lambda *_:None,'handler')):
   r=self.context({},dict.fromkeys((signal.SIGTERM,signal.SIGINT,signal.SIGHUP),state));self.assertEqual(set(r['signals'].values()),{name});self.assertEqual(r['architecture_parameters'],{'CFLAGS':[],'CXXFLAGS':[]})
 def test_malformed_diagnostic_environment_nonfatal(self):
  r=self.context({'CFLAGS':'"'},dict.fromkeys((signal.SIGTERM,signal.SIGINT,signal.SIGHUP),signal.SIG_DFL));self.assertIn('parse_error',r['architecture_parameters']['CFLAGS'])
 def test_cli_preserves_existing_stdout_and_result(self):
  argv=['tool','--root','r','--build','b','--evidence','e','--arch','x86_64','--debug-info','yes','--compiler','c','--disassembler','d','--nm','n']
  outputs=[]
  for m in (old,a):
   o=io.StringIO()
   with patch.object(sys,'argv',argv),patch.dict(os.environ,{},clear=True),patch.object(m.signal,'getsignal',return_value=signal.SIG_DFL),patch.object(m.signal,'signal'),patch.object(m,'install',side_effect=lambda *args:print('NATIVE_ARCHIVES_END unchanged PASS 225')),contextlib.redirect_stdout(o):
    self.assertEqual(m.install_main(),0)
   outputs.append(o.getvalue())
  self.assertTrue(outputs[1].startswith('NATIVE_ARCHIVES_STARTUP '));self.assertEqual(outputs[1].split('\n',1)[1],outputs[0])
 def test_mixed_startup_states_and_parse_error_continue(self):
  custom=lambda *_:None
  states={signal.SIGTERM:signal.SIG_IGN,signal.SIGINT:signal.SIG_DFL,signal.SIGHUP:custom,signal.SIGCHLD:signal.SIG_DFL}
  argv=['tool','--root','r','--build','b','--evidence','e','--arch','x86_64','--debug-info','yes','--compiler','c','--disassembler','d','--nm','n']
  out=io.StringIO()
  with patch.object(sys,'argv',argv),patch.dict(os.environ,{'CFLAGS':'"','CXXFLAGS':'-O2 -march=nehalem'},clear=True),patch.object(a.signal,'getsignal',side_effect=lambda sig:states[sig]),patch.object(a.signal,'signal'),patch.object(a,'install',side_effect=lambda *args:print('NATIVE_ARCHIVES_END unchanged PASS 225')) as install,contextlib.redirect_stdout(out):
   self.assertEqual(a.install_main(),0)
  install.assert_called_once()
  lines=out.getvalue().splitlines()
  self.assertEqual(len(lines),2)
  self.assertTrue(lines[0].startswith('NATIVE_ARCHIVES_STARTUP '))
  obj=json.loads(lines[0].split(' ',1)[1])
  self.assertEqual(obj['signals'],{'SIGTERM':'ignored','SIGINT':'default','SIGHUP':'handler'})
  self.assertEqual(set(obj['architecture_parameters']['CFLAGS']),{'parse_error'})
  self.assertEqual(obj['architecture_parameters']['CXXFLAGS'],['-march=nehalem'])
  self.assertEqual(lines[1],'NATIVE_ARCHIVES_END unchanged PASS 225')
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2,failfast=True).run(unittest.defaultTestLoader.loadTestsFromTestCase(Hardening))
 Path(__file__).with_suffix('.result.json').write_text(json.dumps(dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors),passed=r.wasSuccessful()),indent=2)+'\n')
 sys.exit(not r.wasSuccessful())
