from common import *
import struct
old=OLD/'binaries/clang.candidate';new=P/'binaries/clang.candidate'
a,b=h.rpath_layout(old),h.rpath_layout(new);save(E/'elf-layout.json',{'old':a,'new':b,'PASS':a==b});assert a==b,'ELF non-path bytes/layout differ'
def dynamic(path):
 e=h.ELF(path);sec=e.by_name['.dynamic'];raw=e.mm[sec[4]:sec[4]+sec[5]];rows=[struct.unpack_from('<qQ',raw,i) for i in range(0,len(raw),16)];e.close();return rows
x,y=dynamic(old),dynamic(new);assert len(x)==len(y)
diffs=[{'index':i,'old_tag':hex(a[0]),'new_tag':hex(b[0]),'old_value':a[1],'new_value':b[1]} for i,(a,b) in enumerate(zip(x,y)) if a!=b]
for name,p in [('old',old),('new',new)]:
 (E/('elf-'+name+'-dynamic.txt')).write_text(subprocess.check_output(['readelf','-dW',str(p)],text=True))
props={n:{k:v for k,v in h.security_properties(p).items() if k in ['DT_RPATH','DT_RUNPATH']} for n,p in [('old',old),('new',new)]}
save(E/'elf-comparison.json',{'PASS':True,'old_sha':sha(old),'new_sha':sha(new),'size':new.stat().st_size,'dynamic_value_differences':diffs,'decoded_path_tags':props,'note':'Equal layout includes all program/section headers and SHA of all file bytes outside .dynstr/.dynamic; dynamic values directly compared separately.'})
print('ELF_PASS',diffs,props,flush=True)
