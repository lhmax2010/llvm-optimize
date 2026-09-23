#!/usr/bin/env python3
"""Synthetic format/identity tests; no compiler, linker, or package builds."""
import copy
from pathlib import Path
import struct
import tempfile
import unittest
from inspect_llvm_archives import inspect, mapping_equal, member_kind


def native(symbol='foo'):
    names=b'\0.strtab\0.symtab\0.shstrtab\0.debug_info\0'; strings=b'\0'+symbol.encode()+b'\0'
    syms=b'\0'*24+struct.pack('<IBBHQQ',1,0x10,0,0xfff1,0,0)
    off=64+5*64
    parts=[strings,syms,names,b'x'];offsets=[]
    for part in parts:offsets.append(off);off+=len(part)
    header=b'\x7fELF'+bytes([2,1,1])+b'\0'*9+struct.pack('<HHIQQQIHHHHHH',1,62,1,0,0,64,0,64,0,0,64,5,3)
    def sh(name,typ,start,size,link=0,entsize=0):return struct.pack('<IIQQQQIIQQ',name,typ,0,0,start,size,link,0,1,entsize)
    return header+b'\0'*64+sh(1,3,offsets[0],len(strings))+sh(9,2,offsets[1],len(syms),1,24)+sh(17,3,offsets[2],len(names))+sh(27,1,offsets[3],1)+b''.join(parts)


def member(name,payload):
    header=f'{name:<16}{0:<12}{0:<6}{0:<6}{100644:<8}{len(payload):<10}`\n'.encode()
    assert len(header)==60
    return header+payload+(b'\n' if len(payload)%2 else b'')


def archive(members,index=(),wide=False):
    width=8 if wide else 4;size=width*(1+len(index))+sum(len(s.encode())+1 for s,_ in index)
    offsets=[];pos=8+(60+size+size%2 if index else 0)
    for name,payload in members:offsets.append(pos);pos+=len(member(name+'/',payload))
    result=b'!<arch>\n'
    if index:
        table=len(index).to_bytes(width,'big')+b''.join(offsets[n].to_bytes(width,'big') for _,n in index)+b''.join(s.encode()+b'\0' for s,_ in index)
        result+=member('/SYM64/' if wide else '/',table)
    return result+b''.join(member(name+'/',payload) for name,payload in members)


class ArchiveTests(unittest.TestCase):
    def read(self,data):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'probe.a';p.write_bytes(data);return inspect(p)

    def test_actual_member_magic(self):
        self.assertEqual(member_kind(native()),'machine')
        for magic in (b'BC\xc0\xde',b'\xde\xc0\x17\x0b'):self.assertEqual(member_kind(magic),'bitcode')
        for data in (b'unknown',b'\x7fELF',b''):self.assertEqual(member_kind(data),'other')

    def test_native_index_and_debug_sections(self):
        x=self.read(archive([('one.o',native())],[('foo',0)]))
        self.assertTrue(x['index_equals_machine_symbols']);self.assertEqual(x['machine'],1)
        self.assertEqual(x['members'][0]['debug_sections'],['.debug_info'])

    def test_mixed_archive_partial_index(self):
        x=self.read(archive([('one.o',native()),('two.o',b'BC\xc0\xde...')],[('foo',0)]))
        self.assertTrue(x['index_equals_machine_symbols']);self.assertEqual(x['bitcode'],1)
        self.assertEqual(x['index_entries'],1)

    def test_duplicate_member_names_are_not_collapsed(self):
        members=[('same.o',native('foo')),('same.o',native('bar'))]
        good=self.read(archive(members,[('foo',0),('bar',1)]))
        bad=self.read(archive(members,[('foo',0),('bar',0)]))
        self.assertEqual([m['occurrence'] for m in good['members']],[1,2])
        self.assertTrue(good['index_equals_machine_symbols']);self.assertFalse(bad['index_equals_machine_symbols'])
        self.assertFalse(mapping_equal(good,bad))

    def test_order_and_not_just_count(self):
        members=[('a.o',native('foo')),('b.o',native('bar'))]
        a=self.read(archive(members,[('foo',0),('bar',1)]));b=self.read(archive(members,[('bar',1),('foo',0)]))
        self.assertEqual(a['index_entries'],b['index_entries']);self.assertFalse(mapping_equal(a,b))
        b=copy.deepcopy(a);b['members'][0]['mtime']='999';self.assertTrue(mapping_equal(a,b))

    def test_64bit_index(self):
        x=self.read(archive([('a.o',native())],[('foo',0)],True));self.assertEqual(x['index_entries'],1)
        self.assertTrue(x['index_equals_machine_symbols'])

    def test_gnu_long_name(self):
        table=b'a-very-long-member-name.o/\n'
        x=self.read(b'!<arch>\n'+member('//',table)+member('/0',b'BC\xc0\xde...'))
        self.assertEqual(x['members'][0]['name'],'a-very-long-member-name.o')

    def test_thin_never_reads_external_members(self):
        header=f'{"/0":<16}{0:<12}{0:<6}{0:<6}{100644:<8}{999:<10}`\n'.encode()
        x=self.read(b'!<thin>\n'+member('//',b'/does/not/exist.o/\n')+header)
        self.assertTrue(x['thin']);self.assertEqual(x['other'],1);self.assertIsNone(x['members'][0]['sha256'])

    def test_corrupt_input_rejected(self):
        for raw in [b'invalid!',archive([('a.o',native())],[('foo',0)])[:-2]]:
            with self.subTest(raw=raw[:8]),self.assertRaises(ValueError):self.read(raw)

class CensusGateTests(unittest.TestCase):
    def test_runtime_native_pass_and_bitcode_stop(self):
        import contextlib
        import io
        import json
        from census_llvm_archives import census
        for package, filename, payload, expected in [
            ('compiler-rt','runtime.a',native(),'PASS'),
            ('llvm-static-devel','libLLVMCore.a',b'BC\xc0\xde...','PASS'),
            ('compiler-rt','runtime.a',b'BC\xc0\xde...','FAIL_RUNTIME_FORMAT'),
            ('libomp-devel','libarcher_static.a',b'BC\xc0\xde...','FAIL_RUNTIME_FORMAT'),
            ('libomp-devel','libarcher_static.a',b'unknown','FAIL_RUNTIME_FORMAT')]:
            with self.subTest(package=package,expected=expected),tempfile.TemporaryDirectory() as tmp:
                base=Path(tmp);root=base/'root';root.mkdir();(root/filename).write_bytes(archive([('x.o',payload)]))
                owners=base/'owners.json';owners.write_text(json.dumps({'/'+filename:[{'rpm':package}]}))
                with contextlib.redirect_stdout(io.StringIO()):result=census(root,owners,base/'result')
                self.assertEqual(result['gate'],expected)

if __name__=='__main__':unittest.main(verbosity=2)
