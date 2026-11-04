from pathlib import Path
import json,struct,collections,re,gzip,datetime
from section_compare import layout,chunk_equal,digest,strings
B=Path('/home/linhao/Toolchain/development/llvm-optimize-bolt');E=B/'tools/bolt/results/baseline-attribution-20261105';rs=json.loads((E/'module-program-headers.json').read_text());out=[];exceptions=[]
def ranges(a,b):
 rr=[];start=None
 for i in range(max(len(a),len(b))):
  different=i>=len(a) or i>=len(b) or a[i]!=b[i]
  if different and start is None:start=i
  if not different and start is not None:rr.append([start,i]);start=None
 if start is not None:rr.append([start,max(len(a),len(b))])
 return rr
def sym(data,ss,s):
 st=bytes(ss[s['raw'][6]]['content']);fmt='<IBBHQQ';r=[]
 for i in range(0,s['size'],24):
  z=struct.unpack_from(fmt,s['content'],i);end=st.find(b'\0',z[0]);r.append((st[z[0]:end].decode(errors='replace'),*z[1:]))
 return r
for r in rs:
 a=Path(r['old']).read_bytes();b=Path(r['new']).read_bytes();va,ha,sa=layout(a);vb,hb,sb=layout(b);ma={s['name']:s for s in sa};mb={s['name']:s for s in sb};assert len(ma)==len(sa) and len(mb)==len(sb)
 changes=[];syms=[]
 for name in sorted(ma.keys()|mb.keys()):
  if name not in ma or name not in mb:changes.append({'section':name,'missing':True});continue
  x,y=ma[name],mb[name];same=chunk_equal(x['content'],y['content'])
  if x['raw']!=y['raw'] or not same:
   z={'section':name,'old_header':list(x['raw']),'new_header':list(y['raw']),'ALLOC':bool(x['flags']&2),'content_equal':same,'old_offset':x['offset'],'new_offset':y['offset'],'old_bytes':x['size'],'new_bytes':y['size'],'old_sha':digest(x['content']),'new_sha':digest(y['content']),'ranges_relative':ranges(x['content'],y['content']) if not same else []}
   changes.append(z)
  if name in ('.symtab','.dynsym') and not same:
   u,v=sym(a,sa,x),sym(b,sb,y)
   for i in range(max(len(u),len(v))):
    old=u[i] if i<len(u) else None;new=v[i] if i<len(v) else None
    if old!=new:
     row={'package':r['package'],'path':r['path'],'section':name,'index':i,'old':old,'new':new,'suffix_only':bool(old and new and re.sub(r'\.llvm\.[0-9]+','.llvm.<N>',old[0])==re.sub(r'\.llvm\.[0-9]+','.llvm.<N>',new[0]) and old[1:]==new[1:])};syms.append(row)
     if not row['suffix_only']:exceptions.append(row)
 out.append({k:r[k] for k in ('package','path','old','new')}|{'old_section_order':[s['name'] for s in sa],'new_section_order':[s['name'] for s in sb],'changes':changes,'symbol_changes':syms})
(E/'module-named-sections.json').write_text(json.dumps(out,indent=2)+'\n')
with (E/'module-symbol-exceptions.tsv').open('w') as f:
 f.write('package\tpath\tsection\tindex\told\tnew\n')
 for x in exceptions:f.write('\t'.join(str(x[k]).replace('\t',' ') for k in ['package','path','section','index'])+'\t'+json.dumps(x['old'])+'\t'+json.dumps(x['new'])+'\n')
nonmodule=collections.Counter()
with gzip.open(E/'alloc-layout-details.jsonl.gz','rt') as f:
 for l in f:
  x=json.loads(l)
  if 'ompdModule.so' in x['path']:continue
  nonmodule['ELFs']+=1;nonmodule['ALLOC_changes']+=len(x['ALLOC_changes']);nonmodule['content_different']+=sum(not y['contents_equal'] for y in x['ALLOC_changes'])
summary={'nonmodule':dict(nonmodule),'module_content_changes':[{'path':x['path'],'section':s['section'],'ALLOC':s['ALLOC'],'old_bytes':s['old_bytes'],'new_bytes':s['new_bytes']} for x in out for s in x['changes'] if not s['content_equal']],'module_symbol_exception_count':len(exceptions),'note':'Final MODULE comparison aligns by section name; original ordered traversal is retained as preliminary evidence.'};(E/'module-named-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print('MODULE_NAMED 已结束',datetime.datetime.now().astimezone().isoformat(),'status=ok',flush=True)
