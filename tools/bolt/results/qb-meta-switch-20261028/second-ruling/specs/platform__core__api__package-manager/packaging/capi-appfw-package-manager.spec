Name:       capi-appfw-package-manager
Summary:    Package Manager API
Version:    0.15.3
Release:    1
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-appfw-package-manager.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:	pkgconfig(vconf)
BuildRequires:	pkgconfig(aul)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
The Package Manager API provides functions to install, uninstall the package,
and also privides event listening function.

%package devel
Summary:  Package Manager API (Development)
Group:    System/API
Requires: %{name} = %{version}

%description devel
The Package Manager API provides functions to install, uninstall the package,
and also privides event listening function. (DEV)

%package test
Summary:  Package Manager API (Test Tool)
Group:    System/API
Requires: %{name} = %{version}

%description test
This package includes test tool for package manager apis.

%if 0%{?gcov:1}
%package gcov
Summary:  Package Manager API (gcov)
Group:    System/API

%description gcov
gcov objects for a package manager library
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

make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH="../src"
ctest --verbose %{?_smp_mflags}
%if 0%{?gcov:1}
lcov -c --exclude="tests" --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
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
    /usr/bin/package-manager-unittests
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


%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libcapi-appfw-package-manager.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/appfw/*.h
%{_libdir}/libcapi-appfw-package-manager.so
%{_libdir}/pkgconfig/*.pc

%files test
%manifest %{name}.manifest
%{_bindir}/pkgmgr_tool
%{_bindir}/package-manager-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
