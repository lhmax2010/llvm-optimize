#
# spec file for package gcc-contrib
#
# Copyright (c) 2017 Tizen
# Please submit bugfixes or comments via http://bugs.tizen.org/
#
# we use %%{?macro: ... } as it is more compact

%define quadmath_arch %ix86 x86_64 ia64
%define tsan_arch x86_64 aarch64 riscv64
%define hwasan_arch aarch64
%define itm_arch x86_64 %ix86 %arm ppc ppc64 ppc64le s390 s390x %sparc aarch64
%define atomic_arch x86_64 %ix86 %arm aarch64 ppc ppc64 ppc64le s390 s390x %sparc m68k
%define lsan_arch x86_64 %ix86 armv7l armv7hl aarch64
%define ubsan_arch x86_64 %ix86 ppc ppc64 %arm aarch64 riscv64
%define cilkrts_arch x86_64 %ix86

%ifarch armv7l
%define ARCH armv7l
%define ABI eabi
%endif
%ifarch armv7hl
%define ARCH armv7hl
%define ABI eabihf
%endif
%ifarch %ix86
%define ARCH i586
%endif
%ifarch x86_64
%define ARCH x86_64
%endif
%ifarch aarch64
%define ARCH aarch64
%endif
%ifarch riscv64
%define ARCH riscv64
%endif
%define host_arch %{ARCH}-tizen-linux-gnu%{?ABI}

%define target_cpu %{?cross}%{!?cross:%{ARCH}}
%define target_abi %{?cross:%{?armv7l:eabi}}%{!?cross:%{?ABI}}

%define target_arch %{target_cpu}-tizen-linux-gnu%{?target_abi}
%define libdir %{!?cross:%{_libdir}}%{?cross:%{_prefix}/lib%{?aarch64:64}}
%define libsubdir %{libdir}/gcc/%{target_arch}/%{version}

%define full_as_sanitization :full_address_space=true

%ifarch armv7l armv7hl
%define asan_force_options -fsanitize-recover=address -fsanitize=address -mthumb -Wa,-mimplicit-it=thumb -fno-omit-frame-pointer -Wp,-U_FORTIFY_SOURCE -Wl,--as-needed -ldl -lpthread
%define lsan_force_options -fsanitize=leak -mthumb -Wa,-mimplicit-it=thumb -fno-omit-frame-pointer -Wp,-U_FORTIFY_SOURCE -Wl,--as-needed -ldl -lpthread
%define full_as_sanitization :full_address_space=false
%else
%define asan_force_options -fsanitize-recover=address -fsanitize=address -fno-omit-frame-pointer -Wp,-U_FORTIFY_SOURCE -Wl,--as-needed -ldl -lpthread
%define lsan_force_options -fsanitize=leak -fno-omit-frame-pointer -Wp,-U_FORTIFY_SOURCE -Wl,--as-needed -ldl -lpthread
%endif

%define ubsan_force_options -fsanitize=undefined,bounds-strict,float-divide-by-zero,float-cast-overflow
%define tsan_force_options -fsanitize=thread -fno-omit-frame-pointer -Wp,-U_FORTIFY_SOURCE -Wl,--as-needed -ldl -lpthread
%define gcov_force_options -fprofile-arcs -ftest-coverage
%define asan_runtime_options halt_on_error=false:start_deactivated=true:print_cmdline=true:quarantine_size_mb=1:detect_leaks=0:handle_segv=0:log_path=/tmp/asan.log:log_exe_name=1:fast_unwind_on_fatal=1:allocator_may_return_null=1:exitcode=0%{?full_as_sanitization}
%define ubsan_runtime_options print_cmdline=true:log_path=/tmp/ubsan.log
%define lsan_runtime_options print_cmdline=true:detect_leaks=1:log_path=/tmp/lsan.log:log_exe_name=1:fast_unwind_on_malloc=false:malloc_context_size=5:suppressions=/lsan.supp:print_suppressions=false
%define tsan_runtime_options print_cmdline=true:log_path=/tmp/tsan.log:detect_deadlocks=1:second_deadlock_stack=1
%define hwasan_force_options -fsanitize=hwaddress -fsanitize-recover=hwaddress -Wp,-U_FORTIFY_SOURCE -Wl,--as-needed -ldl -lpthread
%define hwasan_runtime_options halt_on_error=false:print_cmdline=true:handle_segv=0:log_path=/tmp/hwasan.log:log_exe_name=1:exitcode=0

