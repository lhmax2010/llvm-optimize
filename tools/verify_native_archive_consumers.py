#!/usr/bin/env python3
"""Exercise native LLVM archives with GNU ld (no LTO/plugin) and lld.

Run in a bounded scope. Compile and link are separate invocations; links take
only existing .o inputs. C++/glibc are host dependencies, LLVM headers/libraries
are explicitly selected, and the Tizen libxml2 runtime stays in --library-path.
No host installation, binary patching, or fallback after a failed check.
"""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import time

from convert_static_archives import Commands, sha

IR = '''source_filename = "archive-consumer"
define i32 @archive_probe_fn(i32 %x) {
entry:
  %a = add i32 %x, 0
  %b = mul i32 %a, 2
  %c = add i32 %b, 0
  ret i32 %c
}
'''
PROGRAM_A = r'''
#include <llvm/AsmParser/Parser.h>
#include <llvm/IR/LLVMContext.h>
#include <llvm/IR/Module.h>
#include <llvm/IR/Verifier.h>
#include <llvm/Passes/PassBuilder.h>
#include <llvm/Support/SourceMgr.h>
#include <llvm/Support/raw_ostream.h>
extern "C" int archive_probe(const char *filename) {
  llvm::LLVMContext context;
  llvm::SMDiagnostic diagnostic;
  auto module = llvm::parseAssemblyFile(filename, diagnostic, context);
  if (!module) { diagnostic.print("archive-consumer", llvm::errs()); return 1; }
  if (llvm::verifyModule(*module, &llvm::errs())) return 2;
  llvm::LoopAnalysisManager lam;
  llvm::FunctionAnalysisManager fam;
  llvm::CGSCCAnalysisManager cgam;
  llvm::ModuleAnalysisManager mam;
  llvm::PassBuilder pb;
  pb.registerModuleAnalyses(mam);
  pb.registerCGSCCAnalyses(cgam);
  pb.registerFunctionAnalyses(fam);
  pb.registerLoopAnalyses(lam);
  pb.crossRegisterProxies(lam, fam, cgam, mam);
  auto pipeline = pb.buildPerModuleDefaultPipeline(llvm::OptimizationLevel::O2);
  pipeline.run(*module, mam);
  if (llvm::verifyModule(*module, &llvm::errs())) return 3;
  module->print(llvm::outs(), nullptr);
  return 0;
}
#ifndef SHARED_PROBE
int main(int argc, char **argv) {
  return argc == 2 ? archive_probe(argv[1]) : 64;
}
#endif
'''
PROGRAM_B = r'''
#include <lld/Common/Driver.h>
#include <llvm/Support/raw_ostream.h>
LLD_HAS_DRIVER(elf)
int main(int argc, char **argv) {
  if (argc != 3) return 64;
  const char *args[] = {"ld.lld", "-m", "elf_x86_64", "-e", "_start", argv[1], "-o", argv[2]};
  const lld::DriverDef drivers[] = {{lld::Gnu, &lld::elf::link}};
  auto result = lld::lldMain(args, llvm::outs(), llvm::errs(), drivers);
  if (result.retCode != 0 || !result.canRunAgain) return 1;
  llvm::outs() << "lld-in-process-link-ok\n";
  return 0;
}
'''
SHARED_MAIN = r'''
#include <dlfcn.h>
#include <cstdio>
int main(int argc, char **argv) {
  if (argc != 3) return 64;
  void *h = dlopen(argv[1], RTLD_NOW | RTLD_LOCAL);
  if (!h) { std::fprintf(stderr, "%s\n", dlerror()); return 1; }
  auto f = reinterpret_cast<int (*)(const char *)>(dlsym(h, "archive_probe"));
  if (!f) return 2;
  int rc = f(argv[2]);
  if (dlclose(h)) return 3;
  return rc;
}
'''
MINIMAL_ASM = '.text\n.global _start\n_start:\nmov $60,%eax\nmov $37,%edi\nsyscall\n.section .note.GNU-stack,"",@progbits\n'


