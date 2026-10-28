%define enable_system_server 0

Name:           system-server
Summary:        System Server
Version:        10.0.0
Release:        0
Group:          System/Management
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     %{name}.service
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(united-service)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
Requires:       %{name}-worker

%description
System Server

%package worker
Summary:        Worker process of system server
License:        Apache-2.0

%description worker
Worker process of system server

%package worker-devel
Summary:        Worker process of system server
License:        Apache-2.0
Requires:       system-server-worker = %{version}

%description worker-devel
Development header file for system server worker library

%define _moddir %{_datadir}/united-service/%{name}

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DBINDIR=%{__bindir} \
	-DMODDIR=%{_moddir} \
	.

%__make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
install -d %{buildroot}/%{__bindir}

%make_install
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %SOURCE1002 %{buildroot}%{_unitdir}
%install_service multi-user.target.wants %{name}.service

%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%if %{enable_system_server}
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/multi-user.target.wants/%{name}.service
%{_moddir}/%{name}.loader
%{_sysconfdir}/dbus-1/system.d/org.tizen.system.systemserver.conf
%{_datadir}/dbus-1/system-services/org.tizen.system.systemserver.service
%else
%exclude %defattr(-,root,root,-)
%exclude %{_bindir}/%{name}
%exclude %{_unitdir}/%{name}.service
%exclude %{_unitdir}/multi-user.target.wants/%{name}.service
%exclude %{_moddir}/%{name}.loader
%exclude %{_sysconfdir}/dbus-1/system.d/org.tizen.system.systemserver.conf
%exclude %{_datadir}/dbus-1/system-services/org.tizen.system.systemserver.service
%endif

%files worker
%license LICENSE.APLv2
%if %{enable_system_server}
%{_bindir}/system-server-worker
%{_unitdir}/system-server-worker.service
%{_sysconfdir}/dbus-1/system.d/org.tizen.system.systemserver.worker.conf
%{_datadir}/dbus-1/system-services/org.tizen.system.systemserver.worker.service
%{_libdir}/libsystem-server-worker.so.*
%else
%exclude %{_bindir}/system-server-worker
%exclude %{_unitdir}/system-server-worker.service
%exclude %{_sysconfdir}/dbus-1/system.d/org.tizen.system.systemserver.worker.conf
%exclude %{_datadir}/dbus-1/system-services/org.tizen.system.systemserver.worker.service
%exclude %{_libdir}/libsystem-server-worker.so.*
%endif

%files worker-devel
%license LICENSE.APLv2
%if %{enable_system_server}
%{_includedir}/system-server-worker/*.h
%{_libdir}/pkgconfig/system-server-worker.pc
%{_libdir}/libsystem-server-worker.so
%else
%exclude %{_includedir}/system-server-worker/*.h
%exclude %{_libdir}/pkgconfig/system-server-worker.pc
%exclude %{_libdir}/libsystem-server-worker.so
%endif
