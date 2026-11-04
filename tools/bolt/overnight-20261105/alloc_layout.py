from pathlib import Path
import json,mmap,gzip,collections,datetime
from section_compare import *
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=B/'tools/bolt/results/baseline-attribution-20261105';rows=json.loads((E/'attribution-files.json').read_text());counts=collections.Counter();affected=set();compiler=set();samples=[]
f=gzip.open(E/'alloc-layout-details.jsonl.gz','wt')
def audit(a,b,ctx):
 va,ha,sa=layout(a);vb,hb,sb=layout(b);same_names=[x['name'] for x in sa]==[x['name'] for x in sb];out=[]
 for x,y in zip(sa,sb):
  if not x['flags']&2:continue
  same=chunk_equal(x['content'],y['content'])
  if x['raw']!=y['raw'] or not same:
   out.append({'section':x['name'],'old_header':list(x['raw']),'new_header':list(y['raw']),'contents_equal':same,'old_sha':digest(x['content']),'new_sha':digest(y['content']),'old_offset':x['offset'],'new_offset':y['offset']});counts['ALLOC_sections']+=1;counts['content_equal' if same else 'content_different']+=1
 if out:
  key=(ctx['package'],ctx['path']);affected.add(key)
  if ctx['package'].startswith('compiler-rt\t'):compiler.add(key)
  r={**ctx,'section_names_order_equal':same_names,'old_section_names':[x['name'] for x in sa],'new_section_names':[x['name'] for x in sb],'old_function_data_sections':[x['name'] for x in sa if x['name'].startswith(('.text.','.data.','.rodata.','.bss.'))],'new_function_data_sections':[x['name'] for x in sb if x['name'].startswith(('.text.','.data.','.rodata.','.bss.'))],'ALLOC_changes':out,'records':{side:[{'section':s['name'],'offset':s['offset'],'size':s['size'],'strings':dict(strings(s['content']))} for s in ss if s['name'] in RECORDS] for side,ss in [('old',sa),('new',sb)]}}
  f.write(json.dumps(r)+'\n');counts['ELFs']+=1;counts['same_section_names' if same_names else 'different_section_names']+=1
  if len(samples)<5:samples.append(r)
def body(a,b,ctx):
 if bytes(a[:4])==b'\x7fELF':audit(a,b,ctx)
 elif bytes(a[:8])==b'!<arch>\n':
  for x,y in zip(ar_members(a),ar_members(b)):
   if bytes(x['body'][:4])==b'\x7fELF' and not chunk_equal(x['body'],y['body']):audit(x['body'],y['body'],{**ctx,'member':x['name']})
try:
 for r in rows:
  with open(r['old'],'rb') as a,open(r['new'],'rb') as b:
   with mmap.mmap(a.fileno(),0,access=mmap.ACCESS_READ) as aa,mmap.mmap(b.fileno(),0,access=mmap.ACCESS_READ) as bb:body(aa,bb,{k:r[k] for k in ('package','path')})
finally:
 f.close();(E/'alloc-layout-summary.json').write_text(json.dumps({'counts':dict(counts),'files':sorted(affected),'compiler_rt_files':sorted(compiler),'examples':samples},indent=2)+'\n');print('ALLOC_LAYOUT 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok',flush=True)
