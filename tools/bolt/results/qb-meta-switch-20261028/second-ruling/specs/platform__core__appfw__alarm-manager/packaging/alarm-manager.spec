Name:       alarm-manager
Summary:    Alarm library
Version:    0.14.14
Release:    1
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source2:    alarm-server.socket
Source3:    alarm-manager-tmpfilses.conf
Source4:    99-rtc.rules
Source5:    alarm-manager.conf
Source1001: alarm-server.manifest
Source1002: alarm-lib.manifest
Source1003: alarm-server-plugin.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: tidl
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(cert-svc-vcore)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(appsvc)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(pkgmgr)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(capi-system-device)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(eventsystem)
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(rpc-port)
BuildRequires: python-xml
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(tizen-database)
BuildRequires: pkgconfig(tizen-core)
BuildRequires: pkgconfig(united-service)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%if 0%{?gcov:1}
BuildRequires: pkgconfig(gmock)
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%define logdir /var/log/appfw/alarmmgr_log

%description
Alarm Server and devel libraries


%package -n alarm-server
Summary:    Alarm server
Group:      Development/Libraries

%description -n alarm-server
Alarm Server, manages alarms


%package -n libalarm
Summary:    Alarm server libraries
Group:      Development/Libraries
Requires:   alarm-server = %{version}-%{release}

%description -n libalarm
Alarm server libraries for client


%package -n libalarm-devel
Summary:    Alarm server libraries (devel)
Group:      Development/Libraries
Requires:   libalarm = %{version}-%{release}

%description -n libalarm-devel
Alarm server libraries development package (devel)


%package -n alarm-config-all-service-permitted
Summary:    Configuration for permitting all service applications
Group:      Development/Libraries
Requires:   libalarm = %{version}-%{release}

%description -n alarm-config-all-service-permitted
A configuration file package for permitting all service applications


%package -n alarm-config-platform-service-permitted
Summary:    Configuration for permitting platform service applications
Group:      Development/Libraries
Requires:   libalarm = %{version}-%{release}

%description -n alarm-config-platform-service-permitted
A configuration file package for permitting all service applications that have been platform certified


%package -n alarm-config-service-restricted
Summary:    Configuration for restricting service applications
Group:      Development/Libraries
Requires:   libalarm = %{version}-%{release}

%description -n alarm-config-service-restricted
A configuration file package for restricting service applications

#################################################
# plugin
#################################################
%package -n alarm-server-plugin
Summary:    Alarm server plugin libraries
License:    apache-2.0
Group:      Development/Libraries
Requires:   alarm-server-plugin = %{version}-%{release}

%description -n alarm-server-plugin
A plugin package for alarm-server


#################################################
# unittests
#################################################
%package unittests
Summary:    GTest for alarm manager library
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for alarm-manager library


#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Alarm library (gcov)
Group:      Application Framework/Testing

%description gcov
Alarm library gcov objects
%endif

%define _modname esd
%define _moddir %{_datadir}/united-service/%{_modname}


%prep
%setup -q
cp %{SOURCE1001} ./
cp %{SOURCE1002} ./
cp %{SOURCE1003} ./
/bin/bash ./tidl/prebuild.sh

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS+=" -Wno-error=unknown-warning-option"
%endif
}
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%define appfw_feature_alarm_manager_module_log 1
%if 0%{?appfw_feature_alarm_manager_module_log}
	_APPFW_FEATURE_ALARM_MANAGER_MODULE_LOG=ON
%endif

%cmake . -DOBS=1 \
	-DMOD_DIR=%{_moddir} \
	-DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DTZ_SYS_ETC=%{TZ_SYS_ETC} \
	-D_APPFW_FEATURE_ALARM_MANAGER_MODULE_LOG:BOOL=${_APPFW_FEATURE_ALARM_MANAGER_MODULE_LOG} \
	-DALARM_CONF_DIR=%{_datadir}/alarm-manager \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
	%{?asan:-DASAN_BUILD=True} \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

install -m 755 -d %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/alarm-manager.conf

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
ln -sf ../alarm-server.socket %{buildroot}%{_unitdir}/sockets.target.wants/alarm-server.socket

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
mkdir -p %{buildroot}%{_unitdir_user}/sockets.target.wants
install -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/alarm-server.socket
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE3 %{buildroot}%{_tmpfilesdir}/alarm-manager-tmpfilses.conf
mkdir -p %{buildroot}/usr/lib/udev/rules.d
install -m 0644 %SOURCE4 %{buildroot}/usr/lib/udev/rules.d
mkdir -p %{buildroot}%{logdir}

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

#################################################
# generate unittest automation script
#################################################
cat << EOF > run-unittest.sh
#!/bin/bash
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/gtest-alarmmgr
}

teardown() {
    echo "teardown start"
}

main() {
    setup
    test_main
    teardown
}

main "$@"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}

%check
export LD_LIBRARY_PATH=../lib
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n alarm-server

%post -n libalarm
/sbin/ldconfig

%postun -n libalarm
/sbin/ldconfig

%posttrans -n alarm-server
if [ -e /etc/config/model-config.xml ]; then
	grep "feature\/profile.*tv" /etc/config/model-config.xml > /dev/null
	if [ $? -eq 0 ]; then
		rm /usr/lib/udev/rules.d/99-rtc.rules
	fi
fi

%files -n alarm-server
%manifest alarm-server.manifest
%{_bindir}/alarm*
%{_unitdir}/alarm-server.socket
%{_unitdir}/sockets.target.wants/alarm-server.socket
%license LICENSE
%config %{_sysconfdir}/dbus-1/system.d/alarm-service.conf
%config %{_sysconfdir}/alarm-manager.conf
%{_tmpfilesdir}/alarm-manager-tmpfilses.conf
/usr/lib/udev/rules.d/99-rtc.rules
%{_moddir}/mod/libalarm-server.so
%{_moddir}/conf/alarm-server.service
%if 0%{?appfw_feature_alarm_manager_module_log}
%attr(0755,root,root) %{TZ_SYS_ETC}/dump.d/module.d/alarmmgr_log_dump.sh
%attr(0755,app_fw,app_fw) %{logdir}
%endif

%files -n libalarm
%manifest alarm-lib.manifest
%{_libdir}/libalarm.so.*
%license LICENSE

%files -n libalarm-devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files -n alarm-config-all-service-permitted
%{_datadir}/alarm-manager/alarm-config-all-service-permitted

%files -n alarm-config-platform-service-permitted
%{_datadir}/alarm-manager/alarm-config-platform-service-permitted

%files -n alarm-config-service-restricted
%{_datadir}/alarm-manager/alarm-config-service-restricted

#################################################
# plugin
#################################################
%files -n alarm-server-plugin
%manifest alarm-server-plugin.manifest
%{_libdir}/libalarm-server-plugin.so
%license LICENSE

#################################################
# unittests
#################################################
%files unittests
%{_bindir}/gtest*
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
