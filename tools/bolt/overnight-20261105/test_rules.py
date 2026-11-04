import unittest,struct,zlib,sys
from pathlib import Path
from compare_rules import *
O=Path(sys.argv[1]);O.mkdir(exist_ok=False);sys.argv=sys.argv[:1]
def elf(comment=b'Intel Corporation\0clang version 22\0',text=b'ABCD',link=None):
 names=['','.text','.comment']+(['.gnu_debuglink'] if link is not None else [])+['.shstrtab'];st=b'\0';indices={}
 for n in names:indices[n]=len(st) if n else 0;st+=n.encode()+b'\0' if n else b''
 data=bytearray(64);rows=[(0,0,0,0,0,0,0,0,0,0)]
 for name,body,flag in [('.text',text,2),('.comment',comment,0)]+([('.gnu_debuglink',link,0)] if link is not None else [])+[('.shstrtab',st,0)]:
  off=len(data);data+=body;rows.append((indices[name],1 if name!='.shstrtab' else 3,flag,64 if flag else 0,off,len(body),0,0,1,0))
 while len(data)%8:data+=b'\0'
 shoff=len(data)
 for row in rows:data+=struct.pack('<IIQQQQIIQQ',*row)
 data[:16]=b'\x7fELF\x02\x01\x01'+b'\0'*9;struct.pack_into('<HHIQQQIHHHHHH',data,16,1,62,1,0,0,shoff,0,64,0,0,64,len(rows),len(rows)-1);return data
def dl(name,crc):
 x=name.encode()+b'\0';x+=b'\0'*((-len(x))%4);return x+struct.pack('<I',crc)
class Tests(unittest.TestCase):
 def test_common_non_identifier_allowed(self):elf_proof(elf(),elf(b'Intel Corporation\0clang version 23.0\0'))
 def test_changed_non_identifier_rejected(self):
  with self.assertRaisesRegex(AssertionError,'non-identifier'):elf_proof(elf(),elf(b'Other Company\0clang version 22\0'))
 def test_count_change_non_identifier_rejected(self):
  with self.assertRaisesRegex(AssertionError,'non-identifier'):elf_proof(elf(),elf(b'Intel Corporation\0Intel Corporation\0clang version 22\0'))
 def test_debuglink_general_filename(self):self.run_case('ok')
 def test_debuglink_bad_crc(self):self.run_case('badcrc')
 def test_debuglink_bad_filename(self):self.run_case('badname')
 def test_debuglink_bad_symbol(self):self.run_case('badsymbol')
 def test_debuglink_bad_text(self):self.run_case('badtext')
 def run_case(self,kind):
  d=O/kind;d.mkdir();a=elf();b=elf(b'Intel Corporation\0clang version 23\0',text=b'BAD!' if kind=='badsymbol' else b'ABCD');(d/'a.debug').write_bytes(a);(d/'b.debug').write_bytes(b)
  (d/'a').write_bytes(elf(link=dl('other-tool.debug',zlib.crc32(a))));(d/'b').write_bytes(elf(text=b'XXXX' if kind=='badtext' else b'ABCD',link=dl('wrong.debug' if kind=='badname' else 'other-tool.debug',zlib.crc32(b)^(1 if kind=='badcrc' else 0))))
  if kind=='ok':self.assertIn('verified-debuglink',debuglink_proof(d/'a',d/'b',d/'a.debug',d/'b.debug')['classification'])
  else:
   with self.assertRaises(AssertionError):debuglink_proof(d/'a',d/'b',d/'a.debug',d/'b.debug')
unittest.main(verbosity=2)
