%define cross riscv64
%define riscv64 1

#
# spec file for package gcc
#
# Copyright (c) 2009 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2015-2020 Tizen
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.tizen.org/
#
# we use %%{?macro: ... } as it is more compact

# Don't build package with tests when cross-compiling
%{?cross:%undefine build_tests}

# Don't use bootstrap with qemu-accel.
# When start "stage2" build with qemu-accel on system,
# acceleration collect2 cannot use liblto_plugin.so of "stage1".
# Also compiler is not required to support bootstrap for cross-compile
%{?cross:%undefine bootstrap}

# Always build gcc with gcc compiler
%define _toolchain_override gcc

# Bootstrap build constrains for ASan config
%if 0%{?asanbootstrap}
  %ifarch %arm aarch64 # or #if 0#{?qemu_user_space_build}
    %{error:"'asanbootstrap' supposed to be used with i586/x86_64 arch"}
    # The #error macro primitive cannot stop the build because macros are context
    # free, lazily expanded whereever they are needed, not only during build.
    # Use non-existing define for now to abort the build.
    %abort_build
  %endif
  # We'll get 2 libasan runtime conflict: preloaded one and another from build dir.
  %if 0%{?asan}
    %{error:"'asanbootstrap' could not be used with sanitized environment."}
    %{error:"Use 'asanbootstrap' without defined 'asan'"}
    %abort_build
  %endif
%endif

%define quadmath_arch %ix86 x86_64 ia64
%define tsan_arch x86_64 aarch64 riscv64
%define asan_arch x86_64 %ix86 ppc ppc64 %sparc %arm aarch64 riscv64
%define itm_arch x86_64 %ix86 %arm ppc ppc64 ppc64le s390 s390x %sparc aarch64 riscv64
%define atomic_arch x86_64 %ix86 %arm aarch64 ppc ppc64 ppc64le s390 s390x %sparc m68k riscv64
%define lsan_arch x86_64 aarch64 %arm riscv64
%define hwasan_arch aarch64 x86_64
%define ubsan_arch x86_64 %ix86 ppc ppc64 %arm aarch64 riscv64

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

%define target_cpu %{?cross}%{!?cross:%{ARCH}}
%define target_abi %{?cross:%{?armv7l:eabi}%{?armv7hl:eabihf}}%{!?cross:%{?ABI}}
%define target_arch %{target_cpu}-tizen-linux-gnu%{?target_abi}

%define libdir %{!?cross:%{_libdir}}%{?cross:%{_prefix}/lib%{?aarch64:64}%{?riscv64:64}}
%define libsubdir %{libdir}/gcc/%{target_arch}/%{version}

Name:          gcc%{?cross:-%{cross}}
VCS:           platform/upstream/gcc#49c5060508ce8a6ed6beca375233688a6bdd9140
# With generated files in src we could drop the following
BuildRequires: bison
BuildRequires: flex
BuildRequires: gettext-devel
BuildRequires: makeinfo
## until here, but at least renaming and patching info files breaks this
BuildRequires: gcc-c++
BuildRequires: zlib-devel
BuildRequires: xz-devel
BuildRequires: perl
%{?cross:BuildRequires: binutils-%{cross}}
%if 0%{?build_tests}
BuildRequires: toolchain-testing-tool
%endif
URL:           http://gcc.gnu.org/
Version:       14.2.0
Release:       1.4
Source:        gcc-%{version}.tar.bz2
Source10:      gmp-6.2.1.tar.bz2
Source11:      mpfr-4.1.0.tar.bz2
Source12:      mpc-1.2.1.tar.gz
Source13:      isl-0.24.tar.bz2
Source20:      gcc.manifest
Group:         Development/Building
Summary:       The GNU C Compiler and Support Files
License:       GPL-3.0+
%{?cross:ExcludeArch: %{cross}}
%description
Core package for the GNU Compiler Collection, including the C language
frontend.

