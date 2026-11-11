from pathlib import Path
import struct,unittest,shutil
import bolt_helper as h
from test_bolt_helper import Base,elf

def security_elf(path):
    elf(path)
    e=h.ELF(path)
    try:headers=list(e.sections);names=list(e.names)
    finally:e.close()
    data=bytearray(path.read_bytes())
    strings=b'\0exported\0libc.so.6\0GLIBC_2.2.5\0'
    symbols=struct.pack('<IBBHQQ',0,0,0,0,0,0)+struct.pack('<IBBHQQ',1,0x12,0,2,0x400100,1)
    note=struct.pack('<III',4,16,5)+b'GNU\0'+struct.pack('<III',0xc0000002,4,3)+b'\0'*4
    dynamic=b''.join(struct.pack('<qQ',tag,value) for tag,value in [(1,strings.index(b'libc')),(30,8),(0x6ffffffb,0x8000000),(0,0)])
    needs=struct.pack('<HHIII',1,1,strings.index(b'libc'),16,0)+struct.pack('<IHHII',0,0,2,strings.index(b'GLIBC'),0)
    entries=[('.dynstr',3,strings,0,0),('.dynsym',11,symbols,len(headers),24),('.dynamic',6,dynamic,len(headers),16),
             ('.gnu.version',0x6fffffff,struct.pack('<HH',0,2),len(headers)+1,2),('.gnu.version_r',0x6ffffffe,needs,len(headers),0),('.note.gnu.property',7,note,0,0)]
    newnames=names+[row[0] for row in entries];nametable=b'\0';offsets={}
    for name in newnames:offsets[name]=len(nametable);nametable+=name.encode()+b'\0'
    npos=len(data);data.extend(nametable);headers[1]=(offsets['.shstrtab'],3,0,0,npos,len(nametable),0,0,1,0)
    for name,typ,blob,link,entsize in entries:
        pos=len(data);data.extend(blob);headers.append((offsets[name],typ,0,0,pos,len(blob),link,0,1,entsize))
    shoff=len(data)
    for header in headers:data.extend(struct.pack('<IIQQQQIIQQ',*header))
    struct.pack_into('<Q',data,40,shoff);struct.pack_into('<H',data,60,len(headers));struct.pack_into('<H',data,56,3)
    data[120:176]=struct.pack('<IIQQQQQQ',0x6474e551,6,0,0,0,0,0,16)
    prop=headers[-1];data[176:232]=struct.pack('<IIQQQQQQ',0x6474e553,4,prop[4],0,0,prop[5],prop[5],8)
    path.write_bytes(data)

class SecurityTests(Base):
    def files(self):
        a=self.d/'ordinary';b=self.d/'candidate';security_elf(a);shutil.copyfile(a,b);return a,b
    def test_unchanged_pass(self):
        a,b=self.files();self.assertTrue(h.security_compare(a,b)['security_preserved'])
    def test_property_removed(self):
        a,b=self.files();e=h.ELF(b)
        try:sec=e.by_name['.shstrtab'];start=bytes(e.mm[sec[4]:sec[4]+sec[5]]).index(b'.note.gnu.property')+sec[4]
        finally:e.close()
        data=bytearray(b.read_bytes());data[start:start+18]=b'.note.gnu.propertX';struct.pack_into('<H',data,56,2);b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'GNU_PROPERTY|gnu.property'):h.security_compare(a,b)
    def test_stack_permissions_changed(self):
        a,b=self.files();data=bytearray(b.read_bytes());struct.pack_into('<I',data,124,7);b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'GNU_STACK'):h.security_compare(a,b)
    def test_export_deleted(self):
        a,b=self.files();e=h.ELF(b)
        try:sec=e.by_name['.dynsym']
        finally:e.close()
        data=bytearray(b.read_bytes());struct.pack_into('<I',data,sec[4]+24,0);b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'dynsym'):h.security_compare(a,b)
    def test_symbol_binding_changed(self):
        a,b=self.files();e=h.ELF(b)
        try:offset=e.by_name['.dynsym'][4]+24+4
        finally:e.close()
        data=bytearray(b.read_bytes());data[offset]=0x22;b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'dynsym'):h.security_compare(a,b)
    def test_symbol_visibility_changed(self):
        a,b=self.files();e=h.ELF(b)
        try:offset=e.by_name['.dynsym'][4]+24+5
        finally:e.close()
        data=bytearray(b.read_bytes());data[offset]=2;b.write_bytes(data)
        with self.assertRaisesRegex(h.GateError,'dynsym'):h.security_compare(a,b)

if __name__=='__main__':unittest.main()
