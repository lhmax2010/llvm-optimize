#!/usr/bin/env python3
"""Policy tests without converting any real archive member."""
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path
from convert_static_archives import ir_settings, pic_relocations
from inspect_llvm_archives import inspect
from test_inspect_llvm_archives import native


class ConversionPolicyTests(unittest.TestCase):
    def settings(self, extra=''):
        return ir_settings(('target triple = "x86_64-tizen-linux-gnu"\n'
                            'attributes #0 = { "target-cpu"="nehalem" "target-features"="+sse4.2" }\n'
                            + extra).splitlines())

    def test_pic_is_explicit_and_no_lto(self):
        data = self.settings('!1 = !{i32 8, !"PIC Level", i32 2}')
        self.assertIn('-fPIC', data['flags'])
        self.assertIn('-O3', data['flags'])
        self.assertFalse(any('lto' in flag for flag in data['flags']))
        self.assertEqual(data['target_cpu'], ['nehalem'])
        self.assertEqual(data['target_features'], ['+sse4.2'])
        self.assertFalse(any(flag.startswith('-march') for flag in data['flags']))

    def test_pie_and_static_distinguished(self):
        data = self.settings('!1 = !{i32 8, !"PIC Level", i32 2}\n!2 = !{i32 7, !"PIE Level", i32 2}')
        self.assertIn('-fPIE', data['flags'])
        self.assertNotIn('-fPIC', data['flags'])
        self.assertIn('-fno-pic', self.settings()['flags'])

    def test_unsupported_flags_fail(self):
        for extra in ['!1 = !{i32 8, !"PIC Level", i32 3}',
                      '!2 = !{i32 7, !"PIE Level", i32 2}',
                      '!2 = !{i32 7, !"Code Model", i32 1}']:
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                self.settings(extra)

    def test_wrong_target_fails(self):
        with self.assertRaises(ValueError):
            ir_settings(['target triple = "aarch64-tizen-linux-gnu"'])

    def test_native_machine_and_wrong_machine(self):
        data = native()
        self.assertEqual(pic_relocations(data)['forbidden'], [])
        data = bytearray(data); data[18:20] = (183).to_bytes(2, 'little')
        with self.assertRaises(ValueError):
            pic_relocations(data)

    def test_absolute_allocated_relocation_rejected_but_debug_excluded(self):
        def elf(flags, kind):
            header = b'\x7fELF'+bytes([2,1,1])+b'\0'*9+struct.pack('<HHIQQQIHHHHHH',1,62,1,0,0,64,0,64,0,0,64,4,0)
            sym = b'\0'*24+struct.pack('<IBBHQQ',0,0x10,0,1,0,0)
            rela = struct.pack('<QQq',0,(1<<32)|kind,0)
            def sh(typ, flg, off, size, link=0, info=0, stride=0):
                return struct.pack('<IIQQQQIIQQ',0,typ,flg,0,off,size,link,info,1,stride)
            return header+b'\0'*64+sh(1,flags,320,8)+sh(2,0,328,len(sym),stride=24)+sh(4,0,328+len(sym),24,2,1,24)+b'\0'*8+sym+rela
        self.assertEqual(len(pic_relocations(elf(2,10))['forbidden']), 1)
        self.assertEqual(len(pic_relocations(elf(2,1))['forbidden']), 1)
        self.assertEqual(pic_relocations(elf(0,10))['forbidden'], [])
        self.assertEqual(pic_relocations(elf(3,1))['forbidden'], [])
        self.assertEqual(pic_relocations(elf(2,2))['forbidden'], [])

    def test_gnu_packing_keeps_duplicate_names_and_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            objects = []
            for i, symbol in enumerate(['first', 'second']):
                folder = root/str(i); folder.mkdir()
                path = folder/'same.o'; path.write_bytes(native(symbol)); objects.append(str(path))
            results = []
            for name in ['one.a', 'two.a']:
                archive = root/name
                subprocess.run(['/usr/bin/ar','qcDS',str(archive),*objects], check=True, capture_output=True)
                subprocess.run(['/usr/bin/ar','sD',str(archive)], check=True, capture_output=True)
                results.append(archive.read_bytes())
            self.assertEqual(results[0], results[1])
            archive = inspect(root/'one.a')
            self.assertEqual([m['name'] for m in archive['members']], ['same.o', 'same.o'])
            self.assertEqual([m['occurrence'] for m in archive['members']], [1,2])
            self.assertEqual([r[:2] for r in archive['index']], [['first',0],['second',1]])
            self.assertTrue(archive['index_equals_machine_symbols'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
