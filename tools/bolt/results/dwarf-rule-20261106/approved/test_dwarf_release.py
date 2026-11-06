from pathlib import Path
import sys,json,shutil,struct,unittest
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');W=B.parent/'llvm-optimize'
sys.path.insert(0,str(B/'tools/bolt/night-launch-20261105'))
import dwarf_release as d
from section_compare import layout
E=Path(__file__).parent;O=W/'temp/dwarf-rule-20261106/tests-approved';O.mkdir(parents=True,exist_ok=False)
pairs=json.loads((B/'tools/bolt/results/tu-dwarf-20261106/dwarf-pairs.json').read_text())
remarks=next(r for r in pairs if r['path'].endswith('libRemarks.so.22.1.debug'))
omp=next(r for r in pairs if r['path'].endswith('libomp.so.debug'))
observed=[]
def proof(row,new=None,label='positive'):
 a=Path(row['old']);b=Path(new or row['new'])
 try:
  p=d.debug_pair(a,b,O/'proofs');observed.append(dict(label=label,status='PASS',proof=p));return p
 except Exception as e:observed.append(dict(label=label,status='FAIL',error=repr(e)));raise
def changed(row,label,fn):
 raw=bytearray(Path(row['new']).read_bytes());fn(raw)
 p=O/(label+'.debug');p.write_bytes(raw);return p
def sections(buf):return {s['name']:s for s in layout(buf)[2]}
class Rules(unittest.TestCase):
 def test_01_remarks_real(self):
  self.assertEqual(proof(remarks,label='real-Remarks')['classification'],'approved-release-path-DWARF')
 def test_02_omp_real(self):
  self.assertEqual(proof(omp,label='real-libomp')['classification'],'approved-release-path-DWARF')
 def test_line_program_byte(self):
  def edit(raw):
   s=sections(raw)['.debug_line'];u=d.unit(raw,s['offset'],s['offset']+s['size']);raw[u['ps']]^=1
  p=changed(remarks,'line-program',edit)
  with self.assertRaises(AssertionError):proof(remarks,p,'line-program-negative')
 def test_length_plus_minus(self):
  for delta in [-1,1]:
   def edit(raw):
    s=sections(raw)['.debug_line'];u=d.unit(raw,s['offset'],s['offset']+s['size'])
    struct.pack_into('<I',raw,u['hp'],u['hlen']+delta)
   p=changed(remarks,'length-'+str(delta),edit)
   with self.assertRaises(AssertionError):proof(remarks,p,'length-'+str(delta))
 def test_compdir_non_slash(self):
  def edit(raw):
   word=b'/usr/src/debug/llvm-22.1.8-2.1.x86_64///build'
   at=raw.find(word);assert at>=0;raw[at+len(word)-1]=ord('X')
  p=changed(omp,'compdir-nonslash',edit)
  with self.assertRaises(AssertionError):proof(omp,p,'compdir-nonslash')
 def test_compdir_length(self):
  # Also exercise the exact length predicate without relying on parser errors.
  with self.assertRaisesRegex(AssertionError,'byte length'):
   d.comp_dir('/a///b','/a//b',b'old',b'new')
  def edit(raw):
   word=b'/usr/src/debug/llvm-22.1.8-2.1.x86_64///build'
   at=raw.find(word);assert at>=0;raw[at+len(word)-1]=0
  p=changed(omp,'compdir-length',edit)
  with self.assertRaises(AssertionError):proof(omp,p,'compdir-length')
 def test_aranges_byte(self):
  def edit(raw):
   s=sections(raw)['.debug_aranges'];assert s['size']>0;raw[s['offset']+s['size']-1]^=1
  p=changed(remarks,'aranges-byte',edit)
  with self.assertRaisesRegex(AssertionError,'debug_aranges'):proof(remarks,p,'aranges-byte')

 def test_residual_slashes_require_original_equal_length(self):
  import posixpath,re
  old=b'usr/src/debug/llvm-22.1.8-1.x86_64';new=b'usr/src/debug/llvm-22.1.8-2.1.x86_64'
  def attr(value):return '  DW_AT_comp_dir\t("'+value+'")\n'
  plain_old='/'+old.decode()+'/build';plain_new='/'+new.decode()+'/build'
  # Prefix-only case is handled before info_difference: 41/43 bytes are valid.
  self.assertNotEqual(len(plain_old.encode()),len(plain_new.encode()))
  self.assertEqual(d.normal(attr(plain_old),'local',old,new),d.normal(attr(plain_new),'QB',old,new))
  good_old='/'+old.decode()+'/////build';good_new='/'+new.decode()+'///build'
  self.assertEqual(len(good_old.encode()),len(good_new.encode()))
  d.info_difference(attr(good_old),attr(good_new),old,new)
  bad_new='/'+new.decode()+'////build'
  replaced=good_old.replace(old.decode(),new.decode())
  self.assertNotEqual(replaced,bad_new)
  self.assertEqual(re.sub('/+','/',replaced),re.sub('/+','/',bad_new))
  self.assertEqual(posixpath.normpath(replaced),posixpath.normpath(bad_new))
  self.assertNotEqual(len(good_old.encode()),len(bad_new.encode()))
  with self.assertRaisesRegex(AssertionError,'comp_dir byte length'):
   d.info_difference(attr(good_old),attr(bad_new),old,new)
  observed.append(dict(label='residual-slashes-unequal-original-length',status='FAIL-as-required',
   old=good_old,new=bad_new,old_bytes=len(good_old.encode()),new_bytes=len(bad_new.encode()),
   after_prefix_old=replaced,after_prefix_new=bad_new,posix_equal=True,
   expected_error='comp_dir byte length',test='PASS'))
 def test_delta_not_hardcoded(self):
  # Same parser, actual replacement width 3 rather than the real pair's 2.
  import copy
  ha=b'\x01\x01\x01\xfb\x0e\x0d'+b'\0'*12+b'old\0\0\0'
  hb=ha.replace(b'old',b'longer');program=b'\0\x01\x01'
  def make(h):return struct.pack('<IHI',2+4+len(h)+len(program),4,len(h))+h+program
  r=d.line_proof(make(ha),make(hb),b'old',b'longer');self.assertEqual(r[0]['expected_delta'],3)
if __name__=='__main__':
 r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Rules))
 (E/'tests-observed.json').write_text(json.dumps(observed,ensure_ascii=False,indent=2)+'\n')
 (E/'test-result.json').write_text(json.dumps(dict(tests=r.testsRun,failures=len(r.failures),errors=len(r.errors)))+'\n')
 sys.exit(not r.wasSuccessful())
