Name:       strongswan
Summary:    StrongSwan - An OpenSource IPsec-based VPN Solution
Version:    5.7.1
Release:    1
Group:      Security/Service
License:    GPL-2.0+
URL:        http://www.strongswan.org/
Source0:    %{name}-%{version}.tar.gz
Source1001: strongswan.manifest
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  bison
BuildRequires:  gperf
BuildRequires:  flex
BuildRequires:  python
Requires:       security-config

%description
StrongSwan - An OpenSource IPsec-based VPN Solution

%prep
%setup -q
cp -a %{SOURCE1001} .

%build

#cd strongswan-%{version}
export CFLAGS="${CFLAGS} -fPIE -Wno-incompatible-pointer-types"
export LDFLAGS="${LDFLAGS} -pie %{?asan:-lpthread}"

%configure --libexecdir=%{_bindir} --with-ipsecdir=%{_bindir} --with-ipseclibdir=%{_libdir} --with-strongswan-conf=%{_sysconfdir}/strongswan.conf --enable-monolithic --enable-openssl --enable-unity --disable-gmp --disable-pki --disable-stroke --with-capabilities=libcap --with-user=network_fw --with-group=network_fw

make %{?_smp_mflags}

%install
%make_install

#rm -rf %{buildroot}/etc/strongswan.d
rm -rf %{buildroot}/usr/share/strongswan
rm -rf %{buildroot}/usr/share/man
rm -rf %{buildroot}%{_libdir}/libcharon.so
rm -rf %{buildroot}%{_libdir}/libstrongswan.so
rm -rf %{buildroot}%{_libdir}/libvici.so

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest strongswan.manifest
%license LICENSE
%defattr(-,network_fw,network_fw)
%config %{_sysconfdir}/strongswan.conf
%attr(500,network_fw,network_fw) %{_bindir}/*
%attr(500,network_fw,network_fw) %{_libdir}/libcharon.so.*
%attr(500,network_fw,network_fw) %{_libdir}/libstrongswan.so.*
%attr(500,network_fw,network_fw) %{_libdir}/libvici.so.*
#%attr(500,root,root) %{_libdir}/libipsec*
#%attr(500,root,root) %{_libdir}/libsimaka*

/usr/sbin/ipsec
/etc/strongswan.d/*
%attr(500,network_fw,network_fw) /etc/swanctl/swanctl.conf
%attr(500,network_fw,network_fw) /usr/sbin/swanctl

%changelog
