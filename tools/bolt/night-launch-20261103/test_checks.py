from pathlib import Path
import unittest,struct,sys,json,copy,gzip
from checks import *
from release_checks import check_native_archive,ninja_modules

def elf(command=b'-g\0',debug=False):
 names=b'\0.shstrtab\0.GCC.command.line\0.text\0'+(b'.debug_info\0' if debug else b'');payload=b'CODE'+command+names;off=64+len(payload);off=(off+7)//8*8;n=5 if debug else 4
 b=bytearray(off+n*64);b[:16]=b'\x7fELF\x02\x01\x01'+b'\0'*9;struct.pack_into('<HHIQQQIHHHHHH',b,16,1,62,1,0,0,off,0,64,56,0,64,n,1);b[64:64+len(payload)]=payload
 headers=[(0,0,0,0,0,0,0,0,0,0),(1,3,0,0,68+len(command),len(names),0,0,1,0),(11,1,0,0,68,len(command),0,0,1,0),(29,1,6,0,64,4,0,0,1,0)]
 if debug:headers.append((35,1,0,0,64,4,0,0,1,0))
 # Name offsets derived instead of relying on literal lengths.
 headers[2]=(names.index(b'.GCC'),*headers[2][1:]);headers[3]=(names.index(b'.text'),*headers[3][1:])
 if debug:headers[4]=(names.index(b'.debug'),*headers[4][1:])
 for i,h in enumerate(headers):struct.pack_into('<IIQQQQIIQQ',b,off+i*64,*h)
 return bytes(b)

def arc(data,date=b'1'):
 return b'!<arch>\n'+b'm.o/            '+date.ljust(12)+b'0     0     100644  '+str(len(data)).encode().ljust(10)+b'`\n'+data+(b'\n' if len(data)%2 else b'')
class Tests(unittest.TestCase):
 def test_command_bytes(self):
  x=command_byte_proof(elf(b'-g\0'),elf(b'-O\0'));self.assertFalse(next(r for r in x['record_sections'] if r['section']=='.GCC.command.line')['content_equal'])
 def test_code_byte_fails(self):
  x=bytearray(elf());x[64]^=1
  with self.assertRaises(AssertionError):content_proof(elf(),bytes(x))
 def test_header_byte_fails(self):
  x=bytearray(elf());x[24]^=1
  with self.assertRaises(AssertionError):content_proof(elf(),bytes(x))
 def test_size_change_fails(self):
  with self.assertRaises(AssertionError):content_proof(elf(),elf()+b'\0')
 def test_duplicate_section_names(self):
  # Preserve the ordered occurrences instead of imposing ELF name uniqueness.
  x=bytearray(elf());off=struct.unpack_from('<Q',x,40)[0];struct.pack_into('<I',x,off+2*64,1)
  self.assertEqual(content_proof(x,x)['classification'],'identical')
 def test_ar_dates(self):
  x=ar_proof(arc(elf()),arc(elf(),b'2'));self.assertEqual(x['classification'],'allowed-ar-date-difference');self.assertTrue(x['member_content_sha_equal'])
 def test_ar_command_and_date(self):self.assertEqual(ar_proof(arc(elf(b'-g\0')),arc(elf(b'-O\0'),b'2'))['classification'],'ar-command-record-difference')
 def test_ar_content_fails(self):
  x=bytearray(elf());x[64]^=1
  with self.assertRaises(AssertionError):ar_proof(arc(elf()),arc(bytes(x)))
 def test_ar_other_header_fails(self):
  x=bytearray(arc(elf()));x[40]^=1
  with self.assertRaises(AssertionError):ar_proof(arc(elf()),bytes(x))
 def test_dropped_each(self):
  for token in DROP:
   with self.assertRaises(AssertionError):no_dropped(elf(token.encode()+b'\0'))
 def test_release_native(self):
  data=elf();record=dict(members=1,results=[dict(ordinal=0,name='m.o',preserved=False,sha256=hashlib.sha256(data).hexdigest())]);self.assertEqual(check_native_archive(arc(data),record)['converted'],1)
 def test_release_debug_fails(self):
  data=elf(debug=True);record=dict(members=1,results=[dict(ordinal=0,name='m.o',preserved=False,sha256=hashlib.sha256(data).hexdigest())])
  with self.assertRaisesRegex(AssertionError,'unexpectedly emitted debug'):check_native_archive(arc(data),record)
 def test_preserved_native_debug_allowed(self):
  self.assertEqual(check_native_archive(arc(elf(debug=True)),dict(members=1,results=[dict(ordinal=0,name='m.o',preserved=True)]))['preserved'],1)
 def test_real_flags(self):
  E=Path(__file__).parents[1]/'results/second-review-20261104'
  for project in ['toolchain','basedev']:
   r=json.loads((E/(project+'-rehearsal-audit.json')).read_text());log=r['TIZEN_LLVM_NORMALIZED_FLAGS']['text']+'\n'+r['TIZEN_LLVM_DROPPED_FLAGS']['text'];flags_check(log,project)
   with self.assertRaises(AssertionError):flags_check(log+'\nTIZEN_LLVM_FLAGS_WARNING bad',project)
   with self.assertRaises(AssertionError):flags_check(log.replace('LDFLAGS=[]','LDFLAGS=[bad]'),project)
 def test_unknown_critical(self):
  from resource_report import critical_stop
  self.assertEqual(critical_stop(Path('/nonexistent'),dict(mounts={'stdout':'/mount'},remaining_build_processes=[])),'residual-process-or-mount')
if __name__=='__main__':unittest.main(verbosity=2)
