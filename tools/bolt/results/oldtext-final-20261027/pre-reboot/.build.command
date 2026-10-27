#!/bin/sh -x
exec "rpmbuild" "--define" "jobs 8" "--define" "_smp_mflags -j8" "--define" "_costomized_smp_mflags -j20" "--define" "_srcdefattr (-,root,root)" "--nosignature" "--target=x86_64" "--define" "_build_create_debug 1" "-ba" "/home/abuild/rpmbuild/SOURCES/llvm.spec"
