Name:       ccid
Summary:    ccid USB driver
Version:    0.1.2
Release:    0
Group:      Network & Connectivity/Common
License:    LGPL-2.1
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(libpcsclite)
BuildRequires: pkgconfig(libusb-1.0)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
CCID Usb driver

%prep
%setup -q
chmod 644 %{SOURCE0}
cp %{SOURCE1} ./%{name}.manifest

%build

./configure
make %{?_smp_mflags}

%install

%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license COPYING
/usr/lib/pcsc/drivers/ifd-ccid.bundle/Contents/Info.plist
/usr/lib/pcsc/drivers/ifd-ccid.bundle/Contents/Linux/libccid.so
