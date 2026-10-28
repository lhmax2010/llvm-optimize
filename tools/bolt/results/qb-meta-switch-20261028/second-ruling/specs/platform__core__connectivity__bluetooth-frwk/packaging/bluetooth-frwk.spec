# Do not create provides from emulator .so files because the main package
# should anchor any reverse-dependencies
%global __provides_exclude_from ^(.*\\.emulator)$

%bcond_with x
%define _dumpdir /opt/etc/dump.d/module.d
%define _varlibdir /opt/var/lib
%define _meshdir /opt/mesh

Name:       bluetooth-frwk
Summary:    Bluetooth framework for BlueZ and Obexd. This package is Bluetooth framework based on BlueZ and Obexd stack.
Version:    0.10.0
Release:    1
Group:      Network & Connectivity/Bluetooth
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: bluetooth-frwk.manifest

%define bt_bluez_hal ENABLED
%define bt_gatt_client_fd ENABLED
%define bt_permanent_log DISABLED
%define bt_http_proxy DISABLED
%define bt_factory_mode DISABLED
%define bt_vendor_operation DISABLED
%if "%{mv_prj}" == "1"
%define bt_mesh_support DISABLED
%else
%define bt_mesh_support ENABLED
%endif

BuildRequires:  pkgconfig(aul)
%if %{bt_factory_mode} == ENABLED
BuildRequires:  pkgconfig(bincfg)
%endif
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(syspopup-caller)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(capi-network-connection)
BuildRequires:  pkgconfig(alarm-service)
BuildRequires:  pkgconfig(capi-content-mime-type)
BuildRequires:  pkgconfig(eventsystem)
%if %{bt_http_proxy} == ENABLED
BuildRequires:	pkgconfig(libsoup-2.4)
%endif
BuildRequires:  pkgconfig(capi-network-tethering)
BuildRequires:  cmake
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-gdbus)
BuildRequires:  pkgconfig(libtzplatform-config)
%if %{bt_mesh_support} == ENABLED
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(ell)
%endif
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(libactd)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(hal-api-bluetooth)

Requires(post): /usr/bin/vconftool
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Bluetooth framework for BlueZ and Obexd. This package is Bluetooth framework based on BlueZ and Obexd stack.
This package contains API set for BT GAP, BT SDP, BT RFCOMM and BLE Mesh.

%package profile_common
Summary:    bluetooth-frwk service and conf files for common profile
Requires:   %{name} = %{version}-%{release}
Conflicts:  %{name}-profile_da
%description profile_common
Bluetooth framework configuration and service files for Tizen common profile

%package profile_da
Summary:    bluetooth-frwk service and conf files for da profile
Requires:   %{name} = %{version}-%{release}
Conflicts:  %{name}-profile_common
%description profile_da
Bluetooth framework configuration and service files for Tizen da profile

%ifarch %{ix86} x86_64
%package extension-emulator
Summary:    bluetooth-frwk service and conf files for emulator
Requires:   %{name} = %{version}-%{release}
%description extension-emulator
bluetooth-frwk service and conf files for emulator
%endif // ifarch %{ix86} x86_64

%package devel
Summary:    Bluetooth framework for BlueZ and Obexd
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package is development files for Bluetooth framework based on BlueZ and Obexd stack.
This package contains API set for BT GAP, BT SDP, and BT RFCOMM.

%package service
Summary:    Bluetooth Service daemon
Group:      Network & Connectivity/Bluetooth
Requires:   %{name} = %{version}-%{release}

%description service
This package is Bluetooth Service daemon to manage BT services.

%if %{bt_http_proxy} == ENABLED
%package httpproxy
Summary:    Bluetooth HTTP Proxy Service daemon
Group:      Network & Connectivity/Bluetooth
Requires:   %{name} = %{version}-%{release}

%description httpproxy
This package is Bluetooth HTTP Proxy Service daemon
%endif

%package otp
Summary:    Bluetooth OTP Service daemon
Group:      Network & Connectivity/Bluetooth
Requires:   %{name} = %{version}-%{release}

%description otp
This package is Bluetooth OTP Service daemon

