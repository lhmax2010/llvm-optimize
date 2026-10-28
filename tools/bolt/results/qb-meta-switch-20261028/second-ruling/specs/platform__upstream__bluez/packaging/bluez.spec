# Do not create provides fro extension-tm1 because the main package
# should anchor any reverse-dependencies
%global __provides_exclude_from ^(.*\\.tm1)$

#%define __spec_check_pre exit 0
%define unified true

#%define with_libcapng --enable-capng
%define _libpath /usr/lib
Name:       	bluez
Summary:    	Bluetooth Stack for Linux
Version:    	5.79
Release:    	1
Group:      	Network & Connectivity/Bluetooth
License:    	GPL-2.0+ and LGPL-2.1+
URL:        	http://www.bluez.org/
Source:         bluez-%{version}.tar.gz
Source2:        bluez-coldplug.init
Source3:        bluetooth.sysconfig
Source4:        bluetooth.sh
Source5:        baselibs.conf
Source7:        bluetooth.modprobe
Source101:    	obex-root-setup
Source102:    	create-symlinks
Source103:      obex.sh
Source1001:     bluez.manifest
Patch :         Use-g_memdup2-for-glib-2.70-upgrade.patch
#Patch1 :    bluez-ncurses.patch
#Patch2 :    disable-eir-unittest.patch
#Requires:   dbus >= 0.60
#BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(ell)
#BuildRequires:  pkgconfig(glib-2.0)
#BuildRequires:  pkgconfig(ncurses)
#BuildRequires:  flex
#BuildRequires:  bison
#BuildRequires:  readline-devel
#BuildRequires:  openssl-devel
BuildRequires:  flex
BuildRequires:  libcap-ng-devel
BuildRequires:  systemd
%{?systemd_requires}
BuildRequires:  pkgconfig(alsa)
BuildRequires:  automake
BuildRequires:  check-devel
BuildRequires:  glib2-devel >= 2.16
BuildRequires:  libsndfile-devel
BuildRequires:  libtool
BuildRequires:  libudev-devel
BuildRequires:  pkg-config
#BuildRequires:  readline-devel
BuildRequires:  udev
BuildRequires:  pkgconfig(libtzplatform-config)
Requires:	%{name}-compat = %{version}-%{release}
Requires:	security-config
Recommends:	%{name}-profile_common = %{version}-%{release}

%description
The Bluetooth stack for Linux.

%if %{unified} == true
%package extension-bredr
Summary:    Bluez extension for BREDR functionality
Requires:  %{name} = %{version}-%{release}
Conflicts:  %{name}-extension-le = %{version}-%{release}
%description extension-bredr
Bluez extension for BREDR functionality

%package extension-le
Summary:    Bluez extension for LE functionality
Requires:  %{name} = %{version}-%{release}
Conflicts:  %{name}-extension-bredr = %{version}-%{release}
%description extension-le
Bluez extension for LE functionality
%endif

%package -n obexd
Summary:        OBEX Server A basic OBEX server implementation
Group:          Network & Connectivity/Bluetooth
Requires:       tizen-platform-config-tools

%description -n obexd
OBEX Server A basic OBEX server implementation.

%package test
Summary:        Tools for testing of various Bluetooth-functions
License:        GPL-2.0+
Group:          Development/Tools
Requires:       dbus-python
Requires:       python-gobject

%description test
Contains a few tools for testing various bluetooth functions. The
BLUETOOTH trademarks are owned by Bluetooth SIG, Inc., U.S.A.

%package tools
Summary:        Bluez configuration tools
License:        GPL-2.0+
Group:          Development/Tools

%description tools
# !!! WARNING !!!
# Using any tool in this package results direct access to bluez stack,
# so the result of the tool won't be applied to Tizen system properly.
# Recommend to use it cautiously and only in development phase.
Bluez tools to manipulate bluetooth devices and configuartion.

%package profile_common
Summary:	Modified bluez for mobile/common profile
Provides:	%{name}-compat = %{version}-%{release}
Provides:	%{name}-profile_mobile = %{version}-%{release}
Provides:	%{name}-profile_ivi = %{version}-%{release}
Conflicts:	%{name}-profile_wearable
Conflicts:	%{name}-profile_tv
%description profile_common
Bluez default service script for Tizen (mobile/common profile)

