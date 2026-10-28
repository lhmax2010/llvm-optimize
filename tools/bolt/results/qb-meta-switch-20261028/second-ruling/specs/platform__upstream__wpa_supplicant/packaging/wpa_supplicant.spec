Name:           wpa_supplicant
Version:        2.12
Release:        1
License:        BSD-2.0 and GPL-2.0+
Summary:        WPA supplicant implementation
Url:            http://hostap.epitest.fi/wpa_supplicant/
Group:          Network & Connectivity/Wireless
Source0:    %{name}-%{version}.tar.gz
Source1001:     wpa_supplicant.manifest

BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-genl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
BuildRequires: pkgconfig(libtzplatform-config)
Requires:      security-config
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

# for multiprofile
Requires:   %{name}-compat = %{version}-%{release}
Recommends: %{name}-profile_common = %{version}-%{release}

Provides:	%{name}-profile_robot = %{version}-%{release}

%description
wpa_supplicant is an implementation of the WPA Supplicant component,
i.e., the part that runs in the client stations. It implements key
negotiation with a WPA Authenticator and it controls the roaming and
IEEE 802.11 authentication/association of the wlan driver.

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if common || ivi || wearable || "undefined"
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv"
%package profile_common
Summary:	wpa_supplicant for common
Provides:	%{name}-compat = %{version}-%{release}
Provides:	%{name}-profile_ivi = %{version}-%{release}
Provides:	%{name}-profile_wearable = %{version}-%{release}
Conflicts:	%{name}-profile_tv
Conflicts:	%{name}-extension-TM1
Conflicts:	%{name}-extension-TM2

%description profile_common
wpa_supplicant for common/ivi/wearable.
%endif


# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
# For TM1
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%package extension-TM1
Summary:	Extension for mobile TM1
Provides:	%{name}-compat = %{version}-%{release}
Conflicts:	%{name}-profile_tv
Conflicts:	%{name}-profile_common
Conflicts:	%{name}-extension-TM2

%description extension-TM1
Customized wpa_supplicant supporting SPRD-based boards including TM1.
Having such ifdefs in public Tizen is really ugly, but for the sake
of backward-compatibility, we have this subpackage. Please remove
such variations later.
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
# For TM2(wayland)
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%package extension-TM2
Summary:	Extension for mobile TM2
Provides:	%{name}-compat = %{version}-%{release}
Conflicts:	%{name}-profile_tv
Conflicts:	%{name}-profile_common

%description extension-TM2
Customized wpa_supplicant supporting BROADCOM-based boards including TM1.
Having such ifdefs in public Tizen is really ugly, but for the sake
of backward-compatibility, we have this subpackage. Please remove
such variations later.
%endif


# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "mobile" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%package profile_tv
Summary:	Patched wpa_supplicant for TV
Provides:	%{name}-compat = %{version}-%{release}
Conflicts:	%{name}-extension-TM1
Conflicts:	%{name}-extension-TM2
Conflicts:	%{name}-profile_common

%description profile_tv
TV-profile somehow wants to disable WPA_DRIVER_FLAGS_DEDICATED_P2P_DEVICE
unconditionally at wpa_supplicant/wpa_supplicant.c. It should later be
determined at runtime/boottime, not at buildtime.
%endif

%package client_tool
Summary:	Text-based client tool for wpa_supplicant and hostapd
Provides:	%{name}-compat = %{version}-%{release}

%description client_tool
Text-based frontend programs for interacting with wpa_supplicant and hostapd.
It is used to query current status, change configuration,
trigger events, and request interactive user input.

%package profile_robot
Summary:	Patched wpa_supplicant for robot profile
Requires:	%{name} = %{version}-%{release}

%description profile_robot
Extension for Tizen robot profile

%prep
%setup -q

%build
cp %{SOURCE1001} .
cp -v configurations/tizen.config wpa_supplicant/.config
cp -v configurations/tizen_hostapd.config hostapd/.config

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
# build for tm1 extension. only wpa_supplicant and hostapd are different
CONFIG_TIZEN_WLAN_BOARD_SPRD=y; export CONFIG_TIZEN_WLAN_BOARD_SPRD

mkdir -p extension-TM1
make %{?_smp_mflags} -C wpa_supplicant all
make -C hostapd clean
make %{?_smp_mflags} -C hostapd all
cp wpa_supplicant/wpa_supplicant extension-TM1/wpa_supplicant.tm1
cp hostapd/hostapd extension-TM1/hostapd.tm1
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
# For TM2(wayland)
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
# build for tm2 extension. only wpa_supplicant and hostapd are different
unset CONFIG_TIZEN_WLAN_BOARD_SPRD