%package c++
Summary:       The GNU C++ Compiler
License:       GPL-3.0+
Group:         Development/Languages
%description c++
This package contains the GNU compiler for C++.

%package -n libstdc++
Summary:       The standard C++ shared library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libstdc++
The standard C++ library, needed for dynamically linked C++ programs.
%post -n libstdc++ -p /sbin/ldconfig
%postun -n libstdc++ -p /sbin/ldconfig

%package -n libstdc++-devel
Summary:       Include Files and Libraries mandatory for Development
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libstdc++-devel
This package contains all the headers and libraries of the standard C++
library. It is needed for compiling C++ code.

%package -n libgcc
Summary:       C compiler runtime library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libgcc
Libgcc is needed for dynamically linked C programs.
%post -n libgcc -p /sbin/ldconfig
%postun -n libgcc -p /sbin/ldconfig

%package -n libgomp
Summary:       The GNU compiler collection OpenMP runtime library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libgomp
This is the OpenMP runtime library needed by OpenMP enabled programs
that were built with the -fopenmp compiler option and by programs that
were auto-parallelized via the -ftree-parallelize-loops compiler
option.
%post -n libgomp -p /sbin/ldconfig
%postun -n libgomp -p /sbin/ldconfig

%package -n libcc1
Summary:       GNU C Compiler plugin for GDB
License:       GPL-3.0-with-GCC-exception
Group:         Development/Building
%description -n libcc1
The GCC plugin for GDB
%post -n libcc1 -p /sbin/ldconfig
%postun -n libcc1 -p /sbin/ldconfig

%package -n cpp
Summary:       The GCC Preprocessor
License:       GPL-3.0+
Group:         Development/Languages
%description -n cpp
This Package contains just the preprocessor that is used by the X11
packages.

%package fortran
Summary:       The GNU Fortran Compiler and Support Files
License:       GPL-3.0+
Group:         Development/Languages
%description fortran
This is the Fortran compiler of the GNU Compiler Collection (GCC).

%package -n libgfortran
Summary:       The GNU Fortran Compiler Runtime Library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Languages
%description -n libgfortran
The runtime library needed to run programs compiled with the Fortran compiler
of the GNU Compiler Collection (GCC).
%post -n libgfortran -p /sbin/ldconfig
%postun -n libgfortran -p /sbin/ldconfig

%package -n libquadmath
Summary:       The GNU Fortran Compiler Quadmath Runtime Library
License:       LGPL-2.1
Group:         Development/Languages
%description -n libquadmath
The runtime library needed to run programs compiled with the Fortran compiler
of the GNU Compiler Collection (GCC) and quadruple precision floating point
operations.
%post -n libquadmath -p /sbin/ldconfig
%postun -n libquadmath -p /sbin/ldconfig

%package -n libitm
Summary:       The GNU Compiler Transactional Memory Runtime Library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Languages
%description -n libitm
The runtime library needed to run programs compiled with the
-fgnu-tm option of the GNU Compiler Collection (GCC).
%post -n libitm -p /sbin/ldconfig
%postun -n libitm -p /sbin/ldconfig

%package -n libasan
Summary:       The GNU Compiler Address Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libasan
The runtime library needed to run programs compiled with the
-fsanitize=address option of the GNU Compiler Collection (GCC).
%post -n libasan -p /sbin/ldconfig
%postun -n libasan -p /sbin/ldconfig

%package -n libhwasan
Summary:       The GNU Compiler Hardware-assisted Address Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libhwasan
The runtime library needed to run programs compiled with the
-fsanitize=hwaddress option of the GNU Compiler Collection (GCC).
%post -n libhwasan -p /sbin/ldconfig
%postun -n libhwasan -p /sbin/ldconfig

%package -n libtsan
Summary:       The GNU Compiler Thread Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libtsan
The runtime library needed to run programs compiled with the
-fsanitize=thread option of the GNU Compiler Collection (GCC).
%post -n libtsan -p /sbin/ldconfig
%postun -n libtsan -p /sbin/ldconfig

