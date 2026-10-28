Name:           valgrind
Url:            http://valgrind.org/
Summary:        Memory Management Debugger
License:        GPL-2.0+
Group:          Development/Tools/Debuggers
Version:        3.25.0
Release:        0
Source0:        %{name}-%{version}.tar.bz2
Source1001: 	valgrind.manifest
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  libxslt
BuildRequires:  pkgconfig

%description
Valgrind checks all memory operations in an application, like read,
write, malloc, new, free, and delete. Valgrind can find uses of
uninitialized memory, access to already freed memory, overflows,
illegal stack operations, memory leaks, and any illegal
new/malloc/free/delete commands. Another program in the package is
"cachegrind," a profiler based on the valgrind engine.

To use valgrind you should compile your application with "-g -O0"
compiler options. Afterwards you can use it with:

valgrind --tool=memcheck --sloppy-malloc=yes --leak-check=yes
--db-attach=yes my_application, for example.

More valgrind options can be listed via "valgrind --help". A
debugged application runs slower and needs much more memory, but
is usually still usable. Valgrind is still in development, but it
has been successfully used to optimize several KDE applications.


%package devel
Summary:        Memory Management Debugger
Group:          Development/Tools/Debuggers
Requires:       %name = %version

%description devel
Valgrind checks all memory operations in an application, like read,
write, malloc, new, free, and delete. Valgrind can find uses of
uninitialized memory, access to already freed memory, overflows,
illegal stack operations, memory leaks, and any illegal
new/malloc/free/delete commands. Another program in the package is
"cachegrind," a profiler based on the valgrind engine.

To use valgrind you should compile your application with "-g -O0"
compiler options. Afterwards you can use it with:

valgrind --tool=memcheck --sloppy-malloc=yes --leak-check=yes
--db-attach=yes my_application, for example.

More valgrind options can be listed via "valgrind --help". A
debugged application runs slower and needs much more memory, but
is usually still usable. Valgrind is still in development, but it
has been successfully used to optimize several KDE applications.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%{?asan:/usr/bin/gcc-unforce-options}
%{?ubsan:/usr/bin/gcc-unforce-options}
%ifarch %arm
# Valgrind doesn't support compiling for Thumb yet. Remove when it gets
# native thumb support.
RPM_OPT_FLAGS="$(echo $RPM_OPT_FLAGS | sed 's/-mthumb //g')"
RPM_OPT_FLAGS="$(echo $RPM_OPT_FLAGS | sed 's/-Wa,-mimplicit-it=thumb //g')"
%endif

# gcc global option "-fstack_protector" cause error
RPM_OPT_FLAGS="$(echo $RPM_OPT_FLAGS | sed 's/-fstack-protector-strong //g')"
RPM_OPT_FLAGS="$(echo $RPM_OPT_FLAGS | sed 's/-fstack-protector //g')"
RPM_OPT_FLAGS="$(echo $RPM_OPT_FLAGS | sed 's/-flto-partition=none //g')"
RPM_OPT_FLAGS="$(echo $RPM_OPT_FLAGS | sed 's/-flto //g')"

# not a good idea to build valgrind with fortify, as it does not link glibc
RPM_OPT_FLAGS="$(echo $RPM_OPT_FLAGS | sed 's/-Wp,-D_FORTIFY_SOURCE=2 //g')"
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"

%autogen

%ifarch x86_64
%configure --enable-only64bit
%else
%configure
%endif

make %{?_smp_mflags}


%install
%make_install

# extra documentation available online
rm -rf %{buildroot}%{_datadir}/doc/valgrind

