Name:           pacrunner
Version:        0.9
Release:        0
License:        GPL-2.0+
Url:            http://connman.net/
Summary:        Proxy configuration daemon
Group:          Connectivity/Connection Management
Source:         %{name}-%{version}.tar.gz
Source1001: 	pacrunner.manifest
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libcurl)
%description
PACrunner - Proxy configuration daemon.

%package test
Summary:        Test Scripts for pacrunner
Group:          Development/Tools
Requires:       %{name} = %{version}

%description test
PACrunner - Proxy configuration daemon.

Pacrunner tests

%package  proxy-tools
Summary:        Libproxy library Tools
Group:          Connectivity/Connection Management
Requires:       %{name}-libproxy = %{version}

%description proxy-tools
PACrunner - Proxy configuration daemon.

Libproxy library Tools.

%package libproxy
Summary:        Libproxy library
Group:          Connectivity/Connection Management
License:        LGPL-2.1
Requires:       %{name} = %{version}
Provides:       libproxy <= 0.4.11-2
Obsoletes:      libproxy <= 0.4.11-2
Provides:       libproxy-pacrunner-webkit <= 0.4.11-2
Obsoletes:      libproxy-pacrunner-webkit <= 0.4.11-2

%description libproxy
PACrunner - Proxy configuration daemon.

Libproxy library.

%package libproxy-devel
Summary:        Libproxy library Development Files
Group:          Development/Libraries
Requires:       pacrunner-libproxy = %{version}
Provides:       libproxy-devel <= 0.4.11-2
Obsoletes:      libproxy-devel <= 0.4.11-2

%description  libproxy-devel
PACrunner - Proxy configuration daemon.

Libproxy library Development Files.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%reconfigure --enable-libproxy \
            --enable-curl \
            --enable-test
make %{?_smp_mflags}

%install
%make_install


%post  libproxy -p /sbin/ldconfig

%postun  libproxy -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/dbus-1/system.d/pacrunner.conf
/usr/sbin/pacrunner
/usr/share/dbus-1/system-services/org.pacrunner.service

%files  proxy-tools
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/proxy

%files  libproxy
%manifest %{name}.manifest
%license COPYING.LIB
%defattr(-,root,root)
%{_libdir}/libproxy.so.*

%files  libproxy-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/proxy.h
%{_libdir}/libproxy.so
%{_libdir}/pkgconfig/libproxy-1.0.pc

%files test
%manifest %{name}.manifest
%{_libdir}/pacrunner/test/create-proxy-config
%{_libdir}/pacrunner/test/find-proxy-for-url
%{_bindir}/manual-proxy-test

%changelog
