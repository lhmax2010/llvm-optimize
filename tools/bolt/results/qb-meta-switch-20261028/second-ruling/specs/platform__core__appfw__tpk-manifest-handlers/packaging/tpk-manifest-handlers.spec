Name:           tpk-manifest-handlers
Summary:        tpk-manifest-handlers
Version:        1.15.0
Release:        1
Group:          Application Framework/Package Management
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
Source100:      %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(manifest-parser)
BuildRequires:  pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires: lcov
BuildRequires: zip
%endif

%description
Installs tpk parser and handlers based on manifest-parser

%package devel
Summary:    Manifest parser development files
Group:      Application Framework/Package Management
Requires:   %{name} = %{version}

%description devel
This package contains necessaary files for manifest-parser development

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittest binary

%prep
%setup -q
cp %{SOURCE100} .

%build
export CFLAGS="$(echo $CFLAGS | sed 's/-Wl,--as-needed//g')"
export CXXFLAGS="$(echo $CXXFLAGS | sed 's/-Wl,--as-needed//g')"
export FFLAGS="$(echo $FFLAGS | sed 's/-Wl,--as-needed//g')"

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

# BUILD_PARSER macro is defined so we can build two separate projects
# with cmake, which are on one repository. Later this macro
# is used in CMakeLists.txt files to distinguish, which project
# is currently being build.
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type} \
         -DTIZEN_VERSION=%{tizen_version} \
         -DFULLVER=%{version} -DMAJORVER=${MAJORVER}

make %{?_smp_mflags}

%check
export LD_LIBRARY_PATH=../../src/tpk_manifest_handlers
ctest -V
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

setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    CUR_DIR=$(pwd)
    cd /usr/bin
    /usr/bin/tpk-manifest-handlers-unit-test
    cd $CUR_DIR
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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libtpk-manifest-handlers.so.*
%license LICENSE

%files devel
%manifest %{name}.manifest
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libtpk-manifest-handlers.so
%{_includedir}/tpk_manifest_handlers/*.h

#################################################
# tpk-manifest-handlers-gcov
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
%{_bindir}/tpk-manifest-handlers-unit-test
%{_bindir}/test_samples
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
