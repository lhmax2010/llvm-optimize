Name:       openvpn
Summary:    A full-featured SSL VPN solution
Version:    2.5.11
Release:    0
Group:      Security/Network
License:    GPL-2.0
URL:        http://openvpn.net/
Source0:    http://swupdate.openvpn.org/community/releases/%{name}-%{version}.tar.gz
Source1001: 	openvpn.manifest
BuildRequires:  lzo-devel
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pam-devel
BuildRequires:  iproute2
Requires:   	iproute2

%description
OpenVPN is a robust and highly flexible tunneling application that uses all
of the encryption, authentication, and certification features of the
OpenSSL library to securely tunnel IP networks over a single UDP or TCP
port.  It can use the Marcus Franz Xaver Johannes Oberhumer's LZO library
for compression.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS
export LDFLAGS

aclocal && \
	autoheader && \
		libtoolize --automake --copy --force && \
		automake --add-missing --copy && \
		autoconf
%configure --disable-static \
    --enable-iproute2 \
    CFLAGS="$CFLAGS -fPIE" \
    LDFLAGS="$LDFLAGS -pie"

make %{?jobs:-j%jobs}

%install
%make_install
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

chmod -x contrib/openvpn-fwmarkroute-1.00/*

mkdir $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_sbindir}/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING.GPLv2
%doc AUTHORS ChangeLog PORTS
%{_mandir}/man5/%{name}-examples.5*
%{_mandir}/man8/%{name}.8*
%{_datadir}/doc/%{name}/
%{_bindir}/%{name}
%{_libdir}/%{name}/
%config %dir %{_sysconfdir}/%{name}/
%{_includedir}/*.h
%exclude %{_datadir}/doc/%{name}/COPYING
