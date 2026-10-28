# Do not provide .so automatically for the extensions.
%global __provides_exclude_from ^.*\\.extension

Name:       capi-network-wifi-direct
Summary:    Network WiFi-Direct Library
Version:    1.4.0
Release:    1
Group:      Network & Connectivity/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
%if 0%{?gcov:1}
BuildRequires:  gtest-devel
BuildRequires:  lcov
BuildRequires:  tar
%endif
BuildRequires:  pkgconfig(gmock)
BuildRequires:  cmake
BuildRequires:  gettext-devel
Provides:       %{name}-profile_wearable = %{version}-%{release}
Provides:       %{name}-profile_ivi = %{version}-%{release}

Provides: libwifi-direct.so.0

%description
Network WiFi-Direct library in Tizen CAPI (Shared Library)

%package devel
Summary:    Network WiFi-Direct Library (Development)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires: capi-base-common-devel

%description devel
Network WiFi-Direct library in Tizen CAPI (Shared Library) (Development)

%package 	tool
Summary:    Test Application for Wi-Fi Direct
Group:      Network & Connectivity/Testing
Requires:   %{name} = %{version}-%{release}

%description tool
Test Application for Wi-Fi Direct Framework

%if 0%{?gcov:1}
%package gcov
Summary:    ${name} gcov data
Group:      Network & Connectivity/Development
%description gcov
Wi-Fi Direct gcov objects
%endif

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary


%prep
%setup -q

%ifarch %{arm}
export ARCH=arm
%else
export ARCH=i586
%endif

chmod 644 %{SOURCE0}

%build

export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

cmake . \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DLIB_DIR:PATH=%{_libdir} \
        -DBIN_DIR:PATH=%{_bindir} \
        -DINCLUDE_DIR:PATH=%{_includedir} \
        -DFULLVER=%{version} \
        -DMAJORVER=${MAJORVER}
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
    /usr/bin/gtest-wifi-direct
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
tests/gtest-wifi-direct
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

ln -sf libwifi-direct.so.%{version} %{buildroot}/%{_libdir}/libwifi-direct.so.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest capi-network-wifi-direct.manifest
%license LICENSE
%defattr(-,root,root,-)
%exclude %{_libdir}/libwifi-direct.so.*.extension
%{_libdir}/libwifi-direct.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/capi-network-wifi-direct.pc
%{_includedir}/wifi-direct/wifi-direct.h
%{_includedir}/wifi-direct/wifi-direct-internal.h
%{_libdir}/libwifi-direct.so

%files tool
%{_bindir}/wifi_direct_test
%{_bindir}/gtest-wifi-direct

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%{_bindir}/gtest-wifi-direct
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
