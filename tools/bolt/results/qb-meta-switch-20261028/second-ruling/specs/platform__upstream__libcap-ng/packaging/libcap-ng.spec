Name:           libcap-ng
Version:        0.8.5
Release:        0
License:        LGPL-2.1+
Summary:        An alternate POSIX capabilities library
Group:          System/Libraries
Url:            http://people.redhat.com/sgrubb/libcap-ng
Source0:        http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
Source1001:     libcap-ng.manifest
BuildRequires:  kernel-headers >= 2.6.11
BuildRequires:  libattr-devel
BuildRequires:  pkg-config

%description
Libcap-ng is a library that makes using posix capabilities easier

%package devel

License:        LGPL-2.1+
Summary:        Header files for libcap-ng library
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       kernel-headers >= 2.6.11
Requires:       pkgconfig

%description devel
The libcap-ng-devel package contains the files needed for developing
applications that need to use the libcap-ng library.

%package utils

License:        GPL-2.0+
Summary:        Utilities for analysing and setting file capabilities
Group:          System/Base

%description utils
The libcap-ng-utils package contains applications to analyse the
posix capabilities of all the program running on a system. It also
lets you set the file system based capabilities.

%prep
%setup -q
cp %{SOURCE1001} .

%build
./autogen.sh
%configure --disable-static --with-pic --with-python=no
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING.LIB
%{_libdir}/lib*.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/cap-ng.h
%{_libdir}/lib*.so
%{_datadir}/aclocal/cap-ng.m4
%{_libdir}/pkgconfig/libcap-ng.pc

%files utils
%manifest %{name}.manifest
%license COPYING
%{_bindir}/*
%exclude %{_mandir}/
