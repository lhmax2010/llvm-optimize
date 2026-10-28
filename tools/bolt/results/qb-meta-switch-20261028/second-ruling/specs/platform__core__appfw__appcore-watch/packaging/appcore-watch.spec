Name:       appcore-watch
Summary:    Watch Application
Version:    1.7.26
Release:    1
Group:      Application Framework/Libraries
License:    Apache-2.0
Source0:    appcore-watch-%{version}.tar.gz
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(vconf-internal-keys)
BuildRequires:  pkgconfig(alarm-service)
BuildRequires:  pkgconfig(appcore-common)
BuildRequires:  pkgconfig(appcore-ui)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-widget-application)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(screen_connector_provider)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  cmake
Recommends: amd-mod-watch

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Watch application

%if 0%{?gcov:1}
%package gcov
Summary:  Watch application API(gcov)
Group:    Application Framework/Libraries

%description gcov
gcov objects of a watch application library
%endif

%package devel
Summary:    appcore watch
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description devel
appcore watch (developement files)

%package -n capi-appfw-watch-application-devel
Summary:    Watch appliation
Group:      Development/Libraries
Requires:    appcore-watch-devel = %{version}-%{release}
%description -n capi-appfw-watch-application-devel
watch application (developement files)

%package -n appcore-watch-base
Summary:    Watch base library
Group:      Development/Libraries
%description -n appcore-watch-base
Watch base library

%package -n appcore-watch-base-devel
Summary:    Watch base library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description -n appcore-watch-base-devel
Watch base library (development files)

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q


%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
export CFLAGS="$CFLAGS -Wall -Werror -Wno-unused-function -Wno-unused-but-set-variable"
export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	.

make %{?jobs:-j%jobs}

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
    /usr/bin/appcore-watch-unittest
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

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp capi-appfw-watch-application.pc %{buildroot}%{_libdir}/pkgconfig

%check
export LD_LIBRARY_PATH=../../src/base:../../src/efl_base
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o appcore-watch.info
genhtml appcore-watch.info -o appcore-watch.out
zip -r appcore-watch.zip appcore-watch.out
install -m 0644 appcore-watch.zip %{buildroot}%{_datadir}/gcov/obj/
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest appcore-watch.manifest
%defattr(-,root,root,-)
%{_libdir}/libappcore-watch.so.*
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/appcore-watch.pc
%{_libdir}/libappcore-watch.so
%{_includedir}/appcore-watch/appcore-watch.h

%files -n capi-appfw-watch-application-devel
%{_includedir}/appcore-watch/watch_app.h
%{_includedir}/appcore-watch/watch_app_extension.h
%{_includedir}/appcore-watch/watch_app_efl.h
%{_includedir}/appcore-watch/watch_app_internal.h
%{_libdir}/pkgconfig/capi-appfw-watch-application.pc
%{_libdir}/libappcore-watch.so

%files -n appcore-watch-base
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libappcore-watch-base.so.*
%license LICENSE

%files -n appcore-watch-base-devel
%{_includedir}/appcore-watch/watch_base.h
%{_libdir}/pkgconfig/appcore-watch-base.pc
%{_libdir}/libappcore-watch-base.so

%files unittests
%{_bindir}/appcore-watch-unittest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
