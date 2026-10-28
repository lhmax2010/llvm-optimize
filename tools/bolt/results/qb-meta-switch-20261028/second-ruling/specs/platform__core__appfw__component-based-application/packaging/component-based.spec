Name:       component-based
Summary:    Tizen Component-based application
Version:    1.6.9
Release:    1
Group:      Application Framework/Core
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-application.manifest
Source1003: %{name}-widget.manifest
Source1004: %{name}-efl-widget.manifest
Source1005: %{name}-port.manifest

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(ecore-wl2)
BuildRequires: pkgconfig(tizen-core-wl)
BuildRequires: pkgconfig(app-core-multi-window-cpp)
BuildRequires: pkgconfig(app-core-multi-window-tcore-cpp)
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(elementary)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(widget_service)
BuildRequires: pkgconfig(screen_connector_provider)
BuildRequires: pkgconfig(parcel)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-socket)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Tizen Component-based core base

%package tests
Summary:    Unit tests for Component-based core base
Requires:   %{name} = %{version}

%description tests
Unit tests for Component-based core base

%package devel
Summary:  Component-based library (Development)
Group:    Application Framework/Core
Requires: %{name} = %{version}-%{release}

%description devel
Component-based core base library (Development) package.

#################################################
# component-based-tcore
#################################################
%package -n %{name}-tcore
Summary: Library for developing the component-based
Group: Application Framework/Core
License: Apache-2.0

%description -n %{name}-tcore
Provider APIs to develop the component-based

%package -n %{name}-tcore-devel
Summary: Component-based development library (dev)
Group: Development/Libraries
Requires: %{name}-tcore = %{version}-%{release}

%description -n %{name}-tcore-devel
Header & package configuration files to support development of the component-based.

#################################################
# component-based-application
#################################################
%package -n %{name}-application
Summary: Library for developing the component-based application
Group: Application Framework/Core
License: Apache-2.0

%description -n %{name}-application
Provider APIs to develop the component-based application

%package -n %{name}-application-devel
Summary: Component-based application development library (dev)
Group: Development/Libraries
Requires: %{name}-application = %{version}-%{release}

%description -n %{name}-application-devel
Header & package configuration files to support development of the component-based application.

#################################################
# component-based-widget
#################################################
%package -n %{name}-widget
Summary: Library for developing the component-based widget component
Group: Application Framework/Core
License: Apache-2.0

%description -n %{name}-widget
Provider APIs to develop the component-based widget component

%package -n %{name}-widget-devel
Summary: Component-based widget component development library (dev)
Group: Development/Libraries
Requires: %{name}-widget = %{version}-%{release}

%description -n %{name}-widget-devel
Header & package configuration files to support development of the component-based widget

#################################################
# component-based-efl-widget
#################################################
%package -n %{name}-efl-widget
Summary: Library for developing the component-based efl widget component
Group: Application Framework/Core
License: Apache-2.0

%description -n %{name}-efl-widget
Provider APIs to develop the component-based efl widget component

%package -n %{name}-efl-widget-devel
Summary: Component-based efl widget component development library (dev)
Group: Development/Libraries
Requires: %{name}-efl-widget = %{version}-%{release}

%description -n %{name}-efl-widget-devel
Header & package configuration files to support development of the component-based efl widget component.

#################################################
# component-based-port
#################################################
%package -n %{name}-port
Summary: Library for developing the component-based port
Group: Application Framework/Core
License: Apache-2.0

%description -n %{name}-port
Component-based port library package.

%package -n %{name}-port-devel
Summary: Component-based port development library (dev)
Group: Development/Libraries
Requires: %{name}-port = %{version}-%{release}

%description -n %{name}-port-devel
Component-based port library package. (devel)

#################################################
# unittests
#################################################
%package unittests
Summary:    GTest for Component-based library
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for Component-based library

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Component-based library (gcov)
Group:      Application Framework/Testing

%description gcov
Component-based library gcov objects
%endif

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
cp %{SOURCE1004} .
cp %{SOURCE1005} .

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
    -DASAN_ENABLED=FALSE
%else
    -DASAN_ENABLED=TRUE
%endif
%__make %{?_smp_mflags}

%check
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:../../component_based/app_control" > /dev/null 2>&1
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:../../component_based/base" > /dev/null 2>&1
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:../../component_based/efl_base" > /dev/null 2>&1
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:../../component_based/efl_widget_base" > /dev/null 2>&1
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:../../component_based/port" > /dev/null 2>&1
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:../../component_based/uri" > /dev/null 2>&1
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:../../component_based/widget_base" > /dev/null 2>&1
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
    /usr/bin/component-based_unittests
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

