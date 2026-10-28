#These options are DEACTIVATED by default.
%bcond_with emulator
%define extended_storage 0

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

Name:       storaged
Summary:    Storaged
Version:    10.0.0
Release:    1
Group:      System/Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  pkgconfig(argos_watchdog)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(app2sd)
BuildRequires:  pkgconfig(blkid)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(devmapper)

BuildRequires:  pkgconfig(capi-ui-efl-util)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(capi-appfw-preference)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-system-system-settings)
BuildRequires:  pkgconfig(efl-extension)
%if %{extended_storage}
BuildRequires:  pkgconfig(ode)
%endif
%if %{enable_system_server}
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(united-service)
BuildRequires:  pkgconfig(system-server-worker)
%endif

#For /usr/bin/msgfmt
BuildRequires: gettext-tools

Requires(post): /usr/bin/vconftool

Requires: /usr/bin/fsck_msdosfs
Requires: /usr/bin/newfs_msdos

%description
storage daemon.

%package  module_block
Summary:  block module plugin
Requires: %{name} = %{version}-%{release}
%description module_block
block module plugin

%package  module_storage
Summary:  storage module plugin
Requires: %{name} = %{version}-%{release}
%description module_storage
storage module plugin

%package  org.tizen.extended-sd
Summary:  App to setup sdcard
Requires: %{name} = %{version}-%{release}
%description org.tizen.extended-sd
App to setup sdcard

%package auto-test
Summary:  Storaged auto test tool
Group:    System/Utilities
%description auto-test
Storaged helper programs.
This package can be installed optional for auto dbus test.

%prep
%setup -q
cp %{SOURCE1} .

%build
%if %{with emulator}
	%define ARCH emulator
%else
	%ifarch %{arm} aarch64
		%define ARCH arm
	%else
		%define ARCH x86
	%endif
%endif

%ifarch %{arm} %ix86
	%define ARCH_BIT 32
%else
	%define ARCH_BIT 64
%endif

%define APP_PREFIX    "/usr/apps/org.tizen.extended-sd"

%cmake . \
	-DTZ_SYS_ETC=%TZ_SYS_ETC \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_APP_PREFIX=%{APP_PREFIX} \
	-DAPP_INSTALL_PREFIX="%{TZ_SYS_RO_APP}" \
	-DAPP_SHARE_PACKAGES_DIR="%{TZ_SYS_RO_PACKAGES}" \
	-DARCH=%{ARCH} \
	-DARCH_BIT=%{ARCH_BIT} \
	-DPROFILE=mobile \
	-DBLOCK_MODULE=on \
	-DBLOCK_TMPFS=on \
	-DSTORAGE_MODULE=on \
	-DEXTENDED_STORAGE=%{extended_storage} \
	-DCRITICAL_LOG_MODULE=on \
%if %{enable_system_server}
	-DSYSTEM_SERVER_DIR=%{_system_server_dir} \
%endif
	-DENABLE_SYSTEM_SERVER=%{enable_system_server} \
	#eol

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%install_service delayed.target.wants storaged.service

%if "%{asan}" == "1"
mkdir -p %{buildroot}%{_unitdir}/storaged.service.d
install -m 644 systemd/storaged.asan.conf %{buildroot}%{_unitdir}/storaged.service.d
%endif

%find_lang extended-sd

%post
systemctl daemon-reload
if [ "$1" == "1" ]; then
    systemctl restart storaged.service
fi

%postun
systemctl daemon-reload

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%config %{_sysconfdir}/dbus-1/system.d/org.tizen.system.storage.conf
%{_datadir}/dbus-1/system-services/org.tizen.system.storage.service
%{_unitdir}/delayed.target.wants/storaged.service
%{_unitdir}/storaged.service
%if %{enable_system_server}
%{_system_server_dir}/mod/libsystem-server-storaged.so
%{_system_server_dir}/conf/system-server-storaged.service
%else
%{_bindir}/storaged
%endif
%if "%{asan}" == "1"
%{_unitdir}/storaged.service.d/storaged.asan.conf
%endif

%files module_block
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_libdir}/storaged/module_block.so
%config %{_sysconfdir}/storaged/block.conf

%files module_storage
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_libdir}/storaged/module_storage.so
%config %{_sysconfdir}/storaged/storage.conf

%files org.tizen.extended-sd -f extended-sd.lang
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{TZ_SYS_RO_APP}/org.tizen.extended-sd/bin/*
%{TZ_SYS_RO_APP}/org.tizen.extended-sd/res/*
%{TZ_SYS_RO_PACKAGES}/org.tizen.extended-sd.xml
%{TZ_SYS_RO_APP}/org.tizen.extended-sd/res/edje/extended-sd.edj

%files auto-test
%license LICENSE.Apache-2.0
%manifest %{name}.manifest
%{_bindir}/storaged-auto-test
