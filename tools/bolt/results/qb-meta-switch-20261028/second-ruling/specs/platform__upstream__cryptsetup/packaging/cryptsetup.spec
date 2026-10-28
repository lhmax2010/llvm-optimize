Name:     cryptsetup
Summary:  The cryptsetup
Version:  2.6.1
Release:  1
License:  GPL-2.0+, LGPL-2.1+
Group:    Base/Device Management
URL:      http://code.google.com/p/cryptsetup/
Source0:  %{name}-%{version}.tar.xz
Source1:  cryptsetup.manifest

BuildRequires: linux-kernel-headers
BuildRequires: device-mapper-devel
BuildRequires: libgpg-error-devel
BuildRequires: libgcrypt-devel
BuildRequires: libuuid-devel
BuildRequires: util-linux
BuildRequires: popt-devel
BuildRequires: automake
BuildRequires: gettext
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(blkid)

Requires:      libgpg-error
Requires:      device-mapper
Requires:      libgcrypt

%description
setup cryptographic volumes for dm-crypt (including LUKS extension)

%package devel
Summary:    The cryptsetup development package
Group:      Development/Libraries
License:    GPL-2.0+, LGPL-2.1+
Requires:   %{name} = %{version}-%{release}

%description devel
cryptsetup development package

%package locale
License:    GPL-2.0+, LGPL-2.1+
Summary:    The cryptsetup locale package
Group:      Base/Device Management
Requires:   %{name} = %{version}-%{release}

%description locale
locale package for cryptsetup

%package doc 
License:    GPL-2.0+
Summary:    The cryptsetup doc package
Group:      Base/Device Management
Requires:   %{name} = %{version}-%{release}

%description doc
doc package for cryptsetup

%prep
%setup -q
cp %{SOURCE1} ./%{name}.manifest

%build
CFLAGS="$CFLAGS -fno-lto"
LDFLAGS="$LDFLAGS -Wl,-z,relro"

cp %{SOURCE1} .

chmod +x ./autogen.sh
./autogen.sh
%configure \
           --disable-cryptsetup-reencrypt \
           --disable-integritysetup \
           --disable-asciidoc \
           --disable-ssh-token

make %{?jobs:-j%jobs} V=1

%install
rm -rf %{buildroot}
%make_install

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING.GPL-2.0+ COPYING.LGPL-2.1+
%{_libdir}/libcryptsetup.so.*
%{_prefix}/lib/tmpfiles.d/cryptsetup.conf
%{_sbindir}/cryptsetup
%{_sbindir}/veritysetup

%files devel
%manifest %{name}.manifest
%license COPYING.GPL-2.0+ COPYING.LGPL-2.1+
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files locale
%manifest %{name}.manifest
%license COPYING.GPL-2.0+ COPYING.LGPL-2.1+
%{_datarootdir}/locale/cs/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/da/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/de/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/es/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/fi/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/fr/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/id/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/it/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/ja/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/nl/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/pl/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/pt_BR/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/ru/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/sr/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/sv/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/uk/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/vi/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/zh_CN/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/ka/LC_MESSAGES/cryptsetup.mo
%{_datarootdir}/locale/ro/LC_MESSAGES/cryptsetup.mo

%files doc
%manifest %{name}.manifest
%license COPYING.GPL-2.0+
