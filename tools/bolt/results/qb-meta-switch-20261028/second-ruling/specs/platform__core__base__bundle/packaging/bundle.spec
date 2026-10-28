Name:       bundle
Summary:    String key-val dictionary ADT
Version:    0.18.15
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:        bundle-%{version}.tar.gz
Source1001:     bundle.manifest
Source1002:     parcel.manifest
Source1003:     tizen-dlog.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(gmock)

BuildRequires:  rust
BuildRequires:  rust-libc
BuildRequires:  rust-glib-sys
BuildRequires:  rust-mockall
BuildRequires:  rust-mockall_double

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Simple string key-val dictionary ADT

%package devel
Summary:    String key-val dictionary ADT (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Simple string key-val dictionary ADT (devel)

#################################################
# unittests
#################################################
%package unittests
Summary:    GTest for bundle
Group:      Development/Libraries

%description unittests
GTest for bundle

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Simple string key-val dictionary ADT (gcov)
Group:      Application Framework/Testing

%description gcov
Simple string key-val dictionary ADT gcov objects
%endif

#################################################
## parcel
#################################################
%package -n parcel
Summary:    Parcel Library
Group:      Development/Libraries

%description -n parcel
Parcel Library

%package -n parcel-devel
Summary:    Parcel Library (devel)
Group:      Development/Libraries
Requires:   parcel = %{version}-%{release}

%description -n parcel-devel
Parcel Library (devel)

#################################################
# parcel-unittests
#################################################
%package -n parcel-unittests
Summary:    GTest for parcel
Group:      Development/Libraries

%description -n parcel-unittests
GTest for parcel

#################################################
## tizen-libopener-devel
#################################################
%package -n tizen-libopener-devel
Summary:    Tizen-libopener (devel)
Group:      Development/Libraries

%description -n tizen-libopener-devel
C++ wrapper API for dlopen and dlsym

#################################################
# tizen-libopener-unittests
#################################################
%package -n tizen-libopener-unittests
Summary:    GTest for tizen-libopener
Group:      Development/Libraries

%description -n tizen-libopener-unittests
GTest for tizen-libopener

#################################################
## tizen-database-devel
#################################################
%package -n tizen-database-devel
Summary:    Tizen-database Library (devel)
Group:      Development/Libraries

%description -n tizen-database-devel
Tizen-database Library (devel)

#################################################
# tizen-database-unittests
#################################################
%package -n tizen-database-unittests
Summary:    GTest for tizen-database
Group:      Development/Libraries

%description -n tizen-database-unittests
GTest for tizen-database

#################################################
## tizen-dlog
#################################################
%package -n tizen-dlog
Summary:    Tizen-dlog Library
Group:      System/Libraries

%description -n tizen-dlog
Tizen-dlog Library

#################################################
## tizen-dlog-devel
#################################################
%package -n tizen-dlog-devel
Summary:    Tizen-dlog Library (devel)
Group:      Development/Libraries
Requires:   tizen-dlog = %{version}-%{release}

%description -n tizen-dlog-devel
Tizen-dlog Library (devel)

#################################################
# tizen-dlog-unittests
#################################################
%package -n tizen-dlog-unittests
Summary:    GTest for tizen-dlog
Group:      Development/Libraries

%description -n tizen-dlog-unittests
GTest for tizen-dlog

#################################################
## tizen-shared-queue-devel
#################################################
%package -n tizen-shared-queue-devel
Summary:    Tizen-shared-queue Library (devel)
Group:      Development/Libraries

%description -n tizen-shared-queue-devel
Tizen-Shared-Queue Library (devel)

#################################################
# tizen-shared-queue-unittests
#################################################
%package -n tizen-shared-queue-unittests
Summary:    GTest for tizen-shared-queue
Group:      Development/Libraries

%description -n tizen-shared-queue-unittests
GTest for tizen-shared-queue

#################################################
# rust-tizen-bundle
#################################################
%package -n rust-tizen-bundle
Summary:    Bundle Library for Tizen rust applications
Group:      Development/Libraries
Requires:   rust-libc
Requires:   bundle

%description -n rust-tizen-bundle
Bundle Library for Tizen rust applications

#################################################
# rust-tizen-parcel
#################################################
%package -n rust-tizen-parcel
Summary:    Parcel Library for Tizen rust applications
Group:      Development/Libraries
Requires:   rust-libc
Requires:   parcel

%description -n rust-tizen-parcel
parcel Library for Tizen rust applications

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
cp %{SOURCE1001} ./rust-tizen-bundle.manifest
cp %{SOURCE1001} ./rust-tizen-parcel.manifest

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS+=" -fno-delete-null-pointer-checks"
export CXXFLAGS+=" -fno-delete-null-pointer-checks"
%endif
}

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DFULLVER=%{version} \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
    -DMAJORVER=${MAJORVER} \