%package profile_wearable
Summary:	Modified bluez for wearable profile
Provides:	%{name}-compat = %{version}-%{release}
Conflicts:	%{name}-profile_common
Conflicts:	%{name}-profile_tv
%description profile_wearable
Bluez modified service script for Tizen wearable

%package profile_tv
Summary:	Modified bluez for wearable profile
Provides:	%{name}-compat = %{version}-%{release}
Conflicts:	%{name}-profile_common
Conflicts:	%{name}-profile_wearable
%description profile_tv
Bluez modified service script for Tizen TV

%package plugin-headless
Summary:	Bluez headless plugin
Requires:	%{name}-compat = %{version}-%{release}
%description plugin-headless
This package is Bluez plugin to manager headless device

%package plugin-keyboard
Summary:	Bluez keyboard plugin
Requires:	%{name}-compat = %{version}-%{release}
%description plugin-keyboard
This package is Bluez plugin to manager keyboard device

%package plugin-robot
Summary:	Bluez robot plugin
Requires:	%{name}-compat = %{version}-%{release}
%description plugin-robot
This package is Bluez plugin to manager robot device

%package plugin-da
Summary:	Bluez plugin for Digital Appliance
Requires:	%{name}-compat = %{version}-%{release}
%description plugin-da
This package is Bluez plugin to manager Digital Appliance devices

%package mesh
Summary:        contains binaries for bluetooth mesh
Requires:	%{name}-compat = %{version}-%{release}
License:        GPL-2.0+
%description mesh
Contains bluetooth mesh daemon

%prep
%setup -q
cp %{SOURCE1001} .
%patch -p1

%build
autoreconf -fiv

#if "{?profile}" == "ivi"
# TIZEN_FEATURE_BLUEZ_BRCM_CHIP: only in tools/hciattach.c ==> RUNTIME! (profile.h)
#endif

#if "{?profile}" == "wearable"
# TIZEN_FEATURE_BLUEZ_SMS_ONLY: only in obexd/plugins/messages-tizen.c ==> RUNTIME! (profile.h)
# TIZEN_FEATURE_BLUEZ_BRCM_QOS: only in profiles/audio/avdtp.c ==> RUNTIME! (profile.h)
# TIZEN_FEATURE_BLUEZ_ROLE_CHANGE: only in profiles/audio/avdtp.c ==> RUNTIME! (profile.h)
# TIZEN_FEATURE_BLUEZ_CONFIRM_ONLY: only in src/device.c ==> RUNTIME! (profile.h)
#endif


# For LE only

export CFLAGS_DEFAULT="$CFLAGS"

%if %{unified} == true
# Add GCC9 exception
%if %{defined _toolchain}
%if !%{toolchain_is clang}
export CFLAGS="$CFLAGS -Wno-stringop-truncation"
%endif
%else
export CFLAGS="$CFLAGS -Wno-stringop-truncation"
%endif
export CFLAGS="$CFLAGS -Wno-format-truncation -Wno-address-of-packed-member -Wno-varargs"

export LDFLAGS=" -lncurses -Wl,--as-needed "
export CFLAGS="$CFLAGS -Werror -DTIZEN_FEATURE_BLUEZ_MODIFY -DTIZEN_FEATURE_BLUEZ_A2DP_MULTISTREAM -DTIZEN_FEATURE_BLUEZ_PBAP_SIM -DTIZEN_FEATURE_BLUEZ_AVRCP_TARGET -DTIZEN_FEATURE_BLUEZ_AVRCP_CONTROL -DTIZEN_FEATURE_BLUEZ_AVRCP_TARGET -DENABLE_AVRCP_CATEGORY1 -DTIZEN_BT_HID_DEVICE_ENABLE"

