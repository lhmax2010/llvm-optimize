#!/bin/sh
set -eu
export HOME=/home/abuild USER=abuild LOGNAME=abuild SHELL=/bin/sh
export PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin
export LANG=C LC_ALL=C
cd /home/abuild
printf 'BOLT_REHEARSAL_PATH=%s\n' "$PATH"
command -v clang
command -v clang++
rpm --define '_smp_mflags -j4' --eval 'BOLT_REHEARSAL_MACROS toolchain=%{_toolchain} smp=%{_smp_mflags} optflags=%{optflags}'
test "$(rpm --eval '%{_toolchain}')" = clang
exec rpmbuild --define '_smp_mflags -j4' --define '_srcdefattr (-,root,root)' --nosignature --target=x86_64 --define '_build_create_debug 1' -bi --short-circuit /home/abuild/rpmbuild/SOURCES/llvm.spec
