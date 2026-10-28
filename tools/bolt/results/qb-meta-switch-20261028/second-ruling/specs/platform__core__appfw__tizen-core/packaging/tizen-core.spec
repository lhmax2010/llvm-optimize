Name:       tizen-core
Summary:    Tizen core library
Version:    0.4.2
Release:    0
Group:      App Framework/Application Core
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-resource)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Tizen core library package.

%package devel
Summary:  Tizen core library (Development)
Group:    System/API
Requires: %{name} = %{version}

%description devel
Tizen core library (Development) package.

%package util-devel
Summary:  Tizen core Util library (Development)
Group:    System/API
Requires: %{name} = %{version}

%description util-devel
Tizen core Util library (Development) package.

%package unittests
Summary:    GTest for tizen core API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for tizen core API

%if 0%{?gcov:1}
%package gcov
Summary:  tizen core library (gcov)
Group:    System/API

%description gcov
gcov objects of tizen core library.
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
         -DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
%if 0%{?asan} != 1
         -DASAN_ENABLED=FALSE
%else
         -DASAN_ENABLED=TRUE
%endif
%__make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH="../../src/tizen-core"
ctest --verbose %{?_smp_mflags}
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o %{name}.out --legend --show-details
zip -r %{name}.zip %{name}.out
install -m 0644 %{name}.zip %{buildroot}%{_datadir}/gcov/
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
    /usr/bin/tizen-core_unittests
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
%attr(0644,root,root) %{_libdir}/lib%{name}.so.*
%license LICENSE

%files devel
%{_includedir}/tizen-core/*.h
%{_libdir}/pkgconfig/tizen-core.pc
%{_libdir}/lib%{name}.so

%files util-devel
%{_includedir}/tizen-core-util/*.hpp
%{_libdir}/pkgconfig/tizen-core-util.pc

%files unittests
%{_bindir}/tizen-core_unittests
%{_bindir}/tizen-core-util_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
