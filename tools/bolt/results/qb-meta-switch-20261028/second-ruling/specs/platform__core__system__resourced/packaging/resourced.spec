# Note about configuration packages
#
# Consequently, to replace given configuration file it's enough to provide
# it from different package with higher priority.
#
# resourced reserves priorities 0-199 for its own internal use, please do
# not use these. Recommended priorities are 500-999 for packages wishing to
# override resourced-provided configuration files.

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

Name:       resourced
Summary:    Resource management daemon
Version:    10.0.0
Release:    1
Group:      System/Libraries
License:    Apache-2.0 AND BSD-3-Clause
Source0:    %{name}-%{version}.tar.gz

# Notice : to use freezer module, you should install system-freezer plugin
%define cpu_throttling_module   ON
%define cpu_boosting_module     ON
%define memory_module           ON
%define watchdog_module         ON
%define ebpf_enabled            OFF

%define confdir %{_sysconfdir}/resourced
%define plugindir %{_libdir}/resourced/plugins

BuildRequires:  cmake
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(leveldb)
BuildRequires:  pkgconfig(eventsystem)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(cmocka)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-resourced)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(cynara-creds-pid)
BuildRequires:  pkgconfig(security-manager)
BuildRequires:  pkgconfig(cynara-uid)
%if %{enable_system_server}
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(united-service)
BuildRequires:  pkgconfig(system-server-worker)
%endif
%if %{?ebpf_enabled} == ON
Requires:       libbpf
BuildRequires:  libbpf-devel
BuildRequires:  clang >= 10
BuildRequires:  llvm >= 10
BuildRequires:  bpftool
BuildRequires:  kernel-btf-devel
%endif

# for swap plugin
Requires:	%{_sbindir}/mkswap
Requires:	%{_bindir}/dd

%if %{?watchdog_module} == ON
Requires:	%{name}-watchdog-handler = %{version}-%{release}
%endif

Requires:	%{name}-bin = %{version}-%{release}
Requires:	%{name}-config = %{version}-%{release}
%description

%package	light
Summary:	Resourced light binary
Requires:	%{name}-bin = %{version}-%{release}
Requires:	%{name}-config = %{version}-%{release}
%if %{?watchdog_module} == ON
Requires:	%{name}-watchdog-handler = %{version}-%{release}
%endif
%description	light

%package	bin
Summary:	Resourced binary
%description	bin

%package	private-api-devel
Summary:	Headers for resourced modules private API
Requires:	%{name}-bin = %{version}-%{release}
%description	private-api-devel

%package	config
Summary:	Common configuration for resourced
%description	config

%package	config-tv
Summary:	Configuration for tv profile
Requires:	%{name}-config = %{version}-%{release}
%description	config-tv

%package	config-iot-headless
Summary:    Configuration for iot-headless profile
Requires:   %{name}-config = %{version}-%{release}
%description    config-iot-headless

%package	tests
Summary:	Tests for resourced
Requires:	%{name}-bin
%description	tests

%if %{?watchdog_module} == ON
%package	watchdog-handler
Summary:	watchdog module for resourced
%description	watchdog-handler
%endif

%package isu
Summary: ISU package for resourced
Group:   Application Framework/Service

%description isu
Configuration files to generate the ISU (Individual Service Upgrade) package

%package	monitor
Summary:	A monitor tool for resourced
Requires:	%{name}-monitor = %{version}-%{release}
%description	monitor

%prep
%setup -q

%ifarch %{arm} %ix86
%define ISU_ARCH_BIT 32
%else
%define ISU_ARCH_BIT 64
%endif

%build
mkdir -p build
_resourced_srcdir=$(pwd)
cd build
%cmake .. -DFULLVER=%{version}                        \
	 -DCMAKE_BUILD_TYPE=Release                       \
	 -DISU_ARCH_BIT=%{ISU_ARCH_BIT}                   \
	 -DCPU_THROTTLING_MODULE=%{cpu_throttling_module} \
	 -DCPU_BOOSTING_MODULE=%{cpu_boosting_module}     \
	 -DMEMORY_MODULE=%{memory_module}                 \
	 -DPROC_WATCHDOG=%{watchdog_module}               \
	 -DEBPF_ENABLED=%{ebpf_enabled}                   \
	 -DRD_SYS_ETC=%{TZ_SYS_ETC}                       \
	 -DRD_SYS_DATA=%{TZ_SYS_DATA}                     \
	 -DRD_SYS_DB=%{TZ_SYS_DB}                         \
	 -DRD_CONFIG_PATH=%{confdir}                      \
	 -DRD_PRODUCT_CONFIG_PATH=%{TZ_SYS_RO_PRODUCT_ETC}/resourced \
	 -DRD_PLUGIN_PATH=%{plugindir}                    \
	 -DRD_TESTS_PATH=%{_libdir}/resourced-tests       \
	 -DRD_BINARY_NAME=resourced                       \
