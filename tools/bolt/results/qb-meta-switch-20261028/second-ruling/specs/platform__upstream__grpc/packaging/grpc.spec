#
# spec file for package grpc
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define lname libgrpc
%define src_install_dir /usr/src/%{name}
%{?!python_module:%define python_module() python-%{**} python3-%{**}}

Name:           grpc
Version:        1.76.0
Release:        0
Summary:        HTTP/2-based Remote Procedure Call implementation
License:        Apache-2.0
Group:          Development/Tools/Building
Url:            http://grpc.io/
Source:         https://github.com/grpc/grpc/archive/v%{version}.tar.gz
Source1:        grpc.manifest
Source2:       support_lib64_directory.patch
Source3:       disable_download_archive_sse2_option.patch

BuildRequires:  python-cython
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(libcares)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  abseil-cpp-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-lite-devel
BuildRequires:  protobuf-lite-static
BuildRequires:  protobuf-static

%description
The reference implementation of the gRPC protocol, done on top of
HTTP/2 with support for synchronous and asynchronous calls. gRPC uses
Protocol Buffers as the Interface Definition Language by default.

%package -n %lname
Summary:        HTTP/2-based Remote Procedure Call implementation
Group:          System/Libraries

%description -n %lname
The reference implementation of the gRPC protocol, done on top of
HTTP/2 with support for synchronous and asynchronous calls. gRPC uses
Protocol Buffers as the Interface Definition Language by default.

%package devel
Summary:        Development files for grpc, a HTTP/2 Remote Procedure Call implementation
Group:          Development/Tools/Building
Requires:       abseil-cpp-devel
Requires:       %lname = %version
Requires:       pkgconfig(libcares)
Requires:       pkgconfig(protobuf)
Requires:       pkgconfig(re2)

%description devel
This subpackage contains libraries and header files for developing
applications that want to make use of the gRPC reference implementation.

%prep
%setup -q
cp %{SOURCE1} .
%{__patch} -p1 < %{SOURCE2}
%{__patch} -p1 < %{SOURCE3}

%build
CFLAGS="$CFLAGS -Wno-error -Wno-unused-parameter"
CXXFLAGS="$CXXFLAGS -Wno-error -Wno-unused-parameter"


mkdir -p cmake/build
cd cmake/build
%{__cmake} ../.. -DCMAKE_INSTALL_PREFIX=%{_prefix}    \
            -DCMAKE_C_FLAGS="%{optflags} -fPIC" \
            -DCMAKE_CXX_FLAGS="%{optflags} -fPIC" \
            -DCMAKE_EXE_LINKER_FLAGS="-pie"     \
            -DCMAKE_THREAD_LIBS_INIT="-pthread"     \
            -DINCLUDE_INSTALL_DIR=%{_includedir} \
            -DLIB_INSTALL_DIR=%{_libdir}         \
            -DgRPC_BUILD_CSHARP_EXT=ON           \
            -DBUILD_SHARED_LIBS=ON               \
            -DgRPC_INSTALL=ON                    \
            -DgRPC_ABSL_PROVIDER=package         \
            -DgRPC_CARES_PROVIDER=package        \
            -DgRPC_RE2_PROVIDER=package          \
            -DgRPC_PROTOBUF_PROVIDER=package     \
            -DgRPC_SSL_PROVIDER=package          \
            -DgRPC_ZLIB_PROVIDER=package

%{__make} %{?_smp_mflags}

%install
cd cmake/build
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

rm -rf %{buildroot}%{_libdir}/cmake
rm -rf %{buildroot}%{_datadir}/grpc/roots.pem

%post   -n %lname -p /sbin/ldconfig
%postun -n %lname -p /sbin/ldconfig

%files -n %lname
%license LICENSE
%_libdir/libaddress_sorting.so.*
%_libdir/libgpr*.so.*
%_libdir/libgrpc*.so.*
%_libdir/libupb*.so.*
%_libdir/libutf*.so.*

%files devel
%license LICENSE
%_bindir/*
%_includedir/*
%_libdir/pkgconfig/gpr.pc
%_libdir/pkgconfig/grpc++.pc
%_libdir/pkgconfig/grpc.pc
%_libdir/pkgconfig/grpc++_unsecure.pc
%_libdir/pkgconfig/grpc_unsecure.pc
%_libdir/*.so
%_libdir/pkgconfig/grpcpp_otel_plugin.pc
