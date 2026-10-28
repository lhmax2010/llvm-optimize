Name:		capi-network-connection
Summary:	Network Connection library in TIZEN C API
Version:	1.0.126
Release:	0
Group:		System/Network
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(vconf)
BuildRequires:	pkgconfig(network)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(capi-base-common)
BuildRequires:	pkgconfig(capi-system-info)
BuildRequires:  gtest-devel
%if 0%{?gcov:1}
BuildRequires:	lcov
%endif

Requires(post):		/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
Network Connection library in Tizen C API

%package devel
Summary:	Network Connection library in Tizen C API (Development)
Group:		System/Network
Requires:	%{name} = %{version}-%{release}

%description devel
Network Connection library in Tizen C API (Development)

%package tool
Summary: Test Application for Network Connection library
Group: Network & Connectivity/Utilities
Requires: %{name} = %{version}

%description tool
Test Application for Network Connection library

%if 0%{?gcov:1}
%package gcov
Summary:	Network Connection library (gcov)
Group:		Network/Testing

%description gcov
gcov objects for coverage test
%endif

%if 0%{?asan} != 1
%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary
%endif

%prep
%setup -q


%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
%endif

export CFLAGS+=' -Wno-unused-local-typedefs'

%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS+=" -Wno-error=implicit-enum-enum-cast "
%endif
}

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake -DCMAKE_INSTALL_PREFIX=/usr -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
	-DLIB_PATH=%{_lib} -DDEBUG_GCOV=%{?debug_gcov:1}%{!?debug_gcov:0} \
	-DBUILD_UNITTEST=%{?asan:0}%{!?asan:1} \
%if 0%{?model_build_feature_network_dsds} == 1
	-DTIZEN_DUALSIM_ENABLE=1 \
%endif
	.

make %{?_smp_mflags}

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' ! -iname '*mptcp*' ! -path '*/test/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%if 0%{?asan} != 1
cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/tct-connection-core
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
%endif

%check
%if 0%{?gcov:1}
pushd unittest
./run_coverage.sh
popd
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest capi-network-connection.manifest
%attr(644,-,-) %{_libdir}/libcapi-network-connection.so.*
%license LICENSE

%files devel
%{_includedir}/network/*.h
%{_includedir}/tv/network/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-network-connection.so

%files tool
%manifest capi-network-connection.manifest
%{_bindir}/connection_test
%license LICENSE

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%exclude %{_datadir}/gcov/obj/*/*/unittest/*
%endif

%if 0%{?asan} != 1
%files unittests
%{_bindir}/tct-connection-core
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%endif
