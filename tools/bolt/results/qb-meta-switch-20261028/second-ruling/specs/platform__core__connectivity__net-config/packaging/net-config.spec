Name:		net-config
Summary:	TIZEN Network Configuration service
Version:	1.2.15
Release:	1
Group:		System/Network
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(vconf)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(capi-system-info)
BuildRequires:	pkgconfig(capi-vpnsvc)
BuildRequires:	cmake
BuildRequires:	pkgconfig(libtzplatform-config)
BuildRequires:	pkgconfig(key-manager)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(hal-api-wifi)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:  linux-glibc-devel
Requires:		vconf
Requires:		connman
Requires:		systemd
Requires:		security-config
Requires:		iproute2
Requires:		iptables
Requires(post):		systemd
Requires(preun):	systemd
Requires(postun):	systemd
Provides:       %{name}-profile_common = %{version}-%{release}
Provides:       %{name}-profile_mobile = %{version}-%{release}
Provides:       %{name}-profile_ivi = %{version}-%{release}
Provides:       %{name}-profile_robot = %{version}-%{release}

%description
TIZEN Network Configuration service

%package profile_tv
Summary:        net-config extension for TV profile
Requires:       %{name} = %{version}-%{release}
%description profile_tv
TIZEN Network Configuration service extension for Tizen TV profile.

%package profile_robot
Summary:        net-config extension for robot profile
Requires:       %{name} = %{version}-%{release}
%description profile_robot
TIZEN Network Configuration service extension for Tizen robot profile.

%package plugin-headed
Summary:        net-config extension for headed profile
BuildRequires:	pkgconfig(bundle)
BuildRequires:	pkgconfig(eventsystem)
BuildRequires:	pkgconfig(alarm-service)
BuildRequires:	pkgconfig(syspopup-caller)
BuildRequires:	pkgconfig(capi-appfw-application)
Requires:       %{name} = %{version}-%{release}
%description plugin-headed
TIZEN Network Configuration service extension for headed profile.

%package plugin-telephony
Summary:        net-config extension for telephony FW
BuildRequires:	pkgconfig(tapi)
Requires:       %{name} = %{version}-%{release}
%description plugin-telephony
TIZEN Network Configuration service extension for telephony FW.

%package plugin-stc
Summary:        net-config extension for STC FW
BuildRequires:	pkgconfig(capi-network-stc)
Requires:       %{name} = %{version}-%{release}
%description plugin-stc
TIZEN Network Configuration service extension for STC FW.

%package plugin-battery
Summary:        net-config extension for battery FW
Requires:       %{name} = %{version}-%{release}
%description plugin-battery
TIZEN Network Configuration service extension for battery FW.

%package haltests
Summary:        net-config extension for HAL test
BuildRequires:	pkgconfig(gmock)
BuildRequires:	pkgconfig(capi-network-wifi-manager)
BuildRequires:	pkgconfig(capi-network-wifi-direct)
BuildRequires:	pkgconfig(capi-network-softap)
Requires:       %{name} = %{version}-%{release}
%description haltests
TIZEN Network Configuration service extension for HAL test.

%prep
%setup -q

%build

# Build for common packages
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DTIZEN_WLAN_PASSPOINT=1 \
	-DTIZEN_WLAN_USE_P2P_INTERFACE=1 \
	-DTIZEN_DEBUG_ENABLE=0 \
	-DTIZEN_CAPTIVE_PORTAL=0 \
%if "%{?_lib}" == "lib64"
	-DTIZEN_ARCH_64=1 \
%endif
	-DLIB_PATH=%{_lib} \
	-DBIN_DIR=%{_bindir} \
	-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
	.

make %{?_smp_mflags}

%install
%make_install

#Settings file
mkdir -p %{buildroot}/%{_localstatedir}/lib/net-config
cp resources/var/lib/net-config/settings %{buildroot}/%{_localstatedir}/lib/net-config/settings
cp resources/var/lib/net-config/settings-robot %{buildroot}/%{_localstatedir}/lib/net-config/settings-robot

#Systemd service file
mkdir -p %{buildroot}%{_unitdir}

mkdir -p %{buildroot}%{_libdir}/udev/rules.d/
cp resources/usr/lib/udev/rules.d/99-wifiusb-dev.rules %{buildroot}%{_libdir}/udev/rules.d/99-wifiusb-dev.rules
cp resources/usr/lib/systemd/system/net-config_tv.service %{buildroot}%{_unitdir}/net-config.service.tv
cp resources/usr/lib/systemd/system/net-config.service %{buildroot}%{_unitdir}/net-config.service

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants/
ln -s ../net-config.service %{buildroot}%{_unitdir}/multi-user.target.wants/net-config.service

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp resources/usr/share/dbus-1/system-services/net.netconfig.service %{buildroot}%{_datadir}/dbus-1/system-services/net.netconfig.service

