# "on_off foo" wil turn into "ON" or "OFF"
%define on_off() %{expand:%%{?with_%{1}:ON}%%{!?with_%{1}:OFF}}

%define _with_tests on
%define _with_regdumper on
%define _with_livedumper on
%define _with_dumpsystemstateservice on

%bcond_with doc
%bcond_with tests
%bcond_with regdumper
%bcond_with livedumper
%bcond_with dumpsystemstateservice

# NOTE: To disable coredump set DumpCore=0 in configuration file

Name:           crash-worker
Summary:        Coredump handler and report generator for Tizen
Version:        10.0.1
Release:        1
Group:          Framework/system
License:        MIT
Source0:        %{name}-%{version}.tar.gz
Source1:        210.%{name}-platform-extension-migration.sh
Source1001:     crash-worker.manifest
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(rpm)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  cmake
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(libunwind-generic)
BuildRequires:  libcap-devel
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(yaca)
BuildRequires:  pkgconfig(diagnostics)
BuildRequires:  pkgconfig(bugreport)
BuildRequires:  pkgconfig(libisu)
BuildRequires:  pkgconfig(libarchive)
%if %{with dumpsystemstateservice}
BuildRequires:  pkgconfig(dumpsys-system)
%endif

%if %{with doc}
BuildRequires:  doxygen
%endif

%if %{with livedumper}
BuildRequires:  boost-devel
%endif

Requires:       bugreport-service = %{version}-%{release}
Requires:       %{name}-dumpsystemstate-util = %{version}-%{release}
%if %{with dumpsystemstateservice}
Requires:       %{name}-dumpsystemstate-service = %{version}-%{release}
%endif
%if %{with regdumper}
Requires:       %{name}-support-regdump = %{version}-%{release}
%endif
%description

%package        dumpsystemstate-config
Summary:        common configuration for dump_systemstate utility and bugreport-service
License:        MIT
%description    dumpsystemstate-config

%package        dumpsystemstate-util
Summary:        dump_systemstate utility used for dumping basic system information
License:        Apache-2.0 and MIT
Requires:       %{name}-dumpsystemstate-config = %{version}-%{release}
Requires:       %{_bindir}/buxton2ctl
# Ensure crash_worker user is available (created by security-config, package provides crash_worker-owned files)
Requires:       security-config
%description    dumpsystemstate-util

%if %{with dumpsystemstateservice}
%package        dumpsystemstate-service
Summary:        service provides dumpsys provider to system state information
License:        Apache-2.0 and MIT
Requires:       %{name}-dumpsystemstate-config = %{version}-%{release}
%description    dumpsystemstate-service
%endif

%if %{with regdumper}
%package        support-regdump
Summary:        package provides components needed to support kernel-invoked coredump handling
License:        MIT
Requires:       %{name}-support-common = %{version}-%{release}
Requires:       minicoredumper >= 2.1.0
# Ensure crash_worker user is available (created by security-config, package provides crash_worker-owned files)
Requires:       security-config
%description    support-regdump
%endif

%if %{with livedumper}
%package        support-livecoredump
Summary:        package provides components needed to support livecoredumps
License:        Apache-2.0 and MIT
Requires:       %{name}-support-common = %{version}-%{release}
Provides:       %{name}-livedumper = %{version}-%{release}
%description    support-livecoredump
%endif

%package        support-common
Summary:        package provides common components needed to support both kernel-invoked coredump and livedump
License:        Apache-2.0 and BSD-2-Clause and MIT
Requires:       %{name}-dumpsystemstate-util = %{version}-%{release}
Requires:       zip
# Ensure crash_worker user is available (created by security-config, package provides crash_worker-owned files)
Requires:       security-config
Requires:       libisu
%description    support-common

%package -n     libcrash-manager-devel
Summary:        package provides headers needed to develop programs using libcrash-manager
License:        MIT
%description -n libcrash-manager-devel

%package -n     bugreport-service
Summary:        bugreport provides dumpsys provider for diagnostics data
License:        Apache-2.0 and MIT
Requires:       %{name}-dumpsystemstate-util = %{version}-%{release}
%if %{with livedumper}
Requires:       %{name}-support-livecoredump = %{version}-%{release}
%endif
%description -n bugreport-service

%if %{with doc}
%package        doc
Summary:        Documentation package for crash-worker
Group:          Framework/System
%description    doc
%endif

%if %{with tests}
%package        tests
Summary:        Package with binaries and data for crash-worker tests
%description    tests
%endif

