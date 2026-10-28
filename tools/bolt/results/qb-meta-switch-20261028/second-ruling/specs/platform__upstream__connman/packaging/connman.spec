%bcond_with     connman_openconnect
%bcond_without  connman_wireguard
%bcond_without  connman_openvpn
%bcond_without  connman_ipsec
%bcond_without  connman_vpnd

Name:           connman
Version:        1.42
Release:        4
License:        GPL-2.0+
Summary:        Connection Manager
Url:            http://connman.net
Group:          Network & Connectivity/Connection Management
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libiptc)
BuildRequires:  pkgconfig(xtables)
BuildRequires:  pkgconfig(libsmack)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(libsystemd)
%if %{with connman_openconnect}
BuildRequires:  openconnect
%endif
%if %{with connman_openvpn}
BuildRequires:  openvpn
%endif
%if %{with connman_ipsec}
BuildRequires:  strongswan
%endif
#%systemd_requires
Requires:       iptables
Requires:         systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires:         security-config
Provides:       %{name}-profile_common = %{version}-%{release}
Provides:       %{name}-profile_mobile = %{version}-%{release}
Provides:       %{name}-profile_wearable = %{version}-%{release}
Provides:       %{name}-profile_robot = %{version}-%{release}

%description
Connection Manager provides a daemon for managing Internet connections
within embedded devices running the Linux operating system.

%if %{with connman_openconnect}
%package plugin-openconnect
Summary:        Openconnect Support for Connman
Requires:       %{name} = %{version}
Requires:       openconnect

%description plugin-openconnect
Openconnect Support for Connman.
%endif

%if %{with connman_openvpn}
%package plugin-openvpn
Summary:        Openvpn Support for Connman
Requires:       %{name} = %{version}
Requires:       openvpn

%description plugin-openvpn
OpenVPN support for Connman.
%endif

%if %{with connman_ipsec}
%package plugin-ipsec
Summary:        IPsec Support for Connman
Requires:       %{name} = %{version}
Requires:       strongswan

%description plugin-ipsec
OpenVPN support for Connman.
%endif

%if %{with connman_vpnd}
%package connman-vpnd
Summary:        VPN Support for Connman
#BuildRequires:  %{name} = %{version}
Requires:       %{name} = %{version}

%description connman-vpnd
Provides VPN support for Connman
%endif

%if %{with connman_wireguard}
%package plugin-wireguard
Summary:        Wireguard Support for Connman
BuildRequires:  pkgconfig(libmnl)
Requires:       %{name} = %{version}

%description plugin-wireguard
Wireguard Support for Connman.
%endif

%package test
Summary:        Test Scripts for Connection Manager
Group:          Development/Tools
Requires:       %{name} = %{version}
Requires:       dbus-python
Requires:       pygobject
Requires:       python-xml

%description test
Scripts for testing Connman and its functionality

%package devel
Summary:        Development files for connman
Group:          Development/Tools
Requires:       %{name} = %{version}

%description devel
Header files and development files for connman.

%package extension-tv
Summary:        Connman service script for TV profile
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-profile_tv = %{version}-%{release}
Conflicts:      %{name}-extension-ivi
Conflicts:      %{name}-extension-disable-eth
%description extension-tv
Supplies Tizen TV profile systemd service scripts instead of the default one.
This overwrites service script of %{name}.

%package extension-ivi
Summary:        Connman configuration for IVI profile
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-profile_ivi = %{version}-%{release}
Conflicts:      %{name}-extension-tv
Conflicts:      %{name}-extension-disable-eth
%description extension-ivi
Supplies Tizen IVI profile configuration instead of the default one.
This overwrites conf file of %{name}.

%package extension-disable-eth
Summary:        Connman configuration for testing which requires the ethernet to be disabled
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name}-extension-tv
Conflicts:      %{name}-extension-ivi
%description extension-disable-eth
Connman without ethernet support
This overwrites conf file of %{name}.

%package profile_robot
Summary:		connman extension for robot profile
Requires:		%{name} = %{version}-%{release}
%description profile_robot
connman extension for Tizen robot profile

%package isu
Summary: connman ISU pacakge
Group:   Network & Connectivity/Connection Management
%description isu
Configuration files to generate the ISU (Individual Service Upgrade) package

%prep
%setup -q


%build
%if %{with connman_vpnd}
VPN_CFLAGS="$VPN_CFLAGS -DTIZEN_EXT -lsmack -Werror"
%endif

chmod +x bootstrap
./bootstrap
%configure \
	    --sysconfdir=/etc \
	    --enable-client \
	    --enable-tizen-ext \
	    --enable-tizen-ext-eap-on-ethernet \
	    --enable-pacrunner \
            --enable-wifi=builtin \
%if %{with connman_openconnect}
            --enable-openconnect \
%endif
%if %{with connman_openvpn}
            --enable-openvpn \
%endif
%if %{with connman_ipsec}
            --enable-ipsec \
%endif
%if %{without connman_wireguard}
            --disable-wireguard \
%endif
%if 0%{?enable_connman_features}
            %connman_features \
%endif
            --disable-ofono \
            --disable-telephony \
            --enable-test \
	    --enable-loopback \
	    --enable-ethernet \
	    --with-systemdunitdir=%{_unitdir} \
	    --enable-pie \
	    --disable-wispr \
	    --disable-backtrace \
	    --disable-tools

make %{?_smp_mflags}

%install
%make_install

#Systemd service file
mkdir -p %{buildroot}%{_unitdir}

cp src/connman_tv.service %{buildroot}%{_unitdir}/connman.service.tv
cp src/connman.service %{buildroot}%{_unitdir}/connman.service
cp vpn/connman-vpn.service %{buildroot}%{_unitdir}/connman-vpn.service

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
ln -s ../connman.service %{buildroot}%{_unitdir}/multi-user.target.wants/connman.service

