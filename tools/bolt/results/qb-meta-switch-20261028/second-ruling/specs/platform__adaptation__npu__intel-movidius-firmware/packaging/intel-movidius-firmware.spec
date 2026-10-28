Name:		intel-movidius-firmware
Summary:	A collection of Intel Movidius NCS firmware
Version:	1.0.0
Release:	0
Group:		System Environment/Libraries
License:	ISSL
Packager:	MyungJoo Ham <myungjoo.ham@samsung.com>
Source0:	%{name}-%{version}.tar.gz
Source1000:	%{name}.manifest
URL:		https://download.01.org/opencv/2019/openvinotoolkit/R3/inference_engine/
BuildArch:	noarch

%define FIRMWARE_PATH	%{_libdir}/mvnc

%description
A collection of Intel Movidius firmware for Tizen

%prep
%setup -q
cp %{SOURCE1000} .

%build
#Nothing to do

%install
mkdir -p %{buildroot}%{FIRMWARE_PATH}
install -m 0644 ma2450_784/MvNCAPI-ma2450.mvcmd %{buildroot}%{FIRMWARE_PATH}/
install -m 0644 ma2x8x_784/MvNCAPI-ma2x8x.mvcmd %{buildroot}%{FIRMWARE_PATH}/
pushd %{buildroot}%{_libdir}
ln -s ./mvnc/MvNCAPI-ma2450.mvcmd
ln -s ./mvnc/MvNCAPI-ma2x8x.mvcmd
popd

%package ma2450
Summary:		Intel Movidius 2450 Firmware
Version:		784
Provides:		mvnc-2450-firmware
Provides:		intel-mvnc-firmware

%description ma2450
Intel Movidius MA2450 firmware for Tizen
This is from https://download.01.org/opencv/2019/openvinotoolkit/R3/inference_engine/

%files ma2450
%manifest %{name}.manifest
%{FIRMWARE_PATH}/MvNCAPI-ma2450.mvcmd
%{_libdir}/MvNCAPI-ma2450.mvcmd
%license LICENSE

%package ma2x8x
Summary:		Intel Movidius 2x8x Firmware
Version:		784
Provides:		mvnc-2x8x-firmware
Provides:		intel-mvnc-firmware

%description ma2x8x
Intel Movidius MA2x8x firmware for Tizen
This is from https://download.01.org/opencv/2019/openvinotoolkit/R3/inference_engine/

%files ma2x8x
%manifest %{name}.manifest
%{FIRMWARE_PATH}/MvNCAPI-ma2x8x.mvcmd
%{_libdir}/MvNCAPI-ma2x8x.mvcmd
%license LICENSE

%changelog
* Thu Aug 13 2020 Wook Song <wook16.song@samsung.com>
- Include symbolic links to the firmware files of %{FIRMWARE_PATH} in %{_libdir}

* Tue Jun 14 2020 Wook Song <wook16.song@samsung.com>
- Add a sub-package for MA2x8x (Intel NCS2) firmware

* Wed Nov 13 2019 MyungJoo Ham <myungjoo.ham@samsung.com>
- Initial commit with MV2450 firmware
