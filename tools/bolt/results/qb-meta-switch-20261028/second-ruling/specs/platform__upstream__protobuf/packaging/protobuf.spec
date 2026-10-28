Name:           protobuf
Summary:        Protocol Buffers - Google's data interchange format
License:        BSD-3-Clause
Group:          Development/Libraries
Version:        33.1
Release:        1
URL:            https://github.com/google/protobuf
Source0:        protobuf-%{version}.tar.gz
Source1:        protobuf.manifest
Source2:        add_pie_compile_option.patch

BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel
BuildRequires:  cmake
BuildRequires:  abseil-cpp-devel

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data – think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

%package compiler
Summary: Protocol Buffers compiler
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description compiler
This package contains Protocol Buffers compiler for all programming
languages

%package devel
Summary: Protocol Buffers C++ headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-compiler = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains Protocol Buffers compiler for all languages and
C++ headers and libraries

%package static
Summary: Static development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description static
Static libraries for Protocol Buffers

%package lite
Summary: Protocol Buffers LITE_RUNTIME libraries
Group: Development/Libraries

%description lite
Protocol Buffers built with optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-devel
Summary: Protocol Buffers LITE_RUNTIME development libraries
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-lite = %{version}-%{release}

%description lite-devel
This package contains development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package lite-static
Summary: Static development files for %{name}-lite
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description lite-static
This package contains static development libraries built with
optimize_for = LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to generate code
which only depends libprotobuf-lite, which is much smaller than libprotobuf but
lacks descriptors, reflection, and some other features.

%package vim
Summary: Vim syntax highlighting for Google Protocol Buffers descriptions
Group: Development/Libraries
Requires: vim-enhanced

%description vim
This package contains syntax highlighting for Google Protocol Buffers
descriptions in Vim editor

%prep
%setup -q
cp %{SOURCE1} .
%{__patch} -p1 < %{SOURCE2}
chmod 644 examples/*

#%patch3 -p1 -b .generic-atomics
#%patch4 -p1 -b .generic-atomics-makefile

%build
iconv -f iso8859-1 -t utf-8 CONTRIBUTORS.txt > CONTRIBUTORS.txt.utf8
mv CONTRIBUTORS.txt.utf8 CONTRIBUTORS.txt
export PTHREAD_LIBS="-lpthread"

%define CMAKE_OPTS -DCMAKE_CXX_STANDARD=17 -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_ABSL_PROVIDER=package -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DCMAKE_INSTALL_BINDIR=%{_bindir} -DCMAKE_INSTALL_PREFIX=${buildroot} -DCMAKE_POSITION_INDEPENDENT_CODE=ON

# Build shared libs
mkdir -p build_shared && pushd build_shared
cmake .. %{CMAKE_OPTS} -Dprotobuf_BUILD_SHARED_LIBS=ON
cmake --build . %{?_smp_mflags}
popd

# Build static libs
mkdir -p build_static && pushd build_static
cmake .. %{CMAKE_OPTS} -Dprotobuf_BUILD_SHARED_LIBS=OFF
cmake --build . %{?_smp_mflags}
popd

%check
#make %{?_smp_mflags} check

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_bindir}

install -p -m 644 -D editors/proto.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/proto.vim
make -C build_static %{?_smp_mflags} install DESTDIR=%{buildroot} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
make -C build_shared %{?_smp_mflags} install DESTDIR=%{buildroot} STRIPBINARIES=no INSTALL="%{__install} -p" CPPROG="cp -p"
cp ./build_shared/protoc* %{buildroot}%{_bindir}/
cp ./build_shared/*so* %{buildroot}%{_libdir}/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post lite -p /sbin/ldconfig
%postun lite -p /sbin/ldconfig

%post compiler -p /sbin/ldconfig
%postun compiler -p /sbin/ldconfig

%files
%license LICENSE
%manifest protobuf.manifest
%defattr(-, root, root, -)
%{_libdir}/libprotobuf.so.*
%{_libdir}/libutf8_range.so
%{_libdir}/libutf8_range.so.*
%{_libdir}/libutf8_validity.so
%{_libdir}/libutf8_validity.so.*
%doc CONTRIBUTORS.txt README.md

%files compiler
%license LICENSE
%manifest protobuf.manifest
%defattr(-, root, root, -)
%{_bindir}/protoc*
%{_libdir}/libprotoc.so.*
%doc README.md

%files devel
%license LICENSE
%manifest protobuf.manifest
%defattr(-, root, root, -)
%dir %{_includedir}/google
%{_includedir}/google/protobuf/
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
%{_libdir}/pkgconfig/protobuf.pc
%{_includedir}/utf8_range.h
%{_includedir}/utf8_validity.h
%{_includedir}/upb/*
%{_libdir}/libutf8_range.a
%{_libdir}/libutf8_validity.a
%{_libdir}/pkgconfig/utf8_range.pc
%{_libdir}/libupb.a
%{_libdir}/pkgconfig/upb.pc
%{_libdir}/cmake/
%doc examples/add_person.cc examples/addressbook.proto examples/list_people.cc examples/CMakeLists.txt

%files static
%license LICENSE
%manifest protobuf.manifest
%defattr(-, root, root, -)
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%files lite
%license LICENSE
%manifest protobuf.manifest
%defattr(-, root, root, -)
%{_libdir}/libprotobuf-lite.so.*

%files lite-devel
%license LICENSE
%manifest protobuf.manifest
%defattr(-, root, root, -)
%{_libdir}/libprotobuf-lite.so
%{_libdir}/pkgconfig/protobuf-lite.pc

%files lite-static
%license LICENSE
%manifest protobuf.manifest
%defattr(-, root, root, -)
%{_libdir}/libprotobuf-lite.a

%files vim
%license LICENSE
%manifest protobuf.manifest
%defattr(-, root, root, -)
%{_datadir}/vim/vimfiles/syntax/proto.vim
