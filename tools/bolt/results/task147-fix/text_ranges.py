from pathlib import Path
from collections import Counter
import json,sys,struct
W=Path("/home/linhao/Toolchain/development/llvm-optimize")
N=Path(__file__).resolve().parent
sys.path.insert(0,str(W/"archive/task145"))
from elf_analysis import Elf,SY
prefix="_ZN5clang6driver6DriverC"
def bounds(elf,name):
    idx=elf.names.index(".symtab")
    section=elf.raw[idx]
    labels=elf.payload(section[6])
    intervals={}
    for name_offset,info,other,ndx,value,size in SY.iter_unpack(elf.payload(idx)):
        if info&0xf!=2 or not name_offset or not 0<ndx<len(elf.names) or elf.names[ndx]!=name:
            continue
        sym=Elf.string(labels,name_offset)
        if sym.startswith(prefix):
            offset=value-elf.raw[ndx][3]
            intervals[sym]=[offset,offset+size]
    return intervals
def changed_bytes(a,b):
    for i in range(0,min(len(a),len(b)),65536):
        x,y=a[i:i+65536],b[i:i+65536]
        if x!=y:
            yield from (i+j for j,(o,n) in enumerate(zip(x,y)) if o!=n)
def words(l,r,name,ref):
    ld,rd=l.names.index(name),r.names.index(name)
    txt,rtxt=l.names.index(ref),r.names.index(ref)
    lv,rv=l.raw[ld][3],r.raw[rd][3]
    dv=r.raw[rtxt][3]-l.raw[txt][3]-(rv-lv)
    a,b=l.payload(ld),r.payload(rd)
    if len(a)!=len(b):
        return {"before":len(a),"after":len(b),"same_length":False}
    changed=sorted({i-i%4 for i in changed_bytes(a,b)})
    counts=Counter()
    examples=[]
    for i in changed:
        if i+4>len(a):
            counts["partial_field"]+=1
            continue
        before,after=struct.unpack_from("<i",a,i)[0],struct.unpack_from("<i",b,i)[0]
        counts[str(after-before)]+=1
        if len(examples)<4:
            examples.append({"offset":f"{i:#x}","before_hex":a[i:i+4].hex(),"after_hex":b[i:i+4].hex()})
    return {"bytes":len(a),"text_minus_section_VA_delta":dv,"changed_word_delta_counts":dict(counts),"samples":examples}
out={}
for idx in (10,24,25,156):
    p=N/"binaries"/str(idx)
    with Elf(p/"old.symbols") as l,Elf(p/"new.symbols") as r:
        aa=l.section(".text");bb=r.section(".text")
        addrs=[bounds(e,".text") for e in (l,r)]
        uncertain=0
        ex=[]
        count=0
        for i in changed_bytes(aa,bb):
            count+=1
            if not any(x<=i<y for ranges in addrs for x,y in ranges.values()):
                uncertain+=1
                if len(ex)<20:ex.append({"offset":f"{i:#x}","old":f"{aa[i]:02x}","new":f"{bb[i]:02x}"})
        out[idx]={"text_lengths":[len(aa),len(bb)],"constructor_ranges":addrs,
                  "text_byte_differences":count,"text_byte_differences_outside_ctor":uncertain,
                  "outside_examples":ex,"relative_words":{k:words(l,r,k,".text")
                                                    for k in (".rodata",".eh_frame",".eh_frame_hdr")
                                                    if k in l.names and k in r.names}}
(N/"section-offset-proof.json").write_text(json.dumps(out,indent=2)+"\n")
