Name:       mdnsresponder
Summary:    DNS Service Discovery service with dns-sd library
Version:    1556.80.2
Release:    0
Group:      System/Network
License:    Apache-2.0 or BSD-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:    mdnsresponder.manifest
Source1002:    libdns_sd.manifest
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: bison
BuildRequires: flex

Requires(post):	/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
The DNS Service Discovery is part of Bonjour, Apple's implementation of
zero-configuration networking(ZEROCONF).

%package -n libdns_sd
Summary:    DNS-SD - client libraries
%if "%{?_lib}" == "lib64"
Provides: libdns_sd.so()(64bit)
%else
Provides: libdns_sd.so
%endif
Requires:   mdnsresponder = %{version}-%{release}

%description -n libdns_sd
Client libraries for DNS-SD: synchronous and asynchronous

%package devel
Summary:  DNS Service Discovery (Development)
Requires:   libdns_sd = %{version}-%{release}
Requires: pkgconfig

%description devel
DNS-SD development files

%prep
%setup -q
cp -a %{SOURCE1001} .
cp -a %{SOURCE1002} .

%build
%if "%{?_lib}" == "lib64"
CONFIG_TIZEN_64BIT=y; export CONFIG_TIZEN_64BIT
%endif

cd mDNSPosix
#You should check below before change make flags or Makefile
mkdir -p objects/prod
mkdir -p build/prod
make os=tizen %{?_smp_mflags} CC="%{__cc}"

cd ../Clients
make os=tizen %{?_smp_mflags} CC="%{__cc}"

%install
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}/
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_libdir}/pkgconfig/

cp Clients/build/dns-sd %{buildroot}%{_bindir}/dns-sd

mkdir -p %{buildroot}%{_includedir}/
%if "%{?_lib}" == "lib64"
CONFIG_TIZEN_64BIT=y; export CONFIG_TIZEN_64BIT
%endif
cd mDNSPosix
make install os=tizen DESTDIR=%{buildroot} LIBDIR=/%{?_lib}
strip --strip-unneeded %{buildroot}%{_libdir}/libdns_sd.so.%{version}
ln -sf %{_libdir}/libdns_sd.so.%{version} %{buildroot}%{_libdir}/libdns_sd.so.1310
ln -sf %{_libdir}/libdns_sd.so.%{version} %{buildroot}%{_libdir}/libdns_sd.so

cd ..
mkdir -p %{buildroot}%{_unitdir}
cp mdnsd.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
ln -s ../mdnsd.socket %{buildroot}%{_unitdir}/sockets.target.wants/
cp mdnsd.socket %{buildroot}%{_unitdir}

%post

%post -n libdns_sd -p /sbin/ldconfig

%postun -n libdns_sd -p /sbin/ldconfig

%files
%manifest mdnsresponder.manifest
%license LICENSE
%attr(755,root,root) %{_sbindir}/mdnsd
%attr(-,root,root) %{_bindir}/dns-sd
%{_unitdir}/mdnsd.service
%{_unitdir}/mdnsd.socket
%{_unitdir}/sockets.target.wants/mdnsd.socket

%files devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files -n libdns_sd
%manifest libdns_sd.manifest
%license LICENSE
%{_libdir}/libdns_sd.so*
