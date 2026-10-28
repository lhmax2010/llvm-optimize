%bcond_with examples

Name: bcc-tools
Version: 0.35.0
Release: 0
Summary: Tools for BPF-based Linux IO analysis, networking, monitoring
License: Apache-2.0
Vendor: None (open source)
Group: Development/Compilers
URL: https://github.com/iovisor/bcc
Source0: %{name}-%{version}.tar.gz
Requires: /sbin/ldconfig
BuildRequires: gcc >= 3.4
BuildRequires: cmake python3
BuildRequires: python3-setuptools
BuildRequires: bison flex llvm-devel clang-devel libelf-devel
BuildRequires: llvm-static-devel
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libbpf)
BuildRequires: zip
BuildRequires:  libomp

%description
BCC is a toolkit for creating efficient kernel tracing and manipulation
programs, and includes several useful tools and examples. It makes use
of extended BPF (Berkeley Packet Filters), formally known as eBPF, a new
feature that was first added to Linux 3.15. Much of what BCC uses
requires Linux 4.1 and above.

%package devel
Summary: Developer package for BCC
Requires: %{name} = %{version}-%{release}

%description devel
bcc tools - devel
This package provides development libraries.

%package static
Summary: Static library for bcc development
Requires: %{name}-devel = %{version}-%{release}

%description static
bcc tools - static
This package provides development libraries.

%if %{with examples}
%package examples
Summary: Example codes for BCC
License: Apache-2.0

%description examples
This package provides example codes and documents.
%endif

%prep
%setup -q -n bcc-tools-%{version}

%build
#DREVISION - number which will be put at back of the package name if repo isn't available
LLVM_VERSION_MAJOR=$(llvm-config --version | cut -d. -f1)
LLVM_SHARED_FLAG=
if [ "${LLVM_VERSION_MAJOR}" -ge 22 ]; then
    LLVM_SHARED_FLAG="-DENABLE_LLVM_SHARED=ON"
fi

%if %{with examples}
%global install_cpp_examples ON
%else
%global install_cpp_examples OFF
%endif

cmake -DCMAKE_INSTALL_PREFIX=/usr -DINSTALL_CPP_EXAMPLES=%{install_cpp_examples} ${LLVM_SHARED_FLAG} -DREVISION="%{version}" -DCMAKE_USE_LIBBPF_PACKAGE:BOOL=TRUE .
make %{?jobs:-j%jobs}

%install
make install DESTDIR=%{buildroot}

%if %{without examples}
rm -rf %{buildroot}%{_datadir}/bcc
%endif

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libbcc_bpf.so*
%{_libdir}/libbcc.so.*
%{_prefix}/lib/python*/site-packages/bcc*

%files devel
%{_includedir}/*
%{_libdir}/libbcc.so
%{_libdir}/pkgconfig/libbcc.pc

%files static
%{_libdir}/libbcc.a
%{_libdir}/libbcc-loader-static.a
%{_libdir}/libbcc_bpf.a

%if %{with examples}
%files examples
%{_datadir}/bcc/*
%endif
