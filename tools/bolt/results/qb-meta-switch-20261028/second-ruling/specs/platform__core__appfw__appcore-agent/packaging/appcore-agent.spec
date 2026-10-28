%global crate appcore_agent
%global real_crate_name appcore_agent

Name:           appcore-agent
Version:        1.7.7
Release:        1
License:        Apache-2.0
Summary:        Service Application basic
Group:          Application Framework/Service
Source0:        %{name}-%{version}.tar.gz
Source1001:     appcore-agent.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(app-core-cpp)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-libopener)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(vconf-internal-keys)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(tizen-libopener)
BuildRequires:  rust-app-common
BuildRequires:  rust-app-control
BuildRequires:  rust-mockall_double
BuildRequires:  rust-mockall
BuildRequires:  rust-libc
BuildRequires:  rust

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Service Application basic

%package devel
Summary:        Application Core Agent
Group:          Application Framework/Development
Requires:       %{name} = %{version}-%{release}

%description devel
appcore agent (developement files)

%package -n capi-appfw-service-application-devel
Summary:    service appliation
Group:      Development/Libraries
Requires:    appcore-agent-devel = %{version}-%{release}

%description -n capi-appfw-service-application-devel
Service Application basic (developement files)

%package -n rust-appcore-agent
Summary:  appcore-agent for rust
Group:    Rust/Libraries
Requires: %{name} = %{version}-%{release}

%description -n rust-appcore-agent
Service Application basic for rust

%package -n capi-appfw-united-service
Summary: United Service Application
Group: App Framework/Application Core
Requires: capi-appfw-united-service = %{version}-%{release}

%description -n capi-appfw-united-service
United Service Application Library

%package -n capi-appfw-united-service-devel
Summary: United Service Application(devel)
Group: Development/Libraries
Requires: capi-appfw-united-service = %{version}-%{release}

%description -n capi-appfw-united-service-devel
United Service Application Library (developement files)

%if 0%{?gcov:1}
%package gcov
Summary:  Service application library(gcov)
Group:    System/API

%description gcov
gcov objects of a service application library
%endif

%package unittests
Summary:  %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1001} capi-appfw-united-service.manifest

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if 0%{?asan} != 1
	-DASAN_ENABLED=FALSE \
%else
	-DASAN_ENABLED=TRUE \
%endif
	.
%__make %{?_smp_mflags}

%{rustc_std_build} --crate-type=dylib \
        --crate-name=%{real_crate_name} \
        --extern app_common=%{_rust_dylibdir}/libapp_common.so \
        --extern app_control=%{_rust_dylibdir}/libapp_control.so \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        -L native="./src/appcore-agent/" \
        %rust_dylib_extern libc \
        ./src/rust-appcore-agent/src/lib.rs

%{rustc_std_build} --test --crate-type=bin \
        --extern mockall=%{_rust_dylibdir}/libmockall.so \
        --extern mockall_double=%{_rust_dylibdir}/libmockall_double.so \
        --crate-name=unittests_%{real_crate_name} \
        -L native="./src/appcore-agent/" \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        %rust_dylib_extern libc \
        ./src/rust-appcore-agent/src/lib.rs

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

## To run unittest
cat << EOF > run-unittest.sh
#!/bin/bash
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
    /usr/bin/appcore-agent-test
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

main "$@"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/

install -d -m 0755 %{buildroot}%{_rust_dylibdir}
install -m 0644 lib%{real_crate_name}.so %{buildroot}/%{_rust_dylibdir}/lib%{real_crate_name}.so
strip -s -N .rustc %{buildroot}/%{_rust_dylibdir}/lib%{real_crate_name}.so

%check
cd tests/unittests
LD_LIBRARY_PATH=../../src/appcore-agent ctest  -V

cd -
RUST_BACKTRACE=1 RUST_TEST_THREADS=1 ./unittests_%{real_crate_name}

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libappcore-agent.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/appcore-agent.pc
%{_libdir}/libappcore-agent.so

%files -n capi-appfw-service-application-devel
%{_includedir}/appcore-agent/service_app.h
%{_includedir}/appcore-agent/service_app.hpp
%{_includedir}/appcore-agent/service_app_extension.h
%{_includedir}/appcore-agent/service_app_internal.h
%{_libdir}/pkgconfig/capi-appfw-service-application.pc
%{_libdir}/libappcore-agent.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%{_bindir}/appcore-agent-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%files -n capi-appfw-united-service
%manifest capi-appfw-united-service.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libcapi-appfw-united-service.so.*

%files -n capi-appfw-united-service-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/capi-appfw-united-service.pc
%{_libdir}/libcapi-appfw-united-service.so
%{_includedir}/appfw/*.h

%files -n rust-appcore-agent
%manifest %{name}.manifest
%{_rust_dylibdir}/lib%{real_crate_name}.so
