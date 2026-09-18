#!/usr/bin/env python3
"""Offline safety tests; no compiler, linker, GBS or perf is executed."""
import json
from pathlib import Path
import shlex
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

import bench_toolchain as bench
import relink_clang_for_bolt as relink
import verify_compiler_outputs as verify


class BoltPreparation(unittest.TestCase):
    def test_link_rewrite_changes_only_outputs_and_emit_relocs(self):
        original = (': && /bin/clang++ -O3 -flto=thin input.o -o bin/clang-22 '
                    '-Wl,-rpath,"\\$ORIGIN/../lib64:" '
                    '-Xlinker --dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d && :')
        changed = relink.rewrite_command(original,Path('/home/abuild/separate'))
        a = shlex.split(original[5:-5]); b = shlex.split(changed)
        self.assertEqual(b.pop(),'-Wl,--emit-relocs')
        b[b.index('-o')+1]='bin/clang-22'
        b=[s.replace('--dependency-file=/home/abuild/separate/clang-link.d',
                     '--dependency-file=tools/clang/tools/driver/CMakeFiles/clang.dir/link.d') for s in b]
        self.assertEqual(a,b)
        self.assertIn('-Wl,-rpath,"\\$ORIGIN/../lib64:"',changed)
        for bad in [original+'\nsecond-command',original.replace('-o bin/clang-22','-o other'),
                    original.replace('-O3','-O3 -Wl,--emit-relocs')]:
            with self.assertRaises(RuntimeError): relink.rewrite_command(bad,Path('/new'))

    def equality_case(self, mismatch):
        with tempfile.TemporaryDirectory(dir=bench.WORKSPACE/'temp',prefix='bolt-equality-test-') as tmp:
            tmp=Path(tmp); output=tmp/'evidence'
            source=tmp/'input.ii';source.write_text('int x;\n')
            units=[dict(name=name,path=source,flags=['-std=c++17'],sha256=bench.digest(source))
                   for name in ['first','second']]
            calls=[]; real_command=bench.Runner.command
            def command(runner, argv, **kwargs):
                if '-c' not in argv: return real_command(runner,argv,**kwargs)
                calls.append(list(argv))
                # Simulate compiler output, but perform the real ARM-header and cmp checks.
                elf=b'\x7fELF\x01\x01'+b'\0'*10+struct.pack('<HH',1,40)
                data=elf+(b'different' if mismatch and '/bin/false' in argv else b'identical')
                Path(argv[argv.index('-o')+1]).write_bytes(data)
                return {'simulation':True,'argv':list(map(str,argv))}
            argv=['verify','--baseline','/bin/true','--candidate','/bin/false',
                  '--loader','/lib64/ld-linux-x86-64.so.2','--sysroot',str(tmp),
                  '--resource-dir',str(tmp),'--output',str(output)]
            with patch.object(sys,'argv',argv), patch.object(bench,'real_inputs',return_value=units), \
                 patch.object(bench.Runner,'command',command):
                code=verify.main()
            result=json.loads((output/'result.json').read_text())
            self.assertEqual(code,2 if mismatch else 0)
            self.assertEqual(result['status'],'BLOCKER' if mismatch else 'PASS')
            self.assertEqual(len(calls),2 if mismatch else 4)
            self.assertEqual(len(result['units']),1 if mismatch else 2)
            self.assertEqual(calls[0][calls[0].index('-o')+1],calls[1][calls[1].index('-o')+1])
            self.assertEqual(result['units'][0]['byte_equal'],not mismatch)

    def test_identical_outputs_pass(self): self.equality_case(False)
    def test_first_mismatch_stops_before_next_tu(self): self.equality_case(True)


if __name__=='__main__': unittest.main(verbosity=2)
