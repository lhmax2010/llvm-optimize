from collections import Counter, defaultdict
from pathlib import Path
import difflib
import hashlib
import mmap
import re
import shutil
import stat
import struct
import subprocess

EH = struct.Struct("<16sHHIQQQIHHHHHH")
SH = struct.Struct("<IIQQQQIIQQ")
SY = struct.Struct("<IBBHQQ")

class Elf:
    def __init__(self, path):
        self.path = path
        self.handle = path.open("rb")
        self.data = mmap.mmap(self.handle.fileno(),0,access=mmap.ACCESS_READ)
        self.header = list(EH.unpack_from(self.data))
        if not self.header[0].startswith(b"\x7fELF\x02\x01"):
            raise ValueError(f"expected little-endian ELF64: {path}")
        start, count, names = self.header[6], self.header[12], self.header[13]
        if self.header[11] != SH.size or not 0 < names < count:
            raise ValueError(f"unsupported ELF section layout: {path}")
        self.raw = [list(SH.unpack_from(self.data,start+i*SH.size)) for i in range(count)]
        table = self.raw[names]
        namebytes = self.data[table[4]:table[4]+table[5]]
        self.names = [self.string(namebytes,s[0]) for s in self.raw]

    @staticmethod
    def string(table,offset):
        end = table.find(b"\0",offset)
        if end < 0:
            raise ValueError(f"invalid string offset {offset}")
        return table[offset:end].decode("utf-8","replace")

    def payload(self, idx):
        sec = self.raw[idx]
        return self.data[sec[4]:sec[4]+sec[5]]

    def section(self,name):
        return self.payload(self.names.index(name)) if name in self.names else None

    def fingerprints(self):
        ans = defaultdict(list)
        with memoryview(self.data) as data:
            for name,s in zip(self.names[1:],self.raw[1:]):
                t,flags,offset,size = s[1],s[2],s[4],s[5]
                value = None if t==8 else hashlib.sha256(data[offset:offset+size]).hexdigest()
                ans[name].append((t,flags,size,value))
        return dict(ans)

    def id(self):
        payload = self.section(".note.gnu.build-id")
        if not payload or len(payload)<16:
            return None
        namesz,descsz,kind = struct.unpack_from("<III",payload)
        off = 12+(namesz+3)//4*4
        if namesz!=4 or kind!=3 or payload[12:16]!=b"GNU\0" or not 0<descsz<=len(payload)-off:
            raise ValueError(f"invalid GNU build-id: {self.path}")
        return payload[off:off+descsz].hex()

    def close(self):
        self.data.close()
        self.handle.close()

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.close()

def is_elf(p):
    with p.open("rb") as f:
        return f.read(6)==b"\x7fELF\x02\x01"

