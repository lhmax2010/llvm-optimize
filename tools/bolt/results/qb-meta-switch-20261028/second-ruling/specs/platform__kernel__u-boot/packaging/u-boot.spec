Name: u-boot
Version: 2025.10
Release: 0
Summary: Das U-Boot - Tizen bootloader
Group: System/Kernel
License: GPL-2.0+
ExclusiveArch: %{arm}
URL: https://source.denx.de/u-boot/u-boot.git
Source0: %{name}-%{version}.tar.bz2
Source1001: u_boot_rpi4.manifest

BuildRequires: gcc >= 6.0
BuildRequires: bc
BuildRequires: flex
BuildRequires: bison
BuildRequires: pkgconfig(openssl3)

%description
u-boot - Tizen bootloader for Embedded boards based on ARM processor

%package -n u-boot-rpi4-32b
Summary: Das U-Boot bootloader - Tizen RPi4 bootloader
Group: System/Kernel

%description -n u-boot-rpi4-32b
u-boot - Tizen bootloader for RPI4 boards based

%package -n u-boot-tools
Summary: Companion tools for Das U-Boot bootloader
Group: System/Kernel

%description -n u-boot-tools
This package includes the mkimage program, which allows generation of U-Boot
images in various formats, and the fw_printenv and fw_setenv programs to read
and modify U-Boot's environment.

%prep
%setup -q -n u-boot-%{version}

%build
%{?asan:/usr/bin/gcc-unforce-options}
cp %{SOURCE1001} .

CONFIG=tizen_rpi_4_32b_defconfig

make mrproper

# Set configuration
make $CONFIG

%if "%{?dev_sel}" == "1"
sed -i 's/^tizen_bootarg=.*/& selinux=1 enforcing=0/' board/raspberrypi/rpi/tizen_rpi.env
%endif

# Build tools
make %{?_smp_mflags} HOSTCC="%{__cc} $RPM_OPT_FLAGS" HOSTSTRIP=/bin/true tools
make HOSTCC="%{__cc} $RPM_OPT_FLAGS" envtools

# Build u-boot
export PATH="$PATH:tools"
make %{?_smp_mflags} EXTRAVERSION=`echo %{vcs} | sed 's/.*u-boot.*#\(.\{9\}\).*/-g\1-TIZEN.org/'`

# Generate uboot.env
./scripts/get_default_envs.sh > default_envs.txt
mkenvimage -s 16384 -o uboot.env default_envs.txt
rm default_envs.txt

# Build boot.scr
%if 0%{?asan} == 1
mkimage -A arm -T script -C none -n "Tizen RPI4 u-boot helper (ASAN)" -d ./tizen/bootscript/tizen-boot-rpi4.scr.asan ./boot.scr.uimg
%else
mkimage -A arm -T script -C none -n "Tizen RPI4 u-boot helper" -d ./tizen/bootscript/tizen-boot-rpi4.scr ./boot.scr.uimg
%endif

%install
rm -rf %{buildroot}

# Tools installation
mkdir -p %{buildroot}%{_bindir}
install -p -m 0755 tools/mkimage %{buildroot}%{_bindir}
install -p -m 0755 tools/env/fw_printenv %{buildroot}%{_bindir}
install -p -m 0755 scripts/dtc/dtc %{buildroot}%{_bindir}
( cd %{buildroot}%{_bindir}; ln -sf fw_printenv fw_setenv )

# u-boot installation
mkdir -p %{buildroot}/boot
install -m 755 u-boot.bin %{buildroot}/boot/
install -m 755 uboot.env %{buildroot}/boot/
install -m 755 boot.scr.uimg %{buildroot}/boot/

%clean

%files -n u-boot-rpi4-32b
%manifest u_boot_rpi4.manifest
%defattr(-,root,root,-)
/boot/u-boot.bin
/boot/uboot.env
/boot/boot.scr.uimg

%files -n u-boot-tools
%manifest u_boot_rpi4.manifest
%defattr(-,root,root,-)
%{_bindir}/mkimage
%{_bindir}/fw_printenv
%{_bindir}/fw_setenv
%{_bindir}/dtc
