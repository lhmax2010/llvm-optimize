#!/usr/bin/env python3
"""Check consumer driver guard without running acceptance or rebuilding LLVM."""
import unittest
from verify_native_archive_consumers import validate_link_driver

class DriverGuardTests(unittest.TestCase):
    def test_object_only_bfd_and_lld(self):
        for exe in ('/usr/bin/ld.bfd','/tmp/ld.lld'):
            validate_link_driver('clang version 22.1.8\n "'+exe+'" "a.o" "-lLLVMPasses" "-o" "a"\n')

    def test_loader_cc1_regression_rejected(self):
        with self.assertRaises(ValueError):
            validate_link_driver(' "/lib64/ld-linux-x86-64.so.2" "-cc1" "a.cpp"\n')

    def test_all_lto_plugin_forms_rejected(self):
        for flag in ('-flto','-flto=thin','-plugin','--plugin','-plugin=/x','--plugin=/x','-cc1as'):
            with self.subTest(flag=flag),self.assertRaises(ValueError):
                validate_link_driver(' "/usr/bin/ld.bfd" "'+flag+'" "a.o"\n')

if __name__=='__main__':unittest.main(verbosity=2)
