%define cross armv7hl
%define armv7hl 1

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

# Don't build package with tests when cross-compiling
%{?cross:%undefine build_tests}

Name:           binutils%{?cross:-%{cross}}
VCS:            platform/upstream/binutils#518d2e0089ccf79dd8de973276207d3aa638df11
BuildRequires:  binutils-libs
BuildRequires:  makeinfo
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel
BuildRequires:  gcc-c++
%if 0%{?build_tests}
BuildRequires:  toolchain-testing-tool
BuildRequires:  xz
%endif
Version:        2.43
Release:        1.1
Url:            http://www.gnu.org/software/binutils/
Summary:        GNU Binutils
License:        GFDL-1.3 and GPL-3.0+
Group:          Development/Building
%{?cross:ExcludeArch: %{cross}}
Source:         binutils-%{version}.tar.bz2
Source1001:     binutils.manifest

%description
C compiler utilities: ar, as, gprof, ld, nm, objcopy, objdump, ranlib,
size, strings, and strip. These utilities are needed whenever you want
to compile a program or kernel.

%package libs
Summary:        Shared library files for binutils
License:        GPL-2.0+

%description libs
It contains the binutils shared libraries that applications can link
to at runtime.

%ifnarch riscv64
%package gold
Summary:        The gold linker
License:        GPL-3.0+
Group:          Development/Building

%description gold
gold is an ELF linker.	It is intended to have complete support for ELF
and to run as fast as possible on modern systems.  For normal use it is
a drop-in replacement for the older GNU linker.
%endif

%package devel
Summary:        GNU binutils (BFD development files)
License:        GPL-3.0+
Group:          Development/Building
Requires: zlib-devel

%description devel
This package includes header files and static libraries necessary to
build programs which use the GNU BFD library, which is part of
binutils.

%{?build_tests:
%package tests
Summary:       GNU binutils testsuites
License:       GPL-3.0+
Group:         Development/Building
Requires:      dejagnu
Requires:      binutils-libs
Requires:      makeinfo
Requires:      bison
Requires:      flex
Requires:      ncurses-devel
Requires:      zlib-devel
Requires:      gcc-c++
Requires:      glibc-devel-static
AutoReqProv:   off
%description tests
This package contains sources and build output binutils
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
%setup -q -n binutils-%{version}
cp %{SOURCE1001} .

%build
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wno-error %{?cross:-DIGNORE_BROKEN_PLUGINS}"
export CFLAGS="${RPM_OPT_FLAGS}"
export CXXFLAGS="${RPM_OPT_FLAGS}"
%{?asan:
export ASAN_OPTIONS=$(cat /ASAN_OPTIONS)
}

# Remove gdb and sim since they have separate gdb package
rm -rf gdb gdbserver gdbsupport sim

rm -rf build-dir
mkdir -p build-dir
cd build-dir

../configure \
	--prefix=%{_prefix} --libdir=%{_libdir} \
	--infodir=%{_infodir} --mandir=%{_mandir} \
	--with-bugurl=http://bugs.tizen.org/ \
	--with-sysroot=/ \
%ifarch riscv64
	--with-lib-path="=%{_libdir}" \
%endif
	--disable-nls \
	--with-separate-debug-dir=%{_prefix}/lib/debug \
	--with-pic \
	--build=%{_build} --host=%{_host} \
	--target=%{target_arch} \
%{?cross: \
	--enable-targets=%{target_arch} \
	--enable-64-bit-bfd \
} \
%{!?cross: \
	--enable-targets=aarch64-tizen-linux,armv7l-tizen-linux,armv7hl-tizen-linux,armv8l-tizen-linux,i686-tizen-linux,x86_64-tizen-linux,riscv64-tizen-linux \
} \
	--enable-plugins \
%ifnarch riscv64
	--enable-gold \
%endif
	--enable-shared \
	--enable-new-dtags \
	--enable-relro=no \
	--disable-gprofng \
%ifarch %ix86
	--disable-separate-code
%endif

make %{?_smp_mflags}

%install
cd build-dir

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

make DESTDIR=$RPM_BUILD_ROOT install

export LINKERS="ld ld.bfd"
%ifnarch riscv64
# There's neither native gold nor cross-gold for riscv64 yet
%{!?riscv64:export LINKERS="ld ld.bfd ld.gold"}
%endif

# Copy instead of hardlinks
for binary in ar as ${LINKERS} nm objdump objcopy ranlib strip
do
  rm -f %{buildroot}%{_prefix}/%{target_arch}/bin/$binary
%{!?cross:
  cp %{buildroot}%{_bindir}/$binary %{buildroot}%{_prefix}/%{target_arch}/bin/$binary
}
%{?cross:
  cp %{buildroot}%{_bindir}/%{target_arch}-$binary %{buildroot}%{_prefix}/%{target_arch}/bin/$binary
}
done

install -m 644 libiberty/pic/libiberty.a %{buildroot}%{_prefix}/%{_lib}
install -m 644 ../include/libiberty.h %{buildroot}%{_prefix}/include

# Remove unwanted files to shut up rpm
%{remove_docs}
rm -rf %{buildroot}%{_bindir}/gcore
rm -f %{buildroot}%{_libdir}/libbfd.la %{buildroot}%{_libdir}/libctf.la %{buildroot}%{_libdir}/libctf-nobfd.la %{buildroot}%{_libdir}/libopcodes.la %{buildroot}%{_libdir}/libinproctrace.la %{buildroot}%{_libdir}/libsframe.la
%{?cross:
rm -rf %{buildroot}%{_prefix}/%{target_arch}/lib/ldscripts
rm -rf %{buildroot}%{_prefix}/%{_host}
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_prefix}/lib*
rm -rf %{buildroot}%{_datadir}
}

%files
%manifest binutils.manifest
%defattr(-,root,root)
%{_bindir}/*
%{_prefix}/%{target_arch}/bin/*
%{!?cross:
%exclude %{_bindir}/ld.gold
%exclude %{_prefix}/%{target_arch}/bin/ld.gold
%{_prefix}/%{_host}/lib/ldscripts

%files libs
%{_libdir}/*.so*
%{_libdir}/bfd-plugins/*.so

%files devel
%manifest binutils.manifest
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.a

%ifnarch riscv64
%files gold
%manifest binutils.manifest
%defattr(-,root,root)
%{_bindir}/ld.gold
%{_prefix}/%{target_arch}/bin/ld.gold
%endif
}

%{?build_tests:
%files tests
%defattr(-,root,root)
%{_builddir}/%{name}-%{version}.tar.xz
}

%changelog