def validate_link_driver(text):
    """Reject the former loader/cc1 entry bug, LTO, or any plugin injection."""
    for line in text.splitlines():
        if not line.lstrip().startswith('"'):
            continue
        words=shlex.split(line)
        if any(x in ('-cc1','-cc1as','-plugin','--plugin') or
               x.startswith(('-flto','--plugin=','-plugin=')) for x in words):
            raise ValueError('link driver contains a compile job, LTO, or plugin')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline',type=Path,required=True)
    p.add_argument('--archives',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--loader',type=Path,required=True)
    p.add_argument('--library-path',required=True)
    a=p.parse_args()
    baseline,archives,out=a.baseline.resolve(),a.archives.resolve(),a.output.resolve()
    out.mkdir(parents=True,exist_ok=False)
    command=Commands(); result=dict(status='RUNNING',checks=[])
    def save(): (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    def passed(name,**extra): result['checks'].append(dict(name=name,status='PASS',**extra));save()
    def capture(argv,name):
        dest=out/(name+'.txt')
        with dest.open('wb') as stream:command.run(argv,out/name,stdout=stream)
        return dest.read_text()
    try:
        prefix=out/'prefix';(prefix/'bin').mkdir(parents=True)
        (prefix/'include').symlink_to(baseline/'usr/include',target_is_directory=True)
        (prefix/'lib64').symlink_to(archives,target_is_directory=True)
        loader=prefix/'bin/ld-for-config';shutil.copyfile(a.loader,loader);loader.chmod(0o755)
        assert sha(loader)==sha(a.loader)
        config=[str(loader),'--library-path',a.library_path,str(baseline/'usr/bin/llvm-config'),'--link-static']
        def query(name,args):return shlex.split(capture(config+args,'query-'+name))
        cxxflags=query('cxxflags',['--cxxflags']);ldflags=query('ldflags',['--ldflags'])
        libs_a=query('libs-a',['--libs','asmparser','passes','core','support'])
        libs_b=query('libs-all',['--libs','all'])
        system=query('system-libs',['--system-libs','all'])
        resolved=[];substitutions=[]
        for flag in system:
            replacement=flag
            if flag.startswith('-l') and not flag.startswith('-l:'):
                name=flag[2:]
                runtime=[x for d in a.library_path.split(':') for x in sorted(Path(d).glob('lib'+name+'.so.*'))]
                if runtime:replacement=str(runtime[0])
                elif not any((Path(d)/('lib'+name+ext)).exists() for d in ['/usr/lib/x86_64-linux-gnu','/lib/x86_64-linux-gnu'] for ext in ['.so','.a']):
                    candidates=sorted(Path('/usr/lib/x86_64-linux-gnu').glob('lib'+name+'.so.*'))
                    if not candidates:raise RuntimeError('missing host dependency '+flag)
                    replacement=str(candidates[0])
            if replacement!=flag:substitutions.append(dict(original=flag,resolved=replacement,sha256=sha(replacement)))
            resolved.append(replacement)
        result['system_dependency_resolution']=substitutions
        clang=[str(a.loader),'--library-path',a.library_path,str(baseline/'usr/bin/clang-22'),
               '--no-default-config','--driver-mode=g++','--target=x86_64-linux-gnu',
               '-resource-dir',str(baseline/'usr/lib64/clang/22'),'-O2','-fPIC','-ffunction-sections','-fdata-sections']
        lld=out/'ld.lld';lld.write_text('#!/bin/sh\nexec '+shlex.join([str(a.loader),'--library-path',a.library_path,str(baseline/'usr/bin/lld'),'-flavor','gnu'])+' "$@"\n');lld.chmod(0o755)
        def compile_one(name,source,extra=()):
            obj=out/(name+'.o')
            argv=clang+cxxflags+list(extra)+['-v','-c',str(source),'-o',str(obj)]
            command.run(argv,out/('compile-'+name))
            return obj
        def link(name,objects,libs,linker='/usr/bin/ld.bfd',extra=(),search=None):
            if any(x.suffix!='.o' or not x.is_file() for x in objects):raise ValueError('only existing .o compilation inputs allowed at link stage')
            argv=clang+['--ld-path='+str(linker),*map(str,objects),*(ldflags if search is None else search),*extra,*libs,*resolved,'-o',str(out/name)]
            dry=subprocess.run([*argv,'-###'],capture_output=True,text=True,check=True)
            (out/(name+'-driver.txt')).write_text(dry.stdout+dry.stderr)
            validate_link_driver(dry.stderr)
            command.run(argv,out/('link-'+name))
            return out/name
        def run_ir(exe,name,args):
            text=capture([str(a.loader),'--library-path',a.library_path,str(exe),*map(str,args)],'run-'+name)
            if text!=expected:raise RuntimeError('IR differs from baseline opt: '+name)
            needed=capture(['readelf','-dW',str(exe)],name+'-dynamic')
            if 'Shared library: [libLLVM' in needed or 'Shared library: [libclang' in needed:raise RuntimeError('consumer unexpectedly uses LLVM shared library')
            return text
        for name,source in [('a',PROGRAM_A),('b',PROGRAM_B),('shared-main',SHARED_MAIN)]: (out/(name+'.cpp')).write_text(source)
        ir=out/'input.ll';ir.write_text(IR)
        command.run([str(a.loader),'--library-path',a.library_path,str(baseline/'usr/bin/opt'),'-S','-O2',str(ir),'-o',str(out/'expected.ll')],out/'reference-opt')
        expected=(out/'expected.ll').read_text()
        obj_a=compile_one('a',out/'a.cpp')
        # Driver's -v output records actual host GCC header search directories.
        result['environment']=dict(headers='LLVM headers from baseline; C++ and libc headers from host GCC search in compile-a.log',
                                   resource_dir=str(baseline/'usr/lib64/clang/22'),loader=str(a.loader),runtime_library_path=a.library_path,
                                   compiler_sha256=sha(baseline/'usr/bin/clang-22'))
        for flavor,path in [('bfd','/usr/bin/ld.bfd'),('lld',lld)]:
            name='a-'+flavor;exe=link(name,[obj_a],libs_a,path)
            run_ir(exe,name,[ir]);passed(name,bytes=exe.stat().st_size,sha256=sha(exe))
            capture([str(a.loader),'--library-path',a.library_path,'--list',str(exe)],name+'-runtime')
        obj_b=compile_one('b',out/'b.cpp')
        (out/'minimal.s').write_text(MINIMAL_ASM)
        command.run(['/usr/bin/as','--64',str(out/'minimal.s'),'-o',str(out/'minimal.o')],out/'compile-minimal')
        for flavor,path in [('bfd','/usr/bin/ld.bfd'),('lld',lld)]:
            name='b-'+flavor;exe=link(name,[obj_b],['-Wl,--start-group','-llldELF','-llldCommon',*libs_b,'-Wl,--end-group'],path)
            generated=out/(name+'-generated')
            text=capture([str(a.loader),'--library-path',a.library_path,str(exe),str(out/'minimal.o'),str(generated)],'run-'+name)
            if text!='lld-in-process-link-ok\n':raise RuntimeError('unexpected lld public API result')
            argv=['prlimit','--as=4294967296','--core=0','--',str(generated)]
            actual=subprocess.run(argv,capture_output=True,text=True)
            rec=dict(argv=argv,exit=actual.returncode,stdout=actual.stdout,stderr=actual.stderr,expected_exit=37)
            (out/(name+'-generated-run.json')).write_text(json.dumps(rec,indent=2)+'\n')
            if actual.returncode!=37:raise RuntimeError('in-process lld output exit differs from 37')
            passed(name,generated_exit=37)
        shared_obj=compile_one('a-shared',out/'a.cpp',['-DSHARED_PROBE'])
        shared=link('libprobe.so',[shared_obj],libs_a,extra=['-shared','-Wl,-z,defs,-z,text'])
        shared_main=compile_one('shared-main',out/'shared-main.cpp')
        main=link('shared-main',[shared_main],['-ldl'])
        run_ir(main,'shared-a',[shared,ir]);passed('shared-a',loaded_library=str(shared))
        gc=link('a-bfd-gc',[obj_a],libs_a,extra=['-Wl,--gc-sections'])
        run_ir(gc,'a-bfd-gc',[ir]);passed('gc-sections',normal_bytes=(out/'a-bfd').stat().st_size,gc_bytes=gc.stat().st_size)
        search=[x.replace(str(prefix/'lib64'),str(baseline/'usr/lib64')) for x in ldflags]
        argv=clang+['--ld-path=/usr/bin/ld.bfd',str(obj_a),*search,*libs_a,*resolved,'-o',str(out/'negative')]
        dry=subprocess.run([*argv,'-###'],capture_output=True,text=True,check=True)
        (out/'negative-driver.txt').write_text(dry.stderr);validate_link_driver(dry.stderr)
        start=time.monotonic()
        with (out/'negative.log').open('wb') as stream:
            actual=subprocess.run(['prlimit','--as=4294967296','--core=0','--',*argv],stdout=stream,stderr=subprocess.STDOUT)
        negative=dict(argv=argv,exit=actual.returncode,elapsed_seconds=time.monotonic()-start)
        (out/'negative.json').write_text(json.dumps(negative,indent=2)+'\n')
        if actual.returncode==0:raise RuntimeError('unconverted bitcode unexpectedly linked without plugin')
        log=(out/'negative.log').read_text()
        if not any(t in log.lower() for t in ('archive has no index','file format not recognized','file not recognized')):
            raise RuntimeError('negative control failed for an unrecognized reason')
        passed('negative-control',**negative)
        result['status']='PASS';return 0
    except BaseException as error:
        command.cancel();result.update(status='FAIL',reason=str(error));raise
    finally:save()


if __name__=='__main__':raise SystemExit(main())
