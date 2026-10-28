Name: libwidget_service
Summary: Service API for gathering installed widget information
Version: 1.3.12
Release: 1
Group: Applications/Core Applications
License: Flora-1.1 and Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires: cmake, gettext-tools, coreutils
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(db-util)
BuildRequires: pkgconfig(pkgmgr)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(uuid)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-self)
BuildRequires: pkgconfig(pkgmgr-installer)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(tizen-database)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%if "%{model_build_feature_widget}" == "0"
ExclusiveArch:
%endif

%define upgrade_script_path /usr/share/upgrade/scripts

%description
Service API for gathering information of installed widgetes

%package devel
Summary: Files for widget service
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Gathering the installed widget information.

%package -n widget-service-parser-devel
Summary:    Widget element parser library
Group:      Application Framework/Service

%description -n widget-service-parser-devel
This module is for making a widget parser plugin

#################################################
# libwidget_service_gcov
#################################################
%if 0%{?gcov:1}
%package -n libwidget_service-gcov
Summary:  Widget Service API(gcov)
Group:    Applications/Core Applications

%description -n libwidget_service-gcov
gcov objects of a widget service library
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif
%if 0%{?asan:1}
export CXXFLAGS="$CXXFLAGS -Wno-maybe-uninitialized"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER}
%__make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH="../parser/lib:../src"
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o widget_service.info
genhtml widget_service.info -o widget_service.out
zip -r widget_service.zip widget_service.out widget_service.info
install -m 0644 widget_service.zip %{buildroot}%{_datadir}/gcov/obj/
%endif

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{TZ_SYS_DB}
mkdir -p %{buildroot}%{_sysconfdir}/skel/.applications/dbspace

cat /dev/null > .widget.db
cat /dev/null > .widget.db-journal

install -m 0666 .widget.db %{buildroot}%{TZ_SYS_DB}
install -m 0666 .widget.db-journal %{buildroot}%{TZ_SYS_DB}
install -m 0666 .widget.db %{buildroot}%{_sysconfdir}/skel/.applications/dbspace
install -m 0666 .widget.db-journal %{buildroot}%{_sysconfdir}/skel/.applications/dbspace

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
    /usr/bin/widget_service_unittests
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

mkdir -p %{buildroot}%{upgrade_script_path}
cp -f scripts/505.widget_service_upgrade.sh %{buildroot}%{upgrade_script_path}

%post -n %{name}
/sbin/ldconfig
%{_bindir}/widget_recovery init

%postun -n %{name}
/sbin/ldconfig

%posttrans
if [ -e %{_sysconfdir}/config/model-config.xml ]; then
	PROFILE=`grep "feature\/profile" %{_sysconfdir}/config/model-config.xml`
	case "${PROFILE}" in
	*mobile*)
		rm %{_datarootdir}/widget_service/wearable.resolution.ini
		mv -f %{_datarootdir}/widget_service/mobile.resolution.ini %{_datarootdir}/widget_service/resolution.ini
		;;
	*wearable*)
		rm %{_datarootdir}/widget_service/mobile.resolution.ini
		mv -f %{_datarootdir}/widget_service/wearable.resolution.ini %{_datarootdir}/widget_service/resolution.ini
		;;
	*)
		rm %{_datarootdir}/widget_service/mobile.resolution.ini
		rm %{_datarootdir}/widget_service/wearable.resolution.ini
		;;
	esac
else
	rm %{_datarootdir}/widget_service/mobile.resolution.ini
	rm %{_datarootdir}/widget_service/wearable.resolution.ini
fi

#################################################
# libwidget_service-unittests
#################################################
%package -n libwidget_service-unittests
Summary:    GTest for widget_service
Group:      Development/Libraries

%description -n libwidget_service-unittests
GTest for widget_service

%files -n libwidget_service-unittests
%{_bindir}/widget_service_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# libwidget_service-test
#################################################
%package -n libwidget_service-test
Summary:    Command-line test tool for widget_service
Group:      Development/Libraries

%description -n libwidget_service-test
Command-line test tool for widget_service

%files -n %{name}
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.Flora-1.1
%{_libdir}/libwidget_service.so.*
%{_libdir}/libwidget_parser.so.*
%{_sysconfdir}/package-manager/parserlib/libwidget-application.so
%{_sysconfdir}/skel/.applications/dbspace/.widget.db
%{_sysconfdir}/skel/.applications/dbspace/.widget.db-journal
%{TZ_SYS_DB}/.widget.db
%{TZ_SYS_DB}/.widget.db-journal
%{_bindir}/widget_recovery
%{_datarootdir}/widget_service/*
%{_datarootdir}/parser-plugins/widget.info
%attr(0755,root,root) %{upgrade_script_path}/505.widget_service_upgrade.sh

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/widget_service/*
%{_libdir}/pkgconfig/widget_service.pc
%{_libdir}/libwidget_service.so

%if 0%{?gcov:1}
%files -n libwidget_service-gcov
%{_datadir}/gcov/obj/*
%endif

%files -n widget-service-parser-devel
%defattr(-,root,root,-)
%license LICENSE.Apache-2.0
%{_includedir}/widget_parser/*
%{_libdir}/pkgconfig/widget-service-parser.pc
%{_libdir}/libwidget_parser.so

%files -n libwidget_service-test
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/widget_test
