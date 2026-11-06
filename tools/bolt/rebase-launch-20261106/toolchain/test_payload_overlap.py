from pathlib import Path
from unittest.mock import patch
import unittest,hashlib
import release_checks as R
W=Path('/home/linhao/Toolchain/development/llvm-optimize');X=W/'temp/night-revalidation-20261104-overlap-tests';X.mkdir(exist_ok=False)
class Tests(unittest.TestCase):
 def test_identical_no_overwrite(self):
  root=X/'same';root.mkdir();p=root/'header.h';p.write_bytes(b'good');before=p.stat();files={'header.h':{'sha256':hashlib.sha256(b'good').hexdigest()}}
  with patch.object(R,'extract_selected') as extract:r=R.extract_package_payload(Path('fixture.rpm'),{'header.h'},root,files);extract.assert_not_called()
  self.assertEqual(p.stat().st_mtime_ns,before.st_mtime_ns);self.assertEqual(len(r),1)
 def test_conflict_fails(self):
  root=X/'bad';root.mkdir();p=root/'header.h';p.write_bytes(b'bad')
  with self.assertRaisesRegex(AssertionError,'conflicting RPM'):R.extract_package_payload(Path('fixture.rpm'),{'header.h'},root,{'header.h':{'sha256':hashlib.sha256(b'good').hexdigest()}})
  self.assertEqual(p.read_bytes(),b'bad')
 def test_link_fails(self):
  root=X/'link';root.mkdir();(root/'source').write_text('good');(root/'header.h').symlink_to('source')
  with self.assertRaisesRegex(AssertionError,'not regular'):R.extract_package_payload(Path('fixture.rpm'),{'header.h'},root,{'header.h':{'sha256':hashlib.sha256(b'good').hexdigest()}})
if __name__=='__main__':unittest.main(verbosity=2)
