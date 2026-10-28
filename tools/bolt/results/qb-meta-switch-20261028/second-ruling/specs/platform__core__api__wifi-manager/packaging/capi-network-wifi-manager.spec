Name:		capi-network-wifi-manager
Summary:	Network Wi-Fi library in TIZEN C API
Version:	1.3.25
Release:	0
Group:		System/Network
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:	cmake
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(vconf)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(capi-base-common)
BuildRequires:	pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:	pkgconfig(gmock)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Network Wi-Fi Manager library in Tizen C API

%package devel
Summary: Network Wi-Fi Manager library in Tizen C API (Development)
Group: Network & Connectivity/Development
Requires: %{name} = %{version}-%{release}

%description devel
Network Wi-Fi Manager library in Tizen C API (Development)

%package tool
Summary: Test Application for Wi-Fi Manager
Group: Network & Connectivity/Utilities
Requires: %{name} = %{version}

%description tool
Test Application for Wi-Fi Manager

%if 0%{?gcov:1}
%package gcov
Summary: Coverage Data of %{name}
Group: Network & Connectivity/Testing
BuildRequires:  pkgconfig(gmock)
BuildRequires:  gtest-devel
BuildRequires:  lcov
BuildRequires:  tar

%description gcov
The %{name}-gcov pacakge contains gcov objects
%endif

%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q
cp %{SOURCE1001} ./

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

# Build for common
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DBIN_INSTALL_DIR:PATH=%{_bindir}

make %{?_smp_mflags}

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' ! -path '*/tools/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/gtest-wifi-manager
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


%check
%if 0%{?gcov:1}
tests/gtest-wifi-manager
# Calculating linecoverage only for library source code
find . -name "*.gcno" | grep -v src | xargs rm -f
find . -name "*.gcda" | grep -v src | xargs rm -f
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/lib%{name}.so.*
%license LICENSE.APLv2

%files devel
%{_includedir}/network/*.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so

%files tool
%manifest %{name}.manifest
%{_bindir}/wifi_manager_test
%{_bindir}/wifi_mgr_tool
%{_bindir}/wifi_connect_tool
%license LICENSE.APLv2

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%exclude %{_datadir}/gcov/obj/*/*/tests/*
%endif

%files unittests
%{_bindir}/gtest-wifi-manager
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