%package        system-tests
Summary:        System tests for crash-worker components
Requires:       diff
Requires:       gdb
Requires:       coreutils
Requires:       tlm
Requires:       /bin/bash
Requires:       /bin/tar
Requires:       /usr/bin/unzip
Requires:       /usr/bin/mcookie
Requires:       /usr/bin/json-glib-validate
Requires:       %{_sbindir}/minicoredumper
Requires:       %{name}-system-tests-debuginfo = %{version}-%{release}
Requires:       %{name}-support-livecoredump = %{version}-%{release}
Requires:       %{name}-support-regdump = %{version}-%{release}
%description    system-tests

%prep
%setup -q

#Path to store logs and coredump files
%define crash_root_path %{TZ_SYS_CRASH_ROOT}
%define crash_path      %{TZ_SYS_CRASH}
%define crash_temp      %{crash_root_path}/temp

#Debug mode path - existence of file at path below mean that core file should be generated
%define debugmode_path      %{TZ_SYS_ETC}/.debugmode

%define upgrade_script_path %{TZ_SYS_RO_SHARE}/upgrade/scripts

%build
cp %{SOURCE1001} .

export CFLAGS="$CFLAGS -Werror"

%ifarch %{arm} aarch64
	%define ARCH arm
%else
	%define ARCH x86
%endif

%ifarch %{arm} %ix86
	%define ARCH_BIT 32
%else
	%define ARCH_BIT 64
%endif

%cmake . \
	   -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	   -DTMP_FILES_DIR=%{_sysconfdir}/tmpfiles.d \
	   -DARCH=%{ARCH} \
	   -DARCH_BIT=%{ARCH_BIT} \
	   -DDUMP_SYSTEMSTATE_CONFIG_DIR_PATH=%{_sysconfdir}/dump_systemstate.conf.d \
	   -DCRASH_MANAGER_CONFIG_PATH=%{_sysconfdir}/crash-manager.conf \
	   -DCRASH_MANAGER_CONFIG_HAL_PATH=/hal/etc/crash-manager.conf \
	   -DCRASH_ROOT_PATH=%{crash_root_path} \
	   -DCRASH_PATH=%{crash_path} \
	   -DCRASH_TEMP=%{crash_temp} \
	   -DDEBUGMODE_PATH=%{debugmode_path} \
	   -DMINICOREDUMPER_BIN_PATH=%{_sbindir}/minicoredumper \
	   -DMINICOREDUMPER_CONFIG_PATH=%{_sysconfdir}/minicoredumper/minicoredumper.cfg.json \
	   -DLIVEDUMPER_BIN_PATH=%{_bindir}/livedumper \
	   -DDUMP_SYSTEMSTATE_BIN_PATH=%{_bindir}/dump_systemstate \
	   -DCRASH_STACK_BIN_PATH=%{_libexecdir}/crash-stack \
	   -DCRASH_POPUP_BIN_PATH=%{_libexecdir}/crash-popup-launch \
	   -DCRASH_NOTIFY_BIN_PATH=%{_libexecdir}/crash-notify-send \
	   -DCRASH_TESTS_PATH=%{_libexecdir}/crash-worker/tests \
	   -DCRASH_SYSTEM_TESTS_PATH=%{_libexecdir}/crash-worker/system-tests \
	   -DLIVEDUMPER=%{on_off livedumper} \
	   -DDUMP_SYSTEMSTATE_SERVICE=%{on_off dumpsystemstateservice} \
	   -DUPGRADE_SCRIPT_PATH=%{upgrade_script_path} \
	   -DLOGGER=dlog \
	   -DDLOG_LOG_LEVEL=DLOG_INFO \
	   -DTESTS=%{on_off tests} \
	   -DVERSION=%{version}

make %{?jobs:-j%jobs}

%if %{with doc}
make doc
%endif

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/usr/share/platform-extension
install -m 0755 %{SOURCE1} %{buildroot}/usr/share/platform-extension

%if ! %{with regdumper}
rm -f %{buildroot}%{_prefix}/lib/sysctl.d/70-crash-manager.conf
rm -f %{buildroot}%{_bindir}/crash-manager
rm -f %{buildroot}%{_libexecdir}/crash-popup-launch
rm -f %{buildroot}%{_libexecdir}/crash-notify-send
rm -f %{buildroot}%{_prefix}/lib/debug/usr/bin/crash-manager.debug
rm -f %{buildroot}%{_prefix}/lib/debug/usr/libexec/crash-notify-send.debug
rm -f %{buildroot}%{_prefix}/lib/debug/usr/libexec/crash-popup-launch.debug
%endif

