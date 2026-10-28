Name:       capi-appfw-component-manager
Summary:    Component Manager API
Version:    1.2.6
Release:    1
Group:      Application Framework/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
The Component Manager API provides functions to get information about running components.

%package devel
Summary:  Component Manager API (Development)
Group:    Application Framework/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The Component Manager API provides functions to get information about running components. (DEV)

#################################################
# unittests
#################################################
%package unittests
Summary:    GTest for Component Manager API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for Component Manager API

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Component Manager API (gcov)
Group:      Application Framework/Testing

%description gcov
Component Manager API gcov objects
%endif

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER}
%__make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH=../../src/
ctest --verbose %{?_smp_mflags}

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
    /usr/bin/component-manager-unit-test
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
%{_libdir}/libcapi-appfw-component-manager.so.*
%manifest %{name}.manifest
%license LICENSE

%files devel
%{_includedir}/appfw/*.h
%{_libdir}/libcapi-appfw-component-manager.so
%{_libdir}/pkgconfig/*.pc

#################################################
# component-manager-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%files unittests
%{_bindir}/component-manager-unit-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
