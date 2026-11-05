"""Read-only explanation of finished comparison failures; does not rerun or relax gates."""
from pathlib import Path
import json,mmap,struct,hashlib,collections,gzip,difflib
E=Path(__file__).resolve().parent;D=Path('/home/linhao/Toolchain/development/llvm-optimize/temp/night-20261105/toolchain');V=D/'validation'
r=json.loads((V/'qb-rpm-comparison.json').read_text());fm=json.loads((V/'qb-changed-file-paths.json').read_text());maps={(x['package'],x['path']):x for x in fm}
def layout(m):
 if m[:6]!=b'\x7fELF\x02\x01':return None
 h=struct.unpack_from('<HHIQQQIHHHHHH',m,16);ss=[struct.unpack_from('<IIQQQQIIQQ',m,h[5]+i*h[10]) for i in range(h[11])];s=ss[h[12]];ns=m[s[4]:s[4]+s[5]]
 return h,[(ns[x[0]:].split(b'\0',1)[0].decode(),x) for x in ss]
def digest(m,x):
 h=hashlib.sha256()
 if x[1]!=8:
  for p in range(x[4],x[4]+x[5],1024*1024):h.update(m[p:min(p+1024*1024,x[4]+x[5])])
 return h.hexdigest()
results=[];counts=collections.Counter()
for pkg in r:
 for row in pkg['content_changes']:
  z={'package':pkg['package'],'path':row['path'],'gate':row['classification'],'gate_error':row.get('error'),'old_sha256':row['old_sha'],'new_sha256':row['new_sha'],'changed_sections':[]}
  pair=maps.get((pkg['package'],row['path']))
  if pair:
   with open(pair['old'],'rb') as fa,open(pair['new'],'rb') as fb:
    with mmap.mmap(fa.fileno(),0,access=mmap.ACCESS_READ) as a,mmap.mmap(fb.fileno(),0,access=mmap.ACCESS_READ) as b:
     aa,bb=layout(a),layout(b)
     if aa and bb:
      ha,sa=aa;hb,sb=bb;z['program_headers_equal']=a[ha[4]:ha[4]+ha[8]*ha[9]]==b[hb[4]:hb[4]+hb[8]*hb[9]];z['section_order_equal']=[n for n,_ in sa]==[n for n,_ in sb]
      if z['section_order_equal']:
       for (name,x),(_,y) in zip(sa,sb):
        ah,bh=digest(a,x),digest(b,y)
        if ah==bh and x[5]==y[5]:continue
        q={'section':name,'old_size':x[5],'new_size':y[5],'old_offset':x[4],'new_offset':y[4],'old_sha256':ah,'new_sha256':bh};counts[name]+=1
        if name=='.debug_str':
         av=a[x[4]:x[4]+x[5]];bv=b[y[4]:y[4]+y[5]];old=b'usr/src/debug/llvm-22.1.8-1.x86_64';new=b'usr/src/debug/llvm-22.1.8-2.1.x86_64';q['release_prefix_replacement_equal']=av.replace(old,new)==bv;q['old_prefix_count']=av.count(old);q['new_prefix_count']=bv.count(new);q['old_examples']=[v.decode(errors='replace') for v in av.split(b'\0') if old in v][:3];q['new_examples']=[v.decode(errors='replace') for v in bv.split(b'\0') if new in v][:3]
        z['changed_sections'].append(q)
  if row.get('error')=='payload permission/owner/type/link changed':
   base=V/'manifests/toolchain';a=json.loads((base/(pkg['package'].replace('\t','-')+'-old.json')).read_text())[row['path']];b=json.loads((base/(pkg['package'].replace('\t','-')+'-new.json')).read_text())[row['path']];z['metadata_changes']={k:{'old':a.get(k),'new':b.get(k)} for k in ['mode','uid','gid','target'] if a.get(k)!=b.get(k)}
  results.append(z)
(E/'difference-details.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
with gzip.open(E/'all-file-differences.tsv.gz','wt') as f:
 f.write('package\tpath\tkind\tactual_changed_sections\tgate_reason\n')
 for z in results:f.write('\t'.join([z['package'].replace('\t','/'),z['path'],'changed',','.join(x['section'] for x in z['changed_sections']) or 'N/A',z['gate_error'] or ''])+'\n')
 for p in r:
  for k in ['added','removed']:
   for name in p[k]:f.write('\t'.join([p['package'].replace('\t','/'),name,k,'N/A','payload path set differs'])+'\n')
source=V/'payload/toolchain/llvm-src';a=(source/'old/llvm.spec').read_text();b=(source/'new/llvm.spec').read_text();(E/'source-spec.diff').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='local/llvm.spec',tofile='QB/llvm.spec')))
pkg=next(x for x in r if x['package']=='llvm-debugsource\tx86_64');a=json.loads((V/'manifests/toolchain/llvm-debugsource-x86_64-old.json').read_text());b=json.loads((V/'manifests/toolchain/llvm-debugsource-x86_64-new.json').read_text());pairs=[]
for old in pkg['removed']:
 new=old.replace('llvm-22.1.8-1.x86_64','llvm-22.1.8-2.1.x86_64',1)
 if new not in b:pairs.append({'old':old,'new':new,'missing':True});continue
 changes={k:{'old':a[old].get(k),'new':b[new].get(k)} for k in ['mode','uid','gid','bytes','sha256','target'] if a[old].get(k)!=b[new].get(k)}
 pairs.append({'old':old,'new':new,'changes':changes})
with gzip.open(E/'debugsource-prefix-pairs.json.gz','wt') as f:json.dump(pairs,f,ensure_ascii=False,indent=2)
s={'file_changes':len(results),'section_counts':dict(counts),'debugsource_paths_paired':len(pairs),'debugsource_unmatched_or_other_differences':sum(bool(x.get('missing') or x.get('changes')) for x in pairs)}
(E/'difference-summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))