def symbols(shipped, debug, dst):
    """Restore only symbol metadata in an offline copy; keep instruction bytes."""
    funcs = defaultdict(set)
    with Elf(shipped) as s, Elf(debug) as d:
        idx = d.names.index(".symtab")
        sec = d.raw[idx].copy()
        strings = d.payload(sec[6])
        data = bytearray(d.payload(idx))
        if sec[9]!=SY.size or len(data)%SY.size:
            raise ValueError(f"unsupported symtab {debug}")
        mapping = {}
        for i,(name,x) in enumerate(zip(d.names,d.raw)):
            found = [j for j,(n,y) in enumerate(zip(s.names,s.raw)) if n==name and y[3]==x[3] and y[5]==x[5]]
            if len(found)==1:
                mapping[i]=found[0]
        for offset in range(0,len(data),SY.size):
            name,info,other,section,value,size = SY.unpack_from(data,offset)
            if not 0<section<0xff00:
                continue
            mapped = mapping.get(section,0)
            SY.pack_into(data,offset,name,info,other,mapped,value,size)
            if (info&15)==2 and name and size and d.raw[section][2]&4:
                if mapped==0 or not(s.raw[mapped][3]<=value and value+size<=s.raw[mapped][3]+s.raw[mapped][5]):
                    raise ValueError(f"function outside matching executable section: {debug} {offset}")
                funcs[(s.names[mapped],Elf.string(strings,name))].add((value,size))
        if not funcs:
            raise ValueError(f"no executable function symbols: {debug}")
        headers = [x.copy() for x in s.raw]
        name_index = s.header[13]
        names = s.payload(name_index)
        sym_name = len(names)
        strings_name = sym_name+len(b".symtab\0")
        names += b".symtab\0.strtab\0"
        with shipped.open("rb") as source, dst.open("wb") as out:
            shutil.copyfileobj(source,out,1024**2)
            def append(value,alignment):
                out.write(b"\0"*((-out.tell())%alignment))
                location=out.tell()
                out.write(value)
                return location
            headers[name_index][4:6] = [append(names,1),len(names)]
            sec[0],sec[4],sec[6]=sym_name,append(data,8),len(headers)+1
            headers.append(sec)
            headers.append([strings_name,3,0,0,append(strings,1),len(strings),0,0,1,0])
            table = append(b"".join(SH.pack(*x) for x in headers),8)
            h=s.header.copy()
            h[6],h[12]=table,len(headers)
            out.seek(0)
            out.write(EH.pack(*h))
    with Elf(shipped) as s, Elf(dst) as copy:
        for i,(name,sec) in enumerate(zip(s.names,s.raw)):
            if sec[2]&4 and hashlib.sha256(s.payload(i)).digest()!=hashlib.sha256(copy.payload(i)).digest():
                raise ValueError(f"executable bytes changed when restoring metadata: {name}")
    return funcs

def exec_sections(elf):
    return {name:hashlib.sha256(elf.payload(i)).hexdigest()
            for i,(name,sec) in enumerate(zip(elf.names,elf.raw)) if sec[2]&4 and sec[1]!=8}

def run(cmd, stderr):
    with stderr.open("ab") as err:
        p=subprocess.Popen(list(map(str,cmd)),stdout=subprocess.PIPE,stderr=err)
        try:
            yield from p.stdout
        finally:
            p.stdout.close()
            rc=p.wait()
        if rc:
            raise RuntimeError(f"exit={rc} running {cmd}; see {stderr}")

def unit_names(tool, path, err):
    names=set()
    units=0
    in_unit=False
    for raw in run([*tool,"--debug-info","--recurse-depth=0",path],err):
        s=raw.decode("utf-8","replace")
        if re.search(r":\s+DW_TAG_",s):
            in_unit=s.rstrip().endswith("DW_TAG_compile_unit")
            units+=in_unit
        elif in_unit and (m:=re.search(r'DW_AT_name\s*\("(.*)"\)',s)):
            names.add(m[1])
    return names,units

HEX = re.compile(r'(?<![\w.$])(?:-?0x[0-9a-fA-F]+)(?![\w])')
DISPLACEMENT = re.compile(r'(?<!\w)(?:-?0x[0-9a-fA-F]+|-?\d+)(?=\()')
LOCAL = re.compile(r'(?<=<)L\d+(?=>)')
HEAD = re.compile(r'^(?:[0-9a-fA-F]+\s+)?<(.+)>:$')
COLD = re.compile(r'^(.*?)\.cold(?:\.(\d+))?$')

def normalize(line):
    line = re.sub(r'#\s*(?:0x[0-9a-fA-F]+|<[^>]+>).*$',"",line)
    line = LOCAL.sub("ADDR",line)
    line = DISPLACEMENT.sub("OFFSET",line)
    line = re.sub(r"\$(-?0x[0-9a-fA-F]+)",r"IMMEDIATE(\1)",line)
    line = re.sub(r"IMMEDIATE\(([^)]+)\)|"+HEX.pattern,
                  lambda match:"$"+match[1] if match[1] is not None else "ADDR",line)
    return " ".join(line.split())

