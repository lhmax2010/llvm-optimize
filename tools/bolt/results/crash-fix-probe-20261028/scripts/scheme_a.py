from common import *
import re,struct
A=D/'scheme-a';A.mkdir(exist_ok=True)
shutil.copyfile(D/'bolt39/gnu.debug',A/'clang-22.debug')
x=run('scheme-a-add-debuglink',tool('llvm-objcopy')+['--add-gnu-debuglink='+str(A/'clang-22.debug'),WORK/'clang.candidate',A/'clang-22']);assert x['rc']==0
(A/'clang-22').chmod(0o755)
a=h.ELF(WORK/'clang.candidate');b=h.ELF(A/'clang-22');rows=[];diffs=[]
for name,s in a.by_name.items():
 if s[2]&2 and s[1]!=8:
  t=b.by_name.get(name);eq=t is not None and s[3:6]==t[3:6] and a.mm[s[4]:s[4]+s[5]]==b.mm[t[4]:t[4]+t[5]];rows.append({'section':name,'equal':eq});assert eq
for p in a.loads:
 assert p in b.loads
 # Compare in chunks; record exact offsets, including ELF metadata bytes.
 for start in range(p[2],p[2]+p[5],1048576):
  end=min(start+1048576,p[2]+p[5]);x=a.mm[start:end];y=b.mm[start:end]
  if x!=y:diffs.extend(start+i for i,(u,v) in enumerate(zip(x,y)) if u!=v)
props=h.security_properties(A/'clang-22');assert props['DT_RUNPATH']=='$ORIGIN/../lib64'
save('scheme-a-layout.json',{'alloc_sections':rows,'program_headers_equal':a.phdrs==b.phdrs,'load_byte_differences':diffs,'extra_sections':sorted(b.by_name.keys()-a.by_name.keys()),'RUNPATH':props['DT_RUNPATH'],'files':{p.name:{'bytes':p.stat().st_size,'sha256':sha(p)} for p in A.iterdir() if p.is_file()}});a.close();b.close()
addresses=json.loads((B/'tools/bolt/results/crash-probe-20261028/offline-addresses-corrected.json').read_text());save('offline-addresses.json',addresses)
text='\n'.join(x['module_offset'] for x in addresses['addresses'])+'\n'
for role,p in [('debug',A/'clang-22.debug'),('auto-debuglink',A/'clang-22')]:
 x=run('symbolizer-'+role,tool('llvm-symbolizer')+['--obj='+str(p),'--inlining=false'],stdin=text);assert x['rc']==0
units=json.loads((W/'docs/53_hybrid_local_validation_evidence/tu-inputs.json').read_text());keys=list(dict.fromkeys(u['key'].rsplit('/',1)[0] for u in units))[:5];selected=[u for u in units if u['key'].rsplit('/',1)[0] in keys];assert len(selected)==15
slot=A/'same-clang';slot.touch();inode=slot.stat().st_ino;result={}
for role,src in [('final',WORK/'clang.candidate'),('debuglink',A/'clang-22')]:
 shutil.copyfile(src,slot);slot.chmod(0o755);assert slot.stat().st_ino==inode
 for u in selected:
  i=u['index'];out=A/('tu-'+str(i)+'.o');args=list(u['original_argv'][1:]);args.insert(0,'--no-default-config');args[args.index('-c')+1]=u['copy'];args[args.index('-o')+1]=str(out);args=[('-resource-dir='+str(BUILD/'lib64/clang/22') if x.startswith('-resource-dir=') else x) for x in args];assert sha(u['copy'])==u['sha256']
  x=run('tu/'+role+'-'+str(i),['taskset','-c','2',*LD,slot,*args]);assert x['rc']==0,x
  if role=='final':shutil.copyfile(out,A/('ref-'+str(i)+'.o'));result[i]={'key':u['key'],'target':u['target'],'reference_sha256':sha(out)}
  else:result[i].update(candidate_sha256=sha(out),equal=out.read_bytes()==(A/('ref-'+str(i)+'.o')).read_bytes());assert result[i]['equal']
 save('scheme-a-correctness.json',{'PASS':role=='debuglink','pairs':15,'same_inode':inode,'results':result})
print('scheme A layout, symbolizer and 15TU completed',flush=True)
