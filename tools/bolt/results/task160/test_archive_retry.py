from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ARCHIVE = Path(__file__).resolve().parent
W = ARCHIVE.parents[1]
RECIPE = W / 'temp/task131/pgo-dev'
BASE = '750d7a83475a3c3c6fecf545ea74ba110fc845f5'
PATH = 'packaging/llvm-static-archives-native.py'
LOW, HIGH = 4 * 2**30, 8 * 2**30


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RetryTest(unittest.TestCase):
    def setUp(self):
        work = tempfile.TemporaryDirectory(dir=ARCHIVE)
        self.addCleanup(work.cleanup)
        self.work = Path(work.name)
        self.new = load(RECIPE / PATH, 'new_converter')
        old = self.work / 'old.py'
        old.write_bytes(subprocess.check_output(['/usr/bin/git', '-C', RECIPE, 'show', BASE + ':' + PATH]))
        self.old = load(old, 'old_converter')
        self.compiler = self.work / 'compiler'
        self.compiler.write_text('''#!/usr/bin/python3
import os
from pathlib import Path
import resource
import sys
target = Path(sys.argv[-1])
source = Path(sys.argv[-3])
limit = resource.getrlimit(resource.RLIMIT_AS)[0]
name = target.name
with open(os.environ['RETRY_TEST_EVENTS'],'a') as f:
    f.write(f'{name} {limit}\\n')
status = os.environ['RETRY_TEST_MODE']
if name in ('a.o', 'c.o') and status != 'success':
    target.write_bytes(b'partial')
    if status == 'nonmemory':
        sys.stderr.write('compilation error: invalid bitcode\\n')
        sys.exit(1)
    if limit == 4 * 2**30 or status == 'oom-twice':
        sys.stderr.write('mmap: Cannot allocate memory\\n' if status == 'enomem' else 'LLVM ERROR: out of memory\\n')
        sys.exit(1)
    if target.read_bytes() != b'partial':
        sys.exit(2)
target.write_bytes(b'converted:' + source.read_bytes())
''')
        self.compiler.chmod(0o700)

    def run_archive(self, module, mode, use_retry=True, label='run'):
        directory = self.work / label
        root, output = directory / 'buildroot', directory / 'evidence'
        root.mkdir(parents=True)
        archive = root/'libtest.a'
        archive.write_bytes(b'abcdef')
        names = ('a.o','b.o','c.o')
        before = {'members': [dict(name=name, ordinal=i, occurrence=1, kind='bitcode', offset=2*i, size=2,
                                   sha256=hashlib.sha256(archive.read_bytes()[2*i:2*i+2]).hexdigest())
                              for i,name in enumerate(names)],
                  'bitcode':3,'machine':0,'member_count':3,
                  'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'bytes':archive.stat().st_size}
        tools = dict(tool_versions={},tool_directory=str(directory))
        elf = dict(checked=0,forbidden=[])
        fake_ir = dict(flags=['-c'],policy={'dwarf':4},pic_level=0)
        listing = dict(members=[dict(name=name,occurrence=1,debug_sections=True) for name in names],
                       bitcode=0,other=0,index_equals_machine_symbols=True,index_entries=0)
        retry = {'retry_address_space_bytes': HIGH} if use_retry else {}
        self.events = directory / 'events'
        self.log = io.StringIO()
        self.output = output
        with patch.dict(os.environ, {'RETRY_TEST_MODE':mode,'RETRY_TEST_EVENTS':str(self.events)}), \
             patch.object(module,'validate_archive',return_value=before), \
             patch.object(module,'validate_tools',return_value=tools), \
             patch.object(module,'inspect',side_effect=lambda path: dict(
                 listing, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size)), \
             patch.object(module,'ir_settings',return_value=fake_ir), \
             patch.object(module,'pic_relocations',return_value=elf), \
             patch.object(module,'check_symbols',return_value={}), redirect_stdout(self.log):
            module.convert(root,output,self.compiler,Path('/usr/bin/true'),Path('/usr/bin/true'),directory,
                           jobs=2,debug_info='yes',**retry)
        target = output/'archives/libtest.a'
        listing = subprocess.check_output(['/usr/bin/ar','t',target],text=True).splitlines()
        self.assertEqual(listing,list(names))
        return target.read_bytes()

    def test_oom_success_retries_after_parallel_workers_and_in_order(self):
        artifact = self.run_archive(self.new,'oom')
        events=[line.split() for line in self.events.read_text().splitlines()]
        self.assertEqual([int(x[1]) for x in events], [LOW,LOW,LOW,HIGH,HIGH])
        self.assertEqual([x[0] for x in events[-2:]], ['a.o','c.o'])
        self.assertIn(b'converted:ab', artifact)
        self.assertIn(b'converted:ef', artifact)
        for ordinal in ('00000','00002'):
            folder = self.output/'members/libtest.a'/ordinal
            original = json.loads((folder/'convert.json').read_text())
            retry = json.loads((folder/'convert-retry.json').read_text())
            self.assertEqual(original['argv'], retry['argv'])
            self.assertEqual((original['exit'],retry['exit']),(1,0))
        lines = [line for line in self.log.getvalue().splitlines() if line.startswith('ARCHIVE_MEMBER_RETRY')]
        self.assertEqual(lines,[f'ARCHIVE_MEMBER_RETRY libtest.a {name} {HIGH} PASS' for name in ('a.o','c.o')])

    def test_oom_retry_failure_keeps_failed_state(self):
        with self.assertRaises(RuntimeError):
            self.run_archive(self.new,'oom-twice')
        self.assertIn(f'ARCHIVE_MEMBER_RETRY libtest.a a.o {HIGH} FAIL', self.log.getvalue())
        self.assertFalse((self.output/'archives/libtest.a').exists())
        self.assertEqual(json.loads((self.output/'summary.json').read_text())['status'],'FAILED')

    def test_other_failures_and_disabled_retry_do_not_retry(self):
        for use_retry,mode in ((True,'nonmemory'),(False,'oom')):
            with self.subTest(mode=mode):
                with self.assertRaises(RuntimeError):
                    self.run_archive(self.new,mode,use_retry,label=mode)
                self.assertNotIn('ARCHIVE_MEMBER_RETRY',self.log.getvalue())
                self.assertFalse(any(t.endswith(str(HIGH)) for t in self.events.read_text().splitlines()))

    def test_success_matches_the_previous_converter_byte_for_byte(self):
        before = self.run_archive(self.old,'success',False,label='old')
        after = self.run_archive(self.new,'success',label='new')
        self.assertEqual(before,after)
        self.assertNotIn('ARCHIVE_MEMBER_RETRY',self.log.getvalue())

    def test_enomem_diagnostic_and_unrelated_line(self):
        self.run_archive(self.new,'enomem')
        self.assertIn(f'ARCHIVE_MEMBER_RETRY libtest.a a.o {HIGH} PASS',self.log.getvalue())
        self.assertFalse(self.new.archive_memory_error("source.c: error: LLVM ERROR: out of memory"))
        self.assertFalse(self.new.archive_memory_error('killed: Cannot allocate memory'))
        self.assertTrue(self.new.archive_memory_error('prlimit: failed to execute clang: Cannot allocate memory'))


if __name__=='__main__':
    unittest.main()