%package core
Summary:    Bluetooth Core daemon
Group:      Network & Connectivity/Bluetooth
Requires:   %{name} = %{version}-%{release}

%description core
This package is Bluetooth core daemon to manage activation / deactivation.

%package test
Summary:    Bluetooth test application
Group:      Network & Connectivity/Bluetooth
Requires:   %{name} = %{version}-%{release}

%description test
This package is Bluetooth test application.

%package oal
Summary:    Bluetooth OAL
Group:      Network & Connectivity/Bluetooth
Requires:   %{name} = %{version}-%{release}

%description oal
This package is BT stack common interface.

%package plugin-headed
Summary:    Bluetooth plugin Headed
Group:      Network & Connectivity/Bluetooth
Requires:   %{name} = %{version}-%{release}

%description plugin-headed
This package is Bluetooth plugin to manage UI and syspopup

%prep
%setup -q
cp %{SOURCE1001} .


%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_OBEX"
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_PAN_NAP"
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_IPSP"
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_CONTAINER"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%define _servicefile packaging/bluetooth-frwk-common.service
%define _servicedir starter.target.wants

%ifarch x86_64
#export CFLAGS="$CFLAGS -Wall -g -fvisibility=hidden -fPIC"
export CFLAGS="$CFLAGS -fpie"
export CFLAGS="$CFLAGS -DARCH64"
export CXXFLAGS="$CXXFLAGS -DARCH64"
export FFLAGS="$FFLAGS -DARCH64"
%else
export CFLAGS="$CFLAGS -fpie"
export LDFLAGS="$CFLAGS -pie"
%endif

%if %{bt_bluez_hal} == ENABLED
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_RFCOMM_DIRECT -DTIZEN_BT_HAL"
%else
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_RFCOMM_DIRECT"
%endif
export LDFLAGS="$CFLAGS -Wl,--rpath=%{_libdir} -Wl,--as-needed -Wl,--unresolved-symbols=ignore-in-shared-libs"

%if %{bt_gatt_client_fd} == DISABLED
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_GATT_CLIENT_FD_DISABLE"
%endif

%if %{bt_permanent_log} == ENABLED
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_PERMANENT_LOG"
%endif

%if %{bt_http_proxy} == ENABLED
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_HTTP_PROXY"
%endif

%if %{bt_factory_mode} == ENABLED
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_FACTORY_MODE"
%endif

%if %{bt_vendor_operation} == ENABLED
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BT_VENDOR_OPERATION"
%endif

%if %{bt_bluez_hal} == ENABLED
export BT_INCLUDE_OAL_BLUEZ=ENABLED
export CFLAGS="$CFLAGS -DTIZEN_BT_INCLUDE_OAL_BLUEZ"
%else
export BT_INCLUDE_OAL_BLUEZ=DISABLED
%endif

%if %{bt_mesh_support} == ENABLED
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_MESH_SUPPORT"
%endif

%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS="$CFLAGS -Wno-error=implicit-enum-enum-cast"
%endif
}

export CFLAGS_DEFAULT="$CFLAGS"
export CXXFLAGS_DEFAULT="$CXXFLAGS"
export FFLAGS_DEFAULT="$FFLAGS"

# extension-emulator
%ifarch %{ix86} x86_64
export CFLAGS="${CFLAGS} -DTIZEN_FEATURE_BT_RFCOMM_DIRECT"
export CXXFLAGS="${CXXFLAGS} -DTIZEN_FEATURE_BT_RFCOMM_DIRECT"
export FFLAGS="${FFLAGS} -DTIZEN_FEATURE_BT_RFCOMM_DIRECT"

mkdir -p build_emulator

cmake . -DCMAKE_INSTALL_PREFIX=/usr \
-DCMAKE_LIB_DIR=%{_libdir} \
-DTZ_SYS_USER_GROUP=%TZ_SYS_USER_GROUP \
-DTZ_SYS_DEFAULT_USER=%TZ_SYS_DEFAULT_USER \
	-DLIBNOTIFY_SUPPORT=Off \
	-DLIBNOTIFICATION_SUPPORT=Off
make %{?_smp_mflags}

%cmake