mkdir -p extension-TM2
make -C wpa_supplicant clean
make %{?_smp_mflags} -C wpa_supplicant all
make -C hostapd clean
make %{?_smp_mflags} -C hostapd all
cp wpa_supplicant/wpa_supplicant extension-TM2/wpa_supplicant.tm2
cp hostapd/hostapd extension-TM2/hostapd.tm2
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "mobile" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
# build for tv profile subpackage. only wpa_supplicant is different
unset CONFIG_TIZEN_WLAN_BOARD_SPRD
CONFIG_TIZEN_TV_BOARD_PRD=y; export CONFIG_TIZEN_TV_BOARD_PRD

mkdir -p profile_tv
make -C wpa_supplicant clean
make %{?_smp_mflags} -C wpa_supplicant all
cp wpa_supplicant/wpa_supplicant profile_tv/wpa_supplicant.tv
%endif

# build for other common cases.
unset CONFIG_TIZEN_TV_BOARD_PRD

make -C wpa_supplicant clean
make %{?_smp_mflags} -C wpa_supplicant all
make -C hostapd clean
make %{?_smp_mflags} -C hostapd all

%install
mkdir -p %{buildroot}%{_bindir}/systemd/
mkdir -p %{buildroot}%{TZ_SYS_VAR}/lib/hostapd

