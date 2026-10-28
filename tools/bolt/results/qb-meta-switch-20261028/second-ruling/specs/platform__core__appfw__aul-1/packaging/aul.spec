Name:       aul
Summary:    App utility library
Version:    0.85.10
Release:    1
Group:      Application Framework/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-server.manifest
Source1003: %{name}-exec-checker-plugin.manifest
Source1004: %{name}-rsc-mgr.manifest

Requires(post):   /sbin/ldconfig
Requires(post):   /usr/bin/systemctl
Requires(postun): /sbin/ldconfig
Requires(postun): /usr/bin/systemctl
Requires(preun):  /usr/bin/systemctl
Requires:   tizen-platform-config

BuildRequires:  cmake
BuildRequires:  libattr-devel
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(cynara-uid)
BuildRequires:  pkgconfig(libsmack)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(parcel)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  xdgmime-devel, pkgconfig(xdgmime)
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  pkgconfig(libunwind-ptrace)
Requires: libstorage

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

Recommends: amd
Recommends: amd-mod-component-manager
Recommends: amd-mod-watchdog

%description
Application utility library

%package devel
Summary:    App utility library (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Application utility library (devel)

%package exec-checker-plugin
Summary:    App binary executable cheker
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description exec-checker-plugin
Application utility library (exec checker)

%package test
Summary:    App utility test tools
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description test
Application utility library (test tools)

#################################################
# aul-gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    AUL (gcov)
Group:      Application Framework/Testing

%description gcov
AUL gcov objects
%endif

#################################################
# aul-server
#################################################
%package server
Summary:    Application Utility Library (Server)
Group:      Development/Libraries

%description server
Application Utility Library (Server)

%package server-devel
Summary:    Application Utility Library (Server)
Group:      Development/Libraries
Requires:   %{name}-server = %{version}-%{release}

%description server-devel
Application Utility Library (devel)

#################################################
# aul-rsc-mgr
#################################################
%package rsc-mgr
Summary:    Application Utility Library (Resource Manager)
Group:      Development/Libraries

%description rsc-mgr
Application Utility Library (Resource Manager)

%package rsc-mgr-devel
Summary:    Application Utility Library (Resource Manager)
Group:      Development/Libraries
Requires:   %{name}-rsc-mgr = %{version}-%{release}

%description rsc-mgr-devel
Application Utility Library (devel)

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%if "%{?_prelink_enable}" == "y"
%define tizen_feature_prelink 1
%else
%define tizen_feature_prelink 0
%endif

%define _aulresdir /opt/usr/home/owner/share/aul/res
%define appsvc_db_version 2
%define component_db_version 1

%prep
%setup -q
sed -i 's|TZ_SYS_DB|%{TZ_SYS_DB}|g' %{SOURCE1001}
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
cp %{SOURCE1004} .

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

%if 0%{?tizen_feature_prelink}
_TIZEN_FEATURE_PRELINK=ON
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-D_TIZEN_FEATURE_PRELINK:BOOL=${_TIZEN_FEATURE_PRELINK} \
	-DAUL_RES_DIR=%{_aulresdir} \
	-DAPPSVC_DB_VERSION=%{appsvc_db_version} \
	-DCOMPONENT_DB_VERSION=%{component_db_version} \
	-DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
%if 0%{?asan} != 1
	-DASAN_ENABLED=FALSE \
%else
	-DASAN_ENABLED=TRUE \
%endif
	.

%__make %{?_smp_mflags}

sqlite3 .appsvc.db < ./data/appsvc_db.sql
sqlite3 .component.db < ./src/parser/component/data/component_db.sql

%check
export LD_LIBRARY_PATH="../../src/aul:../../src/blink"
ctest -V

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{TZ_SYS_DB}
install -m 0644 .appsvc.db %{buildroot}%{TZ_SYS_DB}
install -m 0644 .appsvc.db-journal %{buildroot}%{TZ_SYS_DB}
install -m 0644 .component.db %{buildroot}%{TZ_SYS_DB}
install -m 0644 .component.db-journal %{buildroot}%{TZ_SYS_DB}

mkdir -p %{buildroot}%{_sysconfdir}/gumd/useradd.d
cp -f scripts/12_appsvc-add.post %{buildroot}%{_sysconfdir}/gumd/useradd.d/12_appsvc-add.post

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
    %{_aulresdir}/tpk/install.sh
}

