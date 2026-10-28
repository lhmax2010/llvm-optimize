Name:           libabigail
VCS:            platform/upstream/libabigail#d324c26e5d7083e1cd8ed3b7f75453d4552844c6
BuildRequires:  autoconf automake libtool pkgconfig(libxml-2.0)
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  flex
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  zip
BuildRequires:  gettext-tools
BuildRequires:  libelf-devel
BuildRequires:  libdw-devel
Summary:        The ABI Generic Analysis and Instrumentation Library
License:        LGPL-3.0
Group:          Development/Building
Version:        2.3
Release:        1.1
Source0:        %name-%version.src.tar.gz
Url:            https://www.sourceware.org/libabigail/

%description
This project aims at providing a C++ library for constructing, manipulating,
serializing and de-serializing ABI-relevant artifacts. The set of artifacts that
we are interested in is made of constructions like types, variables, functions
and declarations of a given library or program. For a given program or library,
this set of constructions is called an ABI corpus.

Thus the project aims at providing a library to manipulate ABI corpora, compare
them, provide detailed information about their differences and help build tools
to infer interesting conclusions about these differences.

%prep
%setup -q -n %{name}-%{version}

%build

export CFLAGS+=" -Wno-error=unused-parameter"
%reconfigure \
    --program-prefix=eu- \
    --enable-maintainer-mode \
    --disable-dependency-tracking \
    --enable-libdebuginfod=dummy \
    --disable-debuginfod
%{__make} %{?_smp_flags} V=1

export LIBS="-pthread -ldw -lelf -ldl -lbz2 -lz -llzma"

%reconfigure \
    --disable-shared \
    --enable-static \
    --disable-dependency-tracking \
    --enable-rpm=yes \
    --enable-deb=no \
    --enable-cxx11=yes

%{__make} %{?_smp_mflags} V=1

%install
%{__make} DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libabigail.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libabigail.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libabigail.so
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig
rm -f $RPM_BUILD_ROOT/usr/share/aclocal/abigail.m4

%files
%defattr(-,root,root)
%attr(755,root,root)
%{_bindir}/abi*
%{_bindir}/kmidiff
%{_libdir}/libabigail.so.2*
%{_libdir}/libabigail/default.abignore