%docs_package

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/*
%dir %{_libexecdir}/valgrind
%ifarch x86_64
%{_libexecdir}/valgrind/*-amd64-linux
%endif
%ifarch %ix86
%{_libexecdir}/valgrind/*-x86-linux
%endif
%ifarch %arm
%{_libexecdir}/valgrind/*-arm-linux
%endif
%ifarch aarch64
%{_libexecdir}/valgrind/*-arm64-linux
%endif
%ifarch riscv64
%{_libexecdir}/valgrind/*-riscv64-linux
%endif

%{_libexecdir}/valgrind/*-linux.so
%{_libexecdir}/valgrind/*.supp
%{_libexecdir}/valgrind/32bit-core-valgrind-s*.xml
%{_libexecdir}/valgrind/32bit-core.xml
%{_libexecdir}/valgrind/32bit-linux-valgrind-s*.xml
%{_libexecdir}/valgrind/32bit-linux.xml
%{_libexecdir}/valgrind/32bit-sse-valgrind-s*.xml
%{_libexecdir}/valgrind/32bit-sse.xml
%{_libexecdir}/valgrind/64bit-avx-valgrind-s1.xml
%{_libexecdir}/valgrind/64bit-avx-valgrind-s2.xml
%{_libexecdir}/valgrind/64bit-avx.xml
%{_libexecdir}/valgrind/64bit-core-valgrind-s*.xml
%{_libexecdir}/valgrind/64bit-core.xml
%{_libexecdir}/valgrind/64bit-linux-valgrind-s*.xml
%{_libexecdir}/valgrind/64bit-linux.xml
%{_libexecdir}/valgrind/64bit-sse-valgrind-s*.xml
%{_libexecdir}/valgrind/64bit-sse.xml
%{_libexecdir}/valgrind/amd64-avx-coresse-valgrind.xml
%{_libexecdir}/valgrind/amd64-avx-coresse.xml
%{_libexecdir}/valgrind/amd64-avx-linux-valgrind.xml
%{_libexecdir}/valgrind/amd64-avx-linux.xml
%{_libexecdir}/valgrind/amd64-coresse-valgrind.xml
%{_libexecdir}/valgrind/amd64-linux-valgrind.xml
%{_libexecdir}/valgrind/arm-core-valgrind-s*.xml
%{_libexecdir}/valgrind/arm-core.xml
%{_libexecdir}/valgrind/arm-vfpv3-valgrind-s*.xml
%{_libexecdir}/valgrind/arm-vfpv3.xml
%{_libexecdir}/valgrind/arm-with-vfpv3-valgrind.xml
%{_libexecdir}/valgrind/arm-with-vfpv3.xml
%{_libexecdir}/valgrind/i386-coresse-valgrind.xml
%{_libexecdir}/valgrind/i386-linux-valgrind.xml
%{_libexecdir}/valgrind/mips-cp0-valgrind-s1.xml
%{_libexecdir}/valgrind/mips-cp0-valgrind-s2.xml
%{_libexecdir}/valgrind/mips-cp0.xml
%{_libexecdir}/valgrind/mips-cpu-valgrind-s1.xml
%{_libexecdir}/valgrind/mips-cpu-valgrind-s2.xml
%{_libexecdir}/valgrind/mips-cpu.xml
%{_libexecdir}/valgrind/mips-fpu-valgrind-s1.xml
%{_libexecdir}/valgrind/mips-fpu-valgrind-s2.xml
%{_libexecdir}/valgrind/mips-fpu.xml
%{_libexecdir}/valgrind/mips-linux-valgrind.xml
%{_libexecdir}/valgrind/mips-linux.xml
%{_libexecdir}/valgrind/mips64-cp0-valgrind-s1.xml
%{_libexecdir}/valgrind/mips64-cp0-valgrind-s2.xml
%{_libexecdir}/valgrind/mips64-cp0.xml
%{_libexecdir}/valgrind/mips64-cpu-valgrind-s1.xml
%{_libexecdir}/valgrind/mips64-cpu-valgrind-s2.xml
%{_libexecdir}/valgrind/mips64-cpu.xml
%{_libexecdir}/valgrind/mips64-fpu-valgrind-s1.xml
%{_libexecdir}/valgrind/mips64-fpu-valgrind-s2.xml
%{_libexecdir}/valgrind/mips64-fpu.xml
%{_libexecdir}/valgrind/mips64-linux-valgrind.xml
%{_libexecdir}/valgrind/mips64-linux.xml
%{_libexecdir}/valgrind/power-altivec-valgrind-s*.xml
%{_libexecdir}/valgrind/power-altivec.xml
%{_libexecdir}/valgrind/power-core-valgrind-s1.xml
%{_libexecdir}/valgrind/power-core-valgrind-s2.xml
%{_libexecdir}/valgrind/power-core.xml
%{_libexecdir}/valgrind/power-fpu-valgrind-s*.xml
%{_libexecdir}/valgrind/power-fpu.xml
%{_libexecdir}/valgrind/power-linux-valgrind-s*.xml
%{_libexecdir}/valgrind/power-linux.xml
%{_libexecdir}/valgrind/power-vsx*.xml
%{_libexecdir}/valgrind/power64-core-valgrind-s*.xml
%{_libexecdir}/valgrind/power64-core2-valgrind-s*.xml
%{_libexecdir}/valgrind/power64-core.xml
%{_libexecdir}/valgrind/power64-linux-valgrind-s*.xml
%{_libexecdir}/valgrind/power64-linux.xml
%{_libexecdir}/valgrind/powerpc-altivec32l-valgrind.xml
%{_libexecdir}/valgrind/powerpc-altivec32l.xml
%{_libexecdir}/valgrind/powerpc-altivec64l-valgrind.xml
%{_libexecdir}/valgrind/powerpc-altivec64l.xml
%{_libexecdir}/valgrind/s390-acr-valgrind-s1.xml
%{_libexecdir}/valgrind/s390-acr-valgrind-s2.xml
%{_libexecdir}/valgrind/s390-acr.xml
%{_libexecdir}/valgrind/s390-fpr-valgrind-s1.xml
%{_libexecdir}/valgrind/s390-fpr-valgrind-s2.xml
%{_libexecdir}/valgrind/s390-fpr.xml
%{_libexecdir}/valgrind/s390x-core64-valgrind-s1.xml
%{_libexecdir}/valgrind/s390x-core64-valgrind-s2.xml
%{_libexecdir}/valgrind/s390x-core64.xml
%{_libexecdir}/valgrind/s390x-generic-valgrind.xml
%{_libexecdir}/valgrind/s390x-generic.xml
%{_libexecdir}/valgrind/s390x-linux64-valgrind-s1.xml
%{_libexecdir}/valgrind/s390x-linux64-valgrind-s2.xml
%{_libexecdir}/valgrind/s390x-linux64.xml
%{_libexecdir}/valgrind/s390-vx-valgrind-s1.xml
%{_libexecdir}/valgrind/s390-vx-valgrind-s2.xml
%{_libexecdir}/valgrind/s390-vx.xml
%{_libexecdir}/valgrind/s390x-vx-linux-valgrind.xml
%{_libexecdir}/valgrind/s390x-vx-linux.xml
%{_libexecdir}/valgrind/valgrind-monitor-def.py
%{_libexecdir}/valgrind/valgrind-monitor.py
%{_libexecdir}/valgrind/riscv64-cpu-valgrind-s1.xml
%{_libexecdir}/valgrind/riscv64-cpu-valgrind-s2.xml
%{_libexecdir}/valgrind/riscv64-cpu.xml
%{_libexecdir}/valgrind/riscv64-fpu-valgrind-s1.xml
%{_libexecdir}/valgrind/riscv64-fpu-valgrind-s2.xml
%{_libexecdir}/valgrind/riscv64-fpu.xml
%{_libexecdir}/valgrind/riscv64-linux-valgrind.xml
%{_libexecdir}/valgrind/riscv64-linux.xml
%exclude %{_libexecdir}/debug/.build-id
%exclude /usr/libexec/valgrind/dh_view.*

%files devel
%manifest %{name}.manifest
%{_includedir}/valgrind
%{_libdir}/pkgconfig/valgrind.pc