%if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE \
%else
    -DASAN_ENABLED=TRUE \
%endif
    .

%__make %{?_smp_mflags}

%{rustc_std_build} --crate-type=dylib \
    --crate-name=tizen_bundle \
    -L native="./src/bundle" \
    %{?rustc_edition:--edition=%{rustc_edition}} \
    %rust_dylib_extern libc \
    src/rust-tizen-bundle/src/lib.rs

%{rustc_std_build} --test --crate-type=bin \
    --crate-name=tizen_bundle_unittests \
    -L native="./src/bundle" \
    %{?rustc_edition:--edition=%{rustc_edition}} \
    %rust_dylib_extern libc \
    %rust_dylib_extern mockall \
    %rust_dylib_extern mockall_double \
    src/rust-tizen-bundle/src/lib.rs

%{rustc_std_build} --crate-type=dylib \
    --crate-name=tizen_parcel \
    -L native="./src/parcel" \
    %{?rustc_edition:--edition=%{rustc_edition}} \
    %rust_dylib_extern libc \
    src/rust-tizen-parcel/src/lib.rs

%{rustc_std_build} --test --crate-type=bin \
    --crate-name=tizen_parcel_unittests \
    -L native="./src/parcel" \
    %{?rustc_edition:--edition=%{rustc_edition}} \
    %rust_dylib_extern libc \
    %rust_dylib_extern mockall \
    %rust_dylib_extern mockall_double \
    src/rust-tizen-parcel/src/lib.rs

%check
export LD_LIBRARY_PATH="../../src/bundle:../../src/parcel:../../src/tizen-dlog"
ctest --verbose %{?_smp_mflags}

export LD_LIBRARY_PATH="%{_rust_dylibdir}:./src/bundle"
RUST_BACKTRACE=1 RUST_TEST_THREADS=1 ./tizen_bundle_unittests

export LD_LIBRARY_PATH="%{_rust_dylibdir}:./src/parcel:"
RUST_BACKTRACE=1 RUST_TEST_THREADS=1 ./tizen_parcel_unittests

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%install
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
PAKCAGE="<NAME>-%{version}"

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
    /usr/bin/<NAME>_unittests
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
sed -i -e 's/<NAME>/bundle/g' %{buildroot}%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/parcel
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/parcel/
sed -i -e 's/<NAME>/parcel/g' %{buildroot}%{_bindir}/tizen-unittests/parcel/run-unittest.sh

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/tizen-database
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/tizen-database/
sed -i -e 's/<NAME>/tizen-database/g' %{buildroot}%{_bindir}/tizen-unittests/tizen-database/run-unittest.sh

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/tizen-dlog
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/tizen-dlog/
sed -i -e 's/<NAME>/tizen-dlog/g' %{buildroot}%{_bindir}/tizen-unittests/tizen-dlog/run-unittest.sh

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/tizen-libopener
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/tizen-libopener/
sed -i -e 's/<NAME>/tizen-libopener/g' %{buildroot}%{_bindir}/tizen-unittests/tizen-libopener/run-unittest.sh

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/tizen-shared-queue
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/tizen-shared-queue/
sed -i -e 's/<NAME>/tizen-shared-queue/g' %{buildroot}%{_bindir}/tizen-unittests/tizen-shared-queue/run-unittest.sh

install -d -m 0755 %{buildroot}%{_libdir}
install -d -m 0755 %{buildroot}%{_rust_dylibdir}
install -m 0644 libtizen_bundle.so %{buildroot}/%{_rust_dylibdir}/libtizen_bundle.so
strip -s -N .rustc %{buildroot}/%{_rust_dylibdir}/libtizen_bundle.so
ln -sf %{_rust_dylibdir}/libtizen_bundle.so %{buildroot}%{_libdir}/libtizen_bundle.so