test_main() {
    echo "test_main start"
    /usr/bin/aul-unit-tests
    /usr/bin/app-control-tests
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

%preun

%post
/sbin/ldconfig

chmod 666 %{TZ_SYS_DB}/.appsvc.db
chmod 666 %{TZ_SYS_DB}/.appsvc.db-journal
chsmack -a 'User::Home' %{TZ_SYS_DB}/.appsvc.db
chsmack -a 'User::Home' %{TZ_SYS_DB}/.appsvc.db-journal
chmod 666 %{TZ_SYS_DB}/.component.db
chmod 666 %{TZ_SYS_DB}/.component.db-journal
chsmack -a 'User::Home' %{TZ_SYS_DB}/.component.db
chsmack -a 'User::Home' %{TZ_SYS_DB}/.component.db-journal

%postun
/sbin/ldconfig

%post test
%if 0%{?gcov:1}
%{_bindir}/aul-unit-tests
%endif

%postun server
/sbin/ldconfig

%post server
/sbin/ldconfig

%postun rsc-mgr
/sbin/ldconfig

%post rsc-mgr
/sbin/ldconfig

%files
%license LICENSE
%manifest %{name}.manifest
%attr(0644,root,root) %{_libdir}/libaul.so.*
%attr(0644,root,root) %{_libdir}/libaul-blink.so.*
%config %{_sysconfdir}/dbus-1/system.d/aul.conf
%{_bindir}/aulctl
%{_bindir}/aul_test
%{_bindir}/app_launcher
%{_bindir}/appgroup_info
%{_bindir}/app_com_tool
%{_bindir}/launch_app
%{_bindir}/appid2pid
%{_bindir}/launch_debug
%{_bindir}/compmgr_tool
%{_bindir}/appsvc-db-recovery
%{_bindir}/component-db-recovery
%{_bindir}/aul_window
%{_datadir}/aul/miregex/*
%{_datadir}/aul/preexec_list.txt
%{_datadir}/parser-plugins/component.info
%{_datadir}/parser-plugins/alias-appid.info
%{_datadir}/parser-plugins/allowed-appid.info
%{_datadir}/parser-plugins/boot-sequencer.info
%{TZ_SYS_DB}/.appsvc.db*
%{TZ_SYS_DB}/.component.db*
%{_sysconfdir}/package-manager/parserlib/metadata/*.so
%{_sysconfdir}/package-manager/parserlib/libcomponent-based-application.so
%{_sysconfdir}/package-manager/parserlib/libboot-sequencer.so

%attr(0755,root,root) %{_sysconfdir}/gumd/useradd.d/*
%attr(0755,root,root) %{_datadir}/upgrade/scripts/501.component_upgrade.sh
%attr(0755,root,root) %{_datadir}/upgrade/scripts/501.appsvc_db_upgrade.sh
%attr(0755,root,root) %{_sysconfdir}/aul/upgrade/scripts/*
%attr(0755,root,root) %{_sysconfdir}/aul/component/upgrade/scripts/*

%files exec-checker-plugin
%manifest %{name}-exec-checker-plugin.manifest
%{_datadir}/parser-plugins/exec-checker.info
%{_sysconfdir}/package-manager/parserlib/libexec-checker.so*

%files test
%{_bindir}/open_app

%files devel
%{_includedir}/aul/*.h
%{_includedir}/aul/api/*.h
%{_includedir}/aul/blink/*.h
%{_libdir}/libaul.so
%{_libdir}/libaul-blink.so
%{_libdir}/pkgconfig/aul.pc
%{_libdir}/pkgconfig/aul-blink.pc

#################################################
# aul-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%files server
%manifest %{name}-server.manifest
%attr(0644,root,root) %{_libdir}/libaul-server.so.*

%files server-devel
%{_includedir}/aul/server/*.h
%{_libdir}/libaul-server.so
%{_libdir}/pkgconfig/aul-server.pc

%files rsc-mgr
%manifest %{name}-rsc-mgr.manifest
%attr(0644,root,root) %{_libdir}/libaul-rsc-mgr.so.*
%{_datadir}/aul/res.xsd

%files rsc-mgr-devel
%{_includedir}/aul/rsc-mgr/*.h
%{_libdir}/libaul-rsc-mgr.so
%{_libdir}/pkgconfig/aul-rsc-mgr.pc

%files unittests
%attr(0755,root,root) %{_bindir}/aul-unit-tests
%attr(0755,root,root) %{_bindir}/app-control-tests
%attr(0755,root,root) %{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%attr(0755,root,root) %{_aulresdir}/*
