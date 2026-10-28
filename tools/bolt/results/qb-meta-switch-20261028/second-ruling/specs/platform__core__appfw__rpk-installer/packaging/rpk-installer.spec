Name:       rpk-installer
Summary:    Resource Package Installer
Version:    0.5.6
Release:    1
Group:      Application Framework/Package Management
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:  cmake
BuildRequires:  app-installers-tests
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(app-installers)
BuildRequires:  pkgconfig(manifest-parser)
BuildRequires:  pkgconfig(tpk-manifest-handlers)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(security-manager)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(aul)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
This package contains rpk-installer library

%package -n rpk-installer-devel
Summary:    Rpk-installer development files
Group:      Application Framework/Package Management
Requires:   %{name} = %{version}

%description devel
This package contains header files of rpk-installer library

%package -n rpk-installer-tests
Summary: Unit tests for rpk-installer
Requires: rpk-installer = %{version}

%description -n rpk-installer-tests
Unit tests for rpk-installer

%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary

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
%cmake . -DCMAKE_VERBOSE_MAKEFILE:BOOL=%{?verbose_make:ON}%{!?verbose_make:OFF} \
         -DUNITDIR=%{_unitdir} \
         -DFULLVER=%{version} \
         -DMAJORVER=${MAJORVER} \
         %if 0%{?asan} != 1
          -DASAN_ENABLED=FALSE
         %else
          -DASAN_ENABLED=TRUE
         %endif

%__make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}/etc/package-manager/backend
ln -s %{_bindir}/unified-backend %{buildroot}%{_sysconfdir}/package-manager/backend/rpk

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

#################################################
# generate unittest automation script
#################################################
cat << EOF > run-unittest.sh
#!/bin/bash
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/rpk-installer-unit-test
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

%post
/sbin/ldconfig

%check
export LD_LIBRARY_PATH=../../src/rpk:../../src/rpk_manifest_handlers/
ctest -V

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_sysconfdir}/package-manager/backendlib/librpk.so
%{_libdir}/librpk-installer.so*
%{_libdir}/librpk-manifest-handlers.so.*
%{_sysconfdir}/package-manager/backend/rpk

%files devel
%{_includedir}/app-installers/rpk/*.h
%{_includedir}/app-installers/rpk/*/*/*.h
%{_includedir}/rpk_manifest_handlers/*.h
%{_libdir}/librpk-manifest-handlers.so
%{_libdir}/pkgconfig/rpk-installer.pc

%files -n rpk-installer-tests
%{_bindir}/rpk-installer-unit-test
%{_bindir}/rpk-installer-ut/smoke-test
%{_bindir}/rpk-installer-ut/extensive-smoke-test
%{_bindir}/rpk-installer-ut/recovery-test
%{_bindir}/rpk-installer-ut/smoke-test-helper
%{_libdir}/librpk-smoke-utils.so*
%{_includedir}/app-installers/smoke_tests/rpk_smoke_utils.h
%{_datadir}/rpk-installer-ut/*

#################################################
# rpk-installer-gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Simple string key-val dictionary ADT (gcov)
Group:      Application Framework/Testing

%description gcov
Simple string key-val dictionary ADT gcov objects
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%files unittests
%{_bindir}/rpk-installer-unit-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
