%define lname	liblmdb
%define prefix  %{_prefix}
%define libdir  %{_libdir}

Name:           lmdb
Summary:        Lightning Memory-Mapped Database Manager
License:        OLDAP-2.8
Group:          Productivity/Databases/Tools
Version:        0.9.17
Release:        0
Url:            http://symas.com/mdb/
Source0:        %{name}-%{version}.tar.gz
# Source99:       baselibs.conf

# BuildRequires:  autoconf
BuildRequires:  automake >= 1.10
BuildRequires:  libtool >= 2

%description
LMDB is a Btree-based database management library with an API similar
to BerkeleyDB. The library is thread-aware and supports concurrent
read/write access from multiple processes and threads. The DB
structure is multi-versioned, and data pages use a copy-on-write
strategy, which also provides resistance to corruption and eliminates
the need for any recovery procedures. The database is exposed in a
memory map, requiring no page cache layer of its own.

%package -n %lname
Summary:        Shared library for Lightning Memory-Mapped Database (LMDB)
Group:          System/Libraries

%description -n %lname
LMDB is a Btree-based database management library with an API similar
to BerkeleyDB. The library is thread-aware and supports concurrent
read/write access from multiple processes and threads. The DB
structure is multi-versioned, and data pages use a copy-on-write
strategy, which also provides resistance to corruption and eliminates
the need for any recovery procedures. The database is exposed in a
memory map, requiring no page cache layer of its own.

This package contains the shared library.

%package devel
Summary:        Development package for lmdb
Group:          Development/Libraries/C and C++
Requires:       %lname = %version

%description devel
LMDB is a Btree-based database management library with an API similar
to BerkeleyDB. The library is thread-aware and supports concurrent
read/write access from multiple processes and threads. The DB
structure is multi-versioned, and data pages use a copy-on-write
strategy, which also provides resistance to corruption and eliminates
the need for any recovery procedures. The database is exposed in a
memory map, requiring no page cache layer of its own.
 
This package contains the files needed to compile programs that use
the liblmdb library.

%prep
%setup

%build
cd libraries/liblmdb
make PREFIX=%{prefix} LIBDIR=%{libdir}

%install
cd libraries/liblmdb
# make install DESTDIR="%buildroot"
make install prefix=$RPM_BUILD_ROOT%{prefix} LIBDIR=$RPM_BUILD_ROOT%{libdir} install

rm -rf %{buildroot}%{_mandir}

%post   -n %lname -p /sbin/ldconfig
%postun -n %lname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*

%files -n %lname
%defattr(-,root,root)
%{libdir}/*.so*

%files devel
%defattr(-,root,root)
%_includedir/*
%{libdir}/*.a

%changelog