%package -n libatomic
Summary:       The GNU Compiler Atomic Operations Runtime Library
License:       GPL-3.0-with-GCC-exception
Group:         Development/Languages
%description -n libatomic
The runtime library for atomic operations of the GNU Compiler Collection (GCC).
%post -n libatomic -p /sbin/ldconfig
%postun -n libatomic -p /sbin/ldconfig

%package -n liblsan
Summary:       The GNU Compiler Leak Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n liblsan
The runtime library needed to run programs compiled with the
-fsanitize=leak option of the GNU Compiler Collection (GCC).
%post -n liblsan -p /sbin/ldconfig
%postun -n liblsan -p /sbin/ldconfig

%package -n libubsan
Summary:       The GNU Compiler Undefined Sanitizer Runtime Library
License:       MIT
Group:         Development/Languages
%description -n libubsan
The runtime library needed to run programs compiled with the
-fsanitize=undefined option of the GNU Compiler Collection (GCC).
%post -n libubsan -p /sbin/ldconfig
%postun -n libubsan -p /sbin/ldconfig

%package plugin-devel
Summary:       GNU GCC Plugin development files
License:       GPL-3.0+
Group:         Development/Languages
%description plugin-devel
This package contains GCC Plugin development files needed for compiler
plugins build.

%package -n sanitizer-sources
Summary:    Sanitizer family tools sources
License:       MIT
Group:      Development/Tools
BuildArch:  noarch

%description -n sanitizer-sources
Sanitizer family tools sources for external tools.

%{!?cross:
%package devel-static
Summary:       GNU GCC static libraries
License:       GPL-3.0+
Group:         Development/Languages
%description devel-static
This package contains static libraries from GCC
}

%{?build_tests:
%package tests
Summary:       GCC and libraries testsuites
License:       GPL-3.0+
Group:         Development/Languages
Requires:      %{name} = %{version}-%{release}
Requires:      dejagnu
Requires:      bison
Requires:      flex
Requires:      gettext-devel
Requires:      makeinfo
Requires:      gcc-c++
Requires:      zlib-devel
Requires:      xz-devel
Requires:      perl
AutoReqProv:   off
%description tests
This package contains sources and build output gcc and libraries
for running testsuites.

%post tests
rm -rf %{_builddir}/%{name}-%{version}
mkdir %{_builddir}/%{name}-%{version}
xz -d < %{_builddir}/%{name}-%{version}.tar.xz | tar x -C %{_builddir}
rm %{_builddir}/%{name}-%{version}.tar.xz

%preun tests
rm -rf %{_builddir}/%{name}-%{version}
}

%prep
%setup -q -n gcc-%{version}
cp %{SOURCE20} .

tar xf %{SOURCE10}
ln -sf gmp-6.2.1 gmp
tar xf %{SOURCE11}
ln -sf mpfr-4.1.0 mpfr
tar xf %{SOURCE12}
ln -sf mpc-1.2.1 mpc
tar xf %{SOURCE13}
ln -sf isl-0.24 isl
(cd isl && autoreconf -vfi)

%global gcc_datestamp `sed -e 's/^.*-//g' %{_builddir}/gcc-%{version}/gcc/DATESTAMP`

%build
%{?asan:
%gcc_unforce_options
%ifarch armv7l
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -marm -Wa,-mimplicit-it=arm -fasynchronous-unwind-tables"
%endif
}

RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g' -e 's/-Wmissing-format-attribute//g' -e 's/-ffortify=.//g' -e 's/-Wall//g' -e 's/-m32//g' -e 's/-m64//g' -e 's/-fexceptions//' -e 's/\([[:space:]]\+.*-D_FORTIFY_SOURCE=\)[[:alnum:]]\+/\10/g'
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D__USE_FORTIFY_LEVEL=0"`
RPM_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | sed 's/-fstack-protector-strong//')
RPM_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | sed 's/-fstack-protector//')