%if %{enable_system_server}
	 -DSYSTEM_SERVER_DIR=%{_system_server_dir} \
%endif
	 -DENABLE_SYSTEM_SERVER=%{enable_system_server} \
	 %{?asan:-DASAN_BUILD=True}

make %{?jobs:-j%jobs}
cd "$_resourced_srcdir"

LIB_DIR=%{_libdir}
sed -ie s,"##LIBDIR##,$LIB_DIR,g" isu/isu.cfg
RD_PLUGIN_PATH=%{plugindir}
RD_PLUGIN_MOUNT_NAME=$(systemd-escape $RD_PLUGIN_PATH).mount
RD_PLUGIN_MOUNT_NAME=${RD_PLUGIN_MOUNT_NAME#?}
sed -ie s,"##PLUGIN_MOUNT##,$RD_PLUGIN_MOUNT_NAME,g" isu/isu.cfg
sed -ie s,"##PLUGIN_MOUNT##,$RD_PLUGIN_MOUNT_NAME,g" isu/resourced.service
sed -ie s,"##PLUGIN_LIB_DIR##,$RD_PLUGIN_PATH,g" isu/usr-lib-resourced-plugins.mount

%install
rm -rf %{buildroot}
_resourced_srcdir=$(pwd)
cd build
%make_install
mkdir -p %{buildroot}/%{TZ_SYS_DATA}/heart
mkdir -p %{buildroot}/%{TZ_SYS_DB}
cd "$_resourced_srcdir"

%if "%{asan}" == "1"
mkdir -p %{buildroot}%{_unitdir}/resourced.service.d
install -m 644 src/resourced/resourced.asan.conf %{buildroot}%{_unitdir}/resourced.service.d
%endif

%if %{?watchdog_module} == ON
%post watchdog-handler
chsmack %{_bindir}/resourced-watchdog-handler -a "System::Tools"
chsmack %{_bindir}/resourced-watchdog-handler.sh -a "System::Tools"
%endif

%post config-tv
mv %{confdir}/optimizer-profile-tv.conf %{confdir}/optimizer.conf

%files
%license LICENSE
%manifest resourced.manifest
%{plugindir}/libplugin-resourced-process-block.so
%{plugindir}/libplugin-resourced-limiter-freezer.so
%{plugindir}/libplugin-resourced-monitor-heart.so
%{plugindir}/libplugin-resourced-optimizer-memory-swap.so
%{plugindir}/libplugin-resourced-optimizer-memory-dedup.so
%{plugindir}/libplugin-resourced-optimizer-memory-compaction.so
%{plugindir}/libplugin-resourced-optimizer-cpu-sched.so
%attr(700, root, root) %{TZ_SYS_ETC}/dump.d/module.d/dump_heart_data.sh

%files bin
%license LICENSE LICENSE.BSD-3-Clause
%manifest resourced.manifest
%{_libdir}/libresourced-private-api.so.*
%dir %{plugindir}
%if %{enable_system_server}
%{_system_server_dir}/mod/libsystem-server-resourced.so
%else
%{_bindir}/resourced
%attr(-,root, root) %{_bindir}/resourced
%endif
%attr(700, root, root) %{TZ_SYS_ETC}/dump.d/module.d/dump_heart_data.sh

%files config
%config %{_sysconfdir}/dbus-1/system.d/org.tizen.resourced.conf
%if %{enable_system_server}
%{_system_server_dir}/conf/system-server-resourced.service
%endif
%{_unitdir}/resourced.service
%{_unitdir}/resourced.socket
%{_unitdir}/multi-user.target.wants/resourced.service
%{_unitdir}/sockets.target.wants/resourced.socket
%{confdir}/limiter.conf
%{confdir}/optimizer.conf
%{confdir}/process.conf
%{confdir}/monitor.conf
%if "%{asan}" == "1"
%{_unitdir}/resourced.service.d/resourced.asan.conf
%endif

%files config-tv
%manifest resourced.manifest
%{confdir}/optimizer-profile-tv.conf

%files config-iot-headless
%manifest resourced.manifest

%if %{?watchdog_module} == ON
%files watchdog-handler
%license LICENSE
%manifest resourced.manifest
%attr(700,root, root) %{_bindir}/resourced-watchdog-handler
%attr(700,root, root) %{_bindir}/resourced-watchdog-handler.sh
%endif

%files light
%manifest resourced.manifest

%files private-api-devel
%manifest resourced.manifest
%license LICENSE
%{_includedir}/resourced/private-api/*.h
%{_libdir}/libresourced-private-api.so
%{_libdir}/pkgconfig/resourced-private-api.pc

%files tests
%manifest resourced.manifest
%defattr(-,root,root)
%{_libdir}/resourced-tests/run_tests.sh
%{_libdir}/resourced-tests/watchdog-test

%files isu
/etc/isu/resourced/*

%files monitor
%{_bindir}/resourced-monitor
