%define _inm_error_analysis "yes"

Name:       inm-manager
Summary:    INM(Intelligent Network Monitoring) daemon
Version:    0.0.35
Release:    1
Group:      Network & Connectivity/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    dbus-%{name}.conf
Source2:    net.inm-manager.service
Source3:	%{name}.service

BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(libnl-route-3.0)
BuildRequires:  pkgconfig(libcares)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python
BuildRequires:  python-xml
Requires:       security-config

%if 0%{?gtests:1}
BuildRequires: pkgconfig(gmock)
%endif

%if 0%{?gcov:1}
BuildRequires: lcov
%endif

%description
An application service platform manager to manage services and sessions

%prep
%setup -q
chmod 644 %{SOURCE0}
chmod 644 %{SOURCE1}
chmod 644 %{SOURCE2}
chmod 644 %{SOURCE3}
cp -a %{SOURCE1} ./inm-manager.conf
cp -a %{SOURCE2} .
cp -a %{SOURCE3} .

%build

export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -Wno-error=incompatible-pointer-types -Wno-error=int-conversion"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBIN_DIR=%{_bindir} \
%if %{_inm_error_analysis} == "yes"
	-DBUILD_ERROR_ANALYSIS=%{?_inm_error_analysis:1}%{!?_inm_error_analysis:0} \
%endif
	-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
	-DBUILD_TEST_APP=%{?test_app:1}%{!?test_app:0}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%make_install

mkdir -p %{buildroot}/%{_localstatedir}/lib/inm-manager
cp resources/var/lib/inm-manager/settings %{buildroot}/%{_localstatedir}/lib/inm-manager/settings

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp net.inm-manager.service %{buildroot}%{_datadir}/dbus-1/system-services/net.inm_manager.service

#DBus DAC (net-config.manifest enables DBus SMACK)
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp inm-manager.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/inm-manager.conf
mkdir -p %{buildroot}%{_unitdir}
cp inm-manager.service %{buildroot}%{_unitdir}/inm-manager.service

#log dump
mkdir -p %{buildroot}/opt/etc/dump.d/module.d
#udev rules for wlan module attach/detach event
#mkdir -p %{buildroot}%{_libdir}/udev/rules.d/
#cp resources/usr/lib/udev/rules.d/99-wifiusb-dev.rules %{buildroot}%{_libdir}/udev/rules.d/99-wifiusb-dev.rules

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,network_fw,network_fw,-)
%attr(500,network_fw,network_fw) %{_bindir}/*
%attr(500,root,root) /opt/etc/dump.d/module.d/inm_network_dump.sh
%attr(600,network_fw,network_fw) /%{_localstatedir}/lib/inm-manager/settings
#%attr(644,root,root) %{_libdir}/udev/rules.d/99-wifiusb-dev.rules
%if 0%{?gtests:1}
	%{_bindir}/gtest*
%endif
%if 0%{?test_app:1}
	%{_bindir}/network_monitoring_test
%endif

#DBus DAC
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/inm-manager.conf
%attr(644,root,root) %{_datadir}/dbus-1/system-services/net.inm_manager.service
%attr(644,root,root) %{_unitdir}/inm-manager.service