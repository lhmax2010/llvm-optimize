Name:           libtirpc
VCS:            platform/upstream/libtirpc#7623cb042a74f4dfb2d3fe0dc4db0cf3863dd3f0
Version:        1.3.3
Release:        1.1
License:        BSD-4-Clause
Summary:        Transport Independent RPC Library
Url:            http://sourceforge.net/projects/libtirpc/
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source1001:     libtirpc.manifest
BuildRequires:  libtool
BuildRequires:  krb5-devel
BuildRequires:  pkgconfig(pkg-config)

%description
The Transport Independent RPC library (TI-RPC) is a replacement for the
standard SunRPC library in glibc which does not support IPv6 addresses.
This implementation allows the support of other transports than UDP and
TCP over IPv4

%package devel
License:        BSD-4-Clause
Summary:        Transport Independent RPC Library
Group:          System/Libraries
Requires:       glibc-devel
Requires:       libtirpc = %{version}

%description devel
The Transport Independent RPC library (TI-RPC) is a replacement for the
standard SunRPC library in glibc which does not support IPv6 addresses.
This implementation allows the support of other transports than UDP and
TCP over IPv4

%prep
%setup -q
cp %{SOURCE1001} .

%build
%reconfigure --disable-static --with-pic --libdir=/%{_lib}
%__make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_libdir}
ln -sf -v /%{_lib}/$(readlink %{buildroot}/%{_lib}/%{name}.so) %{buildroot}%{_libdir}/%{name}.so
rm -rf %{buildroot}/%{_lib}/*.so
rm -f %{buildroot}/etc/bindresvport.blacklist
mv -v %{buildroot}/%{_lib}/pkgconfig %{buildroot}/%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%config %{_sysconfdir}/netconfig
/%{_lib}/libtirpc.so.3*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libtirpc.so
%{_includedir}/tirpc/*
%{_libdir}/pkgconfig/*

%docs_package
%changelog
* Sat May 11 2013 Anas Nashif <anas.nashif@intel.com> submit/tizen/20130509.181316@741ca4b
- Set license using %%license