%ifarch aarch64
echo arch64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%ifarch riscv64
echo riscv64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%ifarch x86_64
echo x86_64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%reconfigure --disable-static \
			--sysconfdir=%{_sysconfdir} \
			--localstatedir=%{_localstatedir} \
			--with-systemdsystemunitdir=%{_libpath}/systemd/system \
			--with-systemduserunitdir=%{_libpath}/systemd/user \
			--libexecdir=%{_libexecdir} \
			--enable-debug \
			--enable-pie \
			--enable-usb=no \
			--enable-tools \
			--disable-bccmd \
			--enable-pcmcia=no \
			--enable-hid2hci=yes \
			--enable-alsa=no \
			--enable-gstreamer=no \
			--disable-dfutool \
			--disable-cups \
			--enable-proximity=yes \
			--enable-tds=yes \
			--enable-dbusoob \
			--enable-test \
			--enable-mesh=yes \
			--with-telephony=tizen \
			--enable-obex \
			--enable-library \
			--enable-gatt \
			--enable-testing \
			--enable-experimental \
			--enable-autopyypair=no \
			--enable-tizenunusedplugin=no \
			--disable-crypto-tests \
			--enable-external-ell

make %{?_smp_mflags} all V=1

mkdir -p le

#%make_install
cp -a  %{buildroot}%{_libexecdir}/bluetooth/bluetoothd le/


# For BREDR only
make distclean

autoreconf -fiv

export CFLAGS="$CFLAGS_DEFAULT"

# Add GCC9 exception
%if %{defined _toolchain}
%if !%{toolchain_is clang}
export CFLAGS="$CFLAGS -Wno-stringop-truncation"
%endif
%else
export CFLAGS="$CFLAGS -Wno-stringop-truncation"
%endif
export CFLAGS="$CFLAGS -Wno-format-truncation -Wno-address-of-packed-member -Wno-varargs"

export LDFLAGS=" -lncurses -Wl,--as-needed "
export CFLAGS="$CFLAGS -Werror -DTIZEN_FEATURE_BLUEZ_MODIFY -DTIZEN_FEATURE_BLUEZ_A2DP_MULTISTREAM -DTIZEN_FEATURE_BLUEZ_PBAP_SIM -DTIZEN_FEATURE_BLUEZ_AVRCP_TARGET -DTIZEN_FEATURE_BLUEZ_AVRCP_CONTROL -DTIZEN_FEATURE_BLUEZ_AVRCP_TARGET -DENABLE_AVRCP_CATEGORY1 -DTIZEN_BT_HID_DEVICE_ENABLE"

%ifarch aarch64
echo arch64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%ifarch riscv64
echo riscv64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%ifarch x86_64
echo x86_64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%reconfigure --disable-static \
			--sysconfdir=%{_sysconfdir} \
			--localstatedir=%{_localstatedir} \
			--with-systemdsystemunitdir=%{_libpath}/systemd/system \
			--with-systemduserunitdir=%{_libpath}/systemd/user \
			--libexecdir=%{_libexecdir} \
			--enable-debug \
			--enable-pie \
			--enable-serial \
			--enable-input \
			--enable-usb=no \
			--enable-tools \
			--disable-bccmd \
			--enable-pcmcia=no \
			--enable-hid2hci=yes \
			--enable-alsa=no \
			--enable-gstreamer=no \
			--disable-dfutool \
			--disable-cups \
			--enable-health=yes \
			--enable-dbusoob \
			--enable-test \
			--enable-mesh=yes \
			--with-telephony=tizen \
			--enable-obex \
			--enable-library \
			--enable-testing \
			--enable-experimental \
			--enable-autopair=no \
			--enable-hid=yes \
			--enable-bredr=yes \
			--enable-tizenunusedplugin=no \
			--disable-crypto-tests \
			--enable-external-ell

make %{?_smp_mflags} all V=1

mkdir -p bredr

#%make_install
cp -a  %{buildroot}%{_libexecdir}/bluetooth/bluetoothd bredr/


# For BREDR + LE
make distclean

autoreconf -fiv
%endif
export CFLAGS="$CFLAGS_DEFAULT"

# Add GCC9 exception
%if %{defined _toolchain}
%if !%{toolchain_is clang}
export CFLAGS="$CFLAGS -Wno-stringop-truncation"
%endif
%else
export CFLAGS="$CFLAGS -Wno-stringop-truncation"
%endif
export CFLAGS="$CFLAGS -Wno-format-truncation -Wno-address-of-packed-member -Wno-varargs"