install -m 0644 libtizen_parcel.so %{buildroot}/%{_rust_dylibdir}/libtizen_parcel.so
strip -s -N .rustc %{buildroot}/%{_rust_dylibdir}/libtizen_parcel.so
ln -sf %{_rust_dylibdir}/libtizen_parcel.so %{buildroot}%{_libdir}/libtizen_parcel.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n parcel
/sbin/ldconfig

%postun -n parcel
/sbin/ldconfig

%post -n tizen-dlog
/sbin/ldconfig

%postun -n tizen-dlog
/sbin/ldconfig

%post unittests
%if 0%{?gcov:1}
%{_bindir}/bundle_unittests
%endif

%post -n rust-tizen-bundle
/sbin/ldconfig

%postun -n rust-tizen-bundle
/sbin/ldconfig

%post -n rust-tizen-parcel
/sbin/ldconfig

%postun -n rust-tizen-parcel
/sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libbundle.so.*
%license LICENSE

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/pkgconfig/bundle.pc
%{_libdir}/libbundle.so

#################################################
# unittests
#################################################
%files unittests
%{_bindir}/bundle_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# bundle-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

#################################################
# parcel
#################################################
%files -n parcel
%manifest parcel.manifest
%license LICENSE
%{_libdir}/libparcel.so.*

%files -n parcel-devel
%manifest parcel.manifest
%{_includedir}/parcel/*
%{_libdir}/pkgconfig/parcel.pc
%{_libdir}/libparcel.so

%files -n parcel-unittests
%{_bindir}/parcel_unittests
%{_bindir}/tizen-unittests/parcel/run-unittest.sh

#################################################
# tizen-libopener-devel
#################################################
%files -n tizen-libopener-devel
%{_includedir}/tizen-libopener/*
%{_libdir}/pkgconfig/tizen-libopener.pc

%files -n tizen-libopener-unittests
%{_bindir}/tizen-libopener_unittests
%{_bindir}/tizen-unittests/tizen-libopener/run-unittest.sh

#################################################
# tizen-database-devel
#################################################
%files -n tizen-database-devel
%{_includedir}/tizen-database/*
%{_libdir}/pkgconfig/tizen-database.pc

%files -n tizen-database-unittests
%{_bindir}/tizen-database_unittests
%{_bindir}/tizen-unittests/tizen-database/run-unittest.sh

#################################################
# tizen-dlog
#################################################
%files -n tizen-dlog
%manifest tizen-dlog.manifest
%license LICENSE
%{_libdir}/libtizen-dlog.so.*

#################################################
# tizen-dlog-devel
#################################################
%files -n tizen-dlog-devel
%manifest tizen-dlog.manifest
%{_includedir}/tizen-dlog/*
%{_libdir}/pkgconfig/tizen-dlog.pc
%{_libdir}/libtizen-dlog.so

%files -n tizen-dlog-unittests
%{_bindir}/tizen-dlog_unittests
%{_bindir}/tizen-unittests/tizen-dlog/run-unittest.sh

#################################################
# tizen-shared-queue-devel
#################################################
%files -n tizen-shared-queue-devel
%{_includedir}/tizen-shared-queue/*
%{_libdir}/pkgconfig/tizen-shared-queue.pc

%files -n tizen-shared-queue-unittests
%{_bindir}/tizen-shared-queue_unittests
%{_bindir}/tizen-unittests/tizen-shared-queue/run-unittest.sh

#################################################
# rust-tizen-bundle
#################################################
%files -n rust-tizen-bundle
%manifest rust-tizen-bundle.manifest
%license LICENSE
%{_rust_dylibdir}/libtizen_bundle.so
%{_libdir}/libtizen_bundle.so

#################################################
# rust-tizen-parcel
#################################################
%files -n rust-tizen-parcel
%manifest rust-tizen-parcel.manifest
%license LICENSE
%{_rust_dylibdir}/libtizen_parcel.so
%{_libdir}/libtizen_parcel.so
