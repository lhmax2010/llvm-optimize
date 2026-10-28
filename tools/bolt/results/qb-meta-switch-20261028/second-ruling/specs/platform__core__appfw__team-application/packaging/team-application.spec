Name:       team-application
Summary:    Tizen team application
Version:    1.4.1
Release:    1
Group:      Application Framework/Core
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

# The headless runtime deliberately carries the SONAME of libteam-application
# so member .so files load into it unchanged; keep rpm from advertising it as a
# second provider of libteam-application.so.1.
%global __provides_exclude_from ^%{_libdir}/team-application/headless/.*$

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: hash-signer
BuildRequires: zip
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(app-core-multi-context-cpp)
# Header only (plugin hints); the ecore library is never linked.
BuildRequires: pkgconfig(app-core-multi-window-cpp)
BuildRequires: pkgconfig(app-core-multi-window-tcore-cpp)
BuildRequires: pkgconfig(tizen-core)
BuildRequires: pkgconfig(tizen-core-wl)
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(widget_service)
BuildRequires: pkgconfig(screen_connector_provider)
BuildRequires: pkgconfig(parcel)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-socket)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(dali2-core)
BuildRequires: pkgconfig(dali2-adaptor)
BuildRequires: pkgconfig(dali2-ui-foundation)
BuildRequires: pkgconfig(dali2-adaptor-integration)

%if 0%{?asan} == 1
BuildRequires: asan-force-options
BuildRequires: asan-build-env
BuildRequires: libasan
%endif

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Tizen Team Application Core

%package tests
Summary:    Unit tests for team application core base
Requires:   %{name} = %{version}

%description tests
Unit tests for team application core base

%package devel
Summary:  Team Application library (Development)
Group:    Application Framework/Core
Requires: %{name} = %{version}-%{release}

%description devel
Team Application core base library (Development) package.

#################################################
# unittests
#################################################
%package unittests
Summary:    GTest for Team-Application library
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for Team-Application library

%package smoketests
Summary:    Device smoke tests for Team-Application library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description smoketests
Standalone device smoke tests for the Team-Application public API.

%if 0%{?scenariotests:1}
%package scenariotests
Summary:    On-device scenario test harness for Team-Application
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description scenariotests
Shell-based on-device scenario tests (install/launch/lifecycle) for
team-application. Run with: sdb shell /root/team-application-test/test.sh
%endif


#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Team-Application library (gcov)
Group:      Application Framework/Testing

%description gcov
Team-Application library gcov objects
%endif

%prep
%setup -q
cp packaging/*.manifest .

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
export CXXFLAGS="$CXXFLAGS -DEFL_BETA_API_SUPPORT "

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
%if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE \
%else
    -DASAN_ENABLED=TRUE \
%endif
%if 0%{?scenariotests:1}
    -DBUILD_SCENARIO_TESTS=TRUE
%else
    -DBUILD_SCENARIO_TESTS=FALSE
%endif
%__make %{?_smp_mflags}

%check
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o %{name}.out --legend --show-details
zip -r %{name}.zip %{name}.out
install -m 0644 %{name}.zip %{buildroot}%{_datadir}/gcov/
%endif

%install
rm -rf %{buildroot}
%make_install
# hash-signer's rpm macro signs the leader. Sign each independently registered
# member package as well, using the same platform certificate.
for pkg in org.tizen.team.smoke.service org.tizen.team.smoke.ui org.tizen.team.smoke.view; do
  /usr/bin/hash-signer.sh -a -d -p platform -b %{buildroot} %{_prefix}/apps/$pkg
done

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
    /usr/bin/team-application-headed-unittest
    /usr/bin/team-application-headless-unittest
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post unittests
%if 0%{?gcov:1}
%{_bindir}/team-application-headed-unittest
%endif

#################################################
# team-application
#################################################
%files -n %{name}
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%dir %{_libdir}/team-application
%dir %{_libdir}/team-application/headed
%{_libdir}/team-application/headed/libteam-application-headed.so.*
%{_libdir}/team-application/headed/libteam-application.so.1
%dir %{_libdir}/team-application/headless
%{_libdir}/team-application/headless/libteam-application-headless.so.*
%{_libdir}/team-application/headless/libteam-application.so.1
%{_bindir}/team-launcher

%files -n %{name}-devel
%{_includedir}/team_app/
%{_libdir}/team-application/headed/libteam-application-headed.so
%{_libdir}/team-application/headless/libteam-application-headless.so
%{_libdir}/libteam-application.so
%{_libdir}/pkgconfig/%{name}.pc

#################################################
# unittests
#################################################
%files unittests
%attr(0755,root,root) %{_bindir}/team-application-headed-unittest
%attr(0755,root,root) %{_bindir}/team-application-headless-unittest
%attr(0755,root,root) %{_bindir}/tizen-unittests/%{name}/run-unittest.sh

# Sign fixture TPK roots so tpk-backend can verify member packages against the leader.
%define tizen_sign_base %{_prefix}/apps/org.tizen.team.smoke
%define tizen_sign 1
%define tizen_author_sign 1
%define tizen_dist_sign 1
%define tizen_sign_level platform

%files smoketests
%attr(0755,root,root) %{_bindir}/team-application-smoke
%attr(0755,root,root) /usr/apps/org.tizen.team.smoke*
%{_datadir}/packages/org.tizen.team.smoke*.xml

#################################################
# scenariotests
#################################################
%if 0%{?scenariotests:1}
%files scenariotests
%defattr(-,root,root,-)
%dir /root/team-application-test
%attr(0755,root,root) /root/team-application-test/test.sh
/root/team-application-test/common/
/root/team-application-test/list/
%dir /root/team-application-test/artifact
/root/team-application-test/artifact/readonly/
%endif

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
