%define _unpackaged_files_terminate_build 0

Name:       libmtp
Summary:    Library for media transfer protocol (mtp)
Version:    1.1.11
Release:    16
Group:      Network & Connectivity/Other
License:    LGPL-2.1
Source0:    libmtp-%{version}.tar.gz
Source1001: autogen.sh

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: pkgconfig(libusb-1.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libexif)
BuildRequires: libtool-ltdl-devel
BuildRequires: gettext-devel

%description
Libmtp support media transfer protocol, role is initiator
This package contains the library.


%package devel
Summary:    libmtp development package
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the development files.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
export CFLAGS+=" -fPIC -DTIZEN_EXT"
export LDFLAGS+=" -Wl,--hash-style=both -Wl,--as-needed -Wl,--rpath=%{_libdir}"
chmod 755 ./autogen.sh

%autogen
%configure --prefix=/usr --disable-static
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest libmtp.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/libmtp.so.*
/lib/udev/rules.d/69-libmtp.rules

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmtp.so
%{_libdir}/pkgconfig/libmtp.pc
/usr/include/*
/usr/bin/mtp-hotplug