%if ! %{with livedumper}
rm -f %{buildroot}%{_bindir}/livedumper
rm -f %{buildroot}%{_prefix}/lib/debug/usr/bin/livedumper.debug
%endif

%if ! %{with regdumper} && ! %{with livedumper}
rm -f %{buildroot}%{_libdir}/libcrash-manager.so*
rm -f %{buildroot}%{_bindir}/crash-json2info
rm -f %{buildroot}%{_libexecdir}/crash-stack
rm -f %{buildroot}%{_sysconfdir}/crash-manager.conf
rm -f %{buildroot}%{_sysconfdir}/crash-manager.conf.d/crash-manager.conf.example
rm -f %{buildroot}%{_prefix}/lib/debug/usr/bin/crash-json2info.debug
rm -f %{buildroot}%{_prefix}/lib/debug/usr/libexec/crash-stack.debug
rm -f %{buildroot}%{_prefix}/lib/debug/usr/lib/libcrash-manager.so*
rm -f %{buildroot}%{_includedir}/crash-manager.h
rm -f %{buildroot}%{_prefix}/lib/pkgconfig/crash-manager.pc
%endif

%files
%license LICENSE.MIT
%manifest crash-worker.manifest

%files dumpsystemstate-util
%manifest crash-worker.manifest
%license LICENSE.Apache-2.0 LICENSE.MIT
# attr() needed because: dump_systemstate has Smack exec_label(=System) set and we don't want to allow everyone to abuse it
%attr(0750,root,crash_worker) %{_bindir}/dump_systemstate

%if %{with dumpsystemstateservice}
%files dumpsystemstate-service
%license LICENSE.Apache-2.0 LICENSE.MIT
%manifest crash-worker.manifest
%{_bindir}/dump_systemstate-service
%{_unitdir}/dump_systemstate.service
%{_datadir}/dbus-1/system-services/org.tizen.dumpsys.providers.org.tizen.systemstate.service
%endif

