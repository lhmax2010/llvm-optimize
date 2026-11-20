from pathlib import Path
from collections import defaultdict
import json,subprocess
from layout14 import OUT,Elf,objdump,byte_line,tag_offset,section
from elf_analysis import SY
def reads(e,base,point):
    sym=e.raw[e.names.index(".symtab")]
    tables=e.payload(sym[6])
    target=e.names.index(".text")
    found=[]
    for st,inf,_,ndx,start,size in SY.iter_unpack(e.section(".symtab")):
        if ndx==target and inf&15==2 and start<=point+base<start+size:
            found.append((start,size,Elf.string(tables,st)))
    if not found: raise RuntimeError(f"No containing function at {point:#x}: {e.path}")
    start,size,name=max(found,key=lambda x:x[0])
    output=subprocess.check_output(list(map(str,[*objdump,"-d","-z","--full-leading-addr","--section=.text",
        f"--start-address={start:#x}",f"--stop-address={start+size:#x}",e.path])))
    for line in output.splitlines():
        if m:=byte_line.match(line):
            pc=int(m[1],16)
            b=bytes.fromhex(m[2].decode())
            if pc<=point+base<pc+len(b):
                return (pc-base,pc,b,m[3],line.decode(errors="replace")),name
    raise RuntimeError(f"Missing instruction for {point:#x}: {e.path}")
def string(e,addr):
    where=section(e,addr)
    if len(where)!=1 or where[0][0]!=".rodata":
        return where,None
    sec,off=where[0]
    data=e.section(sec)
    end=data.find(b"\0",off)
    return where,data[off:end] if end>=0 else None
def main():
    document=json.loads((OUT/"section-offset-proof.json").read_text())
    findings=[]
    for idx in ("24","25"):
        q=OUT/"binaries"/idx
        d=document[idx]
        assert d["text_byte_differences_outside_ctor"]==len(d["outside_examples"])
        with Elf(q/"old.symbols") as l,Elf(q/"new.symbols") as r:
            l_off=l.raw[l.names.index(".text")][3]
            r_off=r.raw[r.names.index(".text")][3]
            used=set()
            for item in d["outside_examples"]:
                offset=int(item["offset"],16)
                if offset in used: continue
                x,a=reads(l,l_off,offset)
                y,b=reads(r,r_off,offset)
                proof=tag_offset(x,y)
                where_l=where_r=val_a=val_b=None
                if proof:
                    _,lt,rt,_,_=proof
                    where_l,val_a=string(l,lt)
                    where_r,val_b=string(r,rt)
                result={"entry":idx,"function_old":a,"function_new":b,"text_instruction_offset":f"{x[0]:#x}",
                        "old_raw":x[-1],"new_raw":y[-1],"only_relative_encoding_differs":bool(proof),
                        "old_target":where_l,"new_target":where_r,
                        "same_string":val_a is not None and val_a==val_b,
                        "old_string":val_a.decode(errors="replace") if val_a is not None else None,
                        "new_string":val_b.decode(errors="replace") if val_b is not None else None}
                findings.append(result)
                used.update(range(x[0],x[0]+len(x[2])))
    (OUT/"clang-dso-other-references.json").write_text(json.dumps(findings,indent=2,ensure_ascii=False)+"\n")
    print([(r["entry"],r["only_relative_encoding_differs"],r["same_string"]) for r in findings],flush=True)
if __name__=="__main__":
    main()
