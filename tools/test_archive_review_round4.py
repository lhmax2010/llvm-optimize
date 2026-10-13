#!/usr/bin/env python3
"""Fourth-review literal gates; real native POSIX sh fixtures, no LLVM/RPM build."""
import contextlib
import inspect
import io
import json
import os
from pathlib import Path
import signal
import struct
import sys
import tempfile
import unittest
from unittest import mock

import llvm_static_archives_source as production
import llvm_static_archives_arm_trial as trial
from test_static_archives_source_v2 import FLAGS
from test_arm_archive_trial import reloc_elf, change_section


def native_shell():
    # The same tests run under ARM Python/QEMU with the root's accel bash.
    return Path('/emul/usr/bin/sh' if Path('/emul/usr/bin/sh').exists() else '/bin/sh').resolve()


def native_header(machine=62):
    value=bytearray(20);value[:7]=b'\x7fELF\x02\x01\x01'
    struct.pack_into('<H',value,18,machine)
    return bytes(value)


def arm_flags(arch):
    # Independent literals, deliberately not read from policy tables.
    return (['clang','-gdwarf-4','-ffunction-sections','-fdata-sections']+
            (['-Os','-march=armv7-a','-mthumb','-mfpu=neon','-mfloat-abi=softfp','-mlittle-endian']
             if arch=='armv7l' else ['-O3','-march=armv8-a+fp+simd+crc+crypto','-mtune=cortex-a53']))


class X86TableTests(unittest.TestCase):
    def test_assembler_rejection_is_one_literal_message(self):
        for module in (production,trial):
            for token in ('-Xassembler','-Wa,-defsym,NAME=1'):
                with self.subTest(module=module.__name__,token=token),self.assertRaises(ValueError) as error:
                    module.classify_options(FLAGS+[token])
                self.assertEqual(str(error.exception),'unclassified original assembler option: -Wa, / -Xassembler')

    def test_table_level_bounds_are_named(self):
        data=bytearray(reloc_elf('aarch64',[2]));struct.pack_into('<H',data,18,62);data=bytes(data)
        self.assertEqual(production.pic_relocations(data),{'checked':1,'forbidden':[]})
        count=struct.unpack_from('<H',data,60)[0]
        cases=[('sh_link',change_section(data,3,6,count)),('sh_info',change_section(data,3,7,count)),
               ('relocation table entsize',change_section(data,3,9,0)),('symbol table entsize',change_section(data,2,9,1)),
               ('relocation table outside',change_section(data,3,4,len(data)+1)),('symbol table outside',change_section(data,2,4,len(data)+1))]
        invalid=bytearray(data);struct.pack_into('<H',invalid,60,65534);cases.append(('section table outside',bytes(invalid)))
        invalid=bytearray(data);struct.pack_into('<H',invalid,58,1);cases.append(('section header stride',bytes(invalid)))
        for label,blob in cases:
            with self.subTest(label=label),self.assertRaisesRegex(ValueError,'x86_64 .*'+label):
                production.pic_relocations(blob)