%files dumpsystemstate-config
%manifest crash-worker.manifest
%license LICENSE.MIT
%{_sysconfdir}/dump_systemstate.conf.d/files/*.conf*
%{_sysconfdir}/dump_systemstate.conf.d/programs/*.conf*
%{_libexecdir}/dump_systemstate/buxton-wait

%if %{with regdumper}
%files support-regdump
%license LICENSE.MIT
%manifest crash-worker.manifest
%{_prefix}/lib/sysctl.d/70-crash-manager.conf
# attr() needed because: crash-worker has Smack exec_label(=System::Privileged) set and we don't want to allow everyone to abuse it
%attr(0750,root,crash_worker) %{_bindir}/crash-manager
%{_libexecdir}/crash-popup-launch
%{_libexecdir}/crash-notify-send
%endif

%if %{with livedumper}
%files support-livecoredump
%license LICENSE.Apache-2.0 LICENSE.MIT
%manifest crash-worker.manifest
%manifest %{name}.manifest
%{_bindir}/livedumper
%endif

%if %{with livedumper} || %{with regdumper}
%files support-common
%license LICENSE.Apache-2.0 LICENSE.BSD LICENSE.MIT
%manifest crash-worker.manifest
%attr(0755,root,root) /usr/share/platform-extension/210.crash-worker-platform-extension-migration.sh
%{_libdir}/libcrash-manager.so.*
%{_bindir}/crash-json2info
%{_libexecdir}/crash-stack
%{_sysconfdir}/crash-manager.conf
%{_sysconfdir}/crash-manager.conf.d/crash-manager.conf.example

%files -n libcrash-manager-devel
%license LICENSE.MIT
%manifest crash-worker.manifest
%{_includedir}/crash-manager.h
%{_libdir}/libcrash-manager.so
%{_libdir}/pkgconfig/crash-manager.pc
%endif

%files -n bugreport-service
%license LICENSE.Apache-2.0 LICENSE.MIT
%manifest crash-worker.manifest
%attr(0755,root,root) /usr/share/platform-extension/210.crash-worker-platform-extension-migration.sh
%attr(0750,crash_worker,crash_worker) %{_bindir}/bugreport-service
%attr(-,root,root) %{_unitdir}/bugreport.service
%attr(-,root,root) %{_sysconfdir}/dbus-1/system.d/bugreport-service.conf
%attr(-,root,root) %{_datadir}/dbus-1/system-services/org.tizen.system.crash.livedump.service
%attr(-,root,root) %{_datadir}/dbus-1/system-services/org.tizen.system.diagnostics.service
%attr(-,root,root) %{_datadir}/dbus-1/system-services/org.tizen.dumpsys.providers.org.tizen.bugreport-service.service
%attr(0644,root,root) %{_prefix}/lib/tmpfiles.d/diagnostics-run.conf

%if %{with doc}
%files doc
%{_datadir}/doc/crash-worker
%endif

%if %{with tests}
%files tests
%manifest %{name}.manifest
%license LICENSE.MIT
%{_libexecdir}/crash-worker/tests/test1-default-crash
%{_libexecdir}/crash-worker/tests/test1-default-sleep
%{_libexecdir}/crash-worker/tests/test1-default-ill
%{_libexecdir}/crash-worker/tests/test1-custom-crash
%{_libexecdir}/crash-worker/tests/test1-custom-sleep
%{_libexecdir}/crash-worker/tests/test1-custom-ill
%{_libexecdir}/crash-worker/tests/run_tests.sh
%{_libexecdir}/crash-worker/tests/tests_common.sh
%{_libexecdir}/crash-worker/tests/crash_common.sh

%files system-tests
%manifest %{name}.manifest
%license LICENSE.MIT
%{_bindir}/crash-worker-system-tests-run

%{_libexecdir}/crash-worker/system-tests/bugreport_crash_info_json/bugreport_crash_info_json.sh
%{_libexecdir}/crash-worker/system-tests/bugreport_created/bugreport_created.sh
%{_libexecdir}/crash-worker/system-tests/check_minicore_mem/check_minicore_mem.sh
%{_libexecdir}/crash-worker/system-tests/check_minicore_mem/cp.sh
%{_libexecdir}/crash-worker/system-tests/clean_temp/clean_temp.sh
%{_libexecdir}/crash-worker/system-tests/cmp_backtraces/cmp_backtraces.sh
%{_libexecdir}/crash-worker/system-tests/cmp_backtraces/cp.sh
%{_libexecdir}/crash-worker/system-tests/copy_tizen_manifest/copy_tizen_manifest.sh
%{_libexecdir}/crash-worker/system-tests/crash_root_path/crash_root_path.sh
%{_libexecdir}/crash-worker/system-tests/critical_process/critical_process.sh
%{_libexecdir}/crash-worker/system-tests/dbus_notify/dbus_notify.sh
%{_libexecdir}/crash-worker/system-tests/dbus_notify_legacy/dbus_notify_legacy.sh
%{_libexecdir}/crash-worker/system-tests/dump_systemstate_extras/dump_systemstate_extras.sh
%{_libexecdir}/crash-worker/system-tests/exclude_paths/exclude_paths.sh
%{_libexecdir}/crash-worker/system-tests/extra_script/extra_script.sh
%{_libexecdir}/crash-worker/system-tests/full_core/full_core.sh
%{_libexecdir}/crash-worker/system-tests/info_file/info_file.sh
%{_libexecdir}/crash-worker/system-tests/libbugreport-service/libbugreport-service.sh
%{_libexecdir}/crash-worker/system-tests/libbugreport-service_systemstate/libbugreport-service_systemstate.sh
%{_libexecdir}/crash-worker/system-tests/log_file/log_file.sh
%{_libexecdir}/crash-worker/system-tests/output_param/output_param.sh
%{_libexecdir}/crash-worker/system-tests/report_basic/report_basic.sh
%{_libexecdir}/crash-worker/system-tests/report_type_info/report_type_info.sh
%{_libexecdir}/crash-worker/system-tests/so_info_file/so_info_file.sh
%{_libexecdir}/crash-worker/system-tests/temp_lock/temp_lock.sh
%{_libexecdir}/crash-worker/system-tests/time_test/cp.sh
%{_libexecdir}/crash-worker/system-tests/time_test/time_test.sh
%{_libexecdir}/crash-worker/system-tests/utils/btee
%{_libexecdir}/crash-worker/system-tests/utils/kenny
%{_libexecdir}/crash-worker/system-tests/utils/libbugreport-servicetest
%{_libexecdir}/crash-worker/system-tests/utils/diagnostics_bugreporttest
%{_libexecdir}/crash-worker/system-tests/utils/minicore-utils.sh
%{_libexecdir}/crash-worker/system-tests/wait_for_opt_usr/wait_for_opt_usr.sh
%{_libexecdir}/crash-worker/system-tests/without_so_info_file/without_so_info_file.sh
%{_libexecdir}/crash-worker/system-tests/without_core/without_core.sh

%if %{with livedumper}
%{_libexecdir}/crash-worker/system-tests/livedumper/livedumper.sh
%endif

%endif