def disassemble(tool, path, funcs, raw_path, error_path):
    starts={k:sorted(v) for k,v in funcs.items()}
    rows=defaultdict(list)
    section=None
    block=None
    offset=0
    running=None
    start=None
    count=0
    def flush():
        if running is not None and count:
            rows[block].append((running.hexdigest(),count,start,offset))
    with raw_path.open("wb") as out:
        for raw in run([*tool,"-d","--no-show-raw-insn","--no-leading-addr","--symbolize-operands",path],error_path):
            s=raw.decode("utf-8","replace").rstrip()
            header=HEAD.fullmatch(s)
            if s.startswith("Disassembly of section "):
                flush()
                section=s.removeprefix("Disassembly of section ").removesuffix(":")
                block=None
                running=None
            elif header and not re.fullmatch(r"L\d+",header[1]):
                flush()
                name=header[1]
                block=(section,name)
                running=hashlib.sha256()
                start=offset
                count=0
            elif s.startswith((" ","\t")) and s.strip():
                if running is None:
                    block=(section,"<implicit>")
                    running=hashlib.sha256()
                    start=offset
                    count=0
                running.update((normalize(s)+"\n").encode())
                count+=1
            out.write(raw)
            offset+=len(raw)
        flush()
    addr_map=defaultdict(list)
    for (sec,name),ranges in starts.items():
        for addr,size in ranges:
            addr_map[(sec,addr)].append(name)
    names_present=set(rows)
    missing=sum(not any((sec,n) in names_present for n in names) for (sec,_),names in addr_map.items())
    annotated={key:len(value) for key,value in rows.items()}
    return rows,{"function_symbols":len(funcs),"distinct_function_addresses":len(addr_map),
                 "function_addresses_without_matching_named_block":missing,"disassembly_blocks":len(annotated),
                 "instructions":sum(r[1] for values in rows.values() for r in values)}

def merge(rows,cold):
    grouped=defaultdict(list)
    for (section,name),blocks in rows.items():
        match=COLD.fullmatch(name) if cold and section!=".bolt.org.text" else None
        group=match[1] if match else name
        section_key=".text" if cold and section in (".text",".text.cold") else section
        pos=(1,int(match[2] or 0),name) if match else (0,0,name)
        for seq,record in enumerate(blocks):
            grouped[(section_key,group)].append((pos,seq,record))
    return {k:[record for _,_,record in sorted(v)] for k,v in grouped.items()}

def records(raw_path, spans, limit):
    result=[]
    with raw_path.open("rb") as f:
        for _,_,start,end in spans:
            f.seek(start)
            while f.tell()<end and len(result)<limit:
                result.append(f.readline().decode("utf-8","replace").rstrip("\n"))
    return result

def sequence(raw_path, rows, cold):
    if not rows:
        return None
    if not cold or len(rows)==1:
        return tuple((h,n) for h,n,*_ in rows)
    h=hashlib.sha256()
    n=0
    with raw_path.open("rb") as f:
        for _,_,start,end in rows:
            f.seek(start)
            while f.tell()<end:
                line=f.readline().decode("utf-8","replace").rstrip()
                if line.startswith((" ","\t")) and line.strip():
                    h.update((normalize(line)+"\n").encode())
                    n+=1
    return ((h.hexdigest(),n),)

def compared(lhs,rhs,lhraw,rhraw,cold):
    left,right=merge(lhs,cold),merge(rhs,cold)
    keys=left.keys()|right.keys()
    changed=[]
    for k in sorted(keys):
        l=sequence(lhraw,left.get(k,()),cold)
        r=sequence(rhraw,right.get(k,()),cold)
        if l!=r:
            changed.append(k)
    sample=[]
    for k in changed[:20]:
        l=records(lhraw,left.get(k,()),2400)
        r=records(rhraw,right.get(k,()),2400)
        diff=difflib.unified_diff(l,r,fromfile="PS5 raw",tofile="C2 raw",n=3)
        limit=50
        rows=[]
        for line in diff:
            if len(rows)>=limit:
                break
            rows.append(line.rstrip("\n"))
        sample.append({"section":k[0],"function":k[1],"old_lengths":[x[1] for x in left.get(k,())],
                       "new_lengths":[x[1] for x in right.get(k,())],"raw_diff_first_hunks":rows})
    return {"compared":len(keys),"equal":len(keys)-len(changed),"different":len(changed),
            "old_only":len(left.keys()-right.keys()),"new_only":len(right.keys()-left.keys()),
            "names":[{"section":sec,"function":name} for sec,name in changed],"first_twenty":sample}