# Set up reserve of virtual address space for 32-bit qemu-arm
%ifarch armv7l
%define required_qemu_va_size 0x80000000
%define export_qemu_line export QEMU_RESERVED_VA=%{required_qemu_va_size}
%define set_qemu_va \
	if [[ "$(od -An -j4 -N1 -tx1 /usr/bin/qemu-arm)" == " 01" ]]; then \
	   echo "WARNING:You are using 32-bit qemu-arm binary for emulation" \
	   echo "Address Sanitizer might not function properly in this environment" \
	   echo "Consider revising your qemu_aggregate or mic-boostrap_aggregate." \
	   echo '%{export_qemu_line}' >> /etc/profile \
	   %{export_qemu_line} \
	fi \
	%{nil}
%endif

Name:         gcc-contrib%{?cross:-%{cross}}
VCS:          platform/upstream/gcc-contrib#fc5216b079861e1680eb029cf28d25dbdd468e76
# With generated files in src we could drop the following
## until here, but at least renaming and patching info files breaks this
%{?cross:BuildRequires: binutils-%{cross}}
# here we use %%if because OBS spec parser cannot expand
# %%{?macro:...} correctly
Version:       14.2.0
Release:       1.1
Source15: gcc-force-options
Source16: gcc-unforce-options
Source17: asan_symbolize.py
Source18: gcc-contrib.manifest
Source19: macros.ubsan
Source20: extract-ubsan-logs
Source21: lsan.supp
Source22: macros.asan
Source23: cc1
Source24: macros.gcc_warning
Source25: extract-gcc-warning-logs
Source26: macros.gcov
Source27: extract-gcov-info
Source28: hwasan_stub.c
Source29: run_toolchain_tests.sh
Group:         Development/Building
Summary:       GCC related scripts
License:       MIT
%{?cross:ExcludeArch: %{cross}}
%description
GCC related scripts

%package -n asan-force-options
Summary:    Scripts to enable automatic package sanitization
Group:      System Environment
Requires:   gcc rpm
Requires:   libasan
Requires:   findutils

%description -n asan-force-options
Scripts for ASan instrumentation

%post -n asan-force-options
# Change mode to allow all users to run gcc-force/unforce-options
chmod a+w /usr/bin
chmod a+w %{libsubdir}

