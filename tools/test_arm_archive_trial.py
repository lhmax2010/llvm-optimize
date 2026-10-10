#!/usr/bin/env python3
"""ARM policy draft fixtures and x86 dispatch invariance; no package builds."""
import ast
import importlib.util
from pathlib import Path
import struct
import unittest
from unittest import mock
import llvm_static_archives_arm_trial as trial


def reloc_elf(arch, kinds, writable=False, absolute=False, debug=False):
    bits, machine = (1,40) if arch=='armv7l' else (2,183)
    hs,ss,symsz= (52,40,16) if bits==1 else (64,64,24)
    sfmt='<IIIIIIIIII' if bits==1 else '<IIQQQQIIQQ'
    base=hs+4*ss; target=b'\0'*64
    ndx=0xfff1 if absolute else 1
    sym=(struct.pack('<IIIBBH',0,0,0,0x10,0,ndx) if bits==1 else struct.pack('<IBBHQQ',0,0x10,0,ndx,0,0))
    sym=b'\0'*symsz+sym
    rel=b''.join(struct.pack('<II',i*4,(1<<8)|k) if bits==1 else struct.pack('<QQq',i*4,(1<<32)|k,0) for i,k in enumerate(kinds))
    roff=base+len(target)+len(sym); rs=8 if bits==1 else 24
    def sh(t,flags,off,size,link=0,info=0,ent=0):return struct.pack(sfmt,0,t,flags,0,off,size,link,info,1,ent)
    ident=b'\x7fELF'+bytes([bits,1,1])+b'\0'*9
    hdr=(struct.pack('<HHIIIIIHHHHHH',1,machine,1,0,0,hs,0,hs,0,0,ss,4,0) if bits==1 else
         struct.pack('<HHIQQQIHHHHHH',1,machine,1,0,0,hs,0,hs,0,0,ss,4,0))
    return ident+hdr+b'\0'*ss+sh(1,0 if debug else 2|int(writable),base,len(target))+sh(2,0,base+len(target),len(sym),ent=symsz)+sh(9 if bits==1 else 4,0,roff,len(rel),2,1,rs)+target+sym+rel


class DispatchTests(unittest.TestCase):
    def test_original_functions_are_identical(self):
        def defs(path):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(path.read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
        old=defs(Path(trial.__file__).with_name('llvm_static_archives_source.py'));new=defs(Path(trial.__file__))
        for name in old:
            if name not in ('convert','install_main'):
                self.assertEqual(old[name],new[name],name)

    def test_x86_never_reaches_arm(self):
        with mock.patch.object(trial,'arm_ir_settings',side_effect=AssertionError('ARM reached')),mock.patch.object(trial,'arm_pic_relocations',side_effect=AssertionError('ARM reached')):
            p=trial.policy_for_arch('x86_64')
            self.assertIs(p['relocations'],trial.pic_relocations)
            from test_static_archives_source_v2 import module
            self.assertEqual(p['settings'](module()),trial.ir_settings(module()))
        with self.assertRaises(ValueError):trial.policy_for_arch('riscv64')

    def test_arm_exact_options_and_cross_target_rejection(self):
        common=['clang','-gdwarf-4','-ffunction-sections','-fdata-sections','-flto=thin','-fstack-protector']
        for arch,opt in trial.ARM_OPTIMIZATION.items():
            argv=common+[opt]+sorted(trial.ARM_EXACT_TOKENS[arch])
            self.assertEqual(trial.arm_classify_options(argv,arch)['optimization'],opt)
            for bad in ('-mcpu=cortex-a9','-marm','-mfloat-abi=hard','--target=x86_64-tizen-linux-gnu','-fno-unroll-loops'):
                with self.subTest(arch=arch,bad=bad),self.assertRaises(ValueError):trial.arm_classify_options(argv+[bad],arch)

    def test_arm_ir_and_explicit_abi(self):
        for arch,opt in trial.ARM_OPTIMIZATION.items():
            flags=['clang',opt,'-gdwarf-4','-ffunction-sections','-fdata-sections']+sorted(trial.ARM_EXACT_TOKENS[arch])
            text='target triple = "'+next(iter(trial.ARM_IR_TRIPLES[arch]))+'"\n!llvm.commandline = !{!0}\n!0 = !{!"'+' '.join(flags)+'"}\n!1 = !{i32 8, !"PIC Level", i32 2}\n'
            r=trial.policy_for_arch(arch)['settings'](text.splitlines(True))
            self.assertEqual(r['pic_level'],2);self.assertIn(opt,r['flags']);self.assertNotIn('-flto=thin',r['flags'])
            if arch=='armv7l':self.assertIn('-mfloat-abi=softfp',r['flags'])
            with self.assertRaisesRegex(ValueError,'type metadata'):
                trial.arm_ir_settings((text+'declare i1 @llvm.type.test(ptr, metadata)\n').splitlines(True),arch)

    def test_arm_pic_rel_and_aarch64_rela(self):
        for arch,absrel,safe in [('armv7l',2,[24,26,27,42]),('aarch64',0x101,[0x113,0x115,0x137,0x138])]:
            self.assertTrue(trial.arm_pic_relocations(reloc_elf(arch,[absrel]),arch)['forbidden'])
            for data in (reloc_elf(arch,[absrel],absolute=True),reloc_elf(arch,[absrel],writable=True),reloc_elf(arch,[absrel],debug=True),reloc_elf(arch,safe)):
                self.assertFalse(trial.arm_pic_relocations(data,arch)['forbidden'])
            with self.assertRaisesRegex(ValueError,'uncertified'):
                trial.arm_pic_relocations(reloc_elf(arch,[255]),arch)

    def test_narrow_absolute_writable_rejected(self):
        for arch,kind in [('armv7l',5),('aarch64',0x102)]:
            self.assertTrue(trial.arm_pic_relocations(reloc_elf(arch,[kind],writable=True),arch)['forbidden'])

if __name__=='__main__':unittest.main(verbosity=2)
