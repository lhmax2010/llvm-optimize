Name:       hal-backend-sensor-rpi
Summary:    Sensor HAL backend drivers for RPI targets
Version:    1.0.4
Release:    0
Group:      System/Sensor Framework
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
ExclusiveArch:  %{arm} aarch64

BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
Sensor HAL backend drivers for RPI targets

%prep
%setup -q

%build
%cmake . -DCMAKE_HAL_LIBDIR_PREFIX=%{_hal_libdir} -DCMAKE_HAL_LICENSEDIR_PREFIX=%{_hal_licensedir}
make %{?_smp_mflags}

%install
%make_install

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest packaging/%{name}.manifest
%{_hal_libdir}/libhal-backend-sensor-*.so*
%{_hal_licensedir}/%{name}/LICENSE.Apache-2.0
