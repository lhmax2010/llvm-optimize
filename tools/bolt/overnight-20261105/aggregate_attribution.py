from pathlib import Path
import json,gzip,collections,struct,datetime
from section_compare import layout
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=B/'tools/bolt/results/baseline-attribution-20261105';rows=json.loads((E/'attribution-files.json').read_text());lookup={(x['package'],x['path']):x for x in rows}
files=collections.defaultdict(set);members=collections.Counter();symbols=collections.Counter();examples=collections.defaultdict(list);unexplained=collections.defaultdict(lambda:{'members':set(),'sections':set(),'rows':0});compiler=[];modules=[]
with gzip.open(E/'all-section-audits.jsonl.gz','rt') as f:
 for l in f:
  r=json.loads(l);c=r['context'];key=(c['package'],c['path']);mem=c.get('member','');ch=r['changes']
  if not r['program_headers_equal']:
   files['program-header-change'].add(key)
   if not mem:
    v={k:lookup[key][k] for k in ('package','path','old','new')};v['headers']={}
    for side in ['old','new']:
     data=Path(v[side]).read_bytes();a,h,ss=layout(data);fmt='<IIQQQQQQ' if data[4]==2 else '<IIIIIIII';v['headers'][side]=[list(struct.unpack_from(fmt,a,h[4]+i*h[8])) for i in range(h[9])]
    modules.append(v)
  for x in ch:
   kind=x.get('class','metadata-only');files[kind].add(key);members[kind]+=1
   if len(examples[kind])<6:examples[kind].append({'context':c,'section':x['section'],**{k:x[k] for k in ['exceptions','old_strings','new_strings'] if k in x}})
   if 'suffix_only_semantic_multiset_equal' in x:
    for k in ['changed_rows','exceptions','old_count','new_count']:symbols[k]+=x[k]
   if kind.startswith('unexplained') and x['section']!='.gnu_debuglink':
    u=unexplained[key];u['members'].add(mem);u['sections'].add(x['section']);u['rows']+=1
  if c['package'].startswith('compiler-rt\t') and any(x.get('class','').startswith('unexplained') for x in ch):compiler.append(r)
with gzip.open(E/'compiler-rt-details.json.gz','wt') as f:json.dump(compiler,f,indent=2)
index={'archives':0,'passed':0,'failed':0,'exceptions':[]}
for r in rows:
 for m in r['audit'].get('members',[]):
  if 'index_suffix_and_target_equal' in m:
   index['archives']+=1;index['passed' if m['index_suffix_and_target_equal'] else 'failed']+=1
   if not m['index_suffix_and_target_equal']:index['exceptions'].append({'package':r['package'],'path':r['path'],'member':m['name']})
namecounts=collections.Counter();nameexamples=[]
with gzip.open(E/'all-changed-names.jsonl.gz','rt') as f:
 for l in f:
  x=json.loads(l);namecounts[x['kind']]+=1
  if (x.get('suffix_only') is False or x.get('suffix_and_target_equal') is False or x['kind']=='symbol-semantic-exceptions') and len(nameexamples)<20:
   if 'exceptions' in x:x={**x,'exception_count':len(x['exceptions']),'exceptions':x['exceptions'][:3]}
   nameexamples.append(x)