%make_install
cp %{buildroot}%{_libdir}/libbluetooth-api.so* build_emulator/
_bt_frwk_build_pwd=$(pwd)
cd build_emulator/
for FILE in libbluetooth-api.so*; do mv "${FILE}" "${FILE}.emulator"; done
cd "$_bt_frwk_build_pwd"
%endif

# non-extension-emulator

export CFLAGS="$CFLAGS_DEFAULT -DTIZEN_FEATURE_BT_RFCOMM_DIRECT"
export CXXFLAGS="$CXXFLAGS_DEFAULT -DTIZEN_FEATURE_BT_RFCOMM_DIRECT"
export FFLAGS="$FFLAGS_DEFAULT -DTIZEN_FEATURE_BT_RFCOMM_DIRECT"

%ifarch aarch64
echo arch64
export CFLAGS="$CFLAGS -DARCH64"
export CXXFLAGS="$CXXFLAGS -DARCH64"
export FFLAGS="$FFLAGS -DARCH64"
%endif

%ifarch riscv64
echo riscv64
export CFLAGS="$CFLAGS -DARCH64"
export CXXFLAGS="$CXXFLAGS -DARCH64"
export FFLAGS="$FFLAGS -DARCH64"
%endif

cmake . -DCMAKE_INSTALL_PREFIX=/usr \
-DCMAKE_LIB_DIR=%{_libdir} \
-DTZ_SYS_USER_GROUP=%TZ_SYS_USER_GROUP \
-DTZ_SYS_DEFAULT_USER=%TZ_SYS_DEFAULT_USER \
	-DLIBNOTIFY_SUPPORT=Off \
	-DLIBNOTIFICATION_SUPPORT=Off
make %{?_smp_mflags}

%cmake

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_unitdir}/starter.target.wants
mkdir -p %{buildroot}%{_unitdir}/delayed.target.wants
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
mkdir -p %{buildroot}/%{_prefix}/lib/udev/rules.d
mkdir -p %{buildroot}%{_meshdir}
mkdir -p %{buildroot}%{TZ_SYS_UPGRADE_SCRIPTS}

cp packaging/99-bluetooth-rfkill.rules %{buildroot}/%{_prefix}/lib/udev/rules.d/99-bluetooth-rfkill.rules

# extension-emulator
%ifarch %{ix86} x86_64
cp build_emulator/libbluetooth-api.so*.emulator %{buildroot}%{_libdir}/
#mv %{buildroot}/%{_bindir}/bt-service-emul %{buildroot}/%{_bindir}/bt-service
%endif

# da
install -m 0644 packaging/bluetooth-frwk-da.service %{buildroot}%{_unitdir}/bluetooth-frwk.service.da

# common
install -m 0644 packaging/bluetooth-frwk-common.service %{buildroot}%{_unitdir}/bluetooth-frwk.service.common

# bt-core
install -m 0644 bt-core/bluetooth-frwk-core.service %{buildroot}%{_unitdir}/bluetooth-frwk-core.service

ln -s ../bluetooth-frwk.service %{buildroot}%{_unitdir}/multi-user.target.wants/bluetooth-frwk.service
ln -s ../bluetooth-frwk.service %{buildroot}%{_unitdir}/starter.target.wants/bluetooth-frwk.service

install -m 0755 packaging/500.bluetooth-frwk_upgrade.sh %{buildroot}%{TZ_SYS_UPGRADE_SCRIPTS}

%postun -p /sbin/ldconfig

%post service
/usr/bin/chsmack -a '_' %{_varlibdir}/bluetooth/auto-pair-blocklist
/usr/bin/chown network_fw:network_fw %{_varlibdir}/bluetooth/auto-pair-blocklist
/usr/bin/chown network_fw:network_fw %{_meshdir}

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%{_libdir}/libbluetooth-api.so.*
%exclude %{_libdir}/libbluetooth-api.so*.emulator

