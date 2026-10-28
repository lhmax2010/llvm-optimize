Name:       hal-backend-sensor-emulator
Summary:    Sensor HAL backend drivers for emulator targets
Version:    1.0.4
Release:    0
Group:      System/Sensor Framework
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    99-sensor.rules
Source2:    99-sensorhub.rules

ExcludeArch: %{arm} riscv64

BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
Sensor HAL backend drivers for emulator targets

%prep
%setup -q

%build
%cmake . -DCMAKE_HAL_LIBDIR_PREFIX=%{_hal_libdir} -DCMAKE_HAL_LICENSEDIR_PREFIX=%{_hal_licensedir}
make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}/hal/lib/udev/rules.d

install -m 0644 %SOURCE1 %{buildroot}/hal/lib/udev/rules.d
install -m 0644 %SOURCE2 %{buildroot}/hal/lib/udev/rules.d

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest packaging/%{name}.manifest
/hal/lib/udev/rules.d/99-sensor.rules
/hal/lib/udev/rules.d/99-sensorhub.rules
%{_hal_libdir}/*.so*
%{_hal_licensedir}/%{name}/LICENSE.APLv2
