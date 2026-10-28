%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

%if "%{tizen_profile_name}" == "tv"
%define WITH_VD 1
%else
%define WITH_VD 0
%endif

%if "%{mv_prj}" == "1"
%define WITH_VD_MV 1
%else
%define WITH_VD_MV 0
%endif

%define enable_system_server 0

# display, extcon, power, usb are always enabled

#Just For debugging
%define sdb_prestart off

Name:       deviced
Summary:    Deviced
Version:    10.1.0
Release:    1
Group:      System/Management
License:    Apache-2.0 and MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    deviced.manifest
Source2:    libdeviced.manifest

%define plugindir %{_libdir}/deviced

BuildRequires:  cmake
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(eventsystem)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(hal-api-common)
BuildRequires:  pkgconfig(hal-api-device)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(capi-system-sensor)
BuildRequires:  pkgconfig(fuse)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(libkmod)
BuildRequires:  pkgconfig(libusbgx)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-deviced)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(tizen-dpms-client)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(argos_watchdog)
BuildRequires:  pkgconfig(cmocka)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(security-manager)
%if %{enable_system_server}
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(united-service)
%endif

Requires: %{name}-tools = %{version}-%{release}
%{?systemd_requires}
Requires(post): /usr/bin/vconftool
Requires(post): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives

%description
Deviced

%package -n libdeviced
Summary:    Deviced library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description -n libdeviced
Deviced library for device control.
Libdeviced is profile-independent; i.e., every profile has the same
binary for libdeviced.

%package -n libdeviced-devel
Summary:    Deviced library for (devel)
Group:      Development/Libraries
Requires:   libdeviced = %{version}-%{release}

%description -n libdeviced-devel
Deviced library for device control (devel).
Because this is internal interface, every profile MUST have the same
devel package.

%package tools
Summary:    Deviced tools
Group:      System/Utilities
Requires:   security-config

%description tools
Deviced helper programs.
Deviced-tools is profile-independent; i.e., every profile has the same
binary for deviced-tools.

%package auto-test
Summary:    Deviced auto test tool
Group:      System/Utilities

%description auto-test
Deviced helper programs.
This package can be installed optional for auto dbus test.

%package plugin-profile-common
Summary:    Plugin libraries for common devices
Group:      System/Management
Requires:   %{name} = %{version}-%{release}

%description plugin-profile-common
Plugin libraries for common devices

%package isu
Summary:    ISU package for deviced
Group:      System/Management
Requires:   %{name} = %{version}-%{release}

%description isu
Configuration files to generate the ISU (Individual Service Upgrade) package

%package syscommon-plugin-test
Summary:    libsyscommon function test tool related to deviced
Group:      System/Utilities

%description syscommon-plugin-test
This package can be installed optional for syscommon-plugin test.
It can test resource-driver and plugin backend call test for deviced.

%prep
%setup -q

cp %{SOURCE1} .
cp %{SOURCE2} .

%build
%{?_toolchain:
export CFLAGS+=" -Wl,--as-needed"
}
%ifarch %{arm} aarch64
	%define ARCH arm
%endif

%ifarch %{arm} %ix86
	%define ARCH_BIT 32
%else
	%define ARCH_BIT 64
%endif

%define battery_module on

%cmake . \
	-DTZ_SYS_ETC=%TZ_SYS_ETC \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DARCH=%{ARCH} \
	-DARCH_BIT=%{ARCH_BIT} \
	-DDPMS=%{DPMS} \
	-DDD_PLUGIN_PATH=%{plugindir} \
	-DBATTERY_MODULE=%{battery_module} \
	-DDISPLAY_MODULE=on \
	-DEXTCON_MODULE=on \
	-DIR_MODULE=on \
	-DLED_MODULE=on \
	-DPOWER_MODULE=on \
	-DSDB_PRESTART=%{sdb_prestart} \
	-DTOUCHSCREEN_MODULE=on \
	-DTZIP_MODULE=on \
	-DUSB_MODULE=on \
	-DUSBHOST_MODULE=on \
	-DTHERMAL_MODULE=on \
	-DTIZEN_FEATURE_CPU_MODULE=on \
	-DTIZEN_FEATURE_USBHOST_TEST=on \
	-DTOUCH_SENSITIVITY_MODULE=on \
	-DDUMP_MODULE=on \
	-DDEVICE_BOARD_MODULE=on \
	-DDEVICE_INPUT_MODULE=on \
	-DCRITICAL_LOG_MODULE=on \
