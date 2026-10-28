Name:       hal-backend-bluetooth-usb
Summary:    firmware and tools for bluetooth
Version:    0.1.0
Release:    1
Group:      TO_BE_FILLED
License:    Apache-2.0
Source0:    hal-backend-bluetooth-usb-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
USB firmware and tools for bluetooth

%prep
%setup -q -n hal-backend-bluetooth-usb-%{version}

%build
export CFLAGS="$CFLAGS -fpie -fvisibility=hidden"
export CXXFLAGS="$CXXFLAGS -fpie -fvisibility=hidden"
export LDFLAGS="$LDFLAGS -Wl,--rpath=/usr/lib -Wl,--as-needed -Wl,--unresolved-symbols=ignore-in-shared-libs -pie"

cmake ./ -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPLUGIN_INSTALL_PREFIX=%{_prefix} \
	-DHAL_LIB_DIR=%{_hal_libdir} \
	-DHAL_LICENSE_DIR=%{_hal_licensedir} \
	-DHAL_SYSCONF_DIR=%{_hal_sysconfdir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.APLv2
%{_hal_sysconfdir}/bluetooth/bt-dev-end.sh
%{_hal_sysconfdir}/bluetooth/bt-dev-start.sh
%{_hal_libdir}/*.so*
