Name:       tizen-theme-manager
Summary:    Tizen Theme Manager
Version:    1.3.3
Release:    1
Group:      Application Framework/Package Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}.service
Source1003: %{name}.socket
BuildRequires:  cmake
BuildRequires:  hash-signer
BuildRequires:  tidl
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(pkgmgr-parser)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(tizen-database)
BuildRequires:  pkgconfig(vconf)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Tizen Theme Manager

%package -n capi-appfw-tizen-theme
Summary:  Tizen Theme Manager API
Requires: %{name} = %{version}

%description -n capi-appfw-tizen-theme
The Tizen Theme Manager API provides functions to load theme info or
set current theme.

%package -n capi-appfw-tizen-theme-devel
Summary:  Tizen Theme Manager API (Development package)
Requires: %{name} = %{version}

%description -n capi-appfw-tizen-theme-devel
The Tizen Theme Manager API provides functions to load theme info or
set current theme.

%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary

%define default_dark_theme_pkgid org.tizen.default-dark-theme
%package -n %{default_dark_theme_pkgid}
Summary:  Default dark theme
Requires: %{name} = %{version}

%description -n %{default_dark_theme_pkgid}
Default dark theme package

%define default_light_theme_pkgid org.tizen.default-light-theme
%package -n %{default_light_theme_pkgid}
Summary:  Default light theme
Requires: %{name} = %{version}

%description -n %{default_light_theme_pkgid}
Default light theme package

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
/bin/bash ./tidl/prebuild.sh

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
%if 0%{?asan:1}
export CXXFLAGS+=" -Wno-maybe-uninitialized"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_VERBOSE_MAKEFILE:BOOL=%{?verbose_make:ON}%{!?verbose_make:OFF} \
         -DUNITDIR=%{_unitdir} \
         -DFULLVER=%{version} \
         -DMAJORVER=${MAJORVER} \
         -DDEFAULT_DARK_THEME_PKGID=%{default_dark_theme_pkgid} \
         -DDEFAULT_LIGHT_THEME_PKGID=%{default_light_theme_pkgid} \
         %if 0%{?asan} != 1
          -DASAN_ENABLED=FALSE
         %else
          -DASAN_ENABLED=TRUE
         %endif

%__make %{?_smp_mflags}

%install
%make_install

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
PATH=/bin:/usr/bin:/sbin:/usr/sbin
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/tizen-theme-ut/tizen-theme-unit-test
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
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1002} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1003} %{buildroot}%{_unitdir}/%{name}.socket
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
ln -sf ../%{name}.socket %{buildroot}%{_unitdir}/sockets.target.wants/%{name}.socket

%check
export LD_LIBRARY_PATH=../../src/api:../../src/theme:../../src/theme_provider:../../src/theme_plugin
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
lcov -r %{name}.info "theme_manager_proxy.*" -o %{name}.info
lcov -r %{name}.info "theme_manager_stub.*" -o %{name}.info
lcov -r %{name}.info  "/unit_tests/*" -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post
/sbin/ldconfig
if [ $1 -eq 2 ]; then
  systemctl daemon-reload
fi
systemctl restart %{name}

%preun
if [ $1 -eq 0 ]; then
  systemctl stop %{name}
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  systemctl daemon-reload
fi

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/theme-cmd
%{_bindir}/theme-provider
%{_libdir}/libtizen-theme.so
%{_libdir}/libtizen-theme-provider.so
%{_sysconfdir}/package-manager/parserlib/metadata/libtizen-theme-plugin.so
%{_datarootdir}/parser-plugins/tizen-theme-plugin.info
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_unitdir}/sockets.target.wants/%{name}.socket

%files -n capi-appfw-tizen-theme
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-tizen-theme.so.*

%files -n capi-appfw-tizen-theme-devel
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-tizen-theme.so
%{_includedir}/tizen-theme/*.h
%{_libdir}/pkgconfig/capi-appfw-tizen-theme.pc

#################################################
# tizen-theme-manager-gcov
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
%defattr(-,root,root,-)
%{_datadir}/gcov/obj/*
%endif

%files unittests
%{_bindir}/tizen-theme-ut/tizen-theme-unit-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#Signing
%define tizen_sign_base %{_prefix}/apps/%{default_dark_theme_pkgid};%{_prefix}/apps/%{default_light_theme_pkgid}
%define tizen_sign 1
%define tizen_author_sign 1
%define tizen_dist_sign 1
%define tizen_sign_level platform

%files -n %{default_dark_theme_pkgid}
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_prefix}/apps/%{default_dark_theme_pkgid}/*
%{_datadir}/packages/%{default_dark_theme_pkgid}.xml

%files -n %{default_light_theme_pkgid}
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_prefix}/apps/%{default_light_theme_pkgid}/*
%{_datadir}/packages/%{default_light_theme_pkgid}.xml