%if %{enable_system_server}
	-DSYSTEM_SERVER_DIR=%{_system_server_dir} \
%endif
	-DENABLE_SYSTEM_SERVER=%{enable_system_server} \
	#eol

make %{?jobs:-j%jobs}

LIB_DIR=%{_libdir}
sed -ie s,"##LIBDIR##,$LIB_DIR,g" isu/isu.cfg
DD_PLUGIN_PATH=%{plugindir}
DD_PLUGIN_MOUNT_NAME=$(systemd-escape $DD_PLUGIN_PATH).mount
DD_PLUGIN_MOUNT_NAME=$(cut -c2- <<< $DD_PLUGIN_MOUNT_NAME) > /dev/null
sed -ie s,"##PLUGIN_MOUNT##,$DD_PLUGIN_MOUNT_NAME,g" isu/isu.cfg
sed -ie s,"##PLUGIN_MOUNT##,$DD_PLUGIN_MOUNT_NAME,g" isu/deviced.service
sed -ie s,"##PLUGIN_LIB_DIR##,$DD_PLUGIN_PATH,g" isu/usr-lib-deviced.mount

%install
rm -rf %{buildroot}
%make_install

%install_service multi-user.target.wants deviced.service
# usb_module condition is removed because it is always on
%if %{?sdb_prestart} == on
%install_service basic.target.wants sdb-prestart.service
%endif

mkdir -p %{buildroot}%{TZ_SYS_DUMPGEN}
install -m 775 scripts/dump_pmstate_log.sh %{buildroot}%{TZ_SYS_DUMPGEN}/dump_pmstate_log.sh

%post
# Assume power module is on (-DPOWER_MODULE=on)
update-alternatives --install %{_prefix}/lib/systemd/systemd-shutdown systemd-shutdown %{_prefix}/lib/systemd/deviced-shutdown 500

#memory type vconf key init
users_gid=$(getent group %{TZ_SYS_USER_GROUP} | cut -f3 -d':')

systemctl daemon-reload
if [ $1 -eq 1 ]; then
    systemctl restart deviced.service
fi

%postun
# Assume power module is on (-DPOWER_MODULE=on)
if [ $1 -eq 0 ] ; then
   update-alternatives --remove systemd-shutdown %{_prefix}/lib/systemd/deviced-shutdown

   systemctl daemon-reload
   systemctl stop deviced.service
fi

%posttrans
update-alternatives --remove reboot %{_sbindir}/deviced-power-command || :
update-alternatives --remove halt %{_sbindir}/deviced-power-command || :
update-alternatives --remove poweroff %{_sbindir}/deviced-power-command || :
update-alternatives --remove shutdown %{_sbindir}/deviced-power-command || :

%post -n libdeviced -p /sbin/ldconfig

%postun -n libdeviced -p /sbin/ldconfig

%post tools
chsmack -a 'System::Tools' %{_bindir}/device_board_set_boot_success
chsmack -a 'System::Tools' %{_bindir}/device_board_clear_boot_mode
chsmack -a 'System::Tools' %{_bindir}/device_board_get_boot_mode
chsmack -a 'System::Tools' %{_bindir}/device_board_get_current_partition
chsmack -a 'System::Tools' %{_bindir}/device_board_switch_partition
chsmack -a 'System::Tools' %{_bindir}/device_board_set_partition_ab_cloned
chsmack -a 'System::Tools' %{_bindir}/device_board_clear_partition_ab_cloned
chsmack -a 'System::Tools' %{_bindir}/device_board_get_partition_ab_cloned
chsmack -a 'System::Tools' %{_bindir}/device_board_set_partition_status
chsmack -a 'System::Tools' %{_bindir}/device_board_get_partition_status
chsmack -a 'System::Tools' %{_bindir}/device_board_set_upgrade_progress_status
chsmack -a 'System::Tools' %{_bindir}/device_board_get_upgrade_progress_status
chsmack -a 'System::Tools' %{_bindir}/device_board_set_upgrade_state
chsmack -a 'System::Tools' %{_bindir}/device_board_get_upgrade_state

