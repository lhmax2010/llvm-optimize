Name:       capi-network-bluetooth
Summary:    Network Bluetooth Framework
Version:    0.10.0
Release:    2
Group:      Connectivity/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:	%{name}.manifest
Source1002:	%{name}-devel.manifest
#Requires(post): /sbin/ldconfig
#Requires(postun): /sbin/ldconfig

BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(bluetooth-api)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  cmake
BuildRequires: gtest-devel
%if 0%{?gcov:1}
BuildRequires: lcov
%endif

%description
Network Bluetooth Framework

%package devel
Summary:    Network Bluetooth Framework (DEV)
Group:      Development/Connectivit
Requires:   %{name} = %{version}-%{release}

%description devel
Network Bluetooth Framework.

%devel_desc

%package test
Summary: Network Bluetooth Framework test application
Group:   TO_BE/FILLED
Requires: %{name} = %{version}-%{release}

%description test
This package is C-API test application.

%if 0%{?gcov:1}
%package gcov
Summary: %{name} gcov data

%description gcov
gcov objects
%endif

%package unittests
Summary: %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q
cp %{SOURCE1001} %{SOURCE1002} .

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
%endif

#export CFLAGS="$CFLAGS -DTIZEN_FEATURE_AUDIO_HF_DISABLE -DTIZEN_FEATURE_OTP_SUPPORT"
#export CXXFLAGS="$CXXFLAGS -DTIZEN_FEATURE_AUDIO_HF_DISABLE -DTIZEN_FEATURE_OTP_SUPPORT"
#export FFLAGS="$FFLAGS -DTIZEN_FEATURE_AUDIO_HF_DISABLE -DTIZEN_FEATURE_OTP_SUPPORT"

export CFLAGS="$CFLAGS -DTIZEN_FEATURE_AUDIO_HF_DISABLE -DTIZEN_FEATURE_OTP_SUPPORT -DTIZEN_FEATURE_GATT_RELAY -DTIZEN_GATT_CLIENT"
export CXXFLAGS="$CXXFLAGS -DTIZEN_FEATURE_AUDIO_HF_DISABLE -DTIZEN_FEATURE_OTP_SUPPORT -DTIZEN_FEATURE_GATT_RELAY"
export FFLAGS="$FFLAGS -DTIZEN_FEATURE_AUDIO_HF_DISABLE -DTIZEN_FEATURE_OTP_SUPPORT -DTIZEN_FEATURE_GATT_RELAY"

%ifarch aarch64
echo arch64
export CFLAGS="$CFLAGS -DARCH64"
export CXXFLAGS="$CXXFLAGS -DARCH64"
export FFLAGS="$FFLAGS -DARCH64"
%endif

%ifarch riscv64
echo riscv64
export CFLAGS="$CFLAGS -DARCH64"
export CXXFLAGS="$CXXFLAGS -DARCH64"
export FFLAGS="$FFLAGS -DARCH64"
%endif

%ifarch x86_64
echo x86_64
export CFLAGS="$CFLAGS -DARCH64"
export CXXFLAGS="$CXXFLAGS -DARCH64"
export FFLAGS="$FFLAGS -DARCH64"
%endif

%cmake

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER}

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

#mkdir -p %{buildroot}%{_unitdir}
#install -m 0644 tests/test/bt_infinite_spp_test_server.service %{buildroot}%{_unitdir}/bt_infinite_spp_test_server.service

cat << EOF > run-unittest.sh
#!/bin/bash
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    LD_PRELOAD=/usr/lib/libbluetooth-mock.so /usr/bin/tct-bluetooth-core
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

%check
LD_LIBRARY_PATH=. LD_PRELOAD=tests/unittest/libbluetooth-mock.so tests/unittest/tct-bluetooth-core
%if 0%{?gcov:1}
rm -rf tests
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libcapi-network-bluetooth.so.*

%files test
%manifest %{name}.manifest
%{_bindir}/bt_mesh_unit_test
%{_bindir}/bt_unit_test
%{_bindir}/bt_onoff
%{_bindir}/ble_mouse
%{_bindir}/ble_mouse_with_error
%{_bindir}/hid_keyboard
%{_bindir}/bt_infinite_spp_test
#%{_unitdir}/bt_infinite_spp_test_server.service
#/etc/smack/accesses.d/capi-network-bluetooth-test.efl

%files devel
%manifest %{name}-devel.manifest
%{_includedir}/network/bluetooth.h
%{_includedir}/network/bluetooth_internal.h
%{_includedir}/network/bluetooth_type.h
%{_includedir}/network/bluetooth_type_internal.h
%{_includedir}/network/bluetooth_extension.h
%{_includedir}/network/bluetooth_type_extension.h

%{_libdir}/pkgconfig/capi-network-bluetooth.pc
%{_libdir}/libcapi-network-bluetooth.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%exclude %{_datadir}/gcov/obj/*/*/tests/*
%endif

%files unittests
%{_libdir}/libbluetooth-mock.so
%{_bindir}/tct-bluetooth-core
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