class NativeLauncherTests(unittest.TestCase):
    def adapter(self,timeout=600):
        bash=native_shell();command=trial.Commands(address_space_bytes=4294967296,timeout=timeout)
        return trial.ARMNativeLimitCommands(command,bash,[bash]),bash

    def test_native_soft_hard_and_core_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);command,bash=self.adapter()
            result=trial.arm_address_space_probe(command,p)
            self.assertEqual((result['soft'],result['hard']),('4294967296','4294967296'))
            self.assertTrue(result['address_space_enforced']);self.assertTrue(result['native_limit_launcher'])
            self.assertRegex(result['raw'],r'Max core file size\s+0\s+0\s+bytes')
            row=json.loads((p/'address-space-probe-command.json').read_text())
            self.assertEqual(row['payload_argv'],['/usr/bin/cat','/proc/self/limits'])
            self.assertEqual(row['native_limit_shell_sha256'],production.sha(bash))
            self.assertEqual(row['argv'][:5],['/usr/bin/env','-u','BASH_ENV','-u','ENV']);self.assertEqual(row['argv'][6],'-c')

    def test_ulimit_failure_is_exit_125(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);command,bash=self.adapter()
            # Establish a lower hard ceiling in the test child, then exercise the
            # unmodified setup's refusal to raise it. Never alter the test parent.
            script='ulimit -S -v 65536 || exit 99\nulimit -H -v 65536 || exit 99\n'+trial.ARM_NATIVE_LIMIT_EXEC
            with mock.patch.object(trial,'ARM_NATIVE_LIMIT_EXEC',script),self.assertRaisesRegex(RuntimeError,r'\(125\)'):
                command.run([bash,'-p','-c','exit 0'],p/'limit-failure')
            self.assertEqual(json.loads((p/'limit-failure.json').read_text())['exit'],125)
            self.assertFalse(command.children)

    def test_payload_argv_is_not_shell_interpolated(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);command,bash=self.adapter();out=p/'stdout'
            values=['space here','single\'quote','double"quote','$HOME','$(false)','']
            argv=[bash,'-p','-c','printf "<%s>\\n" "$@"','payload',*values]
            with out.open('wb') as stream:row=command.run(argv,p/'argv',stdout=stream)
            self.assertEqual(out.read_text(),''.join('<'+v+'>\n' for v in values))
            self.assertEqual(row['payload_argv'],list(map(str,argv)))

    def test_bash_env_is_not_executed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);env=p/'env';marker=p/'executed';env.write_text('printf bad > '+str(marker)+'\n')
            command,bash=self.adapter()
            with mock.patch.dict(os.environ,{'BASH_ENV':str(env)}):command.run([bash,'-p','-c','exit 0'],p/'env-check')
            self.assertFalse(marker.exists())

    def test_native_timeout_sigkill_and_reaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);command,bash=self.adapter(timeout=5);ready=p/'ready'
            with self.assertRaisesRegex(RuntimeError,'timeout'):
                command.run([bash,'-p','-c','trap "" TERM; printf ready > "$1"; while :; do :; done','fixture',str(ready)],p/'timeout')
            self.assertTrue(ready.is_file(),'environment did not establish SIGTERM-ignore prerequisite')
            row=json.loads((p/'timeout.json').read_text());self.assertEqual(row['exit'],-signal.SIGKILL)
            self.assertGreaterEqual(row['wall'],8);self.assertFalse(command.children)

    def test_only_configured_tools_and_probe_are_wrapped(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);tools=[p/name for name in ('cc','dis','nm')]
            for t in tools:t.write_bytes(native_header());t.chmod(0o755)
            base=mock.Mock();base.address_space_bytes=4294967296;base.run.return_value={'exit':0}
            command=trial.ARMNativeLimitCommands(base,native_shell(),tools)
            for i,t in enumerate(tools):
                command.run([t,'--version'],p/str(i));argv=base.run.call_args.args[0]
                self.assertEqual(argv[-2:],[str(t),'--version']);self.assertEqual(argv[8],'arm-native-limit')
            for i,argv in enumerate((['ar','t','x.a'],['readelf','-h','x.o'],['/usr/bin/cat','/proc/self/limits'])):
                command.run(argv,p/('plain'+str(i)));self.assertEqual(base.run.call_args.args[0],argv)
            command.probe(p/'probe',io.BytesIO());self.assertEqual(base.run.call_args.args[0][7],trial.ARM_NATIVE_LIMIT_PROBE)

    def test_non_kib_address_space_rejected(self):
        base=mock.Mock();base.address_space_bytes=4294967297
        with self.assertRaisesRegex(ValueError,'multiple of 1024'):
            trial.ARMNativeLimitCommands(base,native_shell(),[native_shell()])


