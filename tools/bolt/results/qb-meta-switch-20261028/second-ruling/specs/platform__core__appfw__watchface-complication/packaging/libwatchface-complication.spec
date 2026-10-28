Name: libwatchface-complication
Summary: Library for developing the watchface complication
Version: 2.2.6
Release: 1
Group: Applications/Application Utility
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-provider.manifest
Source1003: libwatchface-editor.manifest
Source1004: libwatchface-common.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(db-util)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(appsvc)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(pkgmgr)
BuildRequires: pkgconfig(pkgmgr-installer)
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-gdbus)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(capi-base-utils-i18n)
%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif
Requires: %{name}-provider
Requires: libwatchface-common
Recommends: amd-mod-complication

%define upgrade_script_path /usr/share/upgrade/scripts

%description
API for creating a new watchface complication and managing it.

%package devel
Summary: Development Library for watch complication (dev)
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header and package configuration files for the watchface complication development

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
cp %{SOURCE1004} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . \
	-DTZ_SYS_SHARE=/usr/share \
	-DMAJORVER=${MAJORVER} \
	-DFULLVER=%{version}
%__make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{TZ_SYS_DB}
mkdir -p %{buildroot}%{_sysconfdir}/skel/.applications/dbspace

cat /dev/null > .complication_provider.db
cat /dev/null > .complication_provider.db-journal

install -m 0644 .complication_provider.db %{buildroot}%{TZ_SYS_DB}
install -m 0644 .complication_provider.db-journal %{buildroot}%{TZ_SYS_DB}
install -m 0644 .complication_provider.db %{buildroot}%{_sysconfdir}/skel/.applications/dbspace
install -m 0644 .complication_provider.db-journal %{buildroot}%{_sysconfdir}/skel/.applications/dbspace

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
    /usr/bin/watchface-complication_unittests
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
cp -f scripts/504.watchface_complication_upgrade.sh %{buildroot}%{upgrade_script_path}

%check
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o watchface-complication.info
genhtml watchface-complication.info -o watchface-complication.out
zip -r watchface-complication.zip watchface-complication.out
install -m 0644 watchface-complication.zip %{buildroot}%{_datadir}/gcov/obj/
%endif

#################################################
# libwatchface-complication
#################################################
%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files -n %{name}
%manifest %{name}.manifest
%attr(0644,root,root) %{_libdir}/%{name}.so.*
%license LICENSE
%attr(0755,root,root) %{_datadir}/upgrade/scripts/504.watchface_complication_upgrade.sh