export LDFLAGS=" -lncurses -Wl,--as-needed "
export CFLAGS="$CFLAGS -Werror -DTIZEN_FEATURE_BLUEZ_MODIFY -DTIZEN_FEATURE_BLUEZ_A2DP_MULTISTREAM -DTIZEN_FEATURE_BLUEZ_PBAP_SIM -DTIZEN_FEATURE_BLUEZ_AVRCP_TARGET -DTIZEN_FEATURE_BLUEZ_AVRCP_CONTROL -DTIZEN_FEATURE_BLUEZ_AVRCP_TARGET -DENABLE_AVRCP_CATEGORY1 -DTIZEN_BT_HID_DEVICE_ENABLE"

%ifarch aarch64
echo arch64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%ifarch riscv64
echo riscv64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%ifarch x86_64
echo x86_64
export CFLAGS="$CFLAGS -DARCH64"
%endif

%reconfigure --disable-static \
			--sysconfdir=%{_sysconfdir} \
			--localstatedir=%{_localstatedir} \
			--with-systemdsystemunitdir=%{_libpath}/systemd/system \
			--with-systemduserunitdir=%{_libpath}/systemd/user \
			--libexecdir=%{_libexecdir} \
			--enable-debug \
			--enable-pie \
			--enable-serial \
			--enable-input \
			--enable-usb=no \
			--enable-tools \
			--disable-bccmd \
			--enable-pcmcia=no \
			--enable-hid2hci=yes \
			--enable-alsa=no \
			--enable-gstreamer=no \
			--disable-dfutool \
			--disable-cups \
			--enable-health=yes \
			--enable-proximity=yes \
			--enable-tds=yes \
			--enable-dbusoob \
			--enable-test \
			--with-telephony=tizen \
			--enable-obex \
			--enable-mesh=yes \
			--enable-library \
			--enable-gatt \
			--enable-testing \
			--enable-experimental \
			--enable-autopair=no \
			--enable-hid=yes \
			--enable-bredr=yes \
			--enable-tizenunusedplugin=no \
			--disable-crypto-tests \
			--enable-external-ell

make %{?_smp_mflags} all V=1

%check
make check

%install
%make_install

%if %{unified} == true
( cd bredr && for FILE in bluetoothd; do mv "$FILE" "%{buildroot}%{_libexecdir}/bluetooth/$FILE.bredr"; done )

( cd le && for FILE in bluetoothd; do mv "$FILE" "%{buildroot}%{_libexecdir}/bluetooth/$FILE.le"; done )
%endif

# bluez-test
rm -rvf $RPM_BUILD_ROOT/%{_libdir}/gstreamer-*
#install --mode=0755 -D %{S:4} $RPM_BUILD_ROOT/usr/lib/udev/bluetooth.sh
%if %{unified} == true
install -m 0644 -D %{S:7} $RPM_BUILD_ROOT/%{_sysconfdir}/modprobe.d/50-bluetooth.conf
%endif

# no idea why this is suddenly necessary...
install -m 0755 -d $RPM_BUILD_ROOT/var/lib/bluetooth

install -D -m 0644 src/main_w.conf %{buildroot}%{_sysconfdir}/bluetooth/main.conf.wearable
install -D -m 0644 src/main_m.conf %{buildroot}%{_sysconfdir}/bluetooth/main.conf
install -D -m 0644 src/main_headless.conf %{buildroot}%{_sysconfdir}/bluetooth/main.conf.headless
install -D -m 0644 src/main_keyboard.conf %{buildroot}%{_sysconfdir}/bluetooth/main.conf.keyboard
install -D -m 0644 src/main_robot.conf %{buildroot}%{_sysconfdir}/bluetooth/main.conf.robot
install -D -m 0644 src/main_da.conf %{buildroot}%{_sysconfdir}/bluetooth/main.conf.da
install -D -m 0644 profiles/input/input.conf %{buildroot}%{_sysconfdir}/bluetooth/input.conf

#install -D -m 0644 src/org.bluez.service %{buildroot}%{_datadir}/dbus-1/system-services/org.bluez.service

install -D -m 0644 src/bluetooth.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/bluetooth.conf
install -D -m 0644 src/bluetooth_robot.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/bluetooth_robot.conf
#install -D -m 0644 profiles/audio/audio.conf %{buildroot}%{_sysconfdir}/bluetooth/audio.conf
#install -D -m 0644 profiles/network/network.conf %{buildroot}%{_sysconfdir}/bluetooth/network.conf

