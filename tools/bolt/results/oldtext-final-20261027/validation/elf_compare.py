from common import *
import struct
old=W/'temp/runpath-fix-20261026/old-text/clang.candidate';new=P/'binaries/clang.candidate'
assert sha(old)=='13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8'
a,b=h.rpath_layout(old),h.rpath_layout(new);save(E/'elf-layout.json',{'old':a,'new':b,'PASS':a==b});assert a==b,'ELF non-path bytes/layout differ'
def dynamic(path):
 e=h.ELF(path);sec=e.by_name['.dynamic'];raw=e.mm[sec[4]:sec[4]+sec[5]];rows=[struct.unpack_from('<qQ',raw,i) for i in range(0,len(raw),16)];e.close();return rows
x,y=dynamic(old),dynamic(new);assert len(x)==len(y)
diffs=[{'index':i,'old_tag':hex(a[0]),'new_tag':hex(b[0]),'old_value':a[1],'new_value':b[1]} for i,(a,b) in enumerate(zip(x,y)) if a!=b]
assert not diffs,'unexpected raw dynamic tag/value changes'
for name,p in [('old',old),('new',new)]:
 (E/('elf-'+name+'-dynamic.txt')).write_text(subprocess.check_output(['readelf','-dW',str(p)],text=True))
props={n:{k:v for k,v in h.security_properties(p).items() if k in ['DT_RPATH','DT_RUNPATH']} for n,p in [('old',old),('new',new)]}
save(E/'elf-comparison.json',{'PASS':True,'old_sha':sha(old),'new_sha':sha(new),'size':new.stat().st_size,'dynamic_value_differences':diffs,'decoded_path_tags':props,'note':'Equal layout includes all program/section headers and SHA of all file bytes outside .dynstr/.dynamic; dynamic values directly compared separately.'})
print('ELF_PASS',diffs,props,flush=True)

a=h.ELF(old);b=h.ELF(new)
try:
 assert len(a.mm)==len(b.mm)==152532296 and a.phdrs==b.phdrs and a.sections==b.sections
 spans=sorted((sec[4],sec[4]+sec[5]) for name,sec in a.by_name.items() if name in ('.dynstr','.dynamic'));pos=0;compared=0
 for start,end in spans+[(len(a.mm),len(a.mm))]:
  for at in range(pos,start,1024*1024):
   until=min(at+1024*1024,start);assert a.mm[at:until]==b.mm[at:until];compared+=until-at
  pos=end
 assert props['new']=={'DT_RPATH':None,'DT_RUNPATH':'$ORIGIN/../lib64'}
 save(E/'elf-literal-bytes.json',{'PASS':True,'compared_bytes':compared,'file_bytes':len(a.mm),'excluded_ranges':spans,'program_headers_equal':True,'section_headers_equal':True,'raw_dynamic_equal':True})
finally:a.close();b.close()
