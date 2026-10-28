%global crate app_control
%global real_crate_name app_control

Name:       capi-appfw-app-control
Summary:    App control API
Version:    0.26.4
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-appfw-app-control.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(app-core-cpp)
BuildRequires:  pkgconfig(gmock)
%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif
BuildRequires:  rust-mockall_double
BuildRequires:  rust-mockall
BuildRequires:  rust-libc
BuildRequires:  rust

Recommends:   amd-mod-share

%description
An Application Control library in Tizen C API

%package devel
Summary:  An Application Control library in Tizen C API (Development)
Group:    System/API
Requires: %{name} = %{version}-%{release}

%description devel
An Application Control library in Tizen C API (Development) package.

%package -n rust-app-control
Summary:  app-control for rust
Group:    Rust/Libraries
Requires: %{name} = %{version}-%{release}

%description -n rust-app-control
An Application Control library in Tizen rust API

#################################################
# unittests
#################################################
%package unittests
Summary:    GTest for uri
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for app_control

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    app_control(gcov)
Group:      Application Framework/Testing

%description gcov
app_control gcov objects
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

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if 0%{?asan} != 1
        -DASAN_ENABLED=FALSE
%else
        -DASAN_ENABLED=TRUE
%endif
%__make %{?_smp_mflags}

%{rustc_std_build} --crate-type=dylib \
        --crate-name=%{real_crate_name} \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        -L native="./src/app-control/" \
        -L native="./src/uri/" \
        %rust_dylib_extern libc \
        ./src/rust-app-control/src/lib.rs

%{rustc_std_build} --test --crate-type=bin \
        --extern mockall=%{_rust_dylibdir}/libmockall.so \
        --extern mockall_double=%{_rust_dylibdir}/libmockall_double.so \
        --crate-name=unittests_%{real_crate_name} \
        -L native="./src/app-control/" \
        -L native="./src/uri/" \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        %rust_dylib_extern libc \
        ./src/rust-app-control/src/lib.rs

%check
export LD_LIBRARY_PATH="../../src/app-control:../../src/uri"
ctest --verbose %{?_smp_mflags}

export LD_LIBRARY_PATH="./src/app-control/:./src/uri/:%{_rust_dylibdir}"
RUST_BACKTRACE=1 RUST_TEST_THREADS=1 ./unittests_%{real_crate_name}

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
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
PAKCAGE="%{name}-%{version}"

set_perm() {
    ## Sets the permission for applications
    /usr/bin/find /tmp/home/ -print | /usr/bin/xargs -n1 /usr/bin/chsmack -a "System::Run" > /dev/null 2>&1
    /usr/bin/find /tmp/home/ -print | /usr/bin/xargs -n1 /usr/bin/chsmack -a "System::Run" -t > /dev/null 2>&1
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
    /usr/bin/app-control-unit-test
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
%{_libdir}/libcapi-appfw-app-control.so.*
%{_libdir}/libcapi-appfw-app-control-uri.so.*
%license LICENSE

%files devel
%manifest %{name}.manifest
%{_includedir}/appfw/app_control.h
%{_includedir}/appfw/app_control.hpp
%{_includedir}/appfw/app_control_internal.h
%{_includedir}/appfw/app_control_uri.h
%{_libdir}/pkgconfig/capi-appfw-app-control.pc
%{_libdir}/libcapi-appfw-app-control.so
%{_libdir}/libcapi-appfw-app-control-uri.so

#################################################
# unittests
#################################################
%files unittests
%{_bindir}/app-control-unit-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files -n rust-app-control
%manifest %{name}.manifest
%{_rust_dylibdir}/lib%{real_crate_name}.so
