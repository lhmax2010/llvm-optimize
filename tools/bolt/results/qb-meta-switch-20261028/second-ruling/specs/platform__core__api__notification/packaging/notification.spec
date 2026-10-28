%bcond_with wayland
Name:       notification
Summary:    Notification library
Version:    0.12.7
Release:    1
Group:      Applications/Core Applications
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:  %{name}.manifest
Source1002:  %{name}-ex.manifest

BuildRequires: tidl
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(capi-system-resource)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(security-manager)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(uuid)
BuildRequires: pkgconfig(rpc-port)
BuildRequires: pkgconfig(tizen-core)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

BuildRequires: cmake
Requires(post): /sbin/ldconfig
Requires(post): %{TZ_SYS_BIN}/sqlite3
Requires(postun): /sbin/ldconfig

%define upgrade_script_path /usr/share/upgrade/scripts

%description
Client/Server library for sending notifications.

%if 0%{?gcov:1}
%package gcov
Summary:  Notification API(gcov)
Group:    Applications/Core Applications

%description gcov
gcov objects of a notification library
%endif

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
/bin/bash ./src/tidl/prebuild.sh

%package devel
Summary:    Notification library (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files needed to build software that needs to system a system notification.

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DMAJORVER=${MAJORVER} -DFULLVER=%{version} \
    %if 0%{?asan} != 1
     -DASAN_ENABLED=FALSE
    %else
     -DASAN_ENABLED=TRUE
    %endif
%__make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH="../../src/notification:../../src/notification-ex"
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o notification.info
genhtml notification.info -o notification.out
zip -r notification.zip notification.out
install -m 0644 notification.zip %{buildroot}%{_datadir}/gcov/obj/notification.zip
%endif

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/<NAME>-unittests
}

teardown() {
    echo "teardown start"
}

main() {
    setup
    test_main
    teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/
sed -i -e 's/<NAME>/notification/g' %{buildroot}%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

if [ ! -d %{TZ_SYS_DB} ]
then
	mkdir %{TZ_SYS_DB}
fi

%postun -p /sbin/ldconfig

%files
%manifest notification.manifest
%defattr(-,root,root,-)
%{_libdir}/libnotification.so.*
%license LICENSE
%attr(755,root,root) %{_sysconfdir}/gumd/useradd.d/11_notification-add.post
%{_bindir}/notification_init
%attr(0755,root,root) %{upgrade_script_path}/505.notification_upgrade.sh
%attr(755,root,root) %{_bindir}/notification-test-app
%attr(0755,root,root) /etc/notification/upgrade.sh

%files devel
%defattr(-,root,root,-)
%{_includedir}/notification/notification.h
%{_includedir}/notification/notification_db.h
%{_includedir}/notification/notification_internal.h
%{_includedir}/notification/notification_error.h
%{_includedir}/notification/notification_type.h
%{_includedir}/notification/notification_list.h
%{_includedir}/notification/notification_ongoing.h
%{_includedir}/notification/notification_ongoing_flag.h
%{_includedir}/notification/notification_text_domain.h
%{_includedir}/notification/notification_status.h
%{_includedir}/notification/notification_status_internal.h
%{_includedir}/notification/notification_setting.h
%{_includedir}/notification/notification_setting_internal.h
%{_includedir}/notification/notification_ipc.h
%{_includedir}/notification/notification_noti.h
%{_includedir}/notification/notification_setting_service.h
%{_includedir}/notification/notification_viewer.h
%{_includedir}/notification/notification_shared_file.h
%{_includedir}/notification/notification_type_internal.h
%{_libdir}/pkgconfig/notification.pc
%{_libdir}/libnotification.so

#################################################
# notification-ex
#################################################
%package -n %{name}-ex
Summary: Library for developing the notification
Group: Applications/Application Utility
License: Apache-2.0

%description -n %{name}-ex
Provide APIs to develop the notification.

%package -n %{name}-ex-devel
Summary: Notification development library (dev)
Group: Development/Libraries
Requires: %{name}-ex

%description -n %{name}-ex-devel
Header & package configuration files to support development of the notification.

%post -n %{name}-ex
/sbin/ldconfig

%postun -n %{name}-ex -p /sbin/ldconfig

%files -n %{name}-ex
%manifest %{name}-ex.manifest
%attr(0644,root,root) %{_libdir}/libnotification-ex.so.*
%license LICENSE

%files -n %{name}-ex-devel
%{_includedir}/notification-ex/*
%{_libdir}/pkgconfig/notification-ex.pc
%attr(0644,root,root) %{_libdir}/libnotification-ex.so

#################################################
# notification-unittests
#################################################
%package -n notification-unittests
Summary:    GTest for notification
Group:      Development/Libraries

%description -n notification-unittests
GTest for notification

%files -n notification-unittests
%{_bindir}/notification-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
