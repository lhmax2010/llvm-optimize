Name:          unified-backend
Summary:       Unified Tizen package installer backend
Version:       0.1.1
Release:       1
Group:         Application Framework/Package Management
License:       Apache-2.0
Source0:       %{name}-%{version}.tar.gz

Source1000:    %{name}.manifest
Source1001:    unified-installer.manifest
Source1002:    unified-installer-tests.manifest

BuildRequires: app-installers-tests
BuildRequires: cmake
BuildRequires: tpk-installer-tests
BuildRequires: wgt-installer-tests
BuildRequires: pkgconfig(app-installers)
BuildRequires: pkgconfig(libgum)
BuildRequires: pkgconfig(manifest-parser)
BuildRequires: pkgconfig(minizip)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(pkgmgr-installer)
BuildRequires: pkgconfig(pkgmgr-types)
BuildRequires: pkgconfig(tpk-installer)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(wgt-installer)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(rpk-installer)
BuildRequires: pkgconfig(libxml-2.0)

%if 0%{?gcov:1}
BuildRequires: lcov
%endif

%description
This is a package that installs the Unified backend of pkgmgr.

%package -n unified-installer
Summary:    Unified Tizen package installer library
Group:      Application Framework/Package Management

%description -n unified-installer
This package contains unified-installer library

%package -n unified-installer-devel
Summary:  Unified Installer development files
Group:    Application Framework/Package Management
Requires: unified-installer = %{version}

%description -n unified-installer-devel
This package contains header files of unified-installer library

%package -n unified-installer-tests
Summary:  Unit tests for unified-installer
Requires: unified-installer = %{version}

%description -n unified-installer-tests
Unit tests for unified-installer

%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q

cp %{SOURCE1000} .
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
%cmake .
make %{?_smp_mflags}

%install
%make_install

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
    /usr/bin/unified-installer-ut/unified-installer-unit-test
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
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}

mkdir -p %{buildroot}/etc/package-manager/backend
ln -s %{_bindir}/%{name} %{buildroot}%{_sysconfdir}/package-manager/backend/unified

%check
export LD_LIBRARY_PATH=../../src/unified
ctest -V

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/unified-backend
%{_sysconfdir}/package-manager/backend/unified

%files -n unified-installer
%manifest unified-installer.manifest
%{_libdir}/libunified-installer.so*

%files -n unified-installer-devel
%{_includedir}/app-installers/unified/*.h
%{_libdir}/pkgconfig/unified-installer.pc

%files -n unified-installer-tests
%manifest unified-installer-tests.manifest
%{_bindir}/unified-installer-ut/*
%{_datadir}/unified-installer-ut/*

#################################################
# unified-backend-gcov
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
%defattr(-,root,root,-)
%{_datadir}/gcov/obj/*
%endif

%files unittests
%{_bindir}/unified-installer-ut/unified-installer-unit-test
%{_bindir}/unified-installer-ut/test_samples/*
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
