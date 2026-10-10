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

class TLSThumbTests(unittest.TestCase):
    def test_tls_allowed_each_type_readonly_and_writable(self):
        for arch, kinds in trial.ARM_TLS_ALLOWED.items():
            for kind in sorted(kinds):
                for writable in (False, True):
                    with self.subTest(arch=arch, kind=kind, writable=writable):
                        self.assertFalse(trial.arm_pic_relocations(reloc_elf(arch,[kind],writable=writable),arch)['forbidden'])

    def test_local_exec_forbidden_even_debug_writable_and_absolute(self):
        for arch, kinds in trial.ARM_TLS_LOCAL_EXEC.items():
            for kind in sorted(kinds):
                for kwargs in ({}, {'writable':True}, {'debug':True}, {'absolute':True}):
                    with self.subTest(arch=arch, kind=kind, kwargs=kwargs),self.assertRaisesRegex(ValueError,'forbidden .* TLS local-exec'):
                        trial.arm_pic_relocations(reloc_elf(arch,[kind],**kwargs),arch)

    def test_initial_exec_arm_descriptors_and_unknown_stop(self):
        for arch, kinds in trial.ARM_TLS_PENDING.items():
            for kind in sorted(kinds):
                for debug in (False,True):
                    with self.subTest(arch=arch, kind=kind),self.assertRaisesRegex(ValueError,'uncertified'):
                        trial.arm_pic_relocations(reloc_elf(arch,[kind],debug=debug),arch)
        for arch,kind in [('armv7l',41),('aarch64',0x253)]:
            with self.assertRaisesRegex(ValueError,'uncertified'):
                trial.arm_pic_relocations(reloc_elf(arch,[kind]),arch)

    def test_thumb_restore_and_reference_arguments(self):
        argv=['clang','-Os','-gdwarf-4','-ffunction-sections','-fdata-sections',*sorted(trial.ARM_EXACT_TOKENS['armv7l']),'-flto=thin','-D','NAME.cpp','-I','path','-MT','target','-MF','deps','-MD','-o','a.o','-c','a.cpp']
        policy=trial.arm_classify_options(argv,'armv7l')
        self.assertEqual(next(x['category'] for x in policy['tokens'] if x['token']=='-mthumb'),'restore')
        ref=trial.arm_reference_flags({'recorded_command':argv})
        self.assertIn('-mthumb',ref);self.assertIn('NAME.cpp',ref)
        for x in ['-flto=thin','a.cpp','a.o','-MD','deps','target']:self.assertNotIn(x,ref)
        text=['target triple = "thumbv7-tizen-linux-gnueabi"','!llvm.commandline = !{!0}','!0 = !{!"'+' '.join(argv)+'"}']
        self.assertIn('-mthumb',trial.arm_ir_settings(text,'armv7l')['flags'])
        with self.assertRaisesRegex(ValueError,'reference driver'):
            trial.arm_reference_flags({'recorded_command':[x for x in argv if x!='-mthumb']})

    def test_override_warning_is_a_failure(self):
        trial.arm_reject_triple_override({'stderr':''})
        for message in ['[-Woverride-module]','warning: overriding the module target triple with armv7']:
            with self.assertRaisesRegex(ValueError,'changed module target triple'):
                trial.arm_reject_triple_override({'stderr':message})

    def test_module_asm_section_tracking(self):
        lines=['module asm ".text"','module asm ".thumb"','module asm ".pushsection .text.helper,\\22ax\\22"','module asm "nop"','module asm ".popsection"']
        self.assertEqual(trial.arm_module_asm_sections(lines),['.text','.text.helper'])
        self.assertEqual(trial.arm_module_asm_sections([]),[])
        with self.assertRaisesRegex(ValueError,'unbalanced'):
            trial.arm_module_asm_sections(['module asm ".popsection"'])

    def test_thumb_gate_rejects_attribute_mismatch(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/'input.bc';src.write_bytes(b'bc');target=root/'actual.o';target.write_bytes(b'obj')
            def run(argv,prefix,stdout=None):
                if stdout is not None:
                    stdout.write(b'Tag_THUMB_ISA_use: Thumb-2\n' if 'actual.o' in argv[-1] else b'Tag_THUMB_ISA_use: Thumb-1\n')
                else:Path(argv[-1]).write_bytes(b'reference')
                return {'stderr':''}
            with mock.patch.object(trial,'arm_reference_flags',return_value=['-mthumb']),mock.patch.object(trial,'arm_mapping_modes',return_value={}):
                with self.assertRaisesRegex(ValueError,'Thumb/ABI/module-asm'):
                    trial.arm_thumb_gate('clang',src,target,{'module_asm_sections':[],'target_cpu':[],'target_features':[]},mock.Mock(run=run))

if __name__=='__main__':unittest.main(verbosity=2)