mkdir -p %{buildroot}%{TZ_SYS_ETC}
cp resources/etc/resolv.conf %{buildroot}%{TZ_SYS_ETC}/resolv.conf

mkdir -p %{buildroot}%{_sysconfdir}
ln -s %{TZ_SYS_ETC}/resolv.conf %{buildroot}%{_sysconfdir}/resolv.conf

#DBus DAC (net-config.manifest enables DBus SMACK)
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp resources/etc/dbus-1/system.d/net-config.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/net-config.conf
cp resources/etc/dbus-1/system.d/net-config-robot.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/net-config-robot.conf

#log dump
mkdir -p %{buildroot}/opt/etc/dump.d/module.d/
cp resources/opt/etc/dump.d/module.d/network_dump.sh %{buildroot}/opt/etc/dump.d/module.d/network_dump.sh
mkdir -p %{buildroot}/opt/var/lib/net-config/
cp resources/opt/etc/dump.d/module.d/network_dump.sh %{buildroot}/opt/var/lib/net-config/network_dump.sh
cp resources/opt/etc/dump.d/module.d/network_log_dump.sh %{buildroot}/opt/var/lib/net-config/network_log_dump.sh

%post
chsmack -a 'System::Shared' %{_sysconfdir}/resolv.conf
chsmack -a 'System::Shared' %{TZ_SYS_ETC}/resolv.conf

#Network logs
mkdir -p /opt/data/network
chmod 755 /opt/data/network
chown network_fw:network_fw /opt/data/network
#chsmack -a 'System' /opt/data/network

#systemctl daemon-reload
#systemctl restart net-config.service

%preun
#systemctl stop net-config.service

%postun
#systemctl daemon-reload


%files
%manifest net-config.manifest
%attr(500,network_fw,network_fw) %{_bindir}/net-config
%attr(644,network_fw,network_fw) %{_sysconfdir}/resolv.conf
%attr(644,network_fw,network_fw) %{TZ_SYS_ETC}/resolv.conf
%attr(644,root,root) %{_libdir}/udev/rules.d/99-wifiusb-dev.rules
%attr(644,root,root) %{_datadir}/dbus-1/system-services/*
#DBus DAC
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/*
%exclude %{_sysconfdir}/dbus-1/system.d/net-config-robot.conf
%attr(644,root,root) /usr/lib/tmpfiles.d/security-network-config.conf
%attr(644,root,root) %{_unitdir}/net-config.service
%attr(644,root,root) %{_unitdir}/multi-user.target.wants/net-config.service
%attr(644,root,root) /var/lib/net-config/settings
%license LICENSE
%attr(750,network_fw,network_fw) /opt/etc/dump.d/module.d/network_dump.sh
%attr(750,network_fw,network_fw) /opt/var/lib/net-config/network_dump.sh
%attr(750,network_fw,network_fw) /opt/var/lib/net-config/network_log_dump.sh

#### tv profile ####
%post profile_tv
mv %{_unitdir}/net-config.service.tv %{_unitdir}/net-config.service

%files profile_tv
%attr(644,root,root) %{_libdir}/udev/rules.d/99-wifiusb-dev.rules
%attr(644,root,root) %{_unitdir}/net-config.service.tv

#### robot profile ####
%post profile_robot
mv /var/lib/net-config/settings-robot /var/lib/net-config/settings
mv %{_sysconfdir}/dbus-1/system.d/net-config-robot.conf %{_sysconfdir}/dbus-1/system.d/net-config.conf

%files profile_robot
%manifest net-config.manifest
%attr(644,root,root) /var/lib/net-config/settings-robot
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/net-config-robot.conf


#### plugin ####
%files plugin-headed
%manifest net-config.manifest
%attr(500,network_fw,network_fw) %{_libdir}/net-config-plugin-headed.so

%files plugin-telephony
%manifest net-config.manifest
%attr(500,network_fw,network_fw) %{_libdir}/net-config-plugin-telephony.so

%files plugin-stc
%manifest net-config.manifest
%attr(500,network_fw,network_fw) %{_libdir}/net-config-plugin-stc.so

%files plugin-battery
%manifest net-config.manifest
%attr(500,network_fw,network_fw) %{_libdir}/net-config-plugin-battery.so

%files haltests
%manifest net-config.manifest
%{_bindir}/hal/*haltests
