%global crate app_common
%global real_crate_name app_common

Name:       capi-appfw-app-common
Summary:    App common API
Version:    0.16.4
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-appfw-app-common.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(app-core-cpp)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  rust-mockall_double
BuildRequires:  rust-mockall
BuildRequires:  rust-libc
BuildRequires:  rust

Requires:  aul-rsc-mgr

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
An Application Common library in Tizen C API

%package -n rust-app-common
Summary:  app-common for rust
Group:    Rust/Libraries
Requires: %{name} = %{version}-%{release}

%description -n rust-app-common
An Application Common library in Tizen rust API

%package devel
Summary:  An Application Common library in Tizen C API (Development)
Group:    System/API
Requires: %{name} = %{version}-%{release}

%description devel
An Application Common library in Tizen C API (Development) package.

#################################################
# capi-appfw-app-common-unittests
#################################################
%package unittests
Summary:    GTest for app-common API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for app-common API

#################################################
# capi-appfw-app-common-gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    App common API(gcov)
Group:      Application Framework/Testing

%description gcov
App common gcov objects
%endif

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

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if 0%{?asan} != 1
        -DASAN_ENABLED=FALSE
%else
        -DASAN_ENABLED=TRUE
%endif
%__make %{?jobs:-j%jobs}

%{rustc_std_build} --crate-type=dylib \
        --crate-name=%{real_crate_name} \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        -L native="./src/" \
        %rust_dylib_extern libc \
        ./src/rust-app-common/src/lib.rs

%{rustc_std_build} --test --crate-type=bin \
        --extern mockall=%{_rust_dylibdir}/libmockall.so \
        --extern mockall_double=%{_rust_dylibdir}/libmockall_double.so \
        --crate-name=unittests_%{real_crate_name} \
        -L native="./src/" \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        %rust_dylib_extern libc \
        ./src/rust-app-common/src/lib.rs

%check
export LD_LIBRARY_PATH="../../src"
ctest --verbose %{?_smp_mflags}

RUST_BACKTRACE=1 RUST_TEST_THREADS=1 ./unittests_%{real_crate_name}

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o app-common.info
genhtml app-common.info -o app-common.out
zip -r app-common.zip app-common.out app-common.info
install -m 0644 app-common.zip %{buildroot}%{_datadir}/gcov/
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
GCOV_PATH="/tmp/home/abuild/rpmbuild/BUILD"
PACKAGE="%{name}-%{version}"

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
    /usr/bin/app-common_unittests
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

install -d -m 0755 %{buildroot}%{_rust_dylibdir}
install -m 0644 lib%{real_crate_name}.so %{buildroot}/%{_rust_dylibdir}/lib%{real_crate_name}.so
strip -s -N .rustc %{buildroot}/%{_rust_dylibdir}/lib%{real_crate_name}.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-app-common.so.*
%license LICENSE

%files devel
%manifest %{name}.manifest
%{_includedir}/appfw/app_common.h
%{_includedir}/appfw/app_common.hpp
%{_includedir}/appfw/app_common_internal.h
%{_includedir}/appfw/app_event_internal.hh
%{_includedir}/appfw/app_types.h
%{_includedir}/appfw/app_resource_manager.h
%{_includedir}/appfw/app_i18n.h
%{_libdir}/pkgconfig/capi-appfw-app-common.pc
%{_libdir}/libcapi-appfw-app-common.so

#################################################
# capi-appfw-app-common-unittests
#################################################
%files unittests
%{_bindir}/app-common_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# capi-appfw-app-common-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%files -n rust-app-common
%manifest %{name}.manifest
%{_rust_dylibdir}/lib%{real_crate_name}.so