%post -n %{name}-application -p /sbin/ldconfig
%postun -n %{name}-application -p/sbin/ldconfig

%post -n %{name}-widget -p /sbin/ldconfig
%postun -n %{name}-widget -p /sbin/ldconfig

%post -n %{name}-efl-widget -p /sbin/ldconfig
%postun -n %{name}-efl-widget -p /sbin/ldconfig

%post -n %{name}-port -p /sbin/ldconfig
%postun -n %{name}-port -p /sbin/ldconfig

%post unittests
%if 0%{?gcov:1}
%{_bindir}/component-based_unittests
%endif

%files -n %{name}
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libcomponent-based-core-base.so.*
%{_libdir}/libcomponent-based-app-control.so.*
%{_libdir}/libcomponent-based-uri.so.*

%files -n %{name}-devel
%{_includedir}/component_based/base/*.h
%{_includedir}/component_based/base/api/*.h
%{_includedir}/component_based/app_control/*.h
%{_includedir}/component_based/uri/*.h
%{_libdir}/libcomponent-based-core-base.so
%{_libdir}/libcomponent-based-app-control.so
%{_libdir}/libcomponent-based-uri.so
%{_libdir}/pkgconfig/component-based-core-base.pc
%{_libdir}/pkgconfig/component-based-app-control.pc
%{_libdir}/pkgconfig/component-based-uri.pc

#################################################
# component-based-tcore
#################################################
%files -n %{name}-tcore
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libcomponent-based-core-base-tcore.so.*
%{_libdir}/libcomponent-based-app-control.so.*
%{_libdir}/libcomponent-based-uri.so.*

%files -n %{name}-tcore-devel
%{_includedir}/component_based/base/*.h
%{_includedir}/component_based/base/api/*.h
%{_includedir}/component_based/app_control/*.h
%{_includedir}/component_based/uri/*.h
%{_libdir}/libcomponent-based-core-base-tcore.so
%{_libdir}/libcomponent-based-app-control.so
%{_libdir}/libcomponent-based-uri.so
%{_libdir}/pkgconfig/component-based-core-base-tcore.pc
%{_libdir}/pkgconfig/component-based-app-control.pc
%{_libdir}/pkgconfig/component-based-uri.pc

#################################################
# component-based-application
#################################################
%files -n %{name}-application
%license LICENSE
%manifest %{name}-application.manifest
%attr(0644,root,root) %{_libdir}/libcomponent-based-application.so.*

%files -n %{name}-application-devel
%{_includedir}/component_based/efl_base/*.h
%{_includedir}/component_based/efl_base/api/*.h
%{_libdir}/pkgconfig/component-based-application.pc
%{_libdir}/libcomponent-based-application.so

#################################################
# component-based-widget
#################################################
%files -n %{name}-widget
%license LICENSE
%manifest %{name}-widget.manifest
%attr(0644,root,root) %{_libdir}/libcomponent-based-core-widget-base.so.*

%files -n %{name}-widget-devel
%{_includedir}/component_based/widget_base/*.h
%{_includedir}/component_based/widget_base/api/*.h
%{_libdir}/pkgconfig/component-based-core-widget-base.pc
%{_libdir}/libcomponent-based-core-widget-base.so

#################################################
# component-based-efl-widget
#################################################
%files -n %{name}-efl-widget
%license LICENSE
%manifest %{name}-efl-widget.manifest
%attr(0644,root,root) %{_libdir}/libcomponent-based-efl-widget.so.*

%files -n %{name}-efl-widget-devel
%{_includedir}/component_based/efl_widget_base/*.h
%{_includedir}/component_based/efl_widget_base/api/*.h
%{_libdir}/pkgconfig/component-based-efl-widget.pc
%{_libdir}/libcomponent-based-efl-widget.so

#################################################
# component-based-port
#################################################
%files -n %{name}-port
%license LICENSE
%manifest %{name}-port.manifest
%attr(0644,root,root) %{_libdir}/libcomponent-based-port.so.*

%files -n %{name}-port-devel
%{_includedir}/component_based/port/*.hh
%{_includedir}/component_based/port/api/*.h
%{_libdir}/pkgconfig/component-based-port.pc
%{_libdir}/libcomponent-based-port.so

#################################################
# unittests
#################################################
%files unittests
%attr(0755,root,root) %{_bindir}/component-based_unittests
%attr(0755,root,root) %{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# component-based-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
