#!/usr/bin/env python3
"""Independent literal fixtures for the third-review gates; no package builds."""
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import llvm_static_archives_source as source
import llvm_static_archives_arm_trial as trial
from test_static_archives_source_v2 import FLAGS, module
from test_arm_archive_trial import reloc_elf, change_symbol_section, target_ir


class CommonReviewTests(unittest.TestCase):
    def test_a1_assembler_escape_rejected_diagnostics_pass(self):
        for token in ('-Wa,-defsym,NAME=1', '-Wa,--noexecstack'):
            with self.subTest(token=token), self.assertRaisesRegex(ValueError, 'assembler option'):
                source.classify_options(FLAGS+[token])
        for token in ('-Wall', '-Wp,-D_FORTIFY_SOURCE=2'):
            self.assertEqual(source.classify_options(FLAGS+[token])['tokens'][-1]['category'], 'irrelevant')

    def test_a2_full_versions_and_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'CMakeCache.txt').touch()
            tools=[p/name for name in ('clang-22','llvm-dis','llvm-nm')]
            for path in tools:path.write_text('fixture');path.chmod(0o755)
            versions=['22.1.8','22.1.8','22.1.8']
            def run(argv,prefix,stdout):
                i=tools.index(argv[0]);text=('clang version ' if i==0 else 'LLVM (http://llvm.org/):\n  LLVM version ')+versions[i]+'\n'
                stdout.write(text.encode())
            command=mock.Mock(run=run)
            r=source.validate_tools(p,*tools,command,p)
            self.assertEqual([r['tool_versions'][n]['version'] for n in ('compiler','disassembler','nm')],['22.1.8','22.1.8','22.1.8'])
            for i in (1,2):
                for version in ('21.1.0','22.1.9'):
                    versions[i]=version
                    with self.subTest(tool=i,version=version),self.assertRaisesRegex(ValueError,'version differs'):
                        source.validate_tools(p,*tools,command,p)
                versions[i]='22.1.8'

    def test_a3_module_asm_whitelist(self):
        r=source.ir_settings(module('module asm ".globl _ZSt21ios_base_library_initv"\n'))
        self.assertEqual(r['module_asm'],['.globl _ZSt21ios_base_library_initv'])
        for text in ('module asm ".text"','module asm ".globl another"','module asm "nop"'):
            with self.subTest(text=text),self.assertRaisesRegex(ValueError,'module asm'):
                source.ir_settings(module(text))

    def test_a4_undefined_symbol_exactly_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);target=p/'member.o';calls=[];text='                 U _ZSt21ios_base_library_initv\n'
            def run(argv,prefix,stdout):
                calls.append(argv);stdout.write(text.encode())
            cmd=mock.Mock(run=run);statements=['.globl _ZSt21ios_base_library_initv']
            self.assertEqual(source.check_module_asm_symbol('nm',target,statements,cmd)['matches'],[('U','_ZSt21ios_base_library_initv')])
            self.assertEqual(calls,[['nm',str(target)]])
            for text in ('','00000000 T _ZSt21ios_base_library_initv\n','                 w _ZSt21ios_base_library_initv\n',' U _ZSt21ios_base_library_initv\n U _ZSt21ios_base_library_initv\n'):
                with self.subTest(text=text),self.assertRaisesRegex(ValueError,'exactly one U'):
                    source.check_module_asm_symbol('nm',target,statements,cmd)

    def test_a5_symbol_index_bound(self):
        # ELF64 fixture layout is independent of the production parser.
        data=bytearray(reloc_elf('aarch64',[2]));struct.pack_into('<H',data,18,62)
        self.assertEqual(source.pic_relocations(bytes(data))['checked'],1)
        rel_off=struct.unpack_from('<IIQQQQIIQQ',data,64+3*64)[4]
        struct.pack_into('<Q',data,rel_off+8,(2<<32)|2)  # two symbols: indexes 0,1
        with self.assertRaisesRegex(ValueError,'symbol outside table'):
            source.pic_relocations(bytes(data))

    def test_second_archive_replace_failure_records_partial_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);root=p/'root';root.mkdir();out=p/'out';(out/'archives').mkdir(parents=True)
            records=[]
            for name in ('a.a','b.a'):
                dest=root/name;candidate=out/'archives'/name;dest.write_bytes(b'old');candidate.write_bytes(b'new')
                records.append(dict(path=name,before_sha256=source.sha(dest),after_sha256=source.sha(candidate)))
            original=os.replace
            def replace(src,dst):
                if Path(dst)==root/'b.a':raise OSError('injected second archive replacement failure')
                return original(src,dst)
            with mock.patch.object(source,'convert',return_value=dict(status='CONVERTED',archives=records)),mock.patch.object(source.os,'replace',side_effect=replace),contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(OSError,'second archive'):
                    source.install(root,out,'cc','dis','nm',p)
            r=json.loads((out/'summary.json').read_text())
            self.assertEqual(r['status'],'INSTALL_FAILED')
            self.assertEqual([x.get('installed',False) for x in r['archives']],[True,False])
            self.assertEqual((root/'a.a').read_bytes(),b'new');self.assertEqual((root/'b.a').read_bytes(),b'old')

    def test_shared_functions_literal_and_ast_equal(self):
        production=Path(trial.__file__).with_name('llvm_static_archives_source.py').read_text()
        candidate=Path(trial.__file__).read_text()
        defs=lambda s:{n.name:n for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
        p,a=defs(production),defs(candidate)
        for name,node in p.items():
            if name not in ('convert','install','install_main'):
                with self.subTest(name=name):
                    self.assertEqual(ast.dump(node,include_attributes=False),ast.dump(a[name],include_attributes=False))
                    self.assertEqual(ast.get_source_segment(production,node),ast.get_source_segment(candidate,a[name]))


class ARMReviewTests(unittest.TestCase):
    def test_b1_exact_undefined_and_all_negative_forms(self):
        for arch in ('armv7l','aarch64'):
            good=change_symbol_section(reloc_elf(arch,[],symbol_name='_ZSt21ios_base_library_initv'),1,0)
            statements=['.globl _ZSt21ios_base_library_initv']
            r=trial.arm_check_module_asm_symbol(good,arch,statements)
            self.assertEqual({k:r['matches'][0][k] for k in ('info','other','raw_section','section_index','value','size')},dict(info=16,other=0,raw_section=0,section_index=0,value=0,size=0))
            bits=1 if arch=='armv7l' else 2;hs,ss,symsize=(52,40,16) if bits==1 else (64,64,24)
            fmt='<IIIIIIIIII' if bits==1 else '<IIQQQQIIQQ';off=struct.unpack_from(fmt,good,hs+2*ss)[4]+symsize
            variants=[('defined',change_symbol_section(good,1,1)),('ABS',change_symbol_section(good,1,0xfff1)),('COMMON',change_symbol_section(good,1,0xfff2))]
            for label,pos,value in [('WEAK',12 if bits==1 else 4,0x20),('HIDDEN',13 if bits==1 else 5,2),('FUNC',12 if bits==1 else 4,0x12)]:
                blob=bytearray(good);blob[off+pos]=value;variants.append((label,bytes(blob)))
            for label,pos in [('value',4 if bits==1 else 8),('size',8 if bits==1 else 16)]:
                blob=bytearray(good);struct.pack_into('<I' if bits==1 else '<Q',blob,off+pos,1);variants.append((label,bytes(blob)))
            duplicate=bytearray(good);duplicate[off-symsize:off]=duplicate[off:off+symsize];variants.append(('duplicate',bytes(duplicate)))
            for label,blob in variants:
                with self.subTest(arch=arch,label=label),self.assertRaisesRegex(ValueError,'GLOBAL/NOTYPE/DEFAULT/UND'):
                    trial.arm_check_module_asm_symbol(blob,arch,statements)

    def test_b2_tool_versions_must_match_and_arm_elf_tools_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'CMakeCache.txt').touch();tools=[p/name for name in ('clang-22','llvm-dis','llvm-nm')]
            for t in tools:t.write_text('fixture');t.chmod(0o755)
            def run(argv,prefix,stdout):
                stdout.write(b'clang version 22.1.9\n' if argv[0]==tools[0] else b'LLVM version 22.1.8\n')
            with self.assertRaisesRegex(ValueError,'disassembler version differs from clang 22.1.9'):
                trial.validate_arm_tools(p,*tools,mock.Mock(run=run),p,'aarch64',allow_wrapper=True)
            for tool in tools:
                for machine,bits in ((40,1),(183,2)):
                    blob=bytearray(20);blob[:4]=b'\x7fELF';blob[4:7]=bytes([bits,1,1]);struct.pack_into('<H',blob,18,machine);tool.write_bytes(blob)
                    command=mock.Mock()
                    with self.subTest(tool=tool.name,machine=machine),self.assertRaisesRegex(ValueError,'requires native x86_64 ELF64'):
                        trial.validate_arm_tools(p,*tools,command,p,'aarch64',allow_wrapper=True)
                    command.run.assert_not_called()
                tool.write_text('fixture')

    def test_b6_missing_name_table_rejected(self):
        for arch in ('armv7l','aarch64'):
            good=reloc_elf(arch,[]);trial.arm_elf_layout(good,arch)
            blob=bytearray(good);struct.pack_into('<H',blob,50 if arch=='armv7l' else 62,0)
            with self.assertRaisesRegex(ValueError,'section name table'):
                trial.arm_elf_layout(blob,arch)

    def test_two_function_attribute_groups_rejected(self):
        for arch in ('armv7l','aarch64'):
            lines=target_ir(arch);lines[0]='define void @f() #0 #1 {';lines.append(lines[-1].replace('#0','#1'))
            with self.assertRaisesRegex(ValueError,'target attribute group'):
                trial.arm_function_targets(lines,arch)

    def test_tls_pending_nonalloc_rejected(self):
        for arch,kind in (('armv7l',107),('aarch64',539)):
            with self.assertRaisesRegex(ValueError,'uncertified'):
                trial.arm_pic_relocations(reloc_elf(arch,[kind],debug=True),arch)

    def test_b7_unlimited_rejected_without_bypass(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);cmd=mock.Mock();cmd.address_space_bytes=4294967296
            cmd.run.side_effect=lambda argv,prefix,stdout:stdout.write(b'Max address space         unlimited            unlimited            bytes\n')
            with self.assertRaisesRegex(ValueError,'not enforced'):
                trial.arm_address_space_probe(cmd,p)
            r=json.loads((p/'address-space-probe.json').read_text())
            self.assertFalse(r['address_space_enforced']);self.assertNotIn('explicitly_allowed_unenforced',r)
            self.assertEqual((r['soft'],r['hard']),('unlimited','unlimited'))
            self.assertEqual(cmd.run.call_args.args[0],['/usr/bin/cat','/proc/self/limits'])

    def test_b7_matching_mock_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);cmd=mock.Mock();cmd.address_space_bytes=4294967296
            cmd.run.side_effect=lambda argv,prefix,stdout:stdout.write(b'Max address space         4294967296           4294967296           bytes\n')
            r=trial.arm_address_space_probe(cmd,p)
            self.assertTrue(r['address_space_enforced']);self.assertNotIn('explicitly_allowed_unenforced',r)

    def test_b7_x86_wrapper_flag_rejected(self):
        args=['source','--root','/unused/root','--build','/unused/build','--evidence','/unused/out','--arch','x86_64','--compiler','/unused/cc','--disassembler','/unused/dis','--nm','/unused/nm','--allow-wrapper-tools']
        with mock.patch.object(sys,'argv',args),mock.patch.object(trial,'install') as install,contextlib.redirect_stderr(io.StringIO()) as log:
            with self.assertRaises(SystemExit) as error:trial.install_main()
        self.assertEqual(error.exception.code,2);self.assertIn('only valid for ARM',log.getvalue());install.assert_not_called()

    def test_b7_real_limits_host_and_known_emulated_environment(self):
        # Native host must enforce. In the explicitly studied ARM Python/QEMU
        # environment, test the enforced rejection; do not weaken the old AS test.
        with Path(sys.executable).open('rb') as f:header=f.read(20)
        machine=int.from_bytes(header[18:20],'little')
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);cmd=trial.Commands()
            if machine in (40,183):
                with self.assertRaisesRegex(ValueError,'not enforced'):trial.arm_address_space_probe(cmd,p)
                r=json.loads((p/'address-space-probe.json').read_text())
                self.assertFalse(r['address_space_enforced']);self.assertEqual((r['soft'],r['hard']),('unlimited','unlimited'))
            else:
                self.assertEqual(machine,62)
                r=trial.arm_address_space_probe(cmd,p)
                self.assertTrue(r['address_space_enforced']);self.assertEqual((r['soft'],r['hard']),('4294967296','4294967296'))

    def test_real_x86_bitcode_conversion_blocks_every_arm_function(self):
        tools=[Path(os.environ['REVIEW_REAL_'+label]) for label in ('CLANG','DIS','NM')]
        with tempfile.TemporaryDirectory() as tmp,contextlib.ExitStack() as stack:
            p=Path(tmp);root=p/'root';root.mkdir();build=p/'build';build.mkdir();(build/'CMakeCache.txt').touch()
            src=p/'input.c';src.write_text('int answer(void) { return 42; }\n');obj=p/'input.o'
            env=dict(os.environ,CLANG_NO_DEFAULT_CONFIG='1')
            subprocess.run(['/usr/bin/prlimit','--as=4294967296','--',str(tools[0]),'--target=x86_64-tizen-linux-gnu','-O3','-g','-gdwarf-4','-ffunction-sections','-fdata-sections','-fPIC','-flto=thin','-frecord-command-line','-c',str(src),'-o',str(obj)],env=env,check=True,capture_output=True)
            self.assertEqual(obj.read_bytes()[:4],b'BC\xc0\xde')
            subprocess.run(['ar','qcDS',str(root/'input.a'),str(obj)],check=True,capture_output=True)
            names=[name for name,value in vars(trial).items() if callable(value) and (name.startswith('arm_') or name=='validate_arm_tools')]
            self.assertIn('arm_address_space_probe',names)
            for name in names:stack.enter_context(mock.patch.object(trial,name,side_effect=AssertionError('ARM reached: '+name)))
            with contextlib.redirect_stdout(io.StringIO()):r=trial.convert(root,p/'output',*tools,build)
            self.assertEqual((r['status'],r['archives'][0]['converted']),('CONVERTED',1))
            self.assertEqual(trial.inspect(p/'output/archives/input.a')['bitcode'],0)
            member=r['archives'][0]['results'][0]
            self.assertEqual(member['module_asm_symbol'],{'required':False})
            self.assertNotIn('module_asm_symbol',member['conversion'])


if __name__=='__main__':
    unittest.main(verbosity=2)
