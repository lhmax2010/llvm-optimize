import struct,collections
def census(data):
 assert data[:6]==b'\x7fELF\x02\x01'
 shoff=struct.unpack_from('<Q',data,40)[0];entsize,num,strings=struct.unpack_from('<HHH',data,58)
 assert entsize==64 and num>0 and strings<num
 sections=[struct.unpack_from('<IIQQQQIIQQ',data,shoff+i*entsize) for i in range(num)]
 ss=sections[strings];names=data[ss[4]:ss[4]+ss[5]]
 counts=collections.Counter();debug=collections.Counter()
 for sh in sections:
  if sh[1] not in (4,9):continue
  name=names[sh[0]:].split(b'\0',1)[0].decode()
  width=24 if sh[1]==4 else 16
  assert sh[9]==width and sh[5]%width==0
  for offset in range(sh[4],sh[4]+sh[5],width):
   kind=struct.unpack_from('<Q',data,offset+8)[0]&0xffffffff
   counts[kind]+=1
   if name.startswith('.rela.debug_'):debug[kind]+=1
 return counts,debug
