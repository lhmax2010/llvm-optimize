from common import *
import xml.etree.ElementTree as ET
for bid,project,snap in [(1216409,'Tizen-Base-Toolchain','tizen-base-toolchain_20261103.085926'),(1216410,'Tizen-Base-Dev','tizen-base-dev_20261103.090039')]:
 base=f'https://download.tizen.org/RBS/TIZEN/Tizen/{project}/{snap}/'
 u=base+f'builddata/manifest/{snap}_standard.xml';data=get(u);save(f'{bid}/manifest.xml',data,u);print(bid,'LLVM', [p.attrib for p in ET.fromstring(data).findall('.//project') if p.get('name')=='platform/upstream/llvm'],flush=True)
 for arch in ['x86_64','armv7l','aarch64']:
  u=base+f'builddata/buildlogs/standard/{arch}/succeeded/llvm.buildlog.txt'
  try:
   data=get(u);save(f'{bid}/{arch}/llvm.buildlog.txt',data,u);(D/f'{bid}-{arch}.log').write_bytes(data);print(bid,arch,len(data),flush=True)
  except Exception as e:save(f'{bid}/{arch}/download-error.txt',str(e)+'\n',u);print(str(e),flush=True)
