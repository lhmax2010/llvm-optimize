from pathlib import Path
import mmap,struct,zlib,hashlib
from section_compare import *
def crc_file(p):
 c=0
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):c=zlib.crc32(b,c)
 return c&0xffffffff
def link_info(data):
 _,_,ss=layout(data);sections=[s for s in ss if s['name']=='.gnu_debuglink'];assert len(sections)==1,'debuglink count != 1';s=sections[0];raw=bytes(s['content']);name=raw.split(b'\0')[0].decode();assert name and '/' not in name and '\\' not in name,'invalid debuglink filename';at=(len(name)+1+3)&~3;assert at+4==len(raw),'debuglink CRC is not final four bytes';return {'filename':name,'crc32':struct.unpack_from('<I',raw,at)[0],'offset':s['offset'],'size':s['size'],'prefix':raw[:-4]}
def debuglink_name(p):
 with Path(p).open('rb') as f:
  if f.read(4)!=b'\x7fELF':return None
  with mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ) as m:
   error=None;info=None
   try:info=link_info(m)
   except AssertionError as e:error=str(e);e.__traceback__=None
  if error and error!='debuglink count != 1':raise AssertionError(error)
  return info['filename'] if info else None
def debuglink_proof(a,b,da,db):
 symbol_proof=file_proof(da,db)
 with Path(a).open('rb') as fa,Path(b).open('rb') as fb:
  with mmap.mmap(fa.fileno(),0,access=mmap.ACCESS_COPY) as ma,mmap.mmap(fb.fileno(),0,access=mmap.ACCESS_COPY) as mb:
   error=None
   try:
    x,y=link_info(ma),link_info(mb);assert x['filename']==y['filename'] and x['prefix']==y['prefix'],'debuglink filename/padding changed'
    assert x['crc32']==crc_file(da),'old debuglink CRC mismatch';assert y['crc32']==crc_file(db),'new debuglink CRC mismatch'
    at=x['offset']+x['size']-4;bt=y['offset']+y['size']-4;ma[at:at+4]=b'\0'*4;mb[bt:bt+4]=b'\0'*4
    proof=elf_proof(ma,mb)
    answer={'classification':'verified-debuglink-crc-and-record-sections','old_crc':x['crc32'],'new_crc':y['crc32'],'filename':x['filename'],'old_crc_offset':at,'new_crc_offset':bt,'symbol_proof':symbol_proof,'binary_proof':proof}
   except Exception as e:error=str(e);e.__traceback__=None
  if error:raise AssertionError(error)
 return answer
