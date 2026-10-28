Name:       capi-appfw-application
Summary:    An Application library in SLP C API
Version:    0.11.0
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-appfw-application.manifest
Source1002:     appcore-ui-app-ambient.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(alarm-service)
BuildRequires:  pkgconfig(app-core-cpp)
BuildRequires:  pkgconfig(app-core-efl-cpp)
BuildRequires:  pkgconfig(app-core-tcore-cpp)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(vconf-internal-keys)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
An Application library in SLP C API package.

%package devel
Summary:  An Application library in SLP C API (Development)
Group:    System/API
Requires: %{name} = %{version}

%description devel
An Application library in SLP C API (Development) package.

%package unittests
Summary:    GTest for application API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for application API

%if 0%{?gcov:1}
%package gcov
Summary:  An application library(gcov)
Group:    System/API

%description gcov
gcov objects of an application library
%endif

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
         -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
         -DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}
%__make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH="../../appcore_ui_app_ambient:../../src"
ctest --verbose %{?_smp_mflags}
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o appcore_ui_app_ambient.info
genhtml appcore_ui_app_ambient.info -o appcore_ui_app_ambient.out
zip -r appcore_ui_app_ambient.zip appcore_ui_app_ambient.out
install -m 0644 appcore_ui_app_ambient.zip %{buildroot}%{_datadir}/gcov/
%endif

%install
rm -rf %{buildroot}
%make_install
# event-loop backends are dlopen()ed by libcapi-appfw-application only
rm -f %{buildroot}%{_libdir}/libcapi-appfw-application-efl.so
rm -f %{buildroot}%{_libdir}/libcapi-appfw-application-tcore.so

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
GCOV_PATH="/tmp/home/abuild/rpmbuild/BUILD"
PAKCAGE="%{name}-%{version}"

set_perm() {
    ## Sets the permission for applications
    /usr/bin/find /tmp/home/ -print | /usr/bin/xargs -n1 /usr/bin/chsmack -a "System::Run" &> /dev/null
    /usr/bin/find /tmp/home/ -print | /usr/bin/xargs -n1 /usr/bin/chsmack -a "System::Run" -t &> /dev/null
    /usr/bin/chmod -R 777 /tmp/home/
}

setup() {
    echo "setup start"
    /usr/bin/mkdir -p "${GCOV_PATH}/${PACKAGE}"
    set_perm
}

test_main() {
    echo "test_main start"
    export "GCOV_PREFIX=/tmp"
    /usr/bin/application_unittests
    /usr/bin/ui-app-ambient_unittests
}

teardown() {
    echo "teardown start"
    set_perm
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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

################################################
# libappcore-ui-app-ambient
%package -n appcore-ui-app-ambient
Summary: APIs to set lifecycle ui application ambient
Version: 0.0.1
License: Apache-2.0
Group: Applications/Core Applications

%description -n appcore-ui-app-ambient
A set of APIs to set lifecycle ui application ambient

%package -n appcore-ui-app-ambient-devel
Summary: APIs to set lifecycle ui application ambient
Group: Development/Libraries

%description -n appcore-ui-app-ambient-devel
Header & package configuration of appcore-ui-app-ambient

%post -n appcore-ui-app-ambient -p /sbin/ldconfig
%postun -n appcore-ui-app-ambient -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-application.so.*
%{_libdir}/libcapi-appfw-application-efl.so.*
%{_libdir}/libcapi-appfw-application-tcore.so.*
%license LICENSE

%files devel
%manifest %{name}.manifest
%{_includedir}/appfw/app.h
%{_includedir}/appfw/app.hpp
%{_includedir}/appfw/app_internal.h
%{_includedir}/appfw/app_extension.h
%{_libdir}/pkgconfig/capi-appfw-application.pc
%{_libdir}/libcapi-appfw-application.so

%files -n appcore-ui-app-ambient
%manifest appcore-ui-app-ambient.manifest
%license LICENSE
%{_libdir}/libappcore-ui-app-ambient.so.*

%files unittests
%{_bindir}/application_unittests
%{_bindir}/ui-app-ambient_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%files -n appcore-ui-app-ambient-devel
%{_includedir}/appcore-ui-app-ambient/*.h
%{_libdir}/pkgconfig/appcore-ui-app-ambient.pc
%{_libdir}/libappcore-ui-app-ambient.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