%{?cross:
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-m\(arch\|tune\|cpu\)=[^ ]*//g'`
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-m\(sse\|fpmath\)[^ ]*//g'`
}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/  */ /g'`

# -Wall is stripped off now, so -Wformat will not turn on implicitly for
# "-Wformat-.." option group, causing additional build warnings and testsuite
# FAIL ("test for excess errors" type).
# Insert "-Wformat" if we find "-Wformat-..."
if [ ! -z "$(echo $RPM_OPT_FLAGS | grep -o "\B\-Wformat\-")" ]; then
    if [ -z "$(echo $RPM_OPT_FLAGS | grep -Po "\B\-Wformat(\s|\Z)")" ]; then
        RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS | sed -e "s/-Wformat-/-Wformat -Wformat-/")
    fi
fi

%{?bootstrap: RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS -gtoggle) }
%{?asan: RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS -DASAN_INIT_FIRST) }
%{?asan_shadow_scale: RPM_OPT_FLAGS=$(echo $RPM_OPT_FLAGS -Wp,-DASAN_SHADOW_SCALE=%{asan_shadow_scale})}

%ifarch %arm
## Support DA build with armv8 cpu in 32bit mode: prevent Werror on sqrt function
# Extract current march
cur_arch=$(echo ${RPM_OPT_FLAGS} | sed -e 's/.*-march=\([^[:space:]]\+\).*/\1/')
# And apply it to libatomic to prevent conflict
(echo ${RPM_OPT_FLAGS} | grep '\-march=armv8') && \
    sed -e "/@ARCH_ARM_LINUX_TRUE@@HAVE_IFUNC_TRUE@IFUNC_OPTIONS/s/-march=[^[:space:]]\+/-march=${cur_arch}/" -i libatomic/Makefile.in
%endif

# Tell libsanitizer to work with Tizen
# libsanitizer uses it to disable a dozen of sanitizer interceptors
%{!?cross: \
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -DSANITIZER_TIZEN=1"
}

rm -rf obj
mkdir obj
cd obj

CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" XCFLAGS="$RPM_OPT_FLAGS" \
TCFLAGS="$RPM_OPT_FLAGS" GCJFLAGS="$RPM_OPT_FLAGS" \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--libdir=%{libdir} \
	--libexecdir=%{libdir} \
	--enable-languages=c,c++,fortran \
	--enable-checking=release \
	--disable-libssp \
	%{!?bootstrap: --disable-bootstrap} \
	--disable-libvtv \
	--enable-plugin \
	--disable-libgcj \
	--with-slibdir=%{libdir} \
	--with-system-zlib \
	--with-sysroot=/ \
	--enable-__cxa_atexit \
	--enable-libstdcxx-allocator=new \
	--enable-version-specific-runtime-libs \
	--enable-linker-build-id \
	--without-system-libunwind \
	--enable-threads=posix \
	--disable-multilib \
	--disable-cet \
	--enable-lto \
%{!?cross: \
	--enable-libcc1 \
	--enable-libgfortran \
	%{?asanbootstrap:--enable-bootstrap --with-build-config=bootstrap-asan} \
%ifarch armv7l
	--with-arch=armv7-a \
	--with-tune=cortex-a8 \
	--disable-sjlj-exceptions \
%endif
%ifarch armv7hl
	--with-arch=armv7-a+fp \
	--with-tune=cortex-a8 \
	--with-fpu=neon \
	--disable-sjlj-exceptions \
	--with-float=hard \
%endif
%ifarch aarch64
	--with-arch=armv8-a \
	--disable-sjlj-exceptions \
%endif
%ifarch riscv64
	--with-arch=rv64gc \
	--with-abi=lp64d \
%endif
%ifarch %ix86
	--with-arch-32=i586 \
	--with-tune=generic \
	--disable-libmpx \
