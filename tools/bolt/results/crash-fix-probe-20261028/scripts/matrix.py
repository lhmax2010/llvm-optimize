from common import *
import struct,itertools
inputs={'bolt39':WORK/'clang.bolt','bolt37':OLD/'clang.bolt','ordinary':WORK/'ordinary-clang-22'};results=[];ids={};structures={}
for role,src in inputs.items():
 if not src.exists():results.append({'input':role,'status':'missing'});continue
 ids[role]={'path':str(src),'bytes':src.stat().st_size,'sha256':sha(src)};out=D/role;out.mkdir(exist_ok=True)
 for name,argv in [('llvm-keep',tool('llvm-objcopy')+['--only-keep-debug',src,out/'llvm.debug']),('gnu-keep',['/usr/bin/objcopy','--only-keep-debug',src,out/'gnu.debug']),('eu-strip',[*LD,str(R/'usr/bin/eu-strip'),'-f',out/'eu.debug','-o',out/'eu.stripped',src]),('llvm-strip-all',tool('llvm-strip')+['--strip-all','-o',out/'llvm.stripped',src]),('llvm-debuglink',tool('llvm-objcopy')+['--add-gnu-debuglink='+str(out/'gnu.debug'),src,out/'llvm.debuglinked'])]:
  x=run('matrix/'+role+'-'+name,argv,timeout=240);x.update(input=role,operation=name,status='success' if x['rc']==0 else 'crash' if x['rc']<0 else 'error');results.append(x);save('matrix.json',results);print(role,name,x['status'],flush=True)
 run('elf/'+role+'-gnu',['readelf','-h','-l','-S','-W',src]);run('elf/'+role+'-llvm',tool('llvm-readelf')+['-h','-l','-S','-W',src])
 a=h.ELF(src);loads=[(i,p) for i,p in enumerate(a.phdrs) if p[0]==1];shoff=struct.unpack_from('<Q',a.mm,40)[0];rows=[]
 for name,s in a.by_name.items():
  if not name:continue
  inside=[];cross=[]
  for i,p in loads:
   if p[3]<=s[3] and s[3]+s[5]<=p[3]+p[6]:inside.append(i)
   elif s[2]&2 and max(s[3],p[3])<min(s[3]+s[5],p[3]+p[6]):cross.append(i)
  rows.append({'name':name,'type':s[1],'flags':s[2],'offset':s[4],'address':s[3],'size':s[5],'memory_contained_by_LOAD':inside if s[2]&2 else 'non-ALLOC not required','crosses_LOAD_memory_boundary':cross})
 overlaps=[]
 for (i,p),(j,q) in itertools.combinations(loads,2):
  for axis,off,size in [('file',2,5),('memory',3,6)]:
   if max(p[off],q[off])<min(p[off]+p[size],q[off]+q[size]):overlaps.append({'segments':[i,j],'axis':axis})
 structures[role]={'file_bytes':len(a.mm),'section_header_offset':shoff,'section_header_count':len(a.sections),'phdrs':a.phdrs,'LOAD_checks':[{'index':i,'offset':p[2],'vaddr':p[3],'filesz':p[5],'memsz':p[6],'align':p[7],'filesz_le_memsz':p[5]<=p[6],'range_in_file':p[2]+p[5]<=len(a.mm),'congruent':p[7]<=1 or p[2]%p[7]==p[3]%p[7]} for i,p in loads],'LOAD_overlaps':overlaps,'sections':rows};a.close();save('elf-structures.json',structures)
 assert sha(src)==ids[role]['sha256']
save('input-identities.json',ids)
for name,argv in [('gnu-objcopy-version',['objcopy','--version']),('eu-strip-version',[*LD,R/'usr/bin/eu-strip','--version']),('llvm-objcopy-version',tool('llvm-objcopy')+['--version'])]:run(name,argv)
# Inventory existing BOLT work ELF inputs; do not substitute ordinary for a debug relink.
inventory=[]
for p in WORK.iterdir():
 if p.is_file():
  with p.open('rb') as f:magic=f.read(4)
  if magic==b'\x7fELF':
   a=h.ELF(p);inventory.append({'path':str(p),'bytes':p.stat().st_size,'debug_sections':[n for n in a.names if n.startswith(('.debug','.zdebug'))],'relocation_sections':[n for n in a.names if n in ('.rela.text','.rel.text')],'sha256':sha(p)});a.close()
save('relink-inventory.json',inventory);print('matrix completed',flush=True)
