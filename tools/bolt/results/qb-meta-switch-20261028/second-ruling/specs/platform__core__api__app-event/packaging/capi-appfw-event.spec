%global crate rust_app_event
%global real_crate_name rust_app_event

Name:       capi-appfw-event
Summary:    App event API
Version:    0.6.22
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-appfw-event.manifest

Requires: tizen-dlog

BuildRequires:  cmake
BuildRequires:  pkgconfig(tizen-dlog)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(parcel)
BuildRequires:  pkgconfig(eventsystem)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  rust-mockall_double
BuildRequires:  rust-mockall
BuildRequires:  rust-tizen-bundle
BuildRequires:  rust-libc
BuildRequires:  rust

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
An Application event library in Tizen C API

%package devel
Summary:  An Application event library in Tizen C API (Development)
Group:    System/API
Requires: %{name} = %{version}

%description devel
An Application event library in Tizen C API (Development) package.

%package -n rust-app-event
Summary:  app-event for rust
Group:    Rust/Libraries
Requires: %{name} = %{version}-%{release}

%description -n rust-app-event
App Event for rust

%if 0%{?gcov:1}
%package gcov
Summary:  App event API(gcov)
Group:    System/API

%description gcov
gcov objects of an application event library
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
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
    %if 0%{?asan} != 1
      -DASAN_ENABLED=FALSE
    %else
      -DASAN_ENABLED=TRUE
    %endif
%__make %{?jobs:-j%jobs}

%{rustc_std_build} --crate-type=dylib \
        --crate-name=%{real_crate_name} \
        -L native="./src/app-event/" \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        %rust_dylib_extern tizen_base \
        %rust_dylib_extern libc \
        ./src/rust-app-event/src/lib.rs

%{rustc_std_build} --test --crate-type=bin \
        --extern mockall=%{_rust_dylibdir}/libmockall.so \
        --extern mockall_double=%{_rust_dylibdir}/libmockall_double.so \
        --crate-name=unittests_%{real_crate_name} \
        -L native="./src/app-event/" \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        %rust_dylib_extern tizen_base \
        ./src/rust-app-event/src/lib.rs

%check
export LD_LIBRARY_PATH="../../src/app-event"
ctest -V %{?_smp_mflags}

export LD_LIBRARY_PATH="./src/app-event/:%{_rust_dylibdir}"
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
    /usr/bin/app_event_unittests
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

################################################
# app_event_unittests
################################################
%package unittests
Summary:    GTest for app_event
Group:      Development/Libraries

%description unittests
GTest for app_event

%files unittests
%{_bindir}/app_event_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%files
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-event.so.*
%license LICENSE

%files devel
%manifest %{name}.manifest
%{_includedir}/appfw/app_event.h
%{_libdir}/pkgconfig/capi-appfw-event.pc
%{_libdir}/libcapi-appfw-event.so

%files -n rust-app-event
%manifest %{name}.manifest
%{_rust_dylibdir}/lib%{real_crate_name}.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
