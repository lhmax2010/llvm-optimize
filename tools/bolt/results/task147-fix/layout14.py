from collections import Counter,defaultdict
from itertools import zip_longest
from pathlib import Path
import json,re,subprocess,sys,traceback

W=Path("/home/linhao/Toolchain/development/llvm-optimize")
A=W/"archive/task144"
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(W/"archive/task145"))
from elf_analysis import Elf, run
root=A/"b1-a1/gbs-root/local/BUILD-ROOTS/scratch.x86_64.0/usr"
objdump=[root/"lib64/ld-linux-x86-64.so.2","--library-path",root/"lib64",root/"bin/llvm-objdump"]
byte_line=re.compile(rb"^\s*([a-fA-F0-9]+): +([a-fA-F0-9]{2}(?: [a-fA-F0-9]{2})*) *\t(\S.*)$")
PCREL=re.compile(rb"(-?(?:0x[0-9a-f]+|[0-9]+))\(%rip\)")
BRANCH=re.compile(rb"^(?:j[a-z]+|callq?|loop[a-z]*)\s+(0x[0-9a-f]+)(?:\s|$)")
ABS_ANN=re.compile(rb"\s+#\s+0x[0-9a-f]+.*$")
hexn=lambda value:int(value,0)
def section(elf,address):
    found=[]
    for num,s in enumerate(elf.raw):
        if s[2]&2 and s[3]<=address<s[3]+s[5]:
            found.append((elf.names[num],address-s[3]))
    return found
def instructions(image,elf,name):
    idx=elf.names.index(name)
    code=elf.payload(idx)
    address=elf.raw[idx][3]
    end=0
    for l in run([*objdump,"-d","-z","--full-leading-addr","--section="+name,image],OUT/"layout-stderr.txt"):
        m=byte_line.match(l)
        if not m: continue
        pc=int(m[1],16)
        value=bytes.fromhex(m[2].decode())
        pos=pc-address
        if pos!=end or code[pos:pos+len(value)]!=value:
            raise RuntimeError(f"incomplete/nonconsecutive raw byte coverage {image}:{name} {pc:#x} {pos} vs {end}")
        end=pos+len(value)
        yield pos,pc,value,m[3].rstrip(),l.decode(errors="replace").rstrip("\n")
    if end!=len(code): raise RuntimeError(f"disassembly stopped before section end {image}:{name}, {end} vs {len(code)}")
def tag_offset(before,after):
    pos,pc,b,insn,raw=before
    new_pos,new_pc,c,ninsn,nraw=after
    if pos!=new_pos or len(b)!=len(c): return None
    rip=PCREL.search(insn)
    nrip=PCREL.search(ninsn)
    direct=BRANCH.match(insn)
    ndirect=BRANCH.match(ninsn)
    kind=None
    if rip and nrip:
        left=PCREL.sub(b"DISP(%rip)",ABS_ANN.sub(b"",insn))
        right=PCREL.sub(b"DISP(%rip)",ABS_ANN.sub(b"",ninsn))
        d,e=hexn(rip[1]),hexn(nrip[1])
        target,new_target=pc+len(b)+d,new_pc+len(c)+e
        widths=(4,)
        kind="RIP-relative"
    elif direct and ndirect:
        left=insn.split()[0]
        right=ninsn.split()[0]
        target,new_target=hexn(direct[1]),hexn(ndirect[1])
        d,e=target-pc-len(b),new_target-new_pc-len(c)
        widths=(1,4)
        kind="direct branch/call"
    else:
        return None
    if left!=right: return None
    for width in widths:
        if not -(1<<(8*width-1))<=d<1<<(8*width-1) or not -(1<<(8*width-1))<=e<1<<(8*width-1): continue
        db,dc=d.to_bytes(width,"little",signed=True),e.to_bytes(width,"little",signed=True)
        offsets=[i for i in range(len(b)-width+1) if b[i:i+width]==db and c[i:i+width]==dc
                 and b[:i]==c[:i] and b[i+width:]==c[i+width:]]
        if offsets: return kind,target,new_target,offsets[0],width
    return None
def prove(a,b,old,new,name):
    answer=Counter()
    classes=Counter()
    examples=[]
    unproved=[]
    target_deltas=[]
    for x,y in zip_longest(instructions(a,old,name),instructions(b,new,name)):
        answer["instruction_pairs"]+=1
        if x and y and x[0]==y[0] and x[2]==y[2]: continue
        answer["changed_instruction_encodings"]+=1
        pair=tag_offset(x,y) if x and y else None
        if not pair:
            answer["other_changes"]+=1
            if len(unproved)<30: unproved.append((x[-1] if x else None,y[-1] if y else None))
            continue
        t,l,r,offset,width=pair
        ll,rr=section(old,l),section(new,r)
        exact=bool(ll and ll==rr)
        k="same_section_offset" if exact else "target_mapping_differs"
        answer[k]+=1
        classes[(t,k)] += 1
        rec={"kind":t,"encoding_change_at":offset,"size":width,"old":x[-1],"new":y[-1],
             "old_target":ll,"new_target":rr}
        if len(examples)<8: examples.append(rec)
        if not exact and len(target_deltas)<50: target_deltas.append(rec)
    return {"counts":dict(answer),"types":[[str(x),y] for x,y in classes.items()],"samples":examples,
            "other_original":unproved,"different_target_samples":target_deltas}
def main():
    bins=OUT/"binaries"
    results={}
    for idx in (10,98,99,100,101,102,103,104,105,107,144,156):
        work=bins/str(idx)
        try:
            l,r=work/"old.symbols",work/"new.symbols"
            with Elf(l) as old,Elf(r) as new:
                le=old.fingerprints(); re=new.fingerprints()
                change=[name for name in old.names if name in new.names and old.raw[old.names.index(name)][2]&4
                        and le.get(name)!=re.get(name)]
                result={name:prove(l,r,old,new,name) for name in change}
            results[idx]=result
        except Exception:
            stop=traceback.format_exc()
            results[idx]={"STOP":stop}
            (work/"layout-STOP.txt").write_text(stop)
        print(idx,{n:v.get("counts") if isinstance(v,dict) else v for n,v in results[idx].items()},flush=True)
    (OUT/"b-layout.json").write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n")
if __name__=="__main__":
    main()
