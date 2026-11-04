from common import *
import re,xml.etree.ElementTree as ET
out={}
for bid,project,snap in [(1215801,'Tizen-Unified','tizen-unified_20261102.233309'),(1215600,'Tizen-Unified-Toolchain','tizen-unified-toolchain_20261102.122237')]:
 base=f'https://download.tizen.org/snapshots/TIZEN/Tizen/{project}/{snap}/'
 u=base+f'builddata/manifest/{snap}_standard.xml';data=get(u);save(f'{bid}/manifest.xml',data,u)
 tree=ET.fromstring(data);projs=tree.findall('.//project');matches=[p.attrib for p in projs if 'llvm' in p.attrib.get('name','').lower()];out[str(bid)]={'projects':len(projs),'llvm_manifest_entries':matches,'arch':{}}
 print(bid,'PROJECTS',len(projs),'LLVM',matches,flush=True)
 for arch in ['x86_64','armv7l','aarch64']:
  part=f'builddata/buildlogs/standard/{arch}/summary.xml';u=base+part
  try:
   data=get(u);save(f'{bid}/{arch}/summary.xml',data,u);lines=data.decode().splitlines();hits=[dict(line=i,text=l) for i,l in enumerate(lines,1) if re.search(r'\bllvm\b',l,re.I)];out[str(bid)]['arch'][arch]={'llvm_summary_hits':hits};print(bid,arch,'llvm summary',hits,flush=True)
  except Exception as e:out[str(bid)]['arch'][arch]={'error':str(e)};print(str(e),flush=True)
  if arch=='x86_64':
   u=base+f'builddata/buildlogs/standard/{arch}/succeeded/';data=get(u);save(f'{bid}/public/x86-succeeded.html',data,u)
   links=re.findall(r'href="([^"]+)"',data.decode());print(bid,'LLVM_LOGS',[x for x in links if re.search('(^|/)llvm[.-]',x)],flush=True)
   u=base+f'builddata/buildlogs/standard/{arch}/succeeded/llvm.buildlog.txt'
   try:
    data=get(u);save(f'{bid}/x86_64/llvm.buildlog.txt',data,u);out[str(bid)]['llvm_log_http']=200
   except Exception as e:out[str(bid)]['llvm_log_http']=str(e)
(E/'scope-check.json').write_text(json.dumps(out,indent=2)+'\n')