%endif
%ifarch x86_64
	--with-tune=generic \
	--disable-libmpx \
%endif
} \
%{?cross: \
%{?armv7l: \
	--with-arch=armv7-a \
	--with-tune=cortex-a8 \
	--disable-sjlj-exceptions \
} \
%{?armv7hl: \
	--with-arch=armv7-a+fp \
	--with-tune=cortex-a8 \
	--with-fpu=neon \
	--disable-sjlj-exceptions \
	--with-float=hard \
} \
%{?aarch64: \
	--with-arch=armv8-a \
	--disable-sjlj-exceptions \
} \
%{?riscv64: \
	--with-arch=rv64gc \
	--with-abi=lp64d \
} \
	--disable-libcc1 \
	--disable-libgcc \
	--disable-libgfortran \
	--disable-libquadmath \
	--disable-libgomp \
	--disable-libatomic \
	--disable-libstdc++-v3 \
	--disable-libsanitizer \
	--disable-libitm \
} \
	--with-bugurl="http://bugs.tizen.org/" \
	--with-pkgversion="Tizen GCC %{version} %{gcc_datestamp} %{release}" \
	--target=%{target_arch} \
	--host=%{_host} \
	--build=%{_build}

%{?!cross:
  # During native compiler build with qemu-accel enabled we have to provide
  # path to accelerated lto_plugin.so to prevent
  #    error loading plugin: /home/abuild/rpmbuild/BUILD/gcc-12.2.0/obj/./gcc/liblto_plugin.so: wrong ELF class: ELFCLASS32
  # So we have to update:
  # - CC_FOR_TARGET
  # - GCC_FOR_TARGET
  # - CXX_FOR_TARGET
  # - RAW_CXX_FOR_TARGET
  # And provide path to liblto_plugin inside /emul via -B option
  # Changing configure.ac and adding a dependency from qemu-accel there is not
  # reasonable, so here we patch a Makefile after configure is competed

  [ -e '/emul' ] && \
      sed -e '/^\(G\?CC_FOR_TARGET\)=\|^\(\(RAW_\)\?CXX_FOR_TARGET\)=/s#\(xg\(cc\|++\)\)#\1 -B/emul%{libsubdir}/#' -i Makefile
}

make BOOT_CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags} %{?cross:all-host}

%install
cd obj

%{?build_tests:
	mkdir -p %{buildroot}/%{_builddir}

	install -m 0755 -t . %{_rpmconfigdir}/tizen/run_toolchain_tests.sh
	sed "s/^PROJECT_NAME=@PROJECT_NAME@$/PROJECT_NAME=%{name}/g" -i run_toolchain_tests.sh
	sed "s/^VERSION=@VERSION@$/VERSION=%{version}/g" -i run_toolchain_tests.sh
	sed "s/^RELEASE=@RELEASE@$/RELEASE=%{release}/g" -i run_toolchain_tests.sh
	sed "s/^ARCH=@ARCH@$/ARCH=%{_arch}/g" -i run_toolchain_tests.sh

	tar c -C %{_builddir} %{name}-%{version} | xz -3 > \
		%{buildroot}/%{_builddir}/%{name}-%{version}.tar.xz
}

%{!?cross:
	mkdir -p %{buildroot}/src
	tar c ../libsanitizer | xz -3 > %{buildroot}/src/libsanitizer.tar.xz
}

make install%{?cross:-host} DESTDIR=$RPM_BUILD_ROOT

%{remove_docs}
rm -rf %{buildroot}/%{_datadir}/locale

#remove everything we don't need
rm -rf %{buildroot}/%{libsubdir}/install-tools
find %{buildroot}/ -name "*.la" -delete

