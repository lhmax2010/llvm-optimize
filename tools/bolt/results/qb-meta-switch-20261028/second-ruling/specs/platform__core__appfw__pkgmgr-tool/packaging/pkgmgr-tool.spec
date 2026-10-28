Name:       pkgmgr-tool
Summary:    Packager Manager Tool package
Version:    0.14.10
Release:    1
Group:      Application Framework/Package Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

Requires:  unzip
%if 0%{!?dev_wos:1}
Requires:  smack
%endif
Requires:  cryptsetup
Requires:  sqlite3

BuildRequires:  cmake
BuildRequires:  gettext-tools
BuildRequires:  sqlite3
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(iniparser)
%if 0%{!?dev_wos:1}
BuildRequires:  pkgconfig(libsmack)
%endif
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(xdgmime)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(aul-rsc-mgr)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  tizen-database-devel
BuildRequires:  pkgmgr-info-parser-devel
BuildRequires:  pkgmgr-info-parser
BuildRequires:  fdupes
%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif
Requires(posttrans):  /usr/bin/pkg_initdb

%description
Packager Manager Tool for packaging

%package unittests
Summary:    GTest for pkgmgr-tool
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for pkgmgr-tool

%if 0%{?gcov:1}
%package gcov
Summary:  pkgmgr-tool API(gcov)
Group:    System/API

%description gcov
gcov objects of an pkgmgr-tool
%endif

%package migration
Summary:    Migration tool for separated image
Group:      Application Framework/Package Management
# technically it's needed, but its other dependencies don't list it either and this avoids spec branching
# scripts installed by migration subpackage will never by executed without platform-extension anyway so there is no harm except used space
# Requires: platform-extension

%description migration
Summary:    Migration tool for separated image

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%cmake . \
  -DTIZEN_FEATURE_SMACK_DISABLE:BOOL=%{?dev_wos:ON}%{!?dev_wos:OFF} \
%if 0%{?asan} != 1
  -DASAN_ENABLED=FALSE
%else
  -DASAN_ENABLED=TRUE
%endif
%__make %{?_smp_mflags}

%check
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%install
%make_install
mkdir -p %{buildroot}%{_sysconfdir}/opt/upgrade

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
    mkdir -p /tmp/pkgmgr-tool-unittests
    cp -r /usr/share/pkgmgr-tool_unittests/* /tmp/pkgmgr-tool-unittests/
}

test_main() {
    echo "test_main start"
    CUR_DIR=$(pwd)
    cd /tmp/pkgmgr-tool-unittests
    /usr/bin/pkgmgr-tool_unittests
    cd $CUR_DIR
}

teardown() {
    echo "teardown start"
    rm -rf /tmp/pkgmgr-tool-unittests
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

%fdupes %{buildroot}

%post
/sbin/ldconfig
mkdir -p %{_sysconfdir}/skel/priv_shared_res
if command -v chsmack >/dev/null 2>&1; then
  chsmack -t -a User::Home %{_sysconfdir}/skel/priv_shared_res
fi

# Update mime database to support package mime types
update-mime-database %{_datadir}/mime

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_bindir}/pkgcmd
%{_bindir}/pkg_getsize
%{_bindir}/pkg_cleardata
%{_bindir}/pkginfo
%{_bindir}/rsc-slice
%{_bindir}/res-copy
%{_bindir}/pkg_upgrade
%attr(0755,root,root) %{_bindir}/install_preload_pkg
%{_datadir}/mime/packages/mime.wac.xml
%{_datadir}/mime/packages/mime.tpk.xml
%attr(0700,root,root) /etc/package-manager/pkgmgr-unzip-pkg.sh
%attr(0700,root,root) /etc/package-manager/pkgmgr-create-delta.sh
%attr(0700,root,root) /usr/share/upgrade/scripts/700.pkgmgr.patch.sh
%attr(0700,root,root) /etc/package-manager/updates/update.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30000.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30001.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30002.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30003.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30004.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30005.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30006.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30007.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30008.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30009.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30010.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30011.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30012.sh
%attr(0700,root,root) /etc/package-manager/updates/upgrade_to_30013.sh
%attr(0700,root,root) %{_sysconfdir}/package-manager/pkgmgr-label-initial-image.sh

%files unittests
%{_bindir}/pkgmgr-tool_unittests
%{_datadir}/pkgmgr-tool_unittests/*
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%defattr(-,root,root,-)
%{_datadir}/gcov/obj/*
%endif

%files migration
%attr(0755,-,-) %{_datadir}/platform-extension/710.package-manager-migration.sh
%attr(0755,-,-) %{_datadir}/platform-extension/900.package-manager-migration-recovery.sh
