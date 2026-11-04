from pathlib import Path
import sys,mmap,json,struct,hashlib,gzip
T=Path(__file__).parents[2]/'night-launch-20261103';sys.path.insert(0,str(T))
from section_compare import layout,chunk_equal,digest,strings,comment
W=Path('/home/linhao/Toolchain/development/llvm-optimize');E=Path(__file__).parent
C=W/'temp/debuglink-20261028/full-20261030/products/binaries'
P=W/'temp/night-20261103/toolchain/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/home/abuild/rpmbuild/BUILD/llvm-22.1.8/build/clang-bolt'
Q=W/'temp/qb-1216409-1216410/1216409/extracted/usr/lib/debug/usr/bin/clang-22.debug'
def audit(a,b):
 # 35-MB symbol files are small; this also releases all views before closing.
 aa=a.read_bytes();bb=b.read_bytes();va,ha,sa=layout(aa);vb,hb,sb=layout(bb);rows=[];symbol_differences=[]
 for x,y in zip(sa,sb):
  equal=chunk_equal(x['content'],y['content']);row=dict(section=x['name'],old_offset=x['offset'],new_offset=y['offset'],old_size=x['size'],new_size=y['size'],contents_equal=equal,old_sha256=digest(x['content']),new_sha256=digest(y['content']),metadata_changes=[dict(field=k,old=u,new=v) for k,u,v in zip(('name','type','flags','addr','offset','size','link','info','align','entsize'),x['raw'],y['raw']) if u!=v]);rows.append(row)
  if x['name']=='.comment':row.update(old_strings=comment(x['content']),new_strings=comment(y['content']))
  if x['name']=='.GCC.command.line':
   c,d=strings(x['content']),strings(y['content']);row.update(multisets_equal=c==d,old_strings=dict(c),new_strings=dict(d),changes=[dict(string=s,old=c.get(s,0),new=d.get(s,0)) for s in sorted(c.keys()|d.keys()) if c.get(s,0)!=d.get(s,0)])
  if x['name']=='.symtab' and not equal:
   st_a=bytes(next(s['content'] for s in sa if s['name']=='.strtab'));st_b=bytes(next(s['content'] for s in sb if s['name']=='.strtab'))
   def symbol(data,at,st):
    z=struct.unpack_from('<IBBHQQ',data,at);raw=bytes(st);end=raw.find(b'\0',z[0]);return dict(name=raw[z[0]:end].decode(errors='replace'),st_name=z[0],info=z[1],other=z[2],shndx=z[3],value=z[4],size=z[5])
   for at in range(0,min(x['size'],y['size']),24):
    if x['content'][at:at+24]!=y['content'][at:at+24]:symbol_differences.append(dict(index=at//24,old_file_offset=x['offset']+at,new_file_offset=y['offset']+at,old=symbol(x['content'],at,st_a),new=symbol(y['content'],at,st_b)))
 return dict(old=str(a),new=str(b),old_sha256=hashlib.sha256(aa).hexdigest(),new_sha256=hashlib.sha256(bb).hexdigest(),sections=rows,symbol_differences=symbol_differences)
for label,a,b in [('local-vs-certified',C/'clang-22.debug',P/'clang-22.debug'),('local-vs-QB',P/'clang-22.debug',Q)]:
 r=audit(a,b);(E/(label+'-sections.json')).write_text(json.dumps(r,indent=2)+'\n');print(label,'changed sections',[(x['section'],x['old_size'],x['new_size']) for x in r['sections'] if not x['contents_equal']],'symbol changes',len(r['symbol_differences']))
 for x in r['symbol_differences'][:4]:print(x)