%files -n %{name}-devel
%{_includedir}/watchface-complication/*.h
%{_includedir}/watchface-complication/*.hh
%{_includedir}/watchface-common/*.h
%{_includedir}/watchface-common/*.hh
%{_libdir}/pkgconfig/watchface-complication.pc
%attr(0644,root,root) %{_libdir}/%{name}.so

#################################################
# libwatchface-complication-provider
#################################################
%package -n %{name}-provider
Summary: Library for developing the watchface complication provider
Group: Applications/Application Utility
License: Apache-2.0

%description -n %{name}-provider
Provide APIs to develop the watchface complication provider.

%package -n %{name}-provider-devel
Summary: Watchface complication provider development library (dev)
Group: Development/Libraries
Requires: %{name}-provider

%description -n %{name}-provider-devel
Header & package configuration files to support development of the watchface complication provider.

%post -n %{name}-provider
/sbin/ldconfig
chsmack -a 'User::Home' %{TZ_SYS_DB}/.complication_provider.db
chsmack -a 'User::Home' %{TZ_SYS_DB}/.complication_provider.db-journal

%postun -n %{name}-provider -p /sbin/ldconfig

%files -n %{name}-provider
%manifest %{name}-provider.manifest
%attr(0644,root,root) %{_libdir}/%{name}-provider.so.*
%license LICENSE
%{_sysconfdir}/package-manager/parserlib/*
%{_sysconfdir}/skel/.applications/dbspace/.complication_provider.db
%{_sysconfdir}/skel/.applications/dbspace/.complication_provider.db-journal
%{TZ_SYS_DB}/.complication_provider.db
%{TZ_SYS_DB}/.complication_provider.db-journal
%{_datarootdir}/parser-plugins/complication_plugins.txt

%files -n %{name}-provider-devel
%{_includedir}/watchface-complication-provider/*.h
%{_libdir}/pkgconfig/watchface-complication-provider.pc
%attr(0644,root,root) %{_libdir}/%{name}-provider.so

#################################################
# libwatchface-editor
#################################################
%package -n libwatchface-editor
Summary: Library for developing the watchface editor
Group: Applications/Application Utility
License: Apache-2.0

%description -n libwatchface-editor
Provide APIs to develop the watchface editor.

%package -n libwatchface-editor-devel
Summary: Watchface editor development library (dev)
Group: Development/Libraries
Requires: libwatchface-editor

%description -n libwatchface-editor-devel
Header & package configuration files to support development of the watchface editor.

%post -n libwatchface-editor -p /sbin/ldconfig
%postun -n libwatchface-editor -p /sbin/ldconfig

%files -n libwatchface-editor
%manifest libwatchface-editor.manifest
%attr(0644,root,root) %{_libdir}/libwatchface-editor.so.*
%license LICENSE

%files -n libwatchface-editor-devel
%{_includedir}/watchface-editor/*.h
%{_libdir}/pkgconfig/watchface-editor.pc
%attr(0644,root,root) %{_libdir}/libwatchface-editor.so


#################################################
# libwatchface-common
#################################################
%package -n libwatchface-common
Summary: Library for developing the watchface common
Group: Applications/Application Utility
License: Apache-2.0

%description -n libwatchface-common
Provide utility to develop the watchface.

%package -n libwatchface-common-devel
Summary: Watchface common development library (dev)
Group: Development/Libraries
Requires: libwatchface-common

%description -n libwatchface-common-devel
Header & package configuration files to support development of the watchface library.

%post -n libwatchface-common -p /sbin/ldconfig
%postun -n libwatchface-common -p /sbin/ldconfig

%files -n libwatchface-common
%manifest libwatchface-common.manifest
%attr(0644,root,root) %{_libdir}/libwatchface-common.so.*
%license LICENSE

%files -n libwatchface-common-devel
%{_includedir}/watchface-common/*.h
%{_includedir}/watchface-common/*.hh
%{_libdir}/pkgconfig/watchface-common.pc
%attr(0644,root,root) %{_libdir}/libwatchface-common.so

#################################################
# libwatchface-complication-wrapper
#################################################
%package -n libwatchface-complication-wrapper
Summary: Library for developing the watchface
Group: Applications/Application Utility
License: Apache-2.0

%description -n libwatchface-complication-wrapper
Provide utility to develop the watchface.

%package -n libwatchface-complication-wrapper-devel
Summary: Watchface common development library (dev)
Group: Development/Libraries
Requires: libwatchface-complication-wrapper

%description -n libwatchface-complication-wrapper-devel
Header & package configuration files to support development of the watchface editor.

%post -n libwatchface-complication-wrapper -p /sbin/ldconfig
%postun -n libwatchface-complication-wrapper -p /sbin/ldconfig

%files -n libwatchface-complication-wrapper
%manifest libwatchface-common.manifest
%license LICENSE

%files -n libwatchface-complication-wrapper-devel
%{_includedir}/watchface-complication-wrapper/*.h
%{_libdir}/pkgconfig/watchface-complication-wrapper.pc


#################################################
# watchface-complication-unittests
#################################################
%package -n watchface-complication-unittests
Summary:    GTest for watchface-complication
Group:      Development/Libraries

%description -n watchface-complication-unittests
GTest for watchface-complication

%files -n watchface-complication-unittests
%{_bindir}/watchface-complication_unittests
/opt/share/watchface-complication/*
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh


#################################################
# watchface-complication-gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Simple string key-val dictionary ADT (gcov)
Group:      Application Framework/Testing

%description gcov
Simple string key-val dictionary ADT gcov objects
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

# End of a file
