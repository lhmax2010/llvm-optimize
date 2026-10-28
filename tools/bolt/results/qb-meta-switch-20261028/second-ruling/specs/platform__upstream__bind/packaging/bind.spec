#%define source_name bind

Name:       bind
Summary:    Embedded DHCPv6/RA Server & Relay
Version:    9.14.12
Release:    1
Group:      System/Tools
License:    MPL-2.0+
URL:        http://www.isc.org/downloads/bind/
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(openssl3)
Requires:       security-config

%define install_path	/opt/etc/named

%description
BIND is open source software that implements the Domain Name System (DNS)
protocols for the Internet. It is a reference implementation of those protocols,
but it is also production-grade software, suitable for use in high-volume
and high-reliability applications.  The name BIND stands for
“Berkeley Internet Name Domain”, because the software originated
in the early 1980s at the University of California at Berkeley.

BIND is by far the most widely used DNS software on the Internet,
providing a robust and stable platform on top of which organizations
can build distributed computing systems with the knowledge
that those systems are fully compliant with published DNS standards.

%package devel
Summary: Embedded DHCPv6/RA Server & Relay (devel)
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Embedded DHCPv6/RA Server & Relay (devel)

%prep
%setup -q

%build
./autogen.sh
./configure --prefix=%{_prefix} \
		--sysconfdir=%{_sysconfdir} \
		--localstatedir=%{_localstatedir} \
		--enable-threads \
		--with-libtool \
		--disable-static \
		--enable-ipv6 \
		--with-randomdev=/dev/urandom \
		--without-python \
		--disable-linux-caps \
		--disable-isc-spnego

make -j1

%install
%make_install

mkdir -p %{buildroot}%{install_path}/etc/namedb/pz
cp config/named.conf %{buildroot}%{install_path}/etc/named.conf
cp config/root.hints %{buildroot}%{install_path}/etc/namedb/root.hints
cp config/pz/127.0.0 %{buildroot}%{install_path}/etc/namedb/pz/127.0.0

%if "%{?_lib}" == "lib64"
mkdir -p %{buildroot}%{_libdir}
cp -rf %{buildroot}/usr/lib/* %{buildroot}%{_libdir}
rm -rf %{buildroot}/usr/lib
%endif

%post
cd %{install_path}
mkdir -p dev etc/namedb/slave etc/namedb/pz usr/lib/engines var/run/named
mknod %{install_path}/dev/null c 1 3
mknod %{install_path}/dev/urandom c 1 9
chmod 666 %{install_path}/dev/null %{install_path}/dev/urandom
cp %{_sysconfdir}/localtime etc
touch %{install_path}/managed-keys.bind
cp %{_libdir}/engines/libgost.so usr/lib/engines
[ $(uname -m) = arm64 ] && ln -sv lib usr/lib64

%{_sbindir}/rndc-confgen -r /dev/urandom -b 512 > %{_sysconfdir}/rndc.conf
sed '/conf/d;/^#/!d;s:^# ::' %{_sysconfdir}/rndc.conf > %{install_path}/etc/named.conf.rndc

chown -R network_fw:network_fw %{install_path}

%files
%manifest bind.manifest
%defattr(-,root,root,-)
%{_bindir}/*
%exclude %{_bindir}/bind9-config
%exclude %{_bindir}/isc-config.sh
%{_sbindir}/*
%{_libdir}/*.so.*
%{_libdir}/named/*.so
%{_sysconfdir}/bind.keys
%attr(770,network_fw,network_fw) %{install_path}/etc/named.conf
%attr(770,network_fw,network_fw) %{install_path}/etc/namedb/root.hints
%attr(770,network_fw,network_fw) %{install_path}/etc/namedb/pz/127.0.0
%license LICENSE

%files devel
%{_includedir}/bind9
%{_includedir}/dns
%{_includedir}/dst
%{_includedir}/irs
%{_includedir}/isc
%{_includedir}/isccc
%{_includedir}/isccfg
%{_includedir}/ns
%{_includedir}/pk11
%{_includedir}/pkcs11
%{_libdir}/*.so
%{_datadir}/*