#Systemd socket file for DNS proxy
cp src/connman.socket %{buildroot}%{_unitdir}/connman.socket
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
ln -s ../connman.socket %{buildroot}%{_unitdir}/sockets.target.wants/connman.socket

mkdir -p %{buildroot}/%{_localstatedir}/lib/connman
cp resources/var/lib/connman/settings %{buildroot}/%{_localstatedir}/lib/connman/settings
mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
cp resources/usr/share/dbus-1/system-services/net.connman.service %{buildroot}%{_datadir}/dbus-1/system-services/net.connman.service
mkdir -p %{buildroot}/etc/connman

cp src/main_ivi.conf %{buildroot}/etc/connman/main.conf.ivi
cp src/main_tv.conf %{buildroot}/etc/connman/main.conf.tv
cp src/main_disable_eth.conf %{buildroot}/etc/connman/main.conf.disable.eth
cp src/main_robot.conf %{buildroot}/etc/connman/main.conf.robot
cp src/main.conf %{buildroot}/etc/connman/main.conf

rm %{buildroot}%{_sysconfdir}/dbus-1/system.d/*.conf
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d/
cp src/connman.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/
cp src/connman-robot.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/

%if %{with connman_vpnd}
cp vpn/vpn-dbus.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/connman-vpn-dbus.conf
%endif

%post
#chsmack -a 'System' /%{_localstatedir}/lib/connman
#chsmack -a 'System' /%{_localstatedir}/lib/connman/settings

%preun

%postun
systemctl daemon-reload

%docs_package

%files
%manifest connman.manifest
%attr(500,network_fw,network_fw) %{_bindir}/connmand
%attr(500,network_fw,network_fw) %{_bindir}/connmanctl
%attr(600,network_fw,network_fw) /%{_localstatedir}/lib/connman/settings
%attr(644,root,root) %{_datadir}/dbus-1/system-services/net.connman.service
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/*
%exclude %{_sysconfdir}/dbus-1/system.d/connman-robot.conf
%attr(644,network_fw,network_fw) %{_sysconfdir}/connman/main.conf
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/*.conf
%attr(644,root,root) %{_unitdir}/connman.service
%attr(644,root,root) %{_unitdir}/multi-user.target.wants/connman.service
%attr(644,root,root) %{_unitdir}/connman.socket
%attr(644,root,root) %{_unitdir}/sockets.target.wants/connman.socket
%license COPYING

%files test
%manifest connman.manifest
%{_libdir}/%{name}/test/*

%files devel
%manifest connman.manifest
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%if %{with connman_openconnect}
%files plugin-openconnect
%manifest %{name}.manifest
%{_libdir}/connman/plugins-vpn/openconnect.so
%{_libdir}/connman/scripts/openconnect-script
%license COPYING
%endif

%if %{with connman_openvpn}
%files plugin-openvpn
%manifest %{name}.manifest
%{_libdir}/%{name}/plugins-vpn/openvpn.so
%{_libdir}/%{name}/scripts/openvpn-script
%license COPYING
%endif

%if %{with connman_ipsec}
%files plugin-ipsec
%manifest %{name}.manifest
%{_libdir}/%{name}/plugins-vpn/ipsec.so
%{_libdir}/%{name}/scripts/ipsec-script
%license COPYING
%endif

%if %{with connman_vpnd}
%files connman-vpnd
%manifest %{name}.manifest
%{_bindir}/connman-vpnd
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/scripts
%dir %{_libdir}/%{name}/plugins-vpn
%attr(644,root,root) %config %{_sysconfdir}/dbus-1/system.d/connman-vpn-dbus.conf
%{_datadir}/dbus-1/system-services/net.connman.vpn.service
%license COPYING
%attr(644,root,root) %{_unitdir}/connman-vpn.service
%endif

%if %{with connman_wireguard}
%files plugin-wireguard
%manifest %{name}.manifest
%{_libdir}/%{name}/plugins-vpn/wireguard.so
%license COPYING
%endif

%post extension-tv
mv -f %{_unitdir}/connman.service.tv %{_unitdir}/connman.service
mv -f %{_sysconfdir}/connman/main.conf.tv %{_sysconfdir}/connman/main.conf

%files extension-tv
%attr(644,network_fw,network_fw) %{_sysconfdir}/connman/main.conf.tv
%license COPYING
%attr(644,root,root) %{_unitdir}/connman.service.tv

%post extension-ivi
mv -f %{_sysconfdir}/connman/main.conf.ivi %{_sysconfdir}/connman/main.conf

%files extension-ivi
%attr(644,network_fw,network_fw) %{_sysconfdir}/connman/main.conf.ivi
%license COPYING

%post extension-disable-eth
mv -f %{_sysconfdir}/connman/main.conf.disable.eth %{_sysconfdir}/connman/main.conf

%files extension-disable-eth
%attr(644,network_fw,network_fw) %{_sysconfdir}/connman/main.conf.disable.eth
%license COPYING

%post profile_robot
mv %{_sysconfdir}/dbus-1/system.d/connman-robot.conf %{_sysconfdir}/dbus-1/system.d/connman.conf
mv -f %{_sysconfdir}/connman/main.conf.robot %{_sysconfdir}/connman/main.conf

%files profile_robot
%manifest %{name}.manifest
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/connman-robot.conf
%attr(644,network_fw,network_fw) %{_sysconfdir}/connman/main.conf.robot

%files isu
/etc/isu/connman/isu.cfg
/etc/isu/connman/system-services/connman.service