%files devel
%defattr(-, root, root)
%{_includedir}/bt-service/bluetooth-api.h
%{_includedir}/bt-service/bluetooth-hid-api.h
%{_includedir}/bt-service/bluetooth-audio-api.h
%{_includedir}/bt-service/bluetooth-telephony-api.h
%{_includedir}/bt-service/bluetooth-media-control.h
%{_includedir}/bt-service/bluetooth-scmst-api.h
%{_includedir}/bt-service/bluetooth-ipsp-api.h
%{_includedir}/bt-service/bluetooth-gatt-server-api.h
%{_includedir}/bt-service/bluetooth-gatt-client-api.h
%{_includedir}/bt-service/bluetooth-mesh-api.h
%{_libdir}/pkgconfig/bluetooth-api.pc
%{_libdir}/libbluetooth-api.so

# extension-emulator
%ifarch %{ix86} x86_64
%post extension-emulator
for FILE in %{_libdir}/libbluetooth-api.so*.emulator; do mv "${FILE}" "${FILE%.emulator}"; done
%preun extension-emulator
for FILE in %{_libdir}/libbluetooth-api.so*; do mv "${FILE}" "${FILE}.emulator"; done
%files extension-emulator
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libbluetooth-api.so.*.emulator
%{_libdir}/libbluetooth-api.so.emulator
%endif

%files service
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%{_bindir}/bt-service
%{_sysconfdir}/dbus-1/system.d/bluetooth-frwk-service.conf
%{_bindir}/bluetooth-frwk-test
%{_varlibdir}/bluetooth
%{_prefix}/etc/bluetooth
%{_meshdir}
%attr(-,network_fw,network_fw) %{_varlibdir}/bluetooth/auto-pair-blocklist
%{TZ_SYS_UPGRADE_SCRIPTS}/500.bluetooth-frwk_upgrade.sh

%if %{bt_http_proxy} == ENABLED
%files httpproxy
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%{_bindir}/bt-httpproxy
%{_datadir}/dbus-1/system-services/org.projectx.httpproxy.service
%{_sysconfdir}/dbus-1/system.d/bluetooth-frwk-httpproxy.conf
%endif

%files otp
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%{_bindir}/bt-otp
%{_datadir}/dbus-1/system-services/org.projectx.otp.service
%{_sysconfdir}/dbus-1/system.d/bluetooth-frwk-otp.conf

%files core
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%{_unitdir}/bluetooth-frwk-core.service
%{_datadir}/dbus-1/system-services/org.projectx.bt_core.service
%{_bindir}/bt-core
%{_sysconfdir}/dbus-1/system.d/bluetooth-frwk-core.conf
%{_prefix}/lib/udev/rules.d/99-bluetooth-rfkill.rules

%files test
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%{_bindir}/bluetooth-frwk-test
#%{_bindir}/bluetooth-gatt-test
#%{_bindir}/bluetooth-advertising-test

%files plugin-headed
%manifest %{name}.manifest
%license LICENSE
%defattr(-, root, root)
%{_libdir}/bt-plugin-headed.so

%post profile_common
mv %{_unitdir}/bluetooth-frwk.service.common %{_unitdir}/bluetooth-frwk.service
%preun profile_common
mv %{_unitdir}/bluetooth-frwk.service %{_unitdir}/bluetooth-frwk.service.common
%files profile_common
%license LICENSE
%{_unitdir}/multi-user.target.wants/bluetooth-frwk.service
%exclude %{_unitdir}/starter.target.wants/bluetooth-frwk.service
%{_unitdir}/bluetooth-frwk.service.common
%{_datadir}/dbus-1/system-services/org.projectx.bt.service

%post profile_da
mv %{_unitdir}/bluetooth-frwk.service.da %{_unitdir}/bluetooth-frwk.service
%preun profile_da
mv %{_unitdir}/bluetooth-frwk.service %{_unitdir}/bluetooth-frwk.service.da
%files profile_da
%license LICENSE
%{_unitdir}/multi-user.target.wants/bluetooth-frwk.service
%{_unitdir}/bluetooth-frwk.service.da
%{_datadir}/dbus-1/system-services/org.projectx.bt.service

%files oal
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libbt-oal.so*
%{_sysconfdir}/dbus-1/system.d/bluetooth-frwk-gap-agent.conf

%if %{bt_bluez_hal} == ENABLED
%{_libdir}/libbluetooth.default.so*
%endif