cp -v wpa_supplicant/wpa_cli %{buildroot}%{_bindir}/
cp -v hostapd/hostapd %{buildroot}%{_bindir}/
cp -v hostapd/hostapd_cli %{buildroot}%{_bindir}/
cp -v files/wpa_supp.sh %{buildroot}%{_bindir}/

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if common || ivi || wearable || "undefined"
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv"
cp -v wpa_supplicant/wpa_supplicant %{buildroot}%{_bindir}/
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
# For TM1
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
cp -v extension-TM1/* %{buildroot}%{_bindir}/
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
# For TM2(wayland)
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
cp -v extension-TM2/* %{buildroot}%{_bindir}/
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "mobile" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
cp -v profile_tv/* %{buildroot}%{_bindir}/
%endif

# Configurations
mkdir -p %{buildroot}%{TZ_SYS_ETC}/wpa_supplicant/
mkdir -p %{buildroot}%{_sysconfdir}/wpa_supplicant/
cp -v wpa_supplicant/wpa_supplicant.conf %{buildroot}%{TZ_SYS_ETC}/wpa_supplicant/wpa_supplicant.conf
cp -v hostapd/hostapd.conf %{buildroot}%{_sysconfdir}/wpa_supplicant/hostapd.conf

# hostapd whilte/block list for MAC filtering
cp -v hostapd/hostapd.accept %{buildroot}%{TZ_SYS_VAR}/lib/hostapd/hostapd.accept
cp -v hostapd/hostapd.deny %{buildroot}%{TZ_SYS_VAR}/lib/hostapd/hostapd.deny
cp -v hostapd/.hostapd_tmp %{buildroot}%{TZ_SYS_VAR}/lib/hostapd/.hostapd_tmp

# D-Bus
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d/
cp wpa_supplicant/dbus/dbus-wpa_supplicant.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/wpa_supplicant.conf
cp wpa_supplicant/dbus/dbus-wpa_supplicant-robot.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/dbus-wpa_supplicant-robot.conf

# sanitise the example configuration
mkdir -p %{buildroot}%{_defaultdocdir}/wpasupplicant
sed 's/^\([^#]\+=.*\|}\)/#\1/' < ./wpa_supplicant/wpa_supplicant.conf | gzip > %{buildroot}%{_defaultdocdir}/wpasupplicant/README.wpa_supplicant.conf.gz

rm -rf %{buildroot}%{_sbindir}/systemd/
rm -rf %{buildroot}%{_sbindir}/wpa_passphrase

%post
/sbin/ldconfig
# Access control for hostapd accept/deny list
chgrp priv_tethering_admin %{TZ_SYS_VAR}/lib/hostapd/hostapd.accept
chmod g+rwX %{TZ_SYS_VAR}/lib/hostapd/hostapd.accept
chmod o= %{TZ_SYS_VAR}/lib/hostapd/hostapd.accept
chsmack -a "*" %{TZ_SYS_VAR}/lib/hostapd/hostapd.accept
chgrp priv_tethering_admin %{TZ_SYS_VAR}/lib/hostapd/hostapd.deny
chmod g+rwX %{TZ_SYS_VAR}/lib/hostapd/hostapd.deny
chmod o= %{TZ_SYS_VAR}/lib/hostapd/hostapd.deny
chsmack -a "*" %{TZ_SYS_VAR}/lib/hostapd/hostapd.deny
chgrp priv_tethering_admin %{TZ_SYS_VAR}/lib/hostapd/.hostapd_tmp
chmod g+rwX %{TZ_SYS_VAR}/lib/hostapd/.hostapd_tmp
chmod o= %{TZ_SYS_VAR}/lib/hostapd/.hostapd_tmp
chsmack -a "*" %{TZ_SYS_VAR}/lib/hostapd/.hostapd_tmp

%postun -p /sbin/ldconfig

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if mobile || "undefined"
# For TM1
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%post extension-TM1
mv %{_bindir}/wpa_supplicant.tm1 %{_bindir}/wpa_supplicant
mv %{_bindir}/hostapd.tm1 %{_bindir}/hostapd
chmod +x %{_bindir}/hostapd

%preun extension-TM1
# for the storage size optimization, we do not save and restore the
# full version. However, we leave it because we do not want to break
# the whole thing after uninstall.
echo "If you want to keep %{name} appropriately after uninstalling this,"
echo "you need to reinstall %{name}."
echo "If you are uninstalling %{name} as well, please do not mind."
cp %{_bindir}/wpa_supplicant %{_bindir}/wpa_supplicant.tm1
cp %{_bindir}/hostapd %{_bindir}/hostapd.tm1
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# For TM2(wayland)
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%post extension-TM2
mv %{_bindir}/wpa_supplicant.tm2 %{_bindir}/wpa_supplicant
mv %{_bindir}/hostapd.tm2 %{_bindir}/hostapd
chmod +x %{_bindir}/hostapd

%preun extension-TM2
# for the storage size optimization, we do not save and restore the
# full version. However, we leave it because we do not want to break
# the whole thing after uninstall.
echo "If you want to keep %{name} appropriately after uninstalling this,"
echo "you need to reinstall %{name}."
echo "If you are uninstalling %{name} as well, please do not mind."
cp %{_bindir}/wpa_supplicant %{_bindir}/wpa_supplicant.tm2
cp %{_bindir}/hostapd %{_bindir}/hostapd.tm2
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "mobile" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%post profile_tv
mv %{_bindir}/wpa_supplicant.tv %{_bindir}/wpa_supplicant

%preun profile_tv
echo "If you want to keep %{name} appropriately after uninstalling this,"
echo "you need to reinstall %{name}."
echo "If you are uninstalling %{name} as well, please do not mind."
cp %{_bindir}/wpa_supplicant %{_bindir}/wpa_supplicant.tv
%endif

%files
%manifest wpa_supplicant.manifest
%{_bindir}/hostapd
%{TZ_SYS_VAR}/lib/hostapd/hostapd.accept
%{TZ_SYS_VAR}/lib/hostapd/hostapd.deny
%{TZ_SYS_VAR}/lib/hostapd/.hostapd_tmp
%attr(755,network_fw,network_fw) %{_bindir}/wpa_supp.sh
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/*.conf
%exclude %{_sysconfdir}/dbus-1/system.d/dbus-wpa_supplicant-robot.conf
%attr(644,network_fw,network_fw) %{TZ_SYS_ETC}/wpa_supplicant/*.conf
%attr(644,network_fw,network_fw) %{_sysconfdir}/wpa_supplicant/*.conf
%{_defaultdocdir}/wpasupplicant/README.wpa_supplicant.*
%license COPYING.mbsd
%license COPYINGv2

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if common || ivi || wearable || "undefined"
%if "%{?profile}" != "mobile" && "%{?profile}" != "tv"
%files profile_common
%{_bindir}/wpa_supplicant
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# For TM1
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" !="ivi" && "%{?profile}" != "common"
%files extension-TM1
# makes hostapd and wpa_supplicant different
%{_bindir}/wpa_supplicant.tm1
%{_bindir}/hostapd.tm1
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# For TM2(wayland)
%if "%{?profile}" != "wearable" && "%{?profile}" != "tv" && "%{?profile}" !="ivi" && "%{?profile}" != "common"
%files extension-TM2
# makes hostapd and wpa_supplicant different
%{_bindir}/wpa_supplicant.tm2
%{_bindir}/hostapd.tm2
%endif

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# if tv || "undefined"
%if "%{?profile}" != "wearable" && "%{?profile}" != "mobile" && "%{?profile}" != "ivi" && "%{?profile}" != "common"
%files profile_tv
# makes wpa_supplicant different
%{_bindir}/wpa_supplicant.tv
%endif

%files client_tool
%{_bindir}/wpa_cli
%{_bindir}/hostapd_cli

%post profile_robot
mv %{_sysconfdir}/dbus-1/system.d/dbus-wpa_supplicant-robot.conf %{_sysconfdir}/dbus-1/system.d/dbus-wpa_supplicant.conf

%files profile_robot
%manifest wpa_supplicant.manifest
%attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/dbus-wpa_supplicant-robot.conf
