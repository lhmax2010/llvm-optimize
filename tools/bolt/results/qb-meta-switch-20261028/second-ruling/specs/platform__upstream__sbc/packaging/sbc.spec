Name:    sbc
Version: 1.2
Release: 0
Summary: Bluetooth SBC Utilities
Group:   Multimedia/Utilities
License: GPL-2.0 and LGPL-2.1
URL:     http://www.bluez.org
Source0: http://www.kernel.org/pub/linux/bluetooth/%{name}-%{version}.tar.gz
BuildRequires:  pkgconfig(sndfile)

%description
Bluetooth SBC utilities

%package devel
Summary:    Bluetooth SBC development files
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig

%description devel
This package contains Bluetooth SBC development files

%prep
%setup -q

%build
%configure --enable-shared --disable-static --enable-pie --prefix=/usr
%__make %{?_smp_mflags}

%install
%make_install
rm -rf %{buildroot}%{_libdir}/*.la

%clean

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING COPYING.LIB
%defattr(-,root,root,-)
%{_bindir}/sbcinfo
%{_bindir}/sbcdec
%{_bindir}/sbcenc
%{_libdir}/libsbc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/sbc/*
%{_libdir}/libsbc.so
%{_libdir}/pkgconfig/sbc.pc