#install -D -m 0644 COPYING %{buildroot}%{_datadir}/license/bluez
#install -D -m 0644 COPYING %{buildroot}%{_datadir}/license/libbluetooth3
#install -D -m 0644 COPYING %{buildroot}%{_datadir}/license/libbluetooth-devel

#install -D -m 0755 %SOURCE101 %{buildroot}%{_bindir}/obex-root-setup
#install -D -m 0755 %SOURCE102 %{buildroot}%{_sysconfdir}/obex/root-setup.d/000_create-symlinks
#install -D -m 0755 %SOURCE103 %{buildroot}%{_bindir}/obex.sh
install -D -m 0755 tools/btiotest $RPM_BUILD_ROOT/%{_bindir}/
install -D -m 0755 tools/bluetooth-player $RPM_BUILD_ROOT/%{_bindir}/
#install -D -m 0755 tools/mpris-player $RPM_BUILD_ROOT/%{_bindir}/
install -D -m 0755 tools/btmgmt $RPM_BUILD_ROOT/%{_bindir}/
install -D -m 0755 tools/scotest $RPM_BUILD_ROOT/%{_bindir}/
install -D -m 0755 tools/bluemoon $RPM_BUILD_ROOT/%{_bindir}/
install -D -m 0755 attrib/gatttool $RPM_BUILD_ROOT/%{_bindir}/
install -D -m 0755 tools/meshctl $RPM_BUILD_ROOT/%{_bindir}/
install -D -m 0755 tools/mesh-cfgclient $RPM_BUILD_ROOT/%{_bindir}/

# mesh conf
install -D -m 0644 mesh/mesh-main.conf %{buildroot}%{_sysconfdir}/bluetooth/mesh-main.conf

install -D -m 0755 tools/obexctl %{buildroot}%{_bindir}/obexctl

install -D -m 0644 obexd/src/obex.service %{buildroot}%{_libpath}/systemd/system/

install -D -m 0644 src/bluetooth.service %{buildroot}%{_libpath}/systemd/system/bluez-start.service

%if %{unified} == true
%post -n bluez-extension-bredr
( cd %{_libexecdir}/bluetooth && for FILE in bluetoothd.bredr; do mv "$FILE" "${FILE%.bredr}"; done )
/sbin/ldconfig