class ARMPolicyTests(unittest.TestCase):
    def test_probe_zero_two_and_nonnumeric_lines_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);cmd=mock.Mock();cmd.address_space_bytes=4294967296
            valid='Max address space 4294967296 4294967296 bytes\n'
            for text in ('',valid+valid,'Max address space invalid 4294967296 bytes\n'):
                cmd.run.side_effect=lambda argv,prefix,stdout,t=text:stdout.write(t.encode())
                with self.subTest(text=text),self.assertRaises(ValueError):trial.arm_address_space_probe(cmd,p)
            self.assertEqual(list(inspect.signature(trial.arm_address_space_probe).parameters),['command','output'])

    def test_probe_mismatch_cannot_be_overridden(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);cmd=mock.Mock();cmd.address_space_bytes=4294967296
            for text in ('Max address space 1073741824 4294967296 bytes\n','Max address space 4294967296 1073741824 bytes\n'):
                cmd.run.side_effect=lambda argv,prefix,stdout,t=text:stdout.write(t.encode())
                with self.assertRaisesRegex(ValueError,'must equal requested'):trial.arm_address_space_probe(cmd,p)
                self.assertFalse(json.loads((p/'address-space-probe.json').read_text())['address_space_enforced'])

    def test_signatures_are_keyword_only(self):
        for function in (trial.install,trial.convert):
            params=inspect.signature(function).parameters
            self.assertEqual(params['arm_native_limit_shell'].kind,inspect.Parameter.KEYWORD_ONLY)
            self.assertIsNone(params['arm_native_limit_shell'].default)
            self.assertEqual(params['arm_allow_wrapper_tools'].kind,inspect.Parameter.KEYWORD_ONLY)
            self.assertIs(params['arm_allow_wrapper_tools'].default,False)
        self.assertFalse(hasattr(trial,'ARM_INSTALL_CONTEXT'));self.assertFalse(hasattr(trial,'arm_install'))

    def test_x86_install_passes_no_arm_keywords(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);out=p/'output';out.mkdir()
            with mock.patch.object(trial,'convert',return_value={'status':'CONVERTED','archives':[]}) as convert,contextlib.redirect_stdout(io.StringIO()):
                trial.install(p,out,'cc','dis','nm',p)
            self.assertEqual(convert.call_args.kwargs,{})

    def test_cli_arm_options_are_exclusive_and_x86_rejected(self):
        base=['source','--root','/unused/root','--build','/unused/build','--evidence','/unused/out','--compiler','/unused/cc','--disassembler','/unused/dis','--nm','/unused/nm']
        for arch,options,reason in [('x86_64',['--native-limit-shell','/bin/bash'],'only valid for ARM'),('x86_64',['--allow-wrapper-tools'],'only valid for ARM'),('armv7l',['--native-limit-shell','/bin/bash','--allow-wrapper-tools'],'mutually exclusive')]:
            with mock.patch.object(sys,'argv',base+['--arch',arch]+options),mock.patch.object(trial,'install') as install,contextlib.redirect_stderr(io.StringIO()) as err:
                with self.assertRaises(SystemExit) as status:trial.install_main()
            self.assertEqual(status.exception.code,2);self.assertIn(reason,err.getvalue());install.assert_not_called()

    def test_x86_cli_passes_no_arm_keywords(self):
        args=['source','--root','/unused/root','--build','/unused/build','--evidence','/unused/out','--arch','x86_64','--compiler','/unused/cc','--disassembler','/unused/dis','--nm','/unused/nm']
        with mock.patch.object(sys,'argv',args),mock.patch.object(trial,'install') as install:trial.install_main()
        self.assertEqual(install.call_args.kwargs,{})

    def test_only_native_x86_elf_or_explicit_wrapper(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'tool';p.touch();p.chmod(0o755)
            for machine in (40,183,243):
                p.write_bytes(native_header(machine))
                with self.subTest(machine=machine),self.assertRaisesRegex(ValueError,'machine 62'):trial.arm_tool_identity(p,True)
            p.write_bytes(native_header());self.assertEqual(trial.arm_tool_identity(p)['machine'],62)
            p.write_text('#!/bin/sh\nexec tool "$@"\n')
            with self.assertRaisesRegex(ValueError,'requires --allow-wrapper-tools'):trial.arm_tool_identity(p)
            r=trial.arm_tool_identity(p,True);self.assertEqual(r['sha256'],production.sha(p));self.assertEqual(r['first_4k'],p.read_text())
            self.assertEqual(r['first_4k_hex'],p.read_bytes().hex())
            with self.assertRaisesRegex(ValueError,'non-ELF'):
                trial.ARMNativeLimitCommands(trial.Commands(),native_shell(),[p])
            with self.assertRaisesRegex(ValueError,'non-ELF'):
                trial.ARMNativeLimitCommands(trial.Commands(),p,[native_shell()])

    def test_missing_nm_and_wrong_major_preserve_both_reasons(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'CMakeCache.txt').touch();cc=p/'cc';di=p/'dis';nm=p/'absent-nm'
            for t in (cc,di):t.write_bytes(native_header());t.chmod(0o755)
            cmd=mock.Mock();cmd.run.side_effect=lambda argv,prefix,stdout:stdout.write(b'clang version 23.0.0\n')
            with self.assertRaises(ValueError) as err:trial.validate_arm_tools(p,cc,di,nm,cmd,p,'aarch64')
            self.assertIn('missing or non-executable --nm',str(err.exception));self.assertIn('uncertified ARM clang major version 23.0.0',str(err.exception))

    def test_targets_must_be_present_identical_and_certified(self):
        for arch,target in [('armv7l','armv7l-tizen-linux-gnueabi'),('aarch64','aarch64-tizen-linux-gnu')]:
            flags=arm_flags(arch)
            self.assertEqual(trial.arm_classify_options(flags+['--target='+target]*2,arch)['optimization'],'-Os' if arch=='armv7l' else '-O3')
            for extra in ([],['--target='+target,'--target=x86_64-tizen-linux-gnu'],['--target=riscv64-linux-gnu']):
                with self.subTest(arch=arch,extra=extra),self.assertRaises(ValueError):trial.arm_classify_options(flags+extra,arch)
        with self.assertRaisesRegex(ValueError,'identical certified'):
            trial.arm_classify_options(arm_flags('armv7l')+['--target=armv7l-tizen-linux-gnueabi','--target=thumbv7-tizen-linux-gnueabi'],'armv7l')


if __name__=='__main__':unittest.main(verbosity=2)
