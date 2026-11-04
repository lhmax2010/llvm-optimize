from common import *
import re,xml.etree.ElementTree as ET,datetime,subprocess
M=['TIZEN_LLVM_NORMALIZED_FLAGS','TIZEN_LLVM_DROPPED_FLAGS','TIZEN_LLVM_FLAGS_WARNING','TIZEN_HYBRID_LINK_OK','BOLT_PROC_OK','BOLT_PROC_MISSING','BOLT_TOOL_DRY_RUN_BEGIN','BOLT_TOOL_DRY_RUN_END','BOLT_NINJA_EXIT_0','BOLT_PIPELINE_PASS','BOLT_DEBUG_SYMBOLS_PASS','BOLT_DEBUGLINK_PASS','BOLT_REAL_GATE_PASS','BOLT_COMPARE_ROOT_PASS','BOLT_CACHE_RELEASE','BOLT_POST_GATE_PASS','BOLT_DISK_REPORT','NATIVE_ARCHIVES_END','find-debuginfo','9e39fa8a61392652bb28b75fc26216675bcad1d5','platform/upstream/llvm']
report={'expected_source':'9e39fa8a61392652bb28b75fc26216675bcad1d5','logs':{},'builds':{},'scope':json.loads((E/'scope-check.json').read_text())}
ex=[]
for bid in [1215801,1215600,1215804,1215603]:
 p=D/f'{bid}-full-log.txt';s=p.read_text();lines=s.splitlines();report['logs'][str(bid)]={'bytes':p.stat().st_size,'lines':len(lines),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'matches':{m:[{'line':i,'text':l} for i,l in enumerate(lines,1) if m in l] for m in M}}
 ex.append(f'=== {bid}/full-log.txt (downloaded original, line numbers) ===')
 for i,l in enumerate(lines,1):
  if ('snapshot_num_url:' in l or 'base_path_url:' in l or 'repodata_url inside get_build_conf_text' in l or any(m in l for m in M)):
   ex.append(f'L{i}: {l}')
for bid in [1215801,1215600,1215802,1215803,1215804,1215805,1215806,1215601,1215602,1215603]:
 p=E/str(bid)/'overview.txt';lines=p.read_text().splitlines();line=next(l for l in lines if l.startswith(str(bid)+'\t'));cells=line.split('\t');duration=cells[3];n=re.findall(r'(\d+)\s+(hour|minute|second)',duration);seconds=sum(int(x)*{'hour':3600,'minute':60,'second':1}[unit] for x,unit in n);start=datetime.datetime.fromisoformat(cells[2]);end=start+datetime.timedelta(seconds=seconds)
 report['builds'][str(bid)]={'status':cells[1],'begin':cells[2],'duration':duration,'seconds':seconds,'end_calculated':end.isoformat(' '),'summary_line':lines.index(line)+1,'summary_raw':line}
 if bid in [1215801,1215600]:
  a=next(i for i,l in enumerate(lines) if l.startswith('Build Package List'));b=next(i for i,l in enumerate(lines[a:],a) if l.startswith(('Package List - Added','Build Type')));save(f'{bid}/package-list.txt','\n'.join(lines[a:b])+'\n',f'https://quickbuild.tizen.org/build/{bid}/overview')
  report['builds'][str(bid)]['package_list_original_lines']=[a+1,b]
 ex.append(f'=== {bid}/overview.txt ===')
 for i,l in enumerate(lines,1):
  if bid in [1215801,1215600] or l==line:ex.append(f'L{i}: {l}')
(E/'analysis.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
(E/'excerpts.txt').write_text('\n'.join(ex)+'\n')
# Exact package-name matching avoids treating building-blocks ... LLVM as clang/llvm RPMs.
from html.parser import HTMLParser
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':self.links.extend(v for k,v in attrs if k=='href')
idx={}
for bid in [1215801,1215600]:
 idx[str(bid)]={}
 for fname in ['repos_standard_packages_x86_64.html','repos_standard_debug.html','x86-succeeded.html']:
  p=E/str(bid)/'public'/fname;parser=Links();parser.feed(p.read_text());matches=[x for x in parser.links if re.match(r'(?:clang(?:-debuginfo)?-\d|llvm(?:-\d|\.buildlog))',x)]
  idx[str(bid)][fname]={'total_links':len(parser.links),'llvm_clang_matches':matches}
(E/'artifact-availability.json').write_text(json.dumps(idx,indent=2)+'\n')
print(json.dumps({'builds':report['builds'],'artifacts':idx},ensure_ascii=False,indent=2))