[ -d /emul/usr/bin ] && chmod a+w /emul/usr/bin/
[ -d /emul/home/abuild/rpmbuild ] && chmod a+w /emul/home/abuild/rpmbuild/BUILD/gcc-*/obj/gcc/
[ -d /emul/usr ] && find -L /emul/usr/*/gcc -name 'collect2' | xargs dirname | xargs chmod a+w

/usr/bin/gcc-force-options %asan_force_options -fno-common
# Add ASan-related macros
cat >> /usr/lib/rpm/tizen_macros << EOF

%%asan_force_options %{asan_force_options}
%%gcc_unforce_options %%{lua: rpm.define("asan_unforced 1"); print("/usr/bin/gcc-unforce-options")}
%%gcc_force_options /usr/bin/gcc-force-options
%%gcc_force_default_options %%gcc_force_options %%asan_force_options -fno-common
%%restore_fcommon \\
  %%gcc_unforce_options \\
  %%gcc_force_options %%asan_force_options -fcommon
EOF

# Add ASan's blacklist macro to tizen_macros
cat %{_rpmconfigdir}/macros.asan >> %{_rpmconfigdir}/tizen_macros

# ASan needs a whole shadow address space
# Using ulimit can only set the value for current user so we need to set /etc/security/limits.conf directly.
[ -e /etc/security/limits.conf ] && \
    sed '/End of file/i\abuild\tsoft\tas\t-1\nabuild\thard\tas\t-1' -i /etc/security/limits.conf

%preun -n asan-force-options
# Restore read-only mode
chmod a-w /usr/bin
chmod a-w %{libsubdir}
/usr/bin/gcc-unforce-options
# Restore limit configurations set for ASan
[ -e /etc/security/limits.conf ] && \
    sed '/abuild/d' -i /etc/security/limits.conf

# Remove additional macros from config
sed -e '\|^\# /etc/rpm/macros.asan$|,\|^\# /etc/rpm/macros.asan ends here|d' -i /usr/lib/rpm/tizen_macros

[ -d /emul/usr/bin ] && chmod a-w /emul/usr/bin/
[ -d /emul/home/abuild/rpmbuild ] && chmod a-w /emul/home/abuild/rpmbuild/BUILD/gcc-*/obj/gcc/
[ -d /emul/usr ] && find -L /emul/usr/*/gcc -name 'collect2' | xargs dirname | xargs chmod a-w

%package -n libhwasan-stub
Summary:    HWASan stub library to enable cross build
Group:      System Environment
Requires:   rpm

%description -n libhwasan-stub
HWASan stub library for cross build

%package -n hwasan-force-options
Summary:    Scripts to enable automatic package sanitization
Group:      System Environment
Requires:   gcc rpm
Requires:   libhwasan
Requires:   findutils

%description -n hwasan-force-options
Scripts for HWASan instrumentation

%post -n hwasan-force-options
# Change mode to allow all users to run gcc-force/unforce-options
chmod a+w /usr/bin
chmod a+w %{libsubdir}

/usr/bin/gcc-force-options %hwasan_force_options -fno-common
# Add ASan-related macros
cat >> /usr/lib/rpm/tizen_macros << EOF

%%hwasan_force_options %{hwasan_force_options}
%%gcc_unforce_options %%{lua: rpm.define("hwasan_unforced 1"); print("/usr/bin/gcc-unforce-options")}
%%gcc_force_options /usr/bin/gcc-force-options
%%gcc_force_default_options %%gcc_force_options %%hwasan_force_options -fno-common
%%restore_fcommon \\
  %%gcc_unforce_options \\
  %%gcc_force_options %%hwasan_force_options -fcommon
EOF

# HWASan needs a whole shadow address space
# Using ulimit can only set the value for current user so we need to set /etc/security/limits.conf directly.
[ -e /etc/security/limits.conf ] && \
    sed '/End of file/i\abuild\tsoft\tas\t-1\nabuild\thard\tas\t-1' -i /etc/security/limits.conf

%preun -n hwasan-force-options
# Restore read-only mode
chmod a-w /usr/bin
chmod a-w %{libsubdir}
/usr/bin/gcc-unforce-options
# Restore limit configurations set for HWASan
[ -e /etc/security/limits.conf ] && \
    sed '/abuild/d' -i /etc/security/limits.conf

%package -n ubsan-force-options
Summary:    Scripts to enable automatic package sanitization
Group:      System Environment
Requires:   gcc
Requires:   libubsan
Requires:   findutils

%description -n ubsan-force-options
Scripts for UBSan instrumentation

%post -n ubsan-force-options
# Change mode to allow all users to run gcc-force/unforce-options
chmod a+w /usr/bin
chmod a+w %{libsubdir}
/usr/bin/gcc-force-options %ubsan_force_options
# Add UBSan-related macros
cat >> /usr/lib/rpm/tizen_macros << EOF

%%ubsan_force_options %{ubsan_force_options}
%%gcc_unforce_options %%{lua: rpm.define("ubsan_unforced 1"); print("/usr/bin/gcc-unforce-options")}
%%gcc_force_options /usr/bin/gcc-force-options
%%gcc_force_default_options %%gcc_force_options %%ubsan_force_options
EOF

%preun -n ubsan-force-options
# Restore read-only mode
chmod a-w /usr/bin
chmod a-w %{libsubdir}
/usr/bin/gcc-unforce-options
# Remove additional macros from config
sed -e '\|^\# /etc/rpm/macros.ubsan$|,\|^\# /etc/rpm/macros.ubsan ends here|d' -i /usr/lib/rpm/tizen_macros

%package -n ubsan-build-env
Summary:    UBSan build environment
Group:      System Environment
Requires:   gcc
Requires:   libubsan rpm

%description -n ubsan-build-env
UBSan build environment support files and scripts

%post -n ubsan-build-env
cat %{_rpmconfigdir}/macros.ubsan >> %{_rpmconfigdir}/tizen_macros

%package -n lsan-force-options
Summary:    Scripts to enable automatic package sanitization
Group:      System Environment
Requires:   gcc
Requires:   liblsan
Requires:   findutils

%description -n lsan-force-options
Scripts for LSan instrumentation

%post -n lsan-force-options
# Change mode to allow all users to run gcc-force/unforce-options
chmod a+w /usr/bin
chmod a+w %{libsubdir}
/usr/bin/gcc-force-options %lsan_force_options
# Add LSan-related macros
cat >> /usr/lib/rpm/tizen_macros << EOF

%%lsan_force_options %{lsan_force_options}
%%gcc_unforce_options /usr/bin/gcc-unforce-options
%%gcc_force_options /usr/bin/gcc-force-options
%%gcc_force_default_options %%gcc_force_options %%lsan_force_options
EOF

%preun -n lsan-force-options
# Restore read-only mode
chmod a-w /usr/bin
chmod a-w %{libsubdir}
/usr/bin/gcc-unforce-options

%package -n gcov-force-options
Summary:    Scripts to enable automatic package coverage instrumentation
Group:      System Environment
Requires:   gcc
Requires:   findutils

%description -n gcov-force-options
Scripts for gcov instrumentation

%post -n gcov-force-options
# Change mode to allow all users to run gcc-force/unforce-options
chmod a+w /usr/bin
chmod a+w %{libsubdir}
/usr/bin/gcc-force-options %gcov_force_options
# Add gcov-related macros
cat >> /usr/lib/rpm/tizen_macros << EOF

%%gcov_force_options %{gcov_force_options}
%%gcc_unforce_options /usr/bin/gcc-unforce-options
%%gcc_force_options /usr/bin/gcc-force-options
%%gcc_force_default_options %%gcc_force_options %%gcov_force_options
EOF

%preun -n gcov-force-options
# Restore read-only mode
chmod a-w /usr/bin
chmod a-w %{libsubdir}
/usr/bin/gcc-unforce-options

%package -n gcov-build-env
Summary:    Gcov build environment
Group:      System Environment
Requires:   gcc
Requires:   rpm

%description -n gcov-build-env
Gcov build environment support files and scripts

%post -n gcov-build-env
cat %{_rpmconfigdir}/macros.gcov >> %{_rpmconfigdir}/tizen_macros

%package -n tsan-force-options
Summary:    Scripts to enable automatic package sanitization
Group:      System Environment
Requires:   gcc
Requires:   libtsan

%description -n tsan-force-options
Scripts for TSan instrumentation

%post -n tsan-force-options
# Change mode to allow all users to run gcc-force/unforce-options
chmod a+w /usr/bin
chmod a+w %{libsubdir}
/usr/bin/gcc-force-options %tsan_force_options
# Add TSan-related macros
cat >> /usr/lib/rpm/tizen_macros << EOF

%%tsan_force_options %{tsan_force_options}
%%gcc_unforce_options /usr/bin/gcc-unforce-options
%%gcc_force_options /usr/bin/gcc-force-options
%%gcc_force_default_options %%gcc_force_options %%tsan_force_options
EOF

%preun -n tsan-force-options
# Restore read-only mode
chmod a-w /usr/bin
chmod a-w %{libsubdir}
/usr/bin/gcc-unforce-options

%package -n tsan-runtime-env
Summary:    TSan runtime environment
Group:      Development/Libraries
Requires:   libtsan
Requires(post): smack

%description -n tsan-runtime-env
TSan runtime environment

%post -n tsan-runtime-env
echo "%{tsan_runtime_options}" > /TSAN_OPTIONS
chsmack -a "_" /TSAN_OPTIONS

%package -n tsan-build-env
Summary:    TSan build environment
Group:      Development/Libraries
Requires:   libtsan

%description -n tsan-build-env
TSan build environment

%post -n tsan-build-env
echo "%{tsan_runtime_options}" > /TSAN_OPTIONS
%ifarch aarch64
echo ":run_under_qemu=1" >> /TSAN_OPTIONS
%endif
chsmack -a "_" /TSAN_OPTIONS

%package -n asan-build-env
Summary:    Asan build environment
Group:      Development/Libraries
Requires:   libasan

%description -n asan-build-env
Asan build environment

%post -n asan-build-env
# Check if the package is already installed
[ -f /etc/ld.so.preload.orig ] && echo "The package is installed, keeping preload as is" && exit 0
[ -f /etc/ld.so.preload ] && grep -q 'libasan.so' /etc/ld.so.preload && echo "libasan.so is already preloaded" && exit 0
# Add /usr/lib/libasan.so to /etc/ld.so.preload
[ -f /etc/ld.so.preload ] && mv -v /etc/ld.so.preload /etc/ld.so.preload.orig
echo "libasan.so" > /etc/ld.so.preload
[ -f /etc/ld.so.preload.orig ] && cat /etc/ld.so.preload.orig >> /etc/ld.so.preload

[ -d /emul/usr/bin ] && chmod a+w /emul/usr/bin/
[ -d /emul/home/abuild/rpmbuild ] && chmod a+w /emul/home/abuild/rpmbuild/BUILD/gcc-*/obj/gcc/
[ -d /emul/usr ] && find -L /emul/usr/*/gcc -name 'collect2' | xargs dirname | xargs chmod a+w

# Set up reserved virtual address space for 32bit qemu-arm
%{?set_qemu_va}

%preun -n asan-build-env
# Restore /etc/ld.so.preload
[ -f /etc/ld.so.preload.orig ] && mv -v /etc/ld.so.preload.orig /etc/ld.so.preload
# And remove our libs even if there was no backup
sed -e '/libasan.so/d' -i /etc/ld.so.preload

[ -d /emul/usr/bin ] && chmod a-w /emul/usr/bin/
[ -d /emul/home/abuild/rpmbuild ] && chmod a-w /emul/home/abuild/rpmbuild/BUILD/gcc-*/obj/gcc/
[ -d /emul/usr ] && find -L /emul/usr/*/gcc -name 'collect2' | xargs dirname | xargs chmod a-w

%package -n hwasan-build-env
Summary:    HWAsan build environment
Group:      Development/Libraries

%description -n hwasan-build-env
HWAsan build environment

%package -n lsan-runtime-env
Summary:    LSan runtime environment
Group:      Development/Libraries
Requires:   liblsan
Requires(post): smack

%description -n lsan-runtime-env
LSan runtime environment

%post -n lsan-runtime-env
# Add /usr/lib64/liblsan.so to /etc/ld.so.preload
[ -f /etc/ld.so.preload ] && mv -v /etc/ld.so.preload /etc/ld.so.preload.orig
echo "%{libdir}/liblsan.so" > /etc/ld.so.preload
[ -f /etc/ld.so.preload.orig ] && cat /etc/ld.so.preload.orig >> /etc/ld.so.preload
echo "%{lsan_runtime_options}" > /LSAN_OPTIONS
chsmack -a "_" /etc/ld.so.preload /LSAN_OPTIONS /lsan.supp

%preun -n lsan-runtime-env
# Restore /etc/ld.so.preload
[ -f /etc/ld.so.preload.orig ] && mv -v /etc/ld.so.preload.orig /etc/ld.so.preload

%package -n sanitizer-devel
Summary:    Sanitizer platform-independent tools
License:       MIT
Group:      Development/Tools
BuildArch:  noarch
Requires:   binutils python
Requires(post): smack

%description -n sanitizer-devel
The package contatins platform-independent tools for sanitization:
- asan_symbolize.py: script for offline symbolization of asan logs

%package -n asan-runtime-env
Summary:    Asan runtime environment for target device
Group:      Development/Libraries
Requires:   libasan
Requires(post):   coreutils

%description -n asan-runtime-env
Asan runtime environment

%post -n asan-runtime-env
# Set up reserved virtual address space for 32bit qemu-arm
%{?set_qemu_va}

%package -n hwasan-runtime-env
Summary:    HWAsan runtime environment for target device
Group:      Development/Libraries

%description -n hwasan-runtime-env
HWAsan runtime environment

%package -n ubsan-runtime-env
Summary:    UBSan runtime environment for target device
Group:      Development/Libraries
Requires:   libubsan

%description -n ubsan-runtime-env
UBSan runtime environment

%post -n ubsan-runtime-env
echo "%{ubsan_runtime_options}" > /UBSAN_OPTIONS

%package -n sanitizer-sources
Summary:    Sanitizer family tools sources
License:       MIT
Group:      Development/Tools
BuildArch:  noarch

%description -n sanitizer-sources
Sanitizer family tools sources for external tools.

%package -n gcc-warning-build-env
Summary:    GCC warning build environment
Group:      System Environment
BuildArch:  noarch
Requires:   gcc rpm

%description -n gcc-warning-build-env
GCC warning build environment support files and scripts

%post -n gcc-warning-build-env
cat %{_rpmconfigdir}/macros.gcc_warning >> %{_rpmconfigdir}/tizen_macros

%package -n gcc-log-wrapper
Summary:    GCC wrapper for logs saving
Group:      Development/Tools
BuildArch:  noarch
Requires:   gcc

%description -n gcc-log-wrapper
GCC wrapper for logs saving

%post -n gcc-log-wrapper
# Warning: below for SVACE tool - it can't capture the data if a wrapper is symlink
PATHCC1=$(gcc -v 2>&1|grep COLLECT_LTO_WRAPPER|sed 's/COLLECT_LTO_WRAPPER=//') ; \
PATHCC1=$(dirname $PATHCC1) ; \
if [ ! -f $PATHCC1/cc1.orig ] ; then \
  mv $PATHCC1/cc1{,.orig} ; \
else \
  rm $PATHCC1/cc1 ; \
fi ; \
if [ ! -f $PATHCC1/cc1plus.orig ] ; then \
  mv $PATHCC1/cc1plus{,.orig} ; \
else \
  rm $PATHCC1/cc1plus ; \
fi ; \
ln /usr/lib/gcc-log-wrapper/cc1 $PATHCC1/cc1 ; \
ln /usr/lib/gcc-log-wrapper/cc1 $PATHCC1/cc1plus

%preun -n gcc-log-wrapper
PATHCC1=$(gcc -v 2>&1|grep COLLECT_LTO_WRAPPER|sed 's/COLLECT_LTO_WRAPPER=//') ; \
PATHCC1=$(dirname $PATHCC1) ; \
if [ -f $PATHCC1/cc1.orig ] ; then \
  rm -f $PATHCC1/cc1 ; \
  mv $PATHCC1/cc1{.orig,} ; \
fi ; \
if [ -f $PATHCC1/cc1plus.orig ] ; then \
  rm -f $PATHCC1/cc1plus ; \
  mv $PATHCC1/cc1plus{.orig,} ; \
fi

%package -n toolchain-testing-tool
Summary:    Toolchain testing script
Group:      Development/Tools
BuildArch:  noarch

%description -n toolchain-testing-tool
Toolchain testing script


%prep

%ifarch x86_64
cp %{SOURCE28} .
%endif

%build
# Generate runtime options for sanitizers
echo "%{asan_runtime_options}"   | tee ASAN_OPTIONS
echo "%{hwasan_runtime_options}" | tee HWASAN_OPTIONS
echo "%{lsan_runtime_options}"  | tee LSAN_OPTIONS
echo "%{tsan_runtime_options}"  | tee TSAN_OPTIONS
echo "%{ubsan_runtime_options}" | tee UBSAN_OPTIONS

echo "libasan.so" | tee asan-runtime-ld.so.preload

%ifarch x86_64
gcc -shared -o libhwasan.so -fPIC hwasan_stub.c
%endif

%install
mkdir -p %buildroot%_prefix
mkdir -p %buildroot%_prefix/bin
mkdir -p %{buildroot}/etc/
sed -e 's|GCC_LIBSUBDIR|%{libsubdir}|' -i %{SOURCE15}

install -m 0755 %{SOURCE15} %{buildroot}%{_prefix}/bin/
install -m 0755 %{SOURCE16} %{buildroot}%{_prefix}/bin/
install -m 0755 %{SOURCE17} %{buildroot}%{_prefix}/bin/

install -m 0644 ASAN_OPTIONS %{buildroot}
install -m 0644 asan-runtime-ld.so.preload %{buildroot}/etc/ld.so.preload

%ifarch x86_64
mkdir -p %{buildroot}/%{_libdir}
install -m 755 libhwasan.so %{buildroot}/%{_libdir}
%endif

%ifarch %hwasan_arch
install -m 0644 HWASAN_OPTIONS %{buildroot}
%endif

%ifarch %lsan_arch
install -m 0644 LSAN_OPTIONS %{buildroot}
install -m 0644 %{SOURCE21} %{buildroot}
%endif

%ifarch %tsan_arch
install -m 0644 TSAN_OPTIONS %{buildroot}
%endif

mkdir -p %{buildroot}/%{_rpmconfigdir}/tizen/
install -m 0644 UBSAN_OPTIONS %{buildroot}/
install -m 0644 %{SOURCE19} %{buildroot}/%{_rpmconfigdir}/
install -m 0644 %{SOURCE22} %{buildroot}/%{_rpmconfigdir}/
install -m 0755 %{SOURCE20} %{buildroot}/%{_rpmconfigdir}/tizen/

mkdir -p %{buildroot}/usr/lib/gcc-log-wrapper
install -m 0755 %{SOURCE23} %{buildroot}/usr/lib/gcc-log-wrapper/
install -m 0644 %{SOURCE24} %{buildroot}/%{_rpmconfigdir}/
install -m 0755 %{SOURCE25} %{buildroot}/%{_rpmconfigdir}/tizen/
install -m 0644 %{SOURCE26} %{buildroot}/%{_rpmconfigdir}/
install -m 0755 %{SOURCE27} %{buildroot}/%{_rpmconfigdir}/tizen/
install -m 0755 %{SOURCE29} %{buildroot}/%{_rpmconfigdir}/tizen/

%files
#%manifest gcc-contrib.manifest

%files -n asan-force-options
%defattr(-,root,root,-)
%{_prefix}/bin/gcc-force-options
%{_prefix}/bin/gcc-unforce-options
%{_rpmconfigdir}/macros.asan

%ifarch %hwasan_arch
%files -n hwasan-force-options
%defattr(-,root,root,-)
%{_prefix}/bin/gcc-force-options
%{_prefix}/bin/gcc-unforce-options
%endif

%files -n ubsan-force-options
%defattr(-,root,root,-)
%{_prefix}/bin/gcc-force-options
%{_prefix}/bin/gcc-unforce-options

%files -n gcov-force-options
%defattr(-,root,root,-)
%{_prefix}/bin/gcc-force-options
%{_prefix}/bin/gcc-unforce-options

%ifarch %lsan_arch
%files -n lsan-force-options
#%manifest gcc-contrib.manifest
%defattr(-,root,root,-)
%{_prefix}/bin/gcc-force-options
%{_prefix}/bin/gcc-unforce-options
%endif

%ifarch %tsan_arch
%files -n tsan-force-options
%defattr(-,root,root,-)
%{_prefix}/bin/gcc-force-options
%{_prefix}/bin/gcc-unforce-options
%endif

%files -n asan-build-env
%defattr(-,root,root,-)
/ASAN_OPTIONS

%files -n asan-runtime-env
%defattr(-,root,root,-)
/ASAN_OPTIONS
/etc/ld.so.preload

%ifarch %hwasan_arch
%files -n hwasan-build-env
%defattr(-,root,root,-)
/HWASAN_OPTIONS

%files -n hwasan-runtime-env
%defattr(-,root,root,-)
/HWASAN_OPTIONS
%endif

%ifarch x86_64
%files -n libhwasan-stub
%defattr(-,root,root,-)
%{libdir}/libhwasan.so
%endif

%ifarch %lsan_arch
%files -n lsan-runtime-env
%defattr(-,root,root,-)
/LSAN_OPTIONS
/lsan.supp
%endif

%ifarch %tsan_arch
%files -n tsan-runtime-env
%defattr(-,root,root,-)
/TSAN_OPTIONS

%files -n tsan-build-env
%defattr(-,root,root,-)
/TSAN_OPTIONS
%endif

%files -n gcov-build-env
%defattr(-,root,root,-)
%{_rpmconfigdir}/macros.gcov
%{_rpmconfigdir}/tizen/extract-gcov-info

%ifarch %ubsan_arch
%files -n ubsan-build-env
%defattr(-,root,root,-)
/UBSAN_OPTIONS
%{_rpmconfigdir}/macros.ubsan
%{_rpmconfigdir}/tizen/extract-ubsan-logs

%files -n ubsan-runtime-env
%defattr(-,root,root,-)
%endif

%files -n sanitizer-devel
%defattr(-,root,root,-)
%{_prefix}/bin/asan_symbolize.py

%files -n gcc-warning-build-env
%defattr(-,root,root,-)
%{_rpmconfigdir}/macros.gcc_warning
%{_rpmconfigdir}/tizen/extract-gcc-warning-logs

%files -n gcc-log-wrapper
%defattr(-,root,root,-)
/usr/lib/gcc-log-wrapper/cc1

%files -n toolchain-testing-tool
%defattr(-,root,root,-)
%{_rpmconfigdir}/tizen/run_toolchain_tests.sh

%changelog
