Name:           linux-firmware
Version:        20141009
Release:        1
Summary:        Firmware for various devices

License:        Redistributable, no modification permitted
Url:            ftp://ftp.kernel.org//pub/linux/kernel/people/dwmw2/firmware/
Group:          System/Kernel
Source0:        ftp://ftp.kernel.org//pub/linux/kernel/people/dwmw2/firmware/linux-firmware-%{version}.tar.bz2
Source1001: 	linux-firmware.manifest
BuildRequires:  fdupes
BuildArch:      noarch

%description
This package contains the firmware required by various devices

%package ivi
Summary:	Firmware files for Tizen IVI platform drivers
Conflicts:	linux-firmware

%description ivi
Firmware files for Tizen IVI platform drivers

%prep
%setup -q
cp %{SOURCE1001} .
find . -type f -exec chmod 0644 {} ';'

%build
# Nothing to build


%install
mkdir -p %{buildroot}/lib/firmware
cp -a * %{buildroot}/lib/firmware/

%fdupes %{buildroot}/lib/firmware

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
/lib/firmware/*

%files ivi
%manifest %{name}.manifest
# NOTE: make sure all the firmware we use in this RPM is documented in
# the 'ivi-firmware.txt' file.
/lib/firmware/iwlwifi-6000g2b-6.ucode
/lib/firmware/iwlwifi-7260-9.ucode
/lib/firmware/iwlwifi-3160-9.ucode
/lib/firmware/intel/ibt-hw-37.7.10-fw-1.80.2.3.d.bseq
/lib/firmware/intel/ibt-hw-37.7.bseq
/lib/firmware/LICENCE.ibt_firmware
/lib/firmware/LICENCE.iwlwifi_firmware
/lib/firmware/v4l-cx23885-avcore-01.fw
/lib/firmware/rtl_nic/rtl8168g-2.fw