%post plugin-profile-common
mv %{_sysconfdir}/deviced/display-profile-common.conf %{_sysconfdir}/deviced/display.conf
mv %{_sysconfdir}/deviced/power-profile-common.conf %{_sysconfdir}/deviced/power.conf
mkdir -p %{_libdir}/deviced
mv %{_libdir}/common-display.so %{_libdir}/deviced/display.so

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%license LICENSE.MIT
%{_libdir}/libdeviced-common-private.so
%if %{enable_system_server}
%{_system_server_dir}/mod/libsystem-server-deviced.so
%{_system_server_dir}/conf/system-server-deviced.service
%else
%{_bindir}/deviced
%endif
%{_unitdir}/multi-user.target.wants/deviced.service
%{_unitdir}/deviced.service
%dir %{plugindir}
%if %{?sdb_prestart} == on
%{_unitdir}/sdb-prestart.service
%{_unitdir}/basic.target.wants/sdb-prestart.service
%endif
%{_datadir}/dbus-1/system-services/org.tizen.system.deviced.service
%config %{_sysconfdir}/dbus-1/system.d/org.tizen.system.deviced.conf
%config %{_sysconfdir}/deviced/init.conf
%config %{_sysconfdir}/deviced/display.conf
%if %{?battery_module} == on
%config %{_sysconfdir}/deviced/battery.conf
%endif
# usbhost_test
%{_sysconfdir}/deviced/usb-host-test/test_gadget.gs
%{_bindir}/usb-host-ffs-test-daemon
%{_unitdir}/usb-host-ffs-test-daemon.service
%{_unitdir}/usb-host-test.socket
%{_sysconfdir}/deviced/usb-host-test/descs
%{_sysconfdir}/deviced/usb-host-test/strs
# dummy mtp-responder
%{_sysconfdir}/mtp-responder-dummy/strs
%{_sysconfdir}/mtp-responder-dummy/descs
%{_unitdir}/mtp-responder-dummy.socket
%{_unitdir}/mtp-responder-dummy.service

# Assume power module is on (-DPOWER_MODULE=on)
%{_unitdir}/deviced-request-shutdown@.service
%{_unitdir}/systemd-reboot.service.d/deviced-request-shutdown-reboot.conf
%{_unitdir}/systemd-poweroff.service.d/deviced-request-shutdown-poweroff.conf
%{_unitdir}/systemd-halt.service.d/deviced-request-shutdown-halt.conf
%{_unitdir}/systemd-exit.service.d/deviced-request-shutdown-exit.conf
%{_prefix}/lib/systemd/deviced-shutdown
%{_sbindir}/deviced-request-shutdown

%files -n libdeviced
%manifest deviced.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{_libdir}/libdeviced.so.*

%files -n libdeviced-devel
%defattr(-,root,root,-)
%{_includedir}/deviced/*.h
%{_includedir}/deviced/core/*.h
%{_includedir}/deviced/shared/*.h
%{_includedir}/deviced/extcon/*.h
%{_libdir}/libdeviced.so
%{_libdir}/pkgconfig/deviced.pc

%files tools
%manifest deviced.manifest
%license LICENSE.Apache-2.0
%{_bindir}/devicectl
#if #{?usb_module} == on ==> always on
%{_bindir}/direct_set_debug.sh
#endif
%{TZ_SYS_DUMPGEN}/dump_pmstate_log.sh
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_set_boot_success
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_clear_boot_mode
%attr(0555,system_fw,system_fw) %{_bindir}/device_board_get_boot_mode
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_get_current_partition
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_switch_partition
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_set_partition_ab_cloned
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_clear_partition_ab_cloned
%attr(0555,system_fw,system_fw) %{_bindir}/device_board_get_partition_ab_cloned
%attr(0555,system_fw,system_fw) %{_bindir}/device_board_set_partition_status
%attr(0555,system_fw,system_fw) %{_bindir}/device_board_get_partition_status
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_set_upgrade_progress_status
%attr(0555,system_fw,system_fw) %{_bindir}/device_board_get_upgrade_progress_status
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_set_upgrade_state
%attr(0555,system_fw,system_fw) %{_bindir}/device_board_get_upgrade_state
%attr(0554,system_fw,system_fw) %{_bindir}/device_board_set_upgrade_type
%attr(0555,system_fw,system_fw) %{_bindir}/device_board_get_upgrade_type

%files auto-test
%manifest deviced.manifest
%license LICENSE.Apache-2.0
%{_bindir}/deviced-auto-test

%files plugin-profile-common
%manifest deviced.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%config %{_sysconfdir}/deviced/display-profile-common.conf
%config %{_sysconfdir}/deviced/power-profile-common.conf
%{_libdir}/common-display.so
%{_unitdir}/rndis.service
%{_bindir}/rndis.sh

%files isu
/etc/isu/deviced/*

%files syscommon-plugin-test
%manifest deviced.manifest
%license LICENSE.Apache-2.0
%{_bindir}/syscommon-plugin-test
