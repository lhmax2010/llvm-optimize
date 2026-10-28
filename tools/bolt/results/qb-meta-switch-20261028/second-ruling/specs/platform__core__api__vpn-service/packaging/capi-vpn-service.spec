Name:       vpnsvc-pkg
Summary:    VPN service library in TIZEN C API
Version:    1.2.1
Release:    1
Group:      System/Network
License:    Apache-2.0
URL:        N/A
Source0:    %{name}-%{version}.tar.gz
BuildRequires:	cmake
BuildRequires:	pkgconfig(dlog)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:	pkgconfig(capi-system-info)
BuildRequires:	pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires: gtest-devel
BuildRequires: lcov
BuildRequires: tar
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
capi-vpn-service

%package -n capi-vpnsvc
Summary:  VPN service library in TIZEN C API
Group:    Development/Libraries
#Requires: capi-vpnsvc

%description -n capi-vpnsvc
capi-vpnsvc CAPI package

%package -n capi-vpnsvc-devel
Summary:  VPN service library in TIZEN C API (Development)
Group:    Development/Libraries
Requires: capi-vpnsvc

%description -n capi-vpnsvc-devel
capi-vpnsvc CAPI devel package

%if 0%{?gcov:1}
%package gcov
Summary: %{name} gcov data

%description gcov
gcov objects for coverage test
%endif

%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
%endif

export LDFLAGS="$LDFLAGS -Wl,--rpath=%{_libdir}"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DVERSION=%{version} \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DCMAKE_BUILD_TYPE=%{?build_type:%build_type}%{!?build_type:RELEASE} \
	-DCMAKE_VERBOSE_MAKEFILE=ON \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DBUILD_UNITTEST=%{?asan:0}%{!?asan:1}

make %{?jobs:-j%jobs}

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -not -path '*/tools/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%if 0%{?asan} != 1
cat << EOF > run-unittest.sh
#!/bin/bash
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/vpn-service-gtest
}

teardown() {
    echo "teardown start"
}

main() {
    setup
    test_main
    teardown
}

main "$@"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}
%endif

%check
%if 0%{?gcov:1}
LD_LIBRARY_PATH=. tests/vpn-service-gtest
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -n capi-vpnsvc -p /sbin/ldconfig

%postun -n capi-vpnsvc -p /sbin/ldconfig

%files -n capi-vpnsvc
%manifest capi-vpnsvc.manifest
%{_libdir}/libcapi-vpnsvc.so.*
%{_bindir}/vpnsvc_test
%license LICENSE

%files -n capi-vpnsvc-devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/capi-vpnsvc.pc
%{_libdir}/libcapi-vpnsvc.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%if 0%{?asan} != 1
%files unittests
%{_bindir}/vpn-service-gtest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%endif
