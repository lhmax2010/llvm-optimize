Name:           libksba
Version:        1.6.7
Release:        1
License:        LGPL-3.0-or-later or GPL-2.0-or-later
Summary:        KSBA Library
Url:            http://www.gnupg.org/aegypten/
Group:          Security/Libraries
Source:         libksba-%{version}.tar.bz2
Source1001: 	libksba.manifest
BuildRequires:  libgpg-error-devel >= 1.8
BuildRequires:  libtool

%description
KSBA is a library to simplify the task of working with X.509
certificates, CMS data, and related data.

%package devel
License:        GPL-3.0-or-later
Summary:        KSBA Library development package
Requires:       libgpg-error-devel
Requires:       libksba = %{version}
Provides:       libksba:/usr/include/ksba.h

%description devel
KSBA is a library to simplify the task of working with X.509
certificates, CMS data, and related data.

This package contains the needed files to compile and link against the
libksba.

%prep
%setup -q -n libksba-%{version}
cp %{SOURCE1001} .

%build
autoreconf -fi
%configure --disable-static --with-pic
%__make %{?_smp_mflags}

%check
# %__make check

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING.LGPLv3 COPYING.GPLv2
%{_libdir}/libksba*.so.*


%files devel
%manifest %{name}.manifest
%license COPYING.GPLv3
%{_libdir}/libksba*.so
%{_includedir}/*
%{_libdir}/pkgconfig/ksba.pc
%doc %{_infodir}/ksba*
%{_datadir}/aclocal/*