result={'files':{k:len(v) for k,v in files.items()},'section_occurrences':dict(members),'symbol_statistics':dict(symbols),'changed_name_records':dict(namecounts),'name_exception_examples':nameexamples,'archive_index':index,'examples':examples,'unexplained_files':[{'package':k[0],'path':k[1],'members':sorted(v['members']),'sections':sorted(v['sections']),'rows':v['rows']} for k,v in sorted(unexplained.items())]}
(E/'attribution-summary.json').write_text(json.dumps(result,indent=2)+'\n');(E/'module-program-headers.json').write_text(json.dumps(modules,indent=2)+'\n')
print('ATTRIBUTION_SUMMARY 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok',flush=True)
# Isolate compiler-rt causal evidence instead of treating an offset as content.
import shlex,difflib
counts=collections.Counter();exceptions=[];content=[];command_diffs=[]
with gzip.open(E/'alloc-layout-details.jsonl.gz','rt') as f:
 for l in f:
  x=json.loads(l)
  for a in x['ALLOC_changes']:
   if not a['contents_equal']:content.append({k:x[k] for k in ('package','path')}|{'member':x.get('member'),'section':a['section'],'old_header':a['old_header'],'new_header':a['new_header'],'old_sha':a['old_sha'],'new_sha':a['new_sha']})
  if not x['package'].startswith('compiler-rt\t'):continue
  counts['members']+=1;counts['same_section_names']+=int(x['section_names_order_equal']);counts['same_function_data_sections']+=int(x['old_function_data_sections']==x['new_function_data_sections']);counts['alloc_content_different']+=sum(not a['contents_equal'] for a in x['ALLOC_changes'])
  aa=[r for r in x['records']['old'] if r['section']=='.GCC.command.line'];bb=[r for r in x['records']['new'] if r['section']=='.GCC.command.line'];ok=False
  if len(aa)==len(bb)==1 and len(aa[0]['strings'])==len(bb[0]['strings'])==1:
   u=shlex.split(next(iter(aa[0]['strings'])));v=shlex.split(next(iter(bb[0]['strings'])));ops=[{'tag':tag,'old':u[i:j],'new':v[k:n]} for tag,i,j,k,n in difflib.SequenceMatcher(a=u,b=v,autojunk=False).get_opcodes() if tag!='equal'];ok=ops==[{'tag':'insert','old':[],'new':['-ffunction-sections','-fdata-sections']}]
   z={k:x[k] for k in ('package','path')}|{'member':x.get('member'),'diff':ops,'old_already_function_sections':'-ffunction-sections' in u,'old_already_data_sections':'-fdata-sections' in u,'old_record_size':aa[0]['size'],'new_record_size':bb[0]['size']};command_diffs.append(z)
   counts['old_already_has_both']+=int(z['old_already_function_sections'] and z['old_already_data_sections'])
  if ok:counts['only_extra_two_tokens']+=1
  else:exceptions.append({k:x[k] for k in ('package','path')}|{'member':x.get('member')})
(E/'compiler-rt-causality.json').write_text(json.dumps({'counts':dict(counts),'exceptions':exceptions,'commands':command_diffs,'all_content_different_ALLOC':content},indent=2)+'\n')
print('COMPILER_RT_CAUSALITY 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok',flush=True)
# Archive index targets include occurrence ordinal, not only basename.
import mmap
from section_compare import ar_members,chunk_equal
index_rows=[]
def decode_index(ms,m):
 body=m['body'];sz=8 if m['name']=='/SYM64/' else 4;fmt='>Q' if sz==8 else '>I';n=struct.unpack_from(fmt,body)[0];off=struct.unpack_from('>'+('Q' if sz==8 else 'I')*n,body,sz);names=bytes(body[sz*(n+1):]).split(b'\0');targets={v['offset']:(i,v['name']) for i,v in enumerate(ms)};return [(names[i].decode(errors='replace'),targets.get(off[i],('INVALID','INVALID'))) for i in range(n)]
def check_index(a,b):
 aa,bb=ar_members(a),ar_members(b);out=[]
 for x,y in zip(aa,bb):
  if x['name'] not in ('/','/SYM64/') or chunk_equal(x['body'],y['body']):continue
  u,v=decode_index(aa,x),decode_index(bb,y);errors=[]
  for i in range(max(len(u),len(v))):
   p=u[i] if i<len(u) else None;q=v[i] if i<len(v) else None
   if not(p and q and re.sub(r'\.llvm\.[0-9]+','.llvm.<N>',p[0])==re.sub(r'\.llvm\.[0-9]+','.llvm.<N>',q[0]) and p[1]==q[1]):errors.append({'index':i,'old':p,'new':q})
  out.append({'member':x['name'],'old_count':len(u),'new_count':len(v),'errors':errors,'PASS':not errors})
 return out
import re
for r in rows:
 if not r['audit'].get('members'):continue
 with open(r['old'],'rb') as a,open(r['new'],'rb') as b:
  with mmap.mmap(a.fileno(),0,access=mmap.ACCESS_READ) as aa,mmap.mmap(b.fileno(),0,access=mmap.ACCESS_READ) as bb:proof=check_index(aa,bb)
 index_rows.append({k:r[k] for k in ('package','path')}|{'index':proof})
(E/'archive-index-ordinal-proof.json').write_text(json.dumps(index_rows,indent=2)+'\n');print('ARCHIVE_INDEX 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok',flush=True)
