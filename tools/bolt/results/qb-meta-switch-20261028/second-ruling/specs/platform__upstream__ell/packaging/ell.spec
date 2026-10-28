Name:    ell
Version: 0.28
Release: 0
Summary: Embedded Linux Library
Group:   Base/Utilities
License: LGPL-2.1
URL:     https://01.org/ell
Source0: http://ftp.be.debian.org/pub/linux/libs/ell/%{name}-%{version}.tar.gz

%description
Embedded Linux Library

%package devel
Summary:    Embedded Linux Library development files
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains Embedded Linux Library development files

%prep
%setup -q

%build
%configure --enable-pie --prefix=/usr
%__make %{?_smp_mflags}

%install
%make_install
rm -rf %{buildroot}%{_libdir}/*.la

%clean

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/libell.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/ell/*
%{_libdir}/libell.so
%{_libdir}/pkgconfig/ell.pc
