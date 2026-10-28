Name:       amd
Summary:    Application Management Daemon
Version:    1.82.15
Release:    1
Group:      Application Framework/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source100:  ac.conf
Source101:  ac.service
Source102:  ac.socket
Source103:  amd.conf
Source1001: %{name}.manifest

Requires(post):   /sbin/ldconfig
Requires(post):   /usr/bin/systemctl
Requires(postun): /sbin/ldconfig
Requires(postun): /usr/bin/systemctl
Requires(preun):  /usr/bin/systemctl
Requires:   tizen-core
Requires:   tizen-platform-config

BuildRequires:  cmake
BuildRequires:  pkgconfig(argos_watchdog)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(aul-server)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(cert-svc-vcore)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(libsessiond)
BuildRequires:  pkgconfig(libsmack)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(parcel)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(rua)
BuildRequires:  pkgconfig(security-manager)
BuildRequires:  pkgconfig(sensor)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-database)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(tizen-launch-client)
BuildRequires:  pkgconfig(tizen-shared-queue)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-tbm-client)
BuildRequires:  pkgconfig(xkbcommon)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Application management daemon

%package devel
Summary:    Application Management Daemon (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Application Management Daemon (devel)

%package -n amd-mod-cooldown
Summary:    AMD module for supporting feature 'cool-down'
Group:      Application Framework/Service

%description -n amd-mod-cooldown
This module is for supporting feature 'cool-down'

%package -n amd-mod-wayland-core
Summary:    AMD module for connecting display server
Group:      Application Framework/Service

%description -n amd-mod-wayland-core
This module is for connecting display server

%package -n amd-mod-splash-screen
Summary:    AMD module for supporting feature 'splash-screen'
Group:      Application Framework/Service

%description -n amd-mod-splash-screen
This module is for supporting feature 'splash-screen'

%package -n amd-mod-input
Summary:    AMD module for controlling key and mouse events
Group:      Application Framework/Service

%description -n amd-mod-input
This module is for controlling key and mouse events

%package -n amd-mod-widget
Summary:    AMD module for widgets
Group:      Application Framework/Service

%description -n amd-mod-widget
This module is for supporting widgets

%package -n amd-mod-share
Summary:    AMD module for sharing application's private files
Group:      Application Framework/Service

%description -n amd-mod-share
This module is for supporting sharing of application's private files

%package -n amd-mod-ui-core
Summary:    AMD module for supporting UI related features
Group:      Application Framework/Service

%description -n amd-mod-ui-core
This module is for supporting UI related features such as 'app-group' and 'rua'

%package -n amd-mod-extractor
Summary:    AMD module for mounting and unmouting tizen package files
Group:      Application Framework/Service

%description -n amd-mod-extractor
This module is for mounting and unmouting tizen package files such as '.tep' and '.tpk'

%package -n amd-mod-cynara-core
Summary:    AMD module for access-control
Group:      Application Framework/Service

%description -n amd-mod-cynara-core
This module is for checking privileges

%package -n amd-mod-rua
Summary:    AMD module for managing recently-used-application
Group:      Application Framework/Service

%description -n amd-mod-rua
This module is for managing recently-used-application

%package -n amd-mod-watch
Summary:    AMD module for managing watch-application
Group:      Application Framework/Service

%description -n amd-mod-watch
This module is for managing watch-application

%package -n amd-mod-job-scheduler
Summary:    AMD module for supporting job-scheduler
Group:      Application Framework/Service

%description -n amd-mod-job-scheduler
This module is for supporting job-scheduler

%package -n amd-mod-boost
Summary:    AMD module for supporting cpu boost
Group:      Application Framework/Service

%description -n amd-mod-boost
This module is for supporting cpu boost

%package -n amd-mod-rpc-port
Summary:    AMD module for supporting rpc-port
Group:      Application Framework/Service

%description -n amd-mod-rpc-port
This module is for supporting rpc-port

%package -n amd-mod-complication
Summary:    AMD module for supporting complication
Group:      Application Framework/Service

%description -n amd-mod-complication
This module is for supporting complication

%package -n amd-mod-watchdog
Summary:    AMD module for supporting watchdog
Group:      Application Framework/Service

%description -n amd-mod-watchdog
This module is for supporting watchdog

%package -n amd-mod-screen-resolution
Summary:    AMD module for screen resolution
Group:      Application Framework/Service

%description -n amd-mod-screen-resolution
This module is for screen resolution

%package -n amd-mod-component-manager
Summary:    AMD module for managing components of component-based application
Group:      Application Framework/Service

%description -n amd-mod-component-manager
This module is for managing components of component-based application

%package -n amd-mod-loader-manager
Summary:    AMD module for managing loaders
Group:      Application Framework/Service

%description -n amd-mod-loader-manager
This module is for managing loaders

%package -n amd-mod-light-user
Summary:    AMD module for light user
Group:      Application Framework/Service

%description -n amd-mod-light-user
This module is for light user

%package -n amd-mod-argos-watchdog
Summary:    AMD module for using argos watchdog
Group:      Application Framework/Service

%description -n amd-mod-argos-watchdog
This module is for using argos watchdog

%package -n amd-mod-proc-group
Summary:    AMD module for managing proc groups
Group:      Application Framework/Service

%description -n amd-mod-proc-group
This module is for managing proc groups

%package -n org.tizen.NUIGadgetViewer
Summary:    NUIGadgetViewer Application
Group:      Application Framework/Service

%description -n org.tizen.NUIGadgetViewer
This package is for NUIGadget developers

%package -n amd-mod-cpu-monitor
Summary:    AMD module for monitoring cpu usage
Group:      Application Framework/Service

%description -n amd-mod-cpu-monitor
This module is for monitoring cpu usage

%package isu
Summary: ISU package for sensord
Group:   Application Framework/Service

%description isu
Configuration files to generate the ISU (Individual Service Upgrade) package


%if 0%{?gcov:1}
%package gcov
Summary:    AMD (gcov)
Group:      Application Framework/Testing

%description gcov
AMD gcov objects
%endif

%define _moddir %{_datadir}/amd
%define _preload_tpk_dir %{TZ_SYS_RO_APP}/.preload-tpk

%if "%{?_prelink_enable}" == "y"
%define tizen_feature_prelink 1
%else
%define tizen_feature_prelink 0
%endif

%prep
%setup -q
sed -i 's|TZ_SYS_DB|%{TZ_SYS_DB}|g' %{SOURCE1001}
cp %{SOURCE1001} .
cp %{SOURCE1001} ./org.tizen.NUIGadgetViewer.manifest

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

%if 0%{?simulator}
CFLAGS="%{optflags} -D__emul__"; export CFLAGS
%endif

%if 0%{?tizen_feature_terminate_unmanageable_app}
_TIZEN_FEATURE_TERMINATE_UNMANAGEABLE_APP=ON
%endif
%if 0%{?tizen_feature_block_input}
_TIZEN_FEATURE_BLOCK_INPUT=ON
%endif

%if 0%{?tizen_feature_prelink}
_TIZEN_FEATURE_PRELINK=ON
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DAMD_MODULES_DIR=%{_moddir} \
	-DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
	-D_TIZEN_FEATURE_PRELINK:BOOL=${_TIZEN_FEATURE_PRELINK} \
%if 0%{?asan} != 1
	-DASAN_ENABLED=FALSE \
%else
	-DASAN_ENABLED=TRUE \
%endif
	.

%__make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE100 %{buildroot}%{_tmpfilesdir}/ac.conf
install -m 0644 %SOURCE101 %{buildroot}%{_unitdir}/ac.service
install -m 0644 %SOURCE102 %{buildroot}%{_unitdir}/ac.socket
ln -sf ../ac.service %{buildroot}%{_unitdir}/basic.target.wants/ac.service
ln -sf ../ac.socket %{buildroot}%{_unitdir}/sockets.target.wants/ac.socket

mkdir -p %{buildroot}%{_datadir}/amd/conf
install -m 0644 %SOURCE103 %{buildroot}%{_datadir}/amd/conf/amd.conf

%preun
if [ "$1" = "0" ]; then
    systemctl stop ac.service
    systemctl disable ac
fi

%post
/sbin/ldconfig

systemctl daemon-reload
if [ "$1" = "1" ]; then
    systemctl restart ac.service
fi

%postun
/sbin/ldconfig
systemctl daemon-reload

%files
%license LICENSE
%manifest %{name}.manifest
%{_tmpfilesdir}/ac.conf
%{_unitdir}/ac.service
%{_unitdir}/basic.target.wants/ac.service
%{_unitdir}/ac.socket
%{_unitdir}/sockets.target.wants/ac.socket
%{_bindir}/amd
%{_libdir}/libamd.so.*
%{_moddir}/conf/amd.conf

%files devel
%{_includedir}/amd/*.h*
%{_libdir}/libamd.so
%{_libdir}/pkgconfig/*pc

%files -n amd-mod-cooldown
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-cooldown.so
%config %{_sysconfdir}/dbus-1/system.d/org.tizen.application.manager.conf

%files -n amd-mod-wayland-core
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-wayland-core.so

%files -n amd-mod-splash-screen
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-splash-screen.so

%files -n amd-mod-input
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-input.so
%{_moddir}/conf/amd_input.conf

%files -n amd-mod-widget
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-widget.so

%files -n amd-mod-share
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-share.so

%files -n amd-mod-ui-core
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-ui-core.so

%files -n amd-mod-extractor
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-extractor.so

%files -n amd-mod-cynara-core
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-cynara-core.so

%files -n amd-mod-rua
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-rua.so

%files -n amd-mod-watch
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-watch.so

%files -n amd-mod-job-scheduler
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-job-scheduler.so

%files -n amd-mod-boost
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-boost.so

%files -n amd-mod-rpc-port
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-rpc-port.so

%files -n amd-mod-complication
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-complication.so

%files -n amd-mod-watchdog
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-watchdog.so
%{_moddir}/conf/amd_watchdog.conf

%files -n amd-mod-screen-resolution
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-screen-resolution.so
%{_moddir}/conf/amd_screen_resolution.conf

%files -n amd-mod-component-manager
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-component-manager.so

%files -n amd-mod-loader-manager
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-loader-manager.so

%files -n amd-mod-light-user
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-light-user.so

%files -n amd-mod-argos-watchdog
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-argos-watchdog.so
%{_moddir}/conf/amd_argos_watchdog.conf

%files -n amd-mod-proc-group
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-proc-group.so

%files -n org.tizen.NUIGadgetViewer
%manifest %{name}.manifest
%license LICENSE
%{_preload_tpk_dir}/org.tizen.NUIGadgetViewer-1.0.0.tpk

%files -n amd-mod-cpu-monitor
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libamd-mod-cpu-monitor.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files isu
/etc/isu/amd/isu.cfg
/etc/isu/amd/system-services/ac.service