%{!?cross:
ln -s gcc %{buildroot}%{_bindir}/cc
mv %{buildroot}%{libsubdir}/libstdc++.so*-gdb.py %{buildroot}%{_datadir}/gcc-%{version}/python/libstdcxx/

# expose plugins for ar (required for lto builds)
mkdir -p %{buildroot}%{_prefix}/lib/bfd-plugins
ln -sf %{libsubdir}/liblto_plugin.so %{buildroot}%{_prefix}/lib/bfd-plugins/liblto_plugin.so

# legacy preprocessor
mkdir -p %{buildroot}/lib
ln -s %{_bindir}/cpp %{buildroot}/lib/cpp

# move libraries to libdir
for lib in asan hwasan atomic gfortran gomp cc1 itm lsan quadmath stdc++ supc++ tsan ubsan
do
  [ -e %{buildroot}%{libsubdir}/lib$lib.a ] && mv %{buildroot}%{libsubdir}/lib$lib.a %{buildroot}%{libdir}/
  [ -e %{buildroot}%{libsubdir}/lib$lib.so ] && mv %{buildroot}%{libsubdir}/lib$lib.so* %{buildroot}%{libdir}/
done
}

%{?cross:
rm -rf %{buildroot}/%{libsubdir}/include-fixed
rm -rf %{buildroot}/%{libsubdir}/include
}

