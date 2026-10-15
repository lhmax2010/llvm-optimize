"""Fetch full endpoint specs; preserve failed attempts and derive packaging-only diff losslessly."""
from common import *
import re
revs={'llvm':('8dfebafe1a477b3dcc678ee4cb18a3a4306d5a7c','67619ec8bbbac7238a6cfc33a481ccfbcd12206f'),'qemu-accel':('e01aa7250a1a73aa8f88ba9ac4a05cbc954d1c9f','2737f3bf78ed33be4333114c0e5c741a1deca467')}
full=(RAW/'llvm_full.diff').read_bytes()
blocks=re.split(br'(?=^diff --git )',full,flags=re.M)
(RAW/'llvm_packaging_complete.diff').write_bytes(b''.join(b for b in blocks if b.startswith(b'diff --git a/packaging/')))
(RAW/'derived_source_provenance.txt').write_text('llvm_packaging_complete.diff: unchanged byte blocks from llvm_full.diff whose diff --git path starts a/packaging/. All endpoint packaging changes retained. llvm_packaging.diff is a preserved failed HTTP 502 response, not a diff.\n')
for repo,(old,new) in revs.items():
 for side,rev in [('old',old),('new',new)]:
  filename='llvm.spec' if repo=='llvm' else 'qemu-accel-armv7l.spec'
  p=RAW/f'{repo}_{side}_{filename}'
  fetch(f'https://git.tizen.org/cgit/platform/upstream/{repo}/plain/packaging/{filename}?id={rev}',p)
fetch(f'https://git.tizen.org/cgit/platform/upstream/qemu-accel/rawdiff/?id={revs["qemu-accel"][1]}&id2={revs["qemu-accel"][0]}&context=3',RAW/'qemu-accel_full_retry.diff')
