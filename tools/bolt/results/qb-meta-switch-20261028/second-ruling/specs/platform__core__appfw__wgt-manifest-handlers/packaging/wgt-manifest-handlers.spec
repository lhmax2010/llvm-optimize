Name:           wgt-manifest-handlers
Summary:        wgt-manifest-handlers
Version:        1.11.4
Release:        1
Group:          Application Framework/Package Management
License:        Apache-2.0 and BSD-3-Clause
Source0:        %{name}-%{version}.tar.gz
Source100:      %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(xdgmime)
BuildRequires:  pkgconfig(manifest-parser)
BuildRequires:  pkgconfig(capi-system-info)

%if 0%{?gcov:1}
BuildRequires: lcov
BuildRequires: zip
%endif

%description
This is a meta package that installs wgt manifest handlers.

%package devel
Summary:    Wgt manifest handlers development files
Group:      Application Framework/Package Management
Requires:   %{name} = %{version}

%description devel
This package contains necessaary files for wgt-manifest-handlers development

%package unittests
Summary: Unit tests for wgt-manifest-handlers
Requires: %{name} = %{version}

%description unittests
Unit tests for al modules of manifest-parser

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
export LD_LIBRARY_PATH=../../src/wgt_manifest_handlers
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
    /usr/bin/wgt-manifest-handlers-unit-test
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
%{_libdir}/libwgt-manifest-handlers.so.*
%license LICENSE LICENSE-xwalk

%files devel
%manifest %{name}.manifest
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libwgt-manifest-handlers.so
%{_includedir}/wgt_manifest_handlers/*.h

%files unittests
%{_bindir}/wgt-manifest-handlers-unit-test
%{_bindir}/test_samples
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# wgt-manifest-handlers-gcov
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
