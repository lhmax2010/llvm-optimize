Name: u-boot-rubikpi3
Version: 2025.10
Release: 0
Summary: Das U-Boot - Tizen bootloader
Group: System/Kernel
License: GPL-2.0+
ExclusiveArch: aarch64
URL: https://source.denx.de/u-boot/u-boot.git
Source0: u-boot-%{version}.tar.bz2
Source1001: u_boot_rubikpi3.manifest

BuildRequires: gcc >= 6.0
BuildRequires: bc
BuildRequires: flex
BuildRequires: bison
BuildRequires: pkgconfig(openssl3)
BuildRequires: python3
BuildRequires: python3-asn1crypto
BuildRequires: python3-cffi
BuildRequires: python3-cryptography
BuildRequires: python3-idna
BuildRequires: python3-six
BuildRequires: vim

%description
u-boot - Tizen bootloader for RubikPi3 boards

%prep
%setup -q -n u-boot-%{version}

%build
%{?asan:/usr/bin/gcc-unforce-options}
cp %{SOURCE1001} .

CONFIG=qcm6490_rubikpi3_defconfig

make mrproper

# Set configuration
make $CONFIG

# Build tools
make %{?_smp_mflags} HOSTCC="%{__cc} $RPM_OPT_FLAGS" HOSTSTRIP=/bin/true tools

make HOSTCC="%{__cc} $RPM_OPT_FLAGS" envtools

# Build u-boot
export PATH="$PATH:tools"
make %{?_smp_mflags} EXTRAVERSION=`echo %{vcs} | sed 's/.*u-boot.*#\(.\{9\}\).*/-g\1-TIZEN.org/'` u-boot.elf
./vendor/qtestsign/qtestsign.py -v6 hyp -o u-boot.mbn u-boot.elf

%install
rm -rf %{buildroot}

# u-boot installation
mkdir -p %{buildroot}/var/tmp/rubikpi3
install -m 755 u-boot.mbn %{buildroot}/var/tmp/rubikpi3

%clean

%files
%manifest u_boot_rubikpi3.manifest
%defattr(-,root,root,-)
/var/tmp/rubikpi3/u-boot.mbn
