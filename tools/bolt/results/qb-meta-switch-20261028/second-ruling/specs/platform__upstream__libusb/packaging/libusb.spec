%define TIZEN_FEATURE_USBHOST_API on

Name:           libusb
Version:        1.0.25
Release:        0
License:        LGPL-2.1+, MIT
Summary:        USB Library
Url:            http://www.libusb.org/
Group:          Base/Device Management
Source:         %{name}-%{version}.tar.bz2
Source1:        baselibs.conf
Source1001: 	libusb.manifest
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
%if %{?TIZEN_FEATURE_USBHOST_API} == on
BuildRequires:  pkgconfig(dbus-1)
%endif

%description
Libusb is a library that allows userspace access to USB devices.

%package devel
Summary:        USB Library
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       libusb = %{version}

%description devel
Libusb is a library that allows userspace access to USB devices.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%reconfigure\
	--with-pic\
%if %{?TIZEN_FEATURE_USBHOST_API} == on
	--enable-usbhost-api \
%endif
	--disable-static
make %{?_smp_mflags}

%install
%make_install
# usbhost_module
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
install -m 644 udev/99-usbhost.rules %{buildroot}%{_prefix}/lib/udev/rules.d/99-usbhost.rules

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE.LGPL-2.1+ LICENSE.MIT
%{_libdir}/*.so.*
# usbhost_module
%{_prefix}/lib/udev/rules.d/99-usbhost.rules

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE.LGPL-2.1+ LICENSE.MIT
%{_includedir}/libusb-1.0
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
