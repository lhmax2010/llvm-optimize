Name:           usbutils
Version:        013
Release:        0
License:        GPL-2.0+
Url:            http://www.linux-usb.org/
Source:         https://www.kernel.org/pub/linux/utils/usb/usbutils/%{name}-%{version}.tar.xz
Source1001:     usbutils.manifest

Summary:        Linux USB utilities
Group:          Base/Device Management
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libudev)

%description
This package contains utilities for inspecting devices connected to a
USB bus.

%prep
%setup -q
cp %{SOURCE1001} .

%build
CFLAGS="-fPIC" LDFLAGS="-pie" \
%reconfigure \
    --datadir=%{_datadir}/hwdata \
    --disable-usbids

%__make %{?_smp_mflags}

%install
%make_install

rm -rf %{buildroot}%{_datadir}/man

# lsusb.py is both python-based and GPL3-licensed - drop it
rm -f %{buildroot}%{_bindir}/lsusb.py

%files
%manifest %{name}.manifest
%license LICENSES/GPL-2.0.txt
%{_bindir}/lsusb
%{_bindir}/usb-devices
%{_bindir}/usbhid-dump
