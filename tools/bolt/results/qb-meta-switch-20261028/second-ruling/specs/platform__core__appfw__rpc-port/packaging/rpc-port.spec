%global crate rust_rpc_port
%global real_crate_name rust_rpc_port

Name:       rpc-port
Summary:    RPC Port library
Version: 	1.21.19
Release:    0
Group:		Application Framework/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    esd-honmun.socket
Source1001: %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(parcel)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(tizen-shared-queue)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(tizen-libopener)
BuildRequires:  pkgconfig(dns_sd)
BuildRequires:  rust-tizen-bundle
BuildRequires:  rust-mockall_double
BuildRequires:  rust-mockall
BuildRequires:  rust

%define _moddir %{_datadir}/esd

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

Requires(post): /sbin/ldconfig
Requires(post): coreutils
Requires(postun): /sbin/ldconfig

Recommends: amd-mod-rpc-port

%description
RPC Port library package.

%package devel
Summary:  RPC Port library (Development)
Group:    Application Framework/Development
Requires: %{name} = %{version}-%{release}

%description devel
RPC Port library (Development) package.

#################################################
# esd-mod-honmun
#################################################
%package -n esd-mod-honmun
Summary:    ESD plugin for rpc-port tcp connection
Group:      Development/Libraries
Requires:   %{name}

%description -n esd-mod-honmun
ESD plugin for rpc-port tcp connection

#################################################
# rpc-port-unittests
#################################################
%package unittests
Summary:    GTest for rpc-port
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for rpc-port

#################################################
# rpc-port-integtests
#################################################
%package integtests
Summary:    GTest for rpc-port
Group:      Development/Libraries
Requires:   %{name}

%description integtests
GTest for rpc-port

#################################################
# rpc-port-gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    RPC Port(gcov)
Group:      Application Framework/Testing

%description gcov
RPC Port gcov objects
%endif

%package -n rust-rpc-port
Summary:  rpc-port for rust
Group:    Rust/Libraries
Requires: %{name} = %{version}-%{release}

%description -n rust-rpc-port
RPC Port library for rust.

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
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DESD_MODULES_DIR=%{_moddir} -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
%if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE
%else
    -DASAN_ENABLED=TRUE
%endif

# Call make instruction with smp support
%__make %{?jobs:-j%jobs}

%{rustc_std_build} --crate-type=dylib \
        --crate-name=%{real_crate_name} \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        -L native="./src/rpc-port/" \
        %rust_dylib_extern libc \
        ./src/rust-rpc-port/src/lib.rs
%{rustc_std_build} --test --crate-type=bin \
        --extern mockall=%{_rust_dylibdir}/libmockall.so \
        --extern mockall_double=%{_rust_dylibdir}/libmockall_double.so \
        --crate-name=unittests_%{real_crate_name} \
        -L native="./src/rpc-port/" \
        %{?rustc_edition:--edition=%{rustc_edition}} \
        ./src/rust-rpc-port/src/lib.rs

%check
export LD_LIBRARY_PATH="../../src/rpc-port"
ctest -V %{?_smp_mflags}

export LD_LIBRARY_PATH="./src/rpc-port/:%{_rust_dylibdir}"
RUST_BACKTRACE=1 RUST_TEST_THREADS=1 ./unittests_%{real_crate_name}

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/esd-honmun.socket
ln -sf ../esd-honmun.socket %{buildroot}%{_unitdir}/sockets.target.wants/esd-honmun.socket

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
    /usr/bin/mkdir -p /tmp/rpc-port-certs
    /usr/bin/cp -f %{_datadir}/rpc-port-unittests/certs/* /tmp/rpc-port-certs/
    /usr/bin/rpc-port_unittests
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

%post -n rust-rpc-port
/sbin/ldconfig

%postun -n rust-rpc-port
/sbin/ldconfig

%files
%manifest %{name}.manifest
%attr(0644,root,root) %{_libdir}/lib%{name}.so.*
%license LICENSE.APLv2
%config %{_sysconfdir}/dbus-1/system.d/rpc-port.conf

%files devel
%{_includedir}/rpc-port/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib%{name}.so

#################################################
# esd-mod-honmun
#################################################
%files -n esd-mod-honmun
%{_moddir}/mod/libesd-mod-honmun.so
%{_unitdir}/esd-honmun.socket
%{_unitdir}/sockets.target.wants/esd-honmun.socket


#################################################
# rpc-port-unittests
#################################################
%files unittests
%{_bindir}/rpc-port_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
/tmp/rpc-port-certs/*

#################################################
# rpc-port-integtests
#################################################
%files integtests
%{_bindir}/rpc-port_integtests
%{_bindir}/mk_certs.sh

#################################################
# rpc-port-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%files -n rust-rpc-port
%manifest %{name}.manifest
%{_rust_dylibdir}/lib%{real_crate_name}.so
