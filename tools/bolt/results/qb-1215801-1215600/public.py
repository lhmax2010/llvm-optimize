from common import *
from urllib.parse import urljoin
import re
for bid,project,snap in [(1215801,'Tizen-Unified','tizen-unified_20261102.233309'),(1215600,'Tizen-Unified-Toolchain','tizen-unified-toolchain_20261102.122237')]:
 base=f'https://download.tizen.org/snapshots/TIZEN/Tizen/{project}/{snap}/'
 for part in ['builddata/manifest/','builddata/buildlogs/standard/x86_64/','repos/standard/packages/x86_64/','repos/standard/debug/']:
  u=base+part
  try:
   data=get(u);save(f'{bid}/public/{part.strip("/").replace("/","_")}.html',data,u)
   links=re.findall(r'href="([^"]+)"',data.decode())
   interesting=[x for x in links if 'llvm' in x.lower() or 'clang-' in x.lower() or '.xml' in x or x in ['succeeded/','failed/']]
   print(bid,u,interesting,flush=True)
  except Exception as e:print(bid,u,type(e).__name__,str(e),flush=True)
