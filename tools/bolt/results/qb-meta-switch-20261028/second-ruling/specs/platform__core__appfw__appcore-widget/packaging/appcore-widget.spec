Name:       appcore-widget
Summary:    Widget Application
Version:    1.6.5
Release:    1
Group:      Application Framework/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(app-core-cpp)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(widget_service)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(app-core-multi-window-cpp)
BuildRequires:  pkgconfig(app-core-multi-window-tcore-cpp)
BuildRequires:  pkgconfig(appcore-multiwindow)
BuildRequires:  pkgconfig(screen_connector_provider)
BuildRequires:  pkgconfig(screen_connector_provider_tcore)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  cmake

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Widget base

%package -n appcore-widget-base
Summary:    Widget base
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
%description -n appcore-widget-base
Requires(postun): /sbin/ldconfig

%package -n appcore-widget-base-devel
Summary:    Widget base
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description -n appcore-widget-base-devel
widget application (development files)

%package -n appcore-widget-base-tcore
Summary:    Widget base
Group:      Development/Libraries
Requires(post): /sbin/ldconfig
%description -n appcore-widget-base-tcore
Requires(postun): /sbin/ldconfig

%package -n appcore-widget-base-tcore-devel
Summary:    Widget base
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description -n appcore-widget-base-tcore-devel
widget application (development files)

%package -n capi-appfw-widget-application-devel
Summary:    Widget application
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description -n capi-appfw-widget-application-devel
widget application (development files)

%package -n appcore-widget-unittests
Summary:    GTest for appcore-widget
Group:      Development/Libraries
%description -n appcore-widget-unittests
GTest for appcore-widget

%if 0%{?gcov:1}
%package gcov
Summary:  Widget application API(gcov)
Group:    Application Framework/Libraries

%description gcov
gcov objects of a widget application library
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

export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DBIN_INSTALL_DIR:PATH=%{_bindir} -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
%__make %{?jobs:-j%jobs}

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
    /usr/bin/appcore-widget-unittest
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

%check
export LD_LIBRARY_PATH=../../src/base:../../src/efl_base
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o appcore-widget.info
genhtml appcore-widget.info -o appcore-widget.out
zip -r appcore-widget.zip appcore-widget.out
install -m 0644 appcore-widget.zip %{buildroot}%{_datadir}/gcov/obj/
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n appcore-widget-base
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libappcore-widget-base.so.*
%license LICENSE

%files -n appcore-widget-base-devel
/usr/include/appfw/widget_base.hh
/usr/include/appfw/widget_base.h
%{_libdir}/pkgconfig/appcore-widget-base.pc
%{_libdir}/libappcore-widget-base.so

%files -n appcore-widget-base-tcore
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libappcore-widget-base-tcore.so.*
%license LICENSE

%files -n appcore-widget-base-tcore-devel
/usr/include/appfw/widget_base.hh
%{_libdir}/pkgconfig/appcore-widget-base-tcore.pc
%{_libdir}/libappcore-widget-base-tcore.so

%files -n appcore-widget
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libcapi-appfw-widget-application.so.*
%license LICENSE

%files -n capi-appfw-widget-application-devel
/usr/include/appfw/widget_app.h
/usr/include/appfw/widget_app.hpp
/usr/include/appfw/widget_app_efl.h
/usr/include/appfw/widget_app_internal.h
%{_libdir}/pkgconfig/capi-appfw-widget-application.pc
%{_libdir}/libcapi-appfw-widget-application.so

%files -n appcore-widget-unittests
%{_bindir}/appcore-widget-unittest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
