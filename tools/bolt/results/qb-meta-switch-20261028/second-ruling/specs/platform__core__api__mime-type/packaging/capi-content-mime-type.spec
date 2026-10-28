Name:       capi-content-mime-type
Summary:    A MIME type library in Tizen C API
Version:    0.1.9
Release:    1
Group:      APIs
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-content-mime-type.manifest
Source1002: 	capi-content-mime-type-unittests.manifest
BuildRequires:  cmake
BuildRequires:  shared-mime-info
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(xdgmime)
%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description

%package devel
Summary:  A MIME type library in Tizen C API (Development)
Group:    APIs
Requires: %{name} = %{version}
Requires:  pkgconfig(capi-base-common)

%description devel

%if 0%{?gcov:1}
%package gcov
Summary:  A MIME type library(gcov)
Group:    System/API

%description gcov
gcov objects of a MIME type library
%endif

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake .  -DFULLVER=%{version} -DMAJORVER=${MAJORVER}

make %{?jobs:-j%jobs}

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
    chmod -r /usr/bin/tizen-unittests/capi-content-mime-type/test_in_accessible.png
    /usr/bin/mkdir -p "${GCOV_PATH}/${PACKAGE}"
    set_perm
}

test_main() {
    echo "test_main start"
    export "GCOV_PREFIX=/tmp"
    su - owner -c '/usr/bin/mime-type-unit-test'
}

teardown() {
    echo "teardown start"
    chmod +r /usr/bin/tizen-unittests/capi-content-mime-type/test_in_accessible.png
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

install -m 664 test/unit_tests/test.png %{buildroot}%{_bindir}/tizen-unittests/%{name}/
install -m 664 test/unit_tests/test_in_accessible.png %{buildroot}%{_bindir}/tizen-unittests/%{name}/

%check
chmod -r test/unit_tests/test_in_accessible.png
export LD_LIBRARY_PATH="../../mime-type"
ctest --verbose %{?_smp_mflags}
chmod -r test/unit_tests/test_in_accessible.png

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/lib*.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/content/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%manifest %{name}-unittests.manifest
%{_bindir}/mime-type-unit-test
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%{_bindir}/tizen-unittests/%{name}/*.png
