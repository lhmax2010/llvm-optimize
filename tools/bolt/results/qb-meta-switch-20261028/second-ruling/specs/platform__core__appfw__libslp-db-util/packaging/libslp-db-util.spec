Name: libslp-db-util
Version: 0.1.2
Release: 0
License: Apache-2.0
Summary: DB Utility
Group: Application Framework/Database
Source0: %{name}-%{version}.tar.gz
Source1001:	%{name}.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(vconf)
BuildRequires: gtest-devel

%if 0%{?gcov:1}
BuildRequires: lcov
%endif

%description
DB Utility.

%package devel
Summary: Devel package for libslp-db-util (devel)
Requires: %{name} = %{version}
%description devel
Devel package for libslp-db-util (devel)

%if 0%{?gcov:1}
%package gcov
Summary: DB Utility(gcov)
%description gcov
libslp-db-util gcov objects
%endif

%package unittests
Summary:    %{name} unittests binary
%description unittests
unittests binary

%prep
%setup -q
cp %{SOURCE1001} ./%{name}.manifest

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version} \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}
make %{?_smp_mflags}

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
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/db-util-gtest
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
install -m 0755 ./tests/db-util-gtest %{buildroot}%{_bindir}


%check
%if 0%{?gcov:1}
pushd tests
./test-collation-db.sh
LD_PRELOAD=./libvconf-mock.so LD_LIBRARY_PATH=.. ./db-util-gtest
popd
lcov -c --ignore-errors mismatch --ignore-errors graph --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/libSLP-db-util.so.*
%license LICENSE.APLv2

%files devel
%{_libdir}/libSLP-db-util.so
%{_libdir}/pkgconfig/db-util.pc
%{_includedir}/db-util/*.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%files unittests
%{_bindir}/db-util-gtest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
