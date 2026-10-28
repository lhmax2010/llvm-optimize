Name:       hal-api-device
Summary:    API library for HAL device modules
Version:    1.0.0
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    hal-api-device.manifest
Source2:    hal-api-device-manifest.xml
BuildRequires:  cmake
BuildRequires:  tidl
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(hal-api-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(rpc-port)

%description
API library for HAL device modules

%package devel
Summary:  API library for HAL device modules (Development)
Group:    System/Development
Requires: %{name} = %{version}-%{release}

%description devel
API library for HAL device modules (Development package)

%package haltests
Summary:        Device HAL(Hardware Abstraction Layer) Test Cases
Requires:       %{name} = %{version}-%{release}

%description haltests
Device HAL(Hardware Abstraction Layer) Test Cases

%prep
%setup -q
mkdir -p ./src/generated
tidlc -p -l C -i ./include/hal_device_display_ipc_1.tidl -o ./src/generated/hal_device_display_proxy_1 -n
tidlc -s -l C -i ./include/hal_device_display_ipc_1.tidl -o ./src/generated/hal_device_display_stub_1 -n
tidlc -p -l C -i ./include/hal_device_led_ipc_1.tidl -o ./src/generated/hal_device_led_proxy_1 -n
tidlc -s -l C -i ./include/hal_device_led_ipc_1.tidl -o ./src/generated/hal_device_led_stub_1 -n
tidlc -p -l C -i ./include/hal_device_battery_ipc_1.tidl -o ./src/generated/hal_device_battery_proxy_1 -n
tidlc -s -l C -i ./include/hal_device_battery_ipc_1.tidl -o ./src/generated/hal_device_battery_stub_1 -n
tidlc -p -l C -i ./include/hal_device_bezel_ipc_1.tidl -o ./src/generated/hal_device_bezel_proxy_1 -n
tidlc -s -l C -i ./include/hal_device_bezel_ipc_1.tidl -o ./src/generated/hal_device_bezel_stub_1 -n
tidlc -p -l C -i ./include/hal_device_external_connection_ipc_1.tidl -o ./src/generated/hal_device_external_connection_proxy_1 -n
tidlc -s -l C -i ./include/hal_device_external_connection_ipc_1.tidl -o ./src/generated/hal_device_external_connection_stub_1 -n

%build
cp %{SOURCE1} .
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} \
		 -DMAJORVER=${MAJORVER} \
		 -DHALTEST=on

%__make %{?jobs:-j%jobs}

%install
mkdir -p %{buildroot}%{_sysconfdir}/hal
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/hal/
%make_install

%post
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

%postun
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_libdir}/hal/libhal-api-device.so*
%{_libdir}/hal/libhal-backend-service-device-display.so
%{_libdir}/hal/libhal-backend-service-device-led.so
%{_libdir}/hal/libhal-backend-service-device-battery.so
%{_libdir}/hal/libhal-backend-service-device-bezel.so
%{_libdir}/hal/libhal-backend-service-device-external-connection.so
%{_sysconfdir}/hal/hal-api-device-manifest.xml

%files devel
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_includedir}/hal/hal-*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/hal/libhal-api-device.so

%files haltests
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_bindir}/hal/device-haltests
