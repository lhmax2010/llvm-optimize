"""Lightweight configuration and POSIX shell checks; no LLVM compilation."""
import os
from pathlib import Path
import subprocess
import bolt_helper as h
from test_bolt_helper import Base


class HybridGateTests(Base):
    def setUp(self):
        super().setUp()
        self.source=Path(h.__file__).resolve().parent.parent
        spec=(self.source/'packaging/llvm.spec').read_text()
        a=spec.index('for hybrid_tool in ');b=spec.index('echo TIZEN_HYBRID_LINK_OK',a)
        self.gate=spec[a:b]+'echo TIZEN_HYBRID_LINK_OK\n'
        (self.d/'bin').mkdir();(self.d/'mock').mkdir()
        for name in ('clang-22','lld','llvm-ar'):(self.d/'bin'/name).write_text('fixture')
    def run_gate(self,needed):
        readelf=self.d/'mock/readelf';readelf.write_text("#!/bin/sh\nprintf '%s\\n' ' 0x1 (NEEDED) Shared library: ["+needed+"]'\n");readelf.chmod(0o755)
        return subprocess.run(['/bin/sh','-e','-c',self.gate],cwd=self.d,env=dict(os.environ,PATH=str(readelf.parent)+':'+os.environ['PATH']),capture_output=True,text=True)
    def test_missing_tool(self):
        (self.d/'bin/lld').unlink();self.assertEqual(self.run_gate('libc.so.6').returncode,1)
    def test_llvm_rejected(self):self.assertEqual(self.run_gate('libLLVM-22.so').returncode,1)
    def test_clang_cpp_rejected(self):self.assertEqual(self.run_gate('libclang-cpp.so.22.1').returncode,1)
    def test_component_link_pass(self):
        r=self.run_gate('libc.so.6');self.assertEqual(r.returncode,0);self.assertIn('TIZEN_HYBRID_LINK_OK',r.stdout)
    def test_empty_component_fatal(self):
        path=self.source/'llvm/cmake/modules/AddLLVM.cmake'
        # Sparse packaging worktrees still carry the exact source in Git.
        s=path.read_text() if path.exists() else subprocess.check_output(
            ['git','-C',str(self.source),'show','HEAD:llvm/cmake/modules/AddLLVM.cmake'],text=True)
        a=s.index('function(tizen_hybrid_llvm_interface ');b=s.index('endfunction()',a)+len('endfunction()')
        cmake='''cmake_minimum_required(VERSION 3.20)
project(probe LANGUAGES NONE)
set(TIZEN_HYBRID_LINK ON)
set(LLVM_LINK_LLVM_DYLIB ON)
add_library(probe STATIC IMPORTED)
set_property(TARGET probe PROPERTY INTERFACE_LINK_LIBRARIES LLVM)
function(llvm_map_components_to_libnames result)
  set(${result} "" PARENT_SCOPE)
endfunction()
'''+s[a:b]+'\ntizen_hybrid_llvm_interface(probe)\n'
        (self.d/'CMakeLists.txt').write_text(cmake)
        p=subprocess.run(['cmake','-S',str(self.d),'-B',str(self.d/'configure')],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0);self.assertIn('probe: empty LLVM component interface',p.stderr);self.assertIn('declare LINK_COMPONENTS',p.stderr)