%post -n bluez-extension-le
( cd %{_libexecdir}/bluetooth && for FILE in bluetoothd.le; do mv "$FILE" "${FILE%.le}"; done )
/sbin/ldconfig
%endif

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
#%{_sysconfdir}/bluetooth/audio.conf
#%{_sysconfdir}/bluetooth/network.conf
#%{_sysconfdir}/bluetooth/rfcomm.conf
#%{_datadir}/man/*/*
%attr(750, network_fw, network_fw)%{_bindir}/hcitool
%{_bindir}/l2ping
%{_bindir}/obexctl
%{_bindir}/rfcomm
%{_bindir}/btsnoop
%{_bindir}/mpris-proxy
%{_bindir}/sdptool
%{_bindir}/ciptool
#%{_bindir}/dfutool
%{_bindir}/btmon
%{_bindir}/hcidump
%attr(750, network_fw, network_fw)%{_bindir}/btattach
%attr(750, network_fw, network_fw)%{_bindir}/hciattach
%attr(750, network_fw, network_fw)%{_bindir}/hciconfig
%attr(755, network_fw, network_fw)%{_libexecdir}/bluetooth/bluetoothd
%exclude %{_libexecdir}/bluetooth/bluetoothd.bredr
%exclude %{_libexecdir}/bluetooth/bluetoothd.le
%exclude %{_includedir}/bluetooth/*
%exclude %{_libdir}/pkgconfig/bluez.pc
#%{_bindir}/bccmd
#%{_sbindir}/hid2hci
%dir /usr/lib/udev
/usr/lib/udev/*
%{_unitdir}/bluez-start.service
%exclude %{_unitdir}/bluetooth.service

%if %{unified} == true
%files -n bluez-extension-bredr
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libexecdir}/bluetooth/bluetoothd.bredr

%files -n bluez-extension-le
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libexecdir}/bluetooth/bluetoothd.le
%config %{_sysconfdir}/dbus-1/system.d/bluetooth.conf
%dir /var/lib/bluetooth
%dir %{_sysconfdir}/modprobe.d
%config(noreplace) %{_sysconfdir}/modprobe.d/50-bluetooth.conf
%endif

%files mesh
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%{_sysconfdir}/dbus-1/system.d/bluetooth-mesh.conf
%attr(755, network_fw, network_fw)%{_libexecdir}/bluetooth/bluetooth-meshd
%{_libpath}/systemd/system/bluetooth-mesh.service
%exclude %{_datadir}/dbus-1/system-services/org.bluez.mesh.service
%exclude /usr/lib/debug/*
%{_sysconfdir}/bluetooth/mesh-main.conf

%files -n obexd
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libexecdir}/bluetooth/obexd
%{_libpath}/systemd/system/obex.service
%{_datadir}/dbus-1/system-services/org.bluez.obex.service
#%{_sysconfdir}/obex/root-setup.d/000_create-symlinks
#%{_bindir}/obex-root-setup
#%{_bindir}/obex.sh

%files tools
%{_bindir}/bluetoothctl
%{_bindir}/btmgmt
%{_bindir}/gatttool
%{_bindir}/bluemoon
%{_bindir}/hex2hcd
%{_bindir}/meshctl
%{_bindir}/mesh-cfgclient
%{_bindir}/bluetooth-player

%files test
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/bluez/test/*
%{_bindir}/l2test
%{_bindir}/rctest
%{_bindir}/btiotest
#%{_bindir}/mpris-player
%{_bindir}/scotest
%{_bindir}/isotest
%{_bindir}/avtest
#%{_bindir}/btattach
%exclude /usr/lib/debug/*
%{_libdir}/libbluetooth.so*

%docs_package

%post profile_wearable
ln -sf main.conf.wearable %{_sysconfdir}/bluetooth/main.conf
%preun profile_wearable
rm %{_sysconfdir}/bluetooth/main.conf
%files profile_wearable
%manifest %{name}.manifest
%{_sysconfdir}/bluetooth/main.conf.wearable
%{_sysconfdir}/dbus-1/system.d/bluetooth.conf

%files profile_tv
%manifest %{name}.manifest
%{_sysconfdir}/bluetooth/main.conf
%exclude %{_datadir}/dbus-1/system-services/org.bluez.service
%{_sysconfdir}/dbus-1/system.d/bluetooth.conf

%files profile_common
%manifest %{name}.manifest
%{_sysconfdir}/bluetooth/main.conf
%{_sysconfdir}/bluetooth/input.conf
%{_sysconfdir}/dbus-1/system.d/bluetooth.conf

%post plugin-headless
ln -sf main.conf.headless %{_sysconfdir}/bluetooth/main.conf
%preun plugin-headless
rm %{_sysconfdir}/bluetooth/main.conf
%files plugin-headless
%manifest %{name}.manifest
%{_sysconfdir}/bluetooth/main.conf.headless

%post plugin-keyboard
ln -sf main.conf.keyboard %{_sysconfdir}/bluetooth/main.conf
%preun plugin-keyboard
rm %{_sysconfdir}/bluetooth/main.conf
%files plugin-keyboard
%manifest %{name}.manifest
%{_sysconfdir}/bluetooth/main.conf.keyboard

%post plugin-robot
ln -sf main.conf.robot %{_sysconfdir}/bluetooth/main.conf
mv %{_sysconfdir}/dbus-1/system.d/bluetooth_robot.conf %{_sysconfdir}/dbus-1/system.d/bluetooth.conf
%preun plugin-robot
rm %{_sysconfdir}/bluetooth/main.conf
%files plugin-robot
%manifest %{name}.manifest
%{_sysconfdir}/bluetooth/main.conf.robot
%{_sysconfdir}/dbus-1/system.d/bluetooth_robot.conf

%post plugin-da
ln -sf main.conf.da %{_sysconfdir}/bluetooth/main.conf
%preun plugin-da
rm %{_sysconfdir}/bluetooth/main.conf
%files plugin-da
%manifest %{name}.manifest
%{_sysconfdir}/bluetooth/main.conf.da

%changelog
