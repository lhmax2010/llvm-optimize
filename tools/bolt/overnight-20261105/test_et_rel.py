import struct,unittest
from section_compare import elf_proof
def elf(record=b'clang version 22\0',kind=1,text=b'ABCD',address=0,flags=2,align=1):
 names=b'\0.comment\0.text\0.shstrtab\0';data=bytearray(64);rows=[(0,0,0,0,0,0,0,0,0,0)]
 for name,body,fl,addr,al in [(1,record,0,0,1),(10,text,flags,address,align),(16,names,0,0,1)]:
  off=len(data);data+=body;rows.append((name,3 if name==16 else 1,fl,addr,off,len(body),0,0,al,0))
 while len(data)%8:data+=b'\0'
 shoff=len(data)
 for row in rows:data+=struct.pack('<IIQQQQIIQQ',*row)
 data[:16]=b'\x7fELF\x02\x01\x01'+b'\0'*9;struct.pack_into('<HHIQQQIHHHHHH',data,16,kind,62,1,0,0,shoff,0,64,0,0,64,len(rows),3);return data
class Tests(unittest.TestCase):
 def test_rel_record_growth(self):self.assertFalse(elf_proof(elf(),elf(b'clang version 22.1.8 longer\0'))['ALLOC_offsets_equal'])
 def test_exec_rejects(self):
  with self.assertRaises(AssertionError):elf_proof(elf(kind=2),elf(b'clang version 23 longer\0',kind=2))
 def test_dyn_rejects(self):
  with self.assertRaises(AssertionError):elf_proof(elf(kind=3),elf(b'clang version 23 longer\0',kind=3))
 def test_other_changes_reject(self):
  for kw in [dict(text=b'ABCE'),dict(text=b'ABCDE'),dict(address=4),dict(flags=6),dict(align=2)]:
   with self.subTest(kw=kw),self.assertRaises(AssertionError):elf_proof(elf(),elf(b'clang version 23 longer\0',**kw))
 def test_unapproved_comment_rejects(self):
  with self.assertRaises(AssertionError):elf_proof(elf(),elf(b'bad injected text\0'))
if __name__=='__main__':unittest.main(verbosity=2)
