Name:		wifi-direct-manager
Summary:	Wi-Fi Direct manger
Version:	1.4.3
Release:	1
Group:      Network & Connectivity/Wireless
License:    Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1:	dbus-wfd-manager.conf
Source2:	net.wifidirect.service
Source3:	wifi-direct-manager.service

BuildRequires:	pkgconfig(capi-network-wifi-direct)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(vconf)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(aul)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:	pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(hal-api-wifi)
%if 0%{?gtests:1}
BuildRequires: pkgconfig(gmock)
%endif
BuildRequires:	cmake

Requires:	net-tools
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Manager for handling wifi-direct functionalities

%package profile_tv
Summary:	Wi-Fi Direct manager for tv
Requires:	%{name} = %{version}-%{release}
%description profile_tv
Manager for handling wifi-direct functionalities for tv

%package -n wifi-direct-plugin-wpasupplicant
Summary:    Wifi direct plugin for wpa supplicant
Group:      Network & Connectivity/Wireless
Requires:   %{name} = %{version}-%{release}
%description -n wifi-direct-plugin-wpasupplicant
Wi-Fi direct manager plugin to abstract wpa_supplicant

#%package -n wifi-direct-prd-plugin-wpasupplicant
#Summary:    Wifi direct prd plugin for wpa supplicant
#Group:      Network & Connectivity/Wireless
#Requires:   %{name} = %{version}-%{release}
#%description -n wifi-direct-prd-plugin-wpasupplicant
#Wi-Fi direct manager prd plugin to abstract wpa_supplicant

%prep
%setup -q
chmod 644 %{SOURCE0}
chmod 644 %{SOURCE1}
chmod 644 %{SOURCE2}
chmod 644 %{SOURCE3}
cp -a %{SOURCE1} ./wfd-manager.conf
cp -a %{SOURCE2} .
cp -a %{SOURCE3} .

%build

export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%ifarch %{arm}
export ARCH=arm
%else

%if 0%{?simulator}
export ARCH=emul
%else
export ARCH=i586
%endif

%endif

%if 0%{?asan:1}
export CFLAGS+=" -Wno-stringop-truncation"
export CXXFLAGS+=" -Wno-stringop-truncation"
%endif

%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DARCHITECTURE=$ARCH \
%if ! 0%{?model_build_feature_network_tethering_disable}
	-DTIZEN_TETHERING_ENABLE=0 \
%endif
	-DTIZEN_DEBUG_DBUS_VALUE=1 \
%if "%{?_lib}" == "lib64"
	-DTIZEN_ARCH_64=1 \
%endif
	-DLIB_DIR=%{_libdir} \
	-DBIN_DIR=%{_bindir} \
	-DSBIN_DIR=%{_sbindir} \
	-DTZ_SYS_RO_ETC=%{TZ_SYS_RO_ETC} \
	-DTZ_SYS_VAR=%{TZ_SYS_VAR} \
	-DTZ_SYS_ETC=%{TZ_SYS_ETC} \
	-DTZ_SYS_RUN=%{TZ_SYS_RUN} \
	-DBUILD_DHCP_TEST=%{?dhcp_test:1}%{!?dhcp_test:0} \
	-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/wifi-direct

# Install tv profile configuration
cp files/wifi-direct-manager.conf.tv %{buildroot}/etc/wifi-direct/wifi-direct-manager.conf.tv

%make_install

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
cp wfd-manager.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/wfd-manager.conf
mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services/
cp net.wifidirect.service %{buildroot}%{_datadir}/dbus-1/system-services/net.wifidirect.service
mkdir -p %{buildroot}%{_unitdir}
cp wifi-direct-manager.service %{buildroot}%{_unitdir}/wifi-direct-manager.service

%post
chmod 644 %{TZ_SYS_RO_ETC}/wifi-direct/wifi-direct-manager.conf
chmod 755 %{_bindir}/wifi-direct-server.sh
chmod 755 %{_sbindir}/p2p_supp.sh

if [ ! -d %{TZ_SYS_VAR}/lib/misc ]; then
	mkdir -p %{TZ_SYS_VAR}/lib/misc
fi

touch %{TZ_SYS_VAR}/lib/misc/dhcpd.leases
chmod 666 %{TZ_SYS_VAR}/lib/misc/dhcpd.leases


# This is for tv
%post profile_tv
mv -f %{_sysconfdir}/wifi-direct/wifi-direct-manager.conf.tv %{_sysconfdir}/wifi-direct/wifi-direct-manager.conf

%files
%manifest wifi-direct-manager.manifest
%license LICENSE
%defattr(-,network_fw,network_fw,-)
%config %{TZ_SYS_RO_ETC}/wifi-direct/ccode.conf
%config %{TZ_SYS_RO_ETC}/wifi-direct/wifi-direct-manager.conf
%config %{_sysconfdir}/dbus-1/system.d/wfd-manager.conf
%attr(755,-,-) %{_bindir}/wifi-direct-server.sh
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/wfd-manager.conf
%attr(644,root,root) %{_datadir}/dbus-1/system-services/*
%attr(644,root,root) %{_unitdir}/wifi-direct-manager.service
%attr(755,-,-) %{_sbindir}/p2p_supp.sh
%attr(755,-,-) %{_bindir}/wfd-manager
%if 0%{?gtests:1}
	%{_bindir}/gtest*
%endif
%if 0%{?dhcp_test:1}
%{_bindir}/dhcpd-test
%endif

%files -n wifi-direct-plugin-wpasupplicant
%manifest wifi-direct-plugin-wpasupplicant.manifest
%license LICENSE
%defattr(-,network_fw,network_fw,-)
%{_libdir}/wifi-direct-plugin-wpasupplicant.so

%files profile_tv
%attr(644,network_fw,network_fw) %{_sysconfdir}/wifi-direct/wifi-direct-manager.conf.tv

#%files -n wifi-direct-prd-plugin-wpasupplicant
#%manifest wifi-direct-prd-plugin-wpasupplicant.manifest
#%license LICENSE
#%defattr(-,network_fw,network_fw,-)
#%{_libdir}/wifi-direct-prd-plugin-wpasupplicant.so
