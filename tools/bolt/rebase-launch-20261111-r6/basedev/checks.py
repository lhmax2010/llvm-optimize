"""Strict byte proofs. No section/member is ignored wholesale."""
from pathlib import Path
import hashlib,struct,json,subprocess,stat,zlib,re,shlex
DROP=['-fno-inline-functions','-Wl,-z,relro,--as-needed','-feliminate-unused-debug-types','--param=ssp-buffer-size=4']
EXPECTED={'strip_all_sha256':'13a07cb7f84bd1ceda4d851c8bd71bddf7ef0c2d4864892eba64cbbb9a0350b8','rpath_adjusted_sha256':'8c2429d870f421a29a9914458bc4d4ff2ce359a15e0bdd20f39bfb4580c40bdf','after_sha256':'4f08e12d499ebd492ce4951f74915ba435f57f2e380dc6f3520f24644996cb17'}
COUNTS={'N':23592,'M':144032,'S':0,'U':1,'Q':383,'R':4.238545331242318e-05,'S_over_N':0.0}
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,r):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(r,indent=2)+'\n')
def sections(b):
 assert b[:4]==b'\x7fELF' and b[5]==1,'ELF little endian required'
 if b[4]==2:off=struct.unpack_from('<Q',b,40)[0];ents,n,idx=struct.unpack_from('<HHH',b,58);fmt='<IIQQQQIIQQ'
 else:assert b[4]==1;off=struct.unpack_from('<I',b,32)[0];ents,n,idx=struct.unpack_from('<HHH',b,46);fmt='<IIIIIIIIII'
 assert ents==struct.calcsize(fmt) and n and idx<n and off+n*ents<=len(b),'invalid section table'
 ss=[struct.unpack_from(fmt,b,off+i*ents) for i in range(n)];st=ss[idx];names=b[st[4]:st[4]+st[5]];out={}
 for s in ss:
  assert s[0]<len(names) or s[0]==0
  end=names.find(b'\0',s[0]);assert end>=s[0];name=names[s[0]:end].decode()
  if s[1]!=8:assert s[4]+s[5]<=len(b)
  out[name]={'offset':s[4],'size':s[5],'type':s[1],'flags':s[2]}
 return out

from section_compare import elf_proof as command_byte_proof, archive_proof as ar_proof, content_proof, file_proof

def members(b):
 assert b[:8]==b'!<arch>\n';i=8;names=b'';out=[]
 while i<len(b):
  hd=b[i:i+60];assert len(hd)==60 and hd[-2:]==b'`\n';n=int(hd[48:58]);data=b[i+60:i+60+n];assert len(data)==n
  raw=hd[:16].decode().strip();name=raw
  if raw=='//':names=data
  elif raw.startswith('/') and raw[1:].isdigit():
   at=int(raw[1:]);end=names.find(b'/\n',at);assert end>=at;name=names[at:end].decode()
  elif raw not in ('/','/SYM64/'):name=raw.rstrip('/')
  out.append(dict(name=name,offset=i,size=n,body=data,sha256=hashlib.sha256(data).hexdigest(),header=hd));i+=60+n+n%2
 assert i==len(b);return out

def debuglink_check(binary,symbols):
 s=sections(binary);assert '.gnu_debuglink' in s;v=s['.gnu_debuglink'];data=binary[v['offset']:v['offset']+v['size']];name=data.split(b'\0',1)[0].decode();at=(len(name)+1+3)&~3;crc=struct.unpack_from('<I',data,at)[0];assert name=='clang-22.debug' and crc==zlib.crc32(symbols)&0xffffffff
 return dict(filename=name,crc32=crc,symbols_sha256=hashlib.sha256(symbols).hexdigest())

def flags_check(log,project):
 lines=(dict(enumerate(log.splitlines(),1)) if isinstance(log,str) else log).items();out={}
 for token in ('NORMALIZED_FLAGS','DROPPED_FLAGS'):
  hits=[dict(line=i,text=t[t.index('TIZEN_LLVM_'):]) for i,t in lines if 'TIZEN_LLVM_'+token+' CFLAGS=[' in t and '+ printf ' not in t and '+ echo ' not in t];assert len(hits)==1,(token,hits);out[token]=hits[0]
 expected='' if project=='toolchain' else ' '.join(DROP)
 assert out['DROPPED_FLAGS']['text']=='TIZEN_LLVM_DROPPED_FLAGS CFLAGS=['+expected+'] CXXFLAGS=['+expected+'] LDFLAGS=[]'
 warnings=[dict(line=i,text=t) for i,t in lines if re.search(r'(?:^|\] )TIZEN_LLVM_FLAGS_WARNING ',t)];assert not warnings,warnings
 assert not any('TIZEN_LLVM_FIXED_FLAGS_FAILED' in t for _,t in lines)
 out['WARNING']=warnings;return out

def no_dropped(data):
 if data.startswith(b'!<arch>\n'):
  return sum(no_dropped(x['body']) for x in members(data) if x['body'].startswith(b'\x7fELF'))
 if not data.startswith(b'\x7fELF'):return 0
 ss=sections(data);n=0
 for name,s in ss.items():
  if name not in ('.GCC.command.line','.llvmcmd'):continue
  text=data[s['offset']:s['offset']+s['size']].replace(b'\0',b' ').decode(errors='replace');tokens=shlex.split(text)
  assert not set(DROP)&set(tokens),('dropped option retained',set(DROP)&set(tokens));n+=1
 return n


def debuglink_proof(old_binary,new_binary,old_symbols,new_symbols):
 # Strict whole-file proof, with exactly the four CRC bytes exempted.
 symbol_proof=file_proof(old_symbols,new_symbols)
 a,b=Path(old_binary).read_bytes(),Path(new_binary).read_bytes()
 assert len(a)==len(b) and sections(a)==sections(b),'debuglink ELF layout changed'
 old=debuglink_check(a,Path(old_symbols).read_bytes());new=debuglink_check(b,Path(new_symbols).read_bytes())
 v=sections(a)['.gnu_debuglink'];at=v['offset']+v['size']-4
 assert a[:at]==b[:at] and a[at+4:]==b[at+4:],'bytes outside debuglink CRC changed'
 return dict(classification='verified-debuglink-crc-only',crc_file_offset=at,old_crc32=old['crc32'],new_crc32=new['crc32'],filename=new['filename'],all_other_bytes_equal=True,symbol_proof=symbol_proof)