%files
%manifest gcc.manifest
%defattr(-,root,root)
%{?cross:
%{_bindir}/*
%{libsubdir}/*
}
%{!?cross:
%{_bindir}/gcc
%{_bindir}/cc
%{_bindir}/gcov
%{_bindir}/gcov-dump
%{_bindir}/gcov-tool
%{_bindir}/gcc-ar
%{_bindir}/gcc-nm
%{_bindir}/gcc-ranlib
%{_bindir}/lto-dump
%{_bindir}/%{target_arch}-gcc
%{_bindir}/%{target_arch}-gcc-%{version}
%{_bindir}/%{target_arch}-gcc-ar
%{_bindir}/%{target_arch}-gcc-nm
%{_bindir}/%{target_arch}-gcc-ranlib
%{libsubdir}/collect2
%{libsubdir}/lto1
%{libsubdir}/lto-wrapper
%{libsubdir}/liblto_plugin.so*
%{_prefix}/lib/bfd-plugins/liblto_plugin.so
%{libsubdir}/g++-mapper-server
%{libsubdir}/include-fixed/*
%{libsubdir}/include/*.h
%{libsubdir}/*.so
%{libsubdir}/*.o
%{libsubdir}/*.spec
%{libdir}/*.so
%{libsubdir}/include/sanitizer/*
%ifarch %asan_arch
%exclude %{libdir}/libasan.so
%endif
%ifarch %hwasan_arch
%exclude %{libdir}/libhwasan.so
%endif
%ifarch %lsan_arch
%exclude %{libdir}/liblsan.so
%endif
%ifarch %tsan_arch
%exclude %{libdir}/libtsan.so
%endif
%ifarch %ubsan_arch
%exclude %{libdir}/libubsan.so
%endif

%files c++
%defattr(-,root,root)
%{libsubdir}/cc1plus
%{_bindir}/g++
%{_bindir}/c++
%{_bindir}/%{target_arch}-g++
%{_bindir}/%{target_arch}-c++

%files -n libstdc++
%manifest gcc.manifest
%license COPYING3 COPYING.RUNTIME
%defattr(-,root,root)
%{libdir}/libstdc++.so.*

%files -n libstdc++-devel
%defattr(-,root,root)
%{libdir}/libstdc++.so
%{libdir}/libstdc++.a
%{libdir}/libsupc++.a
%{libsubdir}/include/c++/*
%{libsubdir}/libstdc++fs.a
%{libsubdir}/libstdc++exp.a
%{_datadir}/gcc-%{version}/python/libstdcxx/*

%files -n libgcc
%manifest gcc.manifest
%license COPYING3 COPYING.RUNTIME
%defattr(-,root,root)
%{libdir}/libgcc_s.so.*
%{libsubdir}/libgcc.a
%{libsubdir}/libgcc_eh.a
%{libsubdir}/libgcov.a

%files -n libgomp
%manifest gcc.manifest
%license COPYING3 COPYING.RUNTIME
%defattr(-,root,root)
%{libdir}/libgomp.so.*

%files -n libcc1
%manifest gcc.manifest
%defattr(-,root,root)
%{libdir}/libcc1.so.*

%ifarch %asan_arch
%files -n libasan
%manifest gcc.manifest
%license libsanitizer/LICENSE.TXT
%defattr(-,root,root)
%{libdir}/libasan.so*
%endif

%ifarch %hwasan_arch
%files -n libhwasan
%manifest gcc.manifest
%license libsanitizer/LICENSE.TXT
%defattr(-,root,root)
%{libdir}/libhwasan.so*
%endif

%ifarch %lsan_arch
%files -n liblsan
%manifest gcc.manifest
%license libsanitizer/LICENSE.TXT
%defattr(-,root,root)
%{libdir}/liblsan.so*
%endif

%ifarch %tsan_arch
%files -n libtsan
%manifest gcc.manifest
%license libsanitizer/LICENSE.TXT
%defattr(-,root,root)
%{libdir}/libtsan.so*
%endif

%ifarch %atomic_arch
%files -n libatomic
%manifest gcc.manifest
%license COPYING3 COPYING.RUNTIME
%defattr(-,root,root)
%{libdir}/libatomic.so.*
%endif

%ifarch %itm_arch
%files -n libitm
%manifest gcc.manifest
%license COPYING3 COPYING.RUNTIME
%defattr(-,root,root)
%{libdir}/libitm.so.*
%endif

%ifarch %ubsan_arch
%files -n libubsan
%manifest gcc.manifest
%license libsanitizer/LICENSE.TXT
%defattr(-,root,root)
%{libdir}/libubsan.so*
%endif

%files fortran
%defattr(-,root,root)
%dir %{libsubdir}/finclude
%{_bindir}/gfortran
%{_bindir}/%{target_arch}-gfortran
%{libsubdir}/f951
%{libsubdir}/finclude/*
%{libdir}/libgfortran.a
%{libdir}/libgfortran.so
%{libsubdir}/libgfortran.spec
%{libsubdir}/libcaf_single.a
%ifarch %quadmath_arch
%{libdir}/libquadmath.a
%{libdir}/libquadmath.so
%endif

%files -n libgfortran
%defattr(-,root,root)
%{libdir}/libgfortran.so.*

%ifarch %quadmath_arch
%files -n libquadmath
%manifest gcc.manifest
%license COPYING.LIB
%defattr(-,root,root)
%{libdir}/libquadmath.so.*
%{libdir}/libquadmath.a
%endif

%files -n cpp
%defattr(-,root,root)
%{_bindir}/cpp
%{libsubdir}/cc1
/lib/cpp

%files plugin-devel
%defattr(-,root,root)
%{libsubdir}/plugin/*

%files -n sanitizer-sources
%defattr(-,root,root,-)
/src/libsanitizer.tar.xz
}

%{!?cross:
%files devel-static
%manifest gcc.manifest
%license COPYING.LIB
%defattr(-,root,root)
%{libdir}/libgomp.a
%ifarch %itm_arch
%{libdir}/libitm.a
%endif
%ifarch %asan_arch
%{libdir}/libasan.a
%endif
%ifarch %hwasan_arch
%{libdir}/libhwasan.a
%endif
%ifarch %lsan_arch
%{libdir}/liblsan.a
%endif
%ifarch %ubsan_arch
%{libdir}/libubsan.a
%endif
%ifarch %tsan_arch
%{libdir}/libtsan.a
%endif
%{libdir}/libatomic.a
%{libsubdir}/libcaf_single.a
}

%{?build_tests:
%files tests
%defattr(-,root,root)
%{_builddir}/%{name}-%{version}.tar.xz
}

%changelog
