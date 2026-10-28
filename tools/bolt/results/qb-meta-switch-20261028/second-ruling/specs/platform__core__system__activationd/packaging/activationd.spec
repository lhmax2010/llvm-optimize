%define with_activationd_glib_support 1

Name:       activationd
Version:    0.2.2
Release:    0
License:    Apache-2.0, MIT
Source0:    %{name}-%{version}.tar.xz
Source1001: %{name}.manifest
Summary:    Event-based activation daemon
Group:      System/Monitoring
Requires:   activationd-plugin
BuildRequires: pkgconfig(vconf)

BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(json-c)
%if %{with_activationd_glib_support}
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libsyscommon)
%endif
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(dlog)

%description
Activationd allows starting systemd units based on various system events.

%package -n activationd-test-services
Summary:    activationd test services
Group:      System/Monitoring
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(glib-2.0)
Requires:   activationd

%description -n activationd-test-services
Services used to test activationd functionality

%package -n event-processing-devel
Summary:    epcd development files
Group:      System/Monitoring

%description  -n event-processing-devel
Files used in external modules development

%package -n libactd
Summary:    Activationd API
Group:      Development/Libraries
License:    MIT

%description -n libactd
This library provides API for interaction with modules

%package -n libactd-devel
Summary:    Activationd API development files
Group:      Development/Libraries
Requires:   libactd = %{version}

%description -n libactd-devel
This library provides development files needed for libactd.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%autogen
%configure \
	--libdir=%{_libdir} \
%if %{with_activationd_glib_support}
	--enable-glib-mainloop \
%endif
	--enable-unit-tests \
	--enable-forced-reboot

make %{?_smp_mflags}

make check

%install
%make_install

mkdir -p %{buildroot}/%{_unitdir}/basic.target.wants
ln -s ../actd.service %{buildroot}/%{_unitdir}/basic.target.wants/actd.service

ln -s %{_sbindir}/actd %{buildroot}/%{_sbindir}/actdctl

%define moduledir %{_libdir}/actd/available-modules/
%define moduleconfdir %{_sysconfdir}/actd/available-modules/
%define enabled_moduledir %{_sysconfdir}/actd/enabled-modules/

mkdir -p %{buildroot}/%{moduledir}
mkdir -p %{buildroot}/%{moduleconfdir}
mkdir -p %{buildroot}/%{enabled_moduledir}

# install_module <module> <package>
%define install_module() \
	ln -s %{moduledir}/%1.so %{buildroot}/%{moduleconfdir}/%1.so; \
	ln -s ../available-modules/%1.so %{buildroot}/%{enabled_moduledir}/%1.so; \
	echo %{moduledir}/%1.so >> %2-files; \
	echo %{moduleconfdir}/%1.so >> %2-files; \
	echo %{enabled_moduledir}/%1.so >> %2-files;

%install_module service_restart_action core
%install_module unit_start_action core
%install_module forward_signal_action core
%install_module vconf_key_changed_event core
%install_module vconf_listener core
%install_module dbus_signal_event core
%install_module dbus_listener core
%install_module unit_control_api core
%install_module unit_control_event core
%install_module unit_control_dm core
%install_module activation_dm core

%files -f core-files
%license COPYING
%manifest %{name}.manifest
%{_sbindir}/actd
%{_sbindir}/actdctl
%{_libdir}/actd/actd.conf
%{_unitdir}/actd.service
%{_unitdir}/basic.target.wants/actd.service
%dir %{_libdir}/actd/modules.conf.d
%{_libdir}/actd/modules.conf.d/activation_eh.conf.d/50-default.conf
%{_libdir}/actd/modules.conf.d/vconf_listener.conf.d/50-default.conf
%{_libdir}/actd/modules.conf.d/dbus_listener.conf.d/50-default.conf
%{_libdir}/actd/modules.conf.d/unit_control_eh.conf.d/50-default.conf
%{_sysconfdir}/dbus-1/system.d/org.tizen.activationd.conf
%{_datadir}/dbus-1/system-services/org.tizen.activationd.service

%files -n libactd
%license LICENSE.MIT
%{_libdir}/libactd.so.*

%files -n libactd-devel
%{_libdir}/libactd.so
%{_libdir}/pkgconfig/libactd.pc
%{_includedir}/actd/*

%files -n event-processing-devel
%license COPYING
%{_libdir}/pkgconfig/epc.pc
%{_includedir}/epc/*

%files -n activationd-test-services
%license COPYING
%manifest %{name}.manifest
%{_bindir}/activationd_unit_tests
%{_bindir}/activationd_acceptance_checker
%{_bindir}/activationd_acceptance_test
%{_bindir}/activationd_acceptance_service
%{_unitdir_user}/activationd-acceptance-test-s-p.service
%{_unitdir}/activationd-acceptance-test-s-p.service
%{_unitdir}/activationd-acceptance-test-s-n.service
%{_unitdir}/activationd-acceptance-test-i-p.service
%{_unitdir}/activationd-acceptance-test-i-n.service
%{_unitdir}/activationd-acceptance-test-d-p.service
%{_unitdir}/activationd-acceptance-test-d-n.service
%{_unitdir}/activationd-acceptance-test-b-p.service
%{_unitdir}/activationd-acceptance-test-b-n.service
%{_libdir}/actd/modules.conf.d/vconf_listener.conf.d/99-acceptance-test.conf
%{_libdir}/actd/modules.conf.d/dbus_listener.conf.d/99-acceptance-test.conf
%{_libdir}/actd/modules.conf.d/activation_eh.conf.d/99-acceptance-test.conf
%{_libdir}/actd/modules.conf.d/unit_control_eh.conf.d/99-acceptance-test.conf

%docs_package
