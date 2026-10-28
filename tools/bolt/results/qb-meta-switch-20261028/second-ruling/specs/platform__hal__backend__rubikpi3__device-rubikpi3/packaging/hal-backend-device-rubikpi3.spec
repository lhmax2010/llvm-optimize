Name:           hal-backend-device-rubikpi3
Summary:        Device HAL backend drivers for QCS6490 & QCS5430
Group  :        System/Hardware Adaptation
Version:        1.0
Release:        0
ExclusiveArch:  aarch64
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

AutoReqProv:    no

%description
Device HAL backend drivers for QCS6490 (Rubik Pi 3) & QCS5430 (RB3 Gen2 Lite)

%prep
%setup -q
cp %{SOURCE1} .

%build
%cmake . -DENABLE_DLOG=on \
	-DHAL_LICENSE_DIR=%{_hal_licensedir} \
	-DHAL_LIB_DIR=%{_hal_libdir}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/hal

# Copy all regular files to /hal
cp -a hal/* %{buildroot}/hal

# hal-backend-device-rubikpi3 symlinks
mkdir -p %{buildroot}/hal/lib/firmware/brcm
mkdir -p %{buildroot}/hal/lib64/driver

# Symlinks to DSP-related files from /vendor
ln -sf "/vendor/usr/lib/dsp" "%{buildroot}/hal/lib64/dsp"

# Symlinks to firmware from /vendor
ln -sf "/vendor/usr/lib/firmware/a660_gmu.bin" "%{buildroot}/hal/lib/firmware/a660_gmu.bin"
ln -sf "/vendor/usr/lib/firmware/a660_sqe.fw" "%{buildroot}/hal/lib/firmware/a660_sqe.fw"
ln -sf "/vendor/usr/lib/firmware/a660_zap.b00" "%{buildroot}/hal/lib/firmware/a660_zap.b00"
ln -sf "/vendor/usr/lib/firmware/a660_zap.b01" "%{buildroot}/hal/lib/firmware/a660_zap.b01"
ln -sf "/vendor/usr/lib/firmware/a660_zap.b02" "%{buildroot}/hal/lib/firmware/a660_zap.b02"
ln -sf "/vendor/usr/lib/firmware/a660_zap.mbn" "%{buildroot}/hal/lib/firmware/a660_zap.mbn"
ln -sf "/vendor/usr/lib/firmware/a660_zap.mdt" "%{buildroot}/hal/lib/firmware/a660_zap.mdt"
ln -sf "/vendor/usr/lib/firmware/ath11k" "%{buildroot}/hal/lib/firmware/ath11k"
ln -sf "/vendor/usr/lib/firmware/aw882xx_acf.bin" "%{buildroot}/hal/lib/firmware/aw882xx_acf.bin"
ln -sf "/vendor/usr/lib/firmware/BCM4345C5_003.006.006.1081.1154.hcd" "%{buildroot}/hal/lib/firmware/BCM4345C5_003.006.006.1081.1154.hcd"
ln -sf "/vendor/usr/lib/firmware/CAMERA_ICP_170.elf" "%{buildroot}/hal/lib/firmware/CAMERA_ICP_170.elf"
ln -sf "/vendor/usr/lib/firmware/config.txt" "%{buildroot}/hal/lib/firmware/config.txt"
ln -sf "/vendor/usr/lib/firmware/fw_bcm43456c5_ag.bin" "%{buildroot}/hal/lib/firmware/fw_bcm43456c5_ag.bin"
ln -sf "/vendor/usr/lib/firmware/LICENSE" "%{buildroot}/hal/lib/firmware/LICENSE"
ln -sf "/vendor/usr/lib/firmware/lt9611uxc_fw.bin" "%{buildroot}/hal/lib/firmware/lt9611uxc_fw.bin"
ln -sf "/vendor/usr/lib/firmware/nvram.txt" "%{buildroot}/hal/lib/firmware/nvram.txt"
ln -sf "/vendor/usr/lib/firmware/qcacld" "%{buildroot}/hal/lib/firmware/qcacld"
ln -sf "/vendor/usr/lib/firmware/qcom" "%{buildroot}/hal/lib/firmware/qcom"
ln -sf "/vendor/usr/lib/firmware/regulatory.db" "%{buildroot}/hal/lib/firmware/regulatory.db"
ln -sf "/vendor/usr/lib/firmware/regulatory.db.p7s" "%{buildroot}/hal/lib/firmware/regulatory.db.p7s"
ln -sf "/vendor/usr/lib/firmware/renesas_usb_fw.mem" "%{buildroot}/hal/lib/firmware/renesas_usb_fw.mem"
ln -sf "/vendor/usr/lib/firmware/sduart8987_combo.bin" "%{buildroot}/hal/lib/firmware/sduart8987_combo.bin"
ln -sf "/vendor/usr/lib/firmware/TC956X_Firmware_PCIeBridge.bin" "%{buildroot}/hal/lib/firmware/TC956X_Firmware_PCIeBridge.bin"
ln -sf "/vendor/usr/lib/firmware/updates" "%{buildroot}/hal/lib/firmware/updates"
ln -sf "/vendor/usr/lib/firmware/wlan" "%{buildroot}/hal/lib/firmware/wlan"

ln -sf "../BCM4345C5_003.006.006.1081.1154.hcd" "%{buildroot}/hal/lib/firmware/brcm/BCM4345C5.hcd"

# Symlinks to GL-related files from /vendor
ln -sf /vendor/usr/lib/libEGL.so %{buildroot}/hal/lib64/driver/libEGL.so
ln -sf /vendor/usr/lib/libGLESv2.so %{buildroot}/hal/lib64/driver/libGLESv2.so

# Licenses
mkdir -p %{buildroot}/%{_hal_licensedir}/%{name}
cp LICENSE %{buildroot}/%{_hal_licensedir}/%{name}
%post
/sbin/ldconfig
systemd-tmpfiles /hal/lib/tmpfiles.d/hal-backend-device-rubikpi3.conf --create

%postun
/sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_hal_libdir}/libhal-backend-device-board.so
%{_hal_libdir}/libhal-backend-device-thermal.so
%{_hal_libdir}/libhal-backend-device-display.so
/hal/lib/tmpfiles.d/hal-backend-device-rubikpi3.conf
%{_hal_licensedir}/%{name}/LICENSE
/hal/lib/tmpfiles.d/hal-backend-device-rubikpi3.conf
/hal/etc/udev/rules.d/*
/hal/lib/firmware/*
/hal/lib64/driver/*
/hal/lib64/dsp
/hal/share/vulkan/icd.d/adrenovk.json
