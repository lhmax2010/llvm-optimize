
%define _unpackaged_files_terminate_build 0
%define daemon_name pass
%define haltest_name pass-haltests
%define unittest_name pass-unittest
%define libpass_resource_monitor_name libpass-resource-monitor
%define libunified_resource_name libunified-resource

%define ebpf_enabled            OFF
%define sysctl_tuner_module     OFF

Name:       %{daemon_name}
Summary:    Power Aware System Service
Version:    2.0.1
Release:    1
Group:      System/Kernel
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{libpass_resource_monitor_name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-common)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-pass)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(hal-api-power)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  ncurses-devel

%if "%{ebpf_enabled}" == "ON"
BuildRequires:  libsyscommon-ebpf-devel
%endif

%description
PASS  (Power-Aware System Service)

%package %{daemon_name}
Summary:    %{daemon_name} main
Group:      main

%description %{daemon_name}
PASS systemd daemon.

%package -n 	%{haltest_name}
Summary: 	PASS HAL test package with gtest
Group:		Development/Tools
Requires:	pass = %{version}-%{release}

%description -n	%{haltest_name}
PASS HAL test package with gtest

%package -n 	%{unittest_name}
Summary: 	PASS unit test package with gtest
Group:		Development/Tools
Requires:	pass = %{version}-%{release}

%description -n	%{unittest_name}
PASS unit test package with gtest

%package -n 	%{libpass_resource_monitor_name}
Summary: 	Tizen Monitor Library package
Group:		Development/Libraries
Requires:	pass = %{version}-%{release}

%description -n	%{libpass_resource_monitor_name}
Tizen Monitor Library package

%package -n 	%{libpass_resource_monitor_name}-devel
Summary: 	Tizen Monitor Headler Files
Group:		Development/Libraries
Requires:	pass = %{version}-%{release}
Requires:	libpass-resource-monitor = %{version}-%{release}

%description -n	%{libpass_resource_monitor_name}-devel
Tizen Monitor Headler Files

%if "%{ebpf_enabled}" == "ON"
%package -n 	pass-resource-monitor-plugin-network
Summary: 	PASS Resource Monitor Network Plugin
Group:		System/Libraries
Requires:	pass = %{version}-%{release}
Requires:	libpass-resource-monitor = %{version}-%{release}

%description -n	pass-resource-monitor-plugin-network
Network resource monitor plugin that extends PASS monitoring capabilities.
Provides TCP retransmission, latency, and socket backlog monitoring via eBPF.

%package -n 	pass-resource-monitor-plugin-network-devel
Summary: 	PASS Resource Monitor Network Plugin Development Headers
Group:		Development/Libraries
Requires:	pass-resource-monitor-plugin-network = %{version}-%{release}
Requires:	libpass-resource-monitor-devel = %{version}-%{release}

%description -n	pass-resource-monitor-plugin-network-devel
Development headers for PASS network resource monitor plugin.
Provides network attribute ID definitions for client applications.
%endif

%prep
%setup -q

%cmake . \
	-DCMAKE_C_COMPILER=%__cc \
	-DCMAKE_CXX_COMPILER=%__cxx \
	-DTZ_SYS_ETC=%TZ_SYS_ETC \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_LIBDIR_PREFIX=%{_libdir} \
	-DEBPF_ENABLED=%{ebpf_enabled} \
	-DSYSCTL_TUNER_MODULE=%{sysctl_tuner_module} \
	#eol

%build
cp %{SOURCE1} .
cp %{SOURCE2} .
make %{?jobs:-j%jobs}

%check
(cd tests/unittest/pass-hal-and-parser && LD_LIBRARY_PATH=../../ ctest -V)
(cd tests/unittest/pass-rescon && LD_LIBRARY_PATH=../../ ctest -V)
(cd tests/unittest/pass-resmon && LD_LIBRARY_PATH=../../ ctest -V)

%install
rm -rf %{buildroot}
%make_install

%install_service delayed.target.wants %{daemon_name}.service
%install_service sockets.target.wants %{daemon_name}-resource-monitor.socket

%post

systemctl daemon-reload
if [ "$1" == "1" ]; then
    systemctl restart %{daemon_name}.service
fi

%preun
if [ "$1" == "0" ]; then
    systemctl stop %{daemon_name}.service
fi

%postun
systemctl daemon-reload

%files -n %{daemon_name}
%manifest %{name}.manifest
%license LICENSE
%config %{_sysconfdir}/dbus-1/system.d/%{daemon_name}.conf
%config %{_sysconfdir}/pass/pass-pmqos.json
%config %{_sysconfdir}/pass/pass-thermal.json
%config %{_sysconfdir}/pass/pass-sysctl.json
%{_bindir}/%{daemon_name}
%{_bindir}/resource-monitor
%{_unitdir}/delayed.target.wants/%{daemon_name}.service
%{_unitdir}/sockets.target.wants/%{daemon_name}-resource-monitor.socket
%{_unitdir}/%{daemon_name}.service
%{_unitdir}/%{daemon_name}-resource-monitor.socket
%{_datadir}/dbus-1/system-services/org.tizen.system.pass.service
%{_datadir}/dbus-1/system-services/org.tizen.system.thermal.service

%files -n %{haltest_name}
%defattr(-,root,root,-)
%{_bindir}/hal/power-haltests

%files -n %{unittest_name}
%defattr(-,root,root,-)
%{_bindir}/pass-tests
%{_bindir}/resource-monitor-tests

%files -n %{libpass_resource_monitor_name}
%license LICENSE
%manifest %{libpass_resource_monitor_name}.manifest
%defattr(-,root,root,-)
%{_libdir}/%{libpass_resource_monitor_name}*.so*

%files -n %{libpass_resource_monitor_name}-devel
%license LICENSE
%manifest %{libpass_resource_monitor_name}.manifest
%defattr(-,root,root,-)
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/%{libpass_resource_monitor_name}.pc

%if "%{ebpf_enabled}" == "ON"
%files -n pass-resource-monitor-plugin-network
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/resource-monitor/plugins/libresource-monitor-plugin-network.so

%files -n pass-resource-monitor-plugin-network-devel
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/resource-monitor-plugins/network-attributes.h
%endif
