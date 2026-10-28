Name:    ode
Version: 0.0.5
Release: 0
License: Apache-2.0
Source0: file://%{name}-%{version}.tar.gz
Summary: Tizen device encryption and secure erase manager
Group:   Security/Service
Requires: systemd
Requires: e2fsprogs
BuildRequires: gcc
BuildRequires: cmake
BuildRequires: gettext-tools
BuildRequires: pkgconfig(klay)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(blkid)
BuildRequires: pkgconfig(capi-system-device)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(ext2fs)
BuildRequires: pkgconfig(com_err)
BuildRequires: pkgconfig(gio-2.0)
Requires: cryptsetup

%global key_storage_plugin_dir %{_libdir}/ode-key-storage-plugin/
%global softreset_dir /usr/system/RestoreDir/softreset/
%define upgrade_script_dir /usr/share/upgrade/scripts/
%global socket_path %{TZ_SYS_RUN}/.ode.sock
%global dbus_system_services_dir %{_datadir}/dbus-1/system-services/
%global dbus_conf_dir %{_sysconfdir}/dbus-1/system.d/
%global dbus_name org.tizen.%{name}

%description
The ode package provides a daemon which is responsible for encrypting/decryption storages and secure erasing.

%files
%manifest ode.manifest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/oded
%{_unitdir}/ode.service
%{_unitdir}/ode.socket
%{dbus_system_services_dir}/%{dbus_name}.service
%{dbus_conf_dir}/%{dbus_name}.conf
%attr(700,root,root) %{TZ_SYS_SBIN}/ode-admin-cli
%attr(700,root,root) %{softreset_dir}/ode_softreset.sh
%attr(750,root,system_share) %{TZ_SYS_SBIN}/ode-fota
%{_datadir}/%{name}
%dir %{key_storage_plugin_dir}
%attr(755,root,root) %{upgrade_script_dir}/500.ode_upgrade.sh

%prep
%setup -q

%build
%{!?build_type:%define build_type "RELEASE"}

%if %{build_type} == "DEBUG" || %{build_type} == "PROFILING" || %{build_type} == "CCOV"
	CFLAGS="$CFLAGS -Wp,-U_FORTIFY_SOURCE"
	CXXFLAGS="$CXXFLAGS -Wp,-U_FORTIFY_SOURCE"
%endif

%cmake . -DVERSION=%{version} \
         -DCMAKE_BUILD_TYPE=%{build_type} \
         -DRUN_DIR=%{TZ_SYS_RUN} \
         -DBIN_DIR=%{TZ_SYS_BIN} \
         -DSBIN_DIR=%{TZ_SYS_SBIN} \
         -DSYSTEMD_UNIT_DIR=%{_unitdir} \
         -DAPP_INSTALL_PREFIX="%{TZ_SYS_RO_APP}" \
         -DAPP_SHARE_PACKAGES_DIR="%{TZ_SYS_RO_PACKAGES}" \
         -DSOFTRESET_DIR="%{softreset_dir}" \
         -DKEY_STORAGE_PLUGIN_DIR="%{key_storage_plugin_dir}" \
         -DUPGRADE_SCRIPT_DIR="%{upgrade_script_dir}" \
         -DSOCKET_PATH="%{socket_path}" \
         -DBUS_SYSTEM_SERVICES_DIR="%{dbus_system_services_dir}" \
         -DBUS_CONF_DIR="%{dbus_conf_dir}" \
         -DBUS_NAME="%{dbus_name}"

make %{?jobs:-j%jobs}

%install
%make_install

%clean
rm -rf %{buildroot}

%pre
if [ $1 = 2 ]; then
    # upgrade
    systemctl stop ode.service
fi

%post
systemctl enable ode.socket
if [ $1 = 1 ]; then
    # installation
    systemctl start ode.socket
elif [ $1 = 2 ]; then
    # update
    systemctl daemon-reload
    systemctl restart ode.socket
fi

%preun
if [ $1 = 0 ]; then
    # uninstall
    systemctl disable ode.socket
    systemctl stop ode.socket
    systemctl stop ode.service
fi

## ODE Client Package ########################################################
%package -n libode
Summary: Library for Tizen device encryption and secure erase
Group: Security/Libraries
BuildRequires: pkgconfig(libtzplatform-config)
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libode
The libode package contains the libraries needed to encrypt/decrypt storages and secure erasing.

%post -n libode -p /sbin/ldconfig

%postun -n libode -p /sbin/ldconfig

%files -n libode
%manifest ode.manifest
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libode.so.%{version}
%{_libdir}/libode.so.0

## Devel Package ##############################################################
%package -n libode-devel
Summary: Libraries and header files for device encryption client development
Group: Development/Libraries
Requires: libode = %{version}-%{release}

%description -n libode-devel
The libode-devel package includes the libraries and header files necessary for
developing device encryption client program.

%files -n libode-devel
%manifest ode.manifest
%defattr(644,root,root,755)
%{_libdir}/libode.so
%{_includedir}/ode
%{_libdir}/pkgconfig/ode.pc

## Plugin Devel Package ##############################################################
%package ksp-devel
Summary: Header files for key storage plugin development
Group: Development/Libraries

%description ksp-devel
The ode-ksp-devel package includes header files necessary for key storage
plugin development

%files ksp-devel
%manifest ode.manifest
%defattr(644,root,root,755)
%{_includedir}/ode-key-storage-plugin
%{_libdir}/pkgconfig/ode-key-storage-plugin.pc

## Unittest Package ###########################################################
%package unit-tests
Summary: Unit tests to verify components of device encryption
Group: Security/Testing
Requires: libode = %{version}-%{release}

%description unit-tests
The libode-devel package includes the libraries and header files necessary for
developing device encryption client program.

%files unit-tests
%manifest ode.manifest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ode-engine-unit-tests

## Dummy key storage plugin Package ###########################################################
%package dummy-ksp
Summary: Dummy key storage plugin for FOTA binary upgrade testing
Group: Security/Testing

%description dummy-ksp
The ode-dummy-ksp package includes the dummy key storage plugin that can be used
for testing the binary upgrade process (FOTA). The plugin will be used by ode to
store the master encryption key in a file to use during FOTA process.

%files dummy-ksp
%manifest ode.manifest
%attr(755,root,root) %{key_storage_plugin_dir}/*
