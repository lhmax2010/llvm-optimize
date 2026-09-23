#!/usr/bin/env python3
"""Consumer acceptance for converted LLVM archives; run in a bounded scope.

LLVM libraries come only from --archives. llvm-config is run through a copy of
the host loader placed in a temporary prefix so its executable-based prefix
discovery works without editing the original executable or installing files.
GNU ld is selected directly by clang, with neither LTO nor a linker plugin.
"""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess

from convert_static_archives import Commands, sha


PROGRAM_A = r'''
#include <llvm/AsmParser/Parser.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/Verifier.h>
#include <llvm/Support/SourceMgr.h>
#include <llvm/Support/raw_ostream.h>
extern "C" int archive_probe() {
  llvm::LLVMContext context;
  llvm::SMDiagnostic diagnostic;
  auto module = llvm::parseAssemblyString("define i32 @archive_probe_fn() { ret i32 42 }", diagnostic, context);
  if (!module || llvm::verifyModule(*module, &llvm::errs())) return 1;
  for (const auto &function : *module) llvm::outs() << function.getName() << "\n";
  return 0;
}
#ifndef SHARED_PROBE
int main() { return archive_probe(); }
#endif
'''
PROGRAM_B = r'''
#include <lld/Common/Driver.h>
#include <llvm/Support/raw_ostream.h>
LLD_HAS_DRIVER(elf)
int main() {
  const char *args[] = {"ld.lld", "--version"};
  const lld::DriverDef drivers[] = {{lld::Gnu, &lld::elf::link}};
  auto result = lld::lldMain(args, llvm::outs(), llvm::errs(), drivers);
  if (result.retCode != 0 || !result.canRunAgain) return 1;
  llvm::outs() << "lld-public-api-ok\n";
  return 0;
}
'''


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline', type=Path, required=True)
    p.add_argument('--archives', type=Path, required=True, help='directory holding converted libLLVM*.a')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--loader', type=Path, required=True)
    p.add_argument('--library-path', required=True)
    a = p.parse_args()
    baseline, archives, out = a.baseline.resolve(), a.archives.resolve(), a.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    command = Commands()
    result = dict(status='RUNNING', checks=[])
    def save():
        (out/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    save()
    try:
        prefix = out/'prefix'
        (prefix/'bin').mkdir(parents=True)
        (prefix/'include').symlink_to(baseline/'usr/include', target_is_directory=True)
        (prefix/'lib64').symlink_to(archives, target_is_directory=True)
        loader = prefix/'bin/ld-for-config'
        shutil.copyfile(a.loader, loader); loader.chmod(0o755)
        assert sha(loader) == sha(a.loader)
        config = [str(loader), '--library-path', a.library_path, str(baseline/'usr/bin/llvm-config')]
        def query(name, args):
            dest = out/(name+'.txt')
            with dest.open('wb') as stream:
                command.run(config+['--link-static', *args], out/('query-'+name), stdout=stream)
            return shlex.split(dest.read_text())
        cxxflags = query('cxxflags', ['--cxxflags'])
        ldflags = query('ldflags', ['--ldflags'])
        libs_a = query('libs-a', ['--libs', 'asmparser', 'core', 'support'])
        libs_b = query('libs-all', ['--libs', 'all'])
        system = query('system-libs', ['--system-libs', 'all'])
        # Resolve -lfoo to an existing versioned host DSO if only its soname is
        # available. Record every such resolution; never substitute LLVM DSOs.
        system_resolved = []
        substitutions = []
        for flag in system:
            replacement = flag
            if flag.startswith('-l') and not flag.startswith('-l:'):
                name = flag[2:]
                runtime = [x for d in a.library_path.split(':')
                           for x in sorted(Path(d).glob('lib'+name+'.so.*'))]
                if runtime:
                    replacement = str(runtime[0])
                elif not any((Path(d)/('lib'+name+ext)).exists() for d in ['/usr/lib/x86_64-linux-gnu','/lib/x86_64-linux-gnu'] for ext in ['.so','.a']):
                    candidates = sorted(Path('/usr/lib/x86_64-linux-gnu').glob('lib'+name+'.so.*'))
                    if not candidates:
                        raise RuntimeError('missing host dependency: '+flag)
                    replacement = str(candidates[0])
            if replacement != flag:
                substitutions.append(dict(original=flag, resolved=replacement, sha256=sha(replacement)))
            system_resolved.append(replacement)
        result['system_dependency_resolution'] = substitutions
        clang = [str(a.loader), '--library-path', a.library_path, str(baseline/'usr/bin/clang-22'),
                 '--no-default-config', '--driver-mode=g++', '--target=x86_64-linux-gnu',
                 '-resource-dir', str(baseline/'usr/lib64/clang/22'), '-O2', '-fPIC']
        lld = out/'ld.lld'
        lld.write_text('#!/bin/sh\nexec '+shlex.join([str(a.loader),'--library-path',a.library_path,str(baseline/'usr/bin/lld'),'-flavor','gnu'])+' "$@"\n')
        lld.chmod(0o755)
        for name, source in [('a', PROGRAM_A), ('b', PROGRAM_B)]:
            (out/(name+'.cpp')).write_text(source)
        def link(name, flags):
            cmd = clang + cxxflags + flags
            dry = subprocess.run(cmd+['-###'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            (out/(name+'-driver.txt')).write_text(dry.stdout)
            if dry.returncode or '-flto' in dry.stdout or '"-plugin"' in dry.stdout or '"--plugin"' in dry.stdout:
                raise RuntimeError('LTO/plugin or bad driver in consumer '+name)
            command.run(cmd, out/('link-'+name))
        outputs = {}
        for name, libs in [('a', libs_a), ('b', ['-Wl,--start-group','-llldELF','-llldCommon',*libs_b,'-Wl,--end-group'])]:
            for linker, path in [('bfd','/usr/bin/ld.bfd'), ('lld',str(lld))]:
                tag = name+'-'+linker; exe = out/tag
                link(tag, ['--ld-path='+path, str(out/(name+'.cpp')), *ldflags, *libs, *system_resolved, '-o', str(exe)])
                text = out/(tag+'-output.txt')
                with text.open('wb') as stream:
                    command.run([str(a.loader),'--library-path',a.library_path,str(exe)], out/('run-'+tag), stdout=stream)
                actual = text.read_text()
                if name == 'a' and actual != 'archive_probe_fn\n':
                    raise RuntimeError('wrong IR consumer result')
                if name == 'b' and ('LLD 22.1.8' not in actual or not actual.endswith('lld-public-api-ok\n')):
                    raise RuntimeError('wrong lld consumer result')
                if name in outputs and actual != outputs[name]:
                    raise RuntimeError('consumer runtime outputs differ')
                outputs[name] = actual
                result['checks'].append(dict(name=tag, status='PASS', output=actual)); save()
        link('shared-a', ['--ld-path=/usr/bin/ld.bfd', '-shared', '-Wl,-z,text,-z,defs', '-DSHARED_PROBE',
                          str(out/'a.cpp'), *ldflags, *libs_a, *system_resolved, '-o', str(out/'libprobe.so')])
        result['checks'].append(dict(name='shared-a', status='PASS')); save()
        # Expected rejection by unconverted baseline archives. Keep identical
        # compiler and flags; only the LLVM -L directory changes.
        flags = [x.replace(str(prefix/'lib64'), str(baseline/'usr/lib64')) for x in ldflags]
        cmd = clang+cxxflags+['--ld-path=/usr/bin/ld.bfd', str(out/'a.cpp'), *flags, *libs_a, *system_resolved, '-o', str(out/'negative')]
        with (out/'negative.log').open('wb') as log:
            status = subprocess.run(['prlimit','--as=4294967296','--core=0','--',*cmd], stdout=log, stderr=subprocess.STDOUT).returncode
        result['negative'] = dict(argv=cmd, exit=status, status='PASS' if status else 'FAIL')
        if status == 0:
            raise RuntimeError('unconverted baseline unexpectedly linked without plugin')
        result['status'] = 'PASS'
        return 0
    except BaseException as error:
        command.cancel()
        result.update(status='FAIL', reason=str(error))
        raise
    finally:
        save()


if __name__ == '__main__':
    raise SystemExit(main())
