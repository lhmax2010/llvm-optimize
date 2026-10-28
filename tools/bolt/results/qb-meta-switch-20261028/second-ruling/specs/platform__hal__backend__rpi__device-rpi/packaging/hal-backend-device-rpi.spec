Name:       hal-backend-device-rpi
Summary:    Device HAL backend drivers for rpi targets
Version:    0.0.1
Release:    0
Group:      System/Hardware Adaptation
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
ExclusiveArch:  %{arm} aarch64
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
Device HAL backend drivers for Raspberry Pi targets

%package -n hal-backend-device-rpi3
Summary: Additional device HAL backend drivers for RPi3
Conflicts: hal-backend-device-rpi4

%description -n hal-backend-device-rpi3
Additional device HAL backend drivers for Raspberry Pi 3

%package -n hal-backend-device-rpi4
Summary: Additional device HAL backend drivers for RPi4
Conflicts: hal-backend-device-rpi3

%description -n hal-backend-device-rpi4
Additional device HAL backend drivers for Raspberry Pi 4

%prep
%setup -q
cp %{SOURCE1} .

%build
%cmake . -DENABLE_DLOG=on \
	-DHAL_LICENSE_DIR=%{_hal_licensedir} \
	-DHAL_LIB_DIR=%{_hal_libdir}

make %{?jobs:-j%jobs}

%install
%make_install

# install conf files
mkdir -p %{buildroot}%{_hal_sysconfdir}/deviced
install -m 644 conf/*.conf %{buildroot}%{_hal_sysconfdir}/deviced

# Reboot register storage
install -D -m 644 hw/reboot/register_storage %{buildroot}%{_hal_sysconfdir}/reboot/register_storage

# peripheral-io ini file
mkdir -p %{buildroot}%{_hal_sysconfdir}/peripheral-io
mkdir %{buildroot}%{_hal_sysconfdir}/peripheral-io/rpi3
mkdir %{buildroot}%{_hal_sysconfdir}/peripheral-io/rpi4
install -m 644  hw/peripheral-io/*.ini %{buildroot}%{_hal_sysconfdir}/peripheral-io
install -m 644  hw/peripheral-io/rpi3/*.ini %{buildroot}%{_hal_sysconfdir}/peripheral-io/rpi3
install -m 644  hw/peripheral-io/rpi4/*.ini %{buildroot}%{_hal_sysconfdir}/peripheral-io/rpi4

# background_copy.list
mkdir -p %{buildroot}%{_hal_sysconfdir}/upgrade
install -m 644 hw/upgrade/* %{buildroot}%{_hal_sysconfdir}/upgrade


%post
/sbin/ldconfig
systemd-tmpfiles /hal/lib/tmpfiles.d/hal-backend-device-rpi.conf --create

%postun
/sbin/ldconfig

%post -n hal-backend-device-rpi3
mv %{_hal_sysconfdir}/peripheral-io/rpi3/gpio.ini %{_hal_sysconfdir}/peripheral-io/
rmdir %{_hal_sysconfdir}/peripheral-io/rpi3

ln -sf libhal-backend-device-display.rpi3.so %{_hal_libdir}/libhal-backend-device-display.so

%post -n hal-backend-device-rpi4
mv %{_hal_sysconfdir}/peripheral-io/rpi4/gpio.ini %{_hal_sysconfdir}/peripheral-io/
rmdir %{_hal_sysconfdir}/peripheral-io/rpi4

ln -sf libhal-backend-device-display.rpi4.so %{_hal_libdir}/libhal-backend-device-display.so

%files
%{_hal_libdir}/libhal-backend-device-board.so
%{_hal_libdir}/libhal-backend-device-haptic.so
%{_hal_libdir}/libhal-backend-device-led.so
%{_hal_libdir}/libhal-backend-device-memory.so
%{_hal_libdir}/libhal-backend-device-thermal.so
%{_hal_libdir}/libhal-backend-device-touchscreen.so
%{_hal_sysconfdir}/reboot/register_storage
%{_hal_sysconfdir}/peripheral-io/*.ini
%{_hal_sysconfdir}/deviced/*
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.Apache-2.0

%files -n hal-backend-device-rpi3
%dir %{_hal_sysconfdir}/peripheral-io/rpi3
%{_hal_sysconfdir}/peripheral-io/rpi3/gpio.ini
%{_hal_libdir}/libhal-backend-device-display.rpi3.so

%files -n hal-backend-device-rpi4
%dir %{_hal_sysconfdir}/peripheral-io/rpi4
%{_hal_sysconfdir}/peripheral-io/rpi4/gpio.ini
%{_hal_sysconfdir}/upgrade/*
%{_hal_libdir}/libhal-backend-device-display.rpi4.so
/hal/lib/tmpfiles.d/hal-backend-device-rpi.conf
