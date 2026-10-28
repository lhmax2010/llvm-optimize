Name:      bluetooth-firmware-bcm
Summary:    firmware and tools for bluetooth
Version:    0.10.0
Release:    1
Group:      Hardware Support/Handset
License:    Apache-2.0 and Broadcom
# NOTE: Source name does not match package name.  This should be
# resolved in the future, by I don't have that power. - Ryan Ware
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)

%description
 firmware and tools for bluetooth

%package exynos3250
Summary:    bcm firmware and tools for exynos3250
Group:      Hardware Support/Handset

%description exynos3250
bcm firmware and tools for exynos3250

%package artik
Summary:    bcm firmware and tools for artik
Group:      Hardware Support/Handset

%description artik
bcm firmware and tools for artik

%package exynos7270
Summary:    bcm firmware and tools for exynos7270
Group:      Hardware Support/Handset

%description exynos7270
BT firmware and tools for exynos7270

%package rpi3
Summary:    bcm firmware and tools for rpi3
Group:      Hardware Support/Handset

%description rpi3
BT firmware and tools for rpi3

%prep
%setup -q

%build
cmake ./ -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DPLUGIN_INSTALL_PREFIX=%{_prefix} \
	-DHAL_LIB_DIR=%{_hal_libdir} \
	-DHAL_LICENSE_DIR=%{_hal_licensedir} \
	-DHAL_SYSCONF_DIR=%{_hal_sysconfdir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%files
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.APLv2
%{_hal_licensedir}/%{name}/LICENSE.Broadcom
#%{_hal_sysconfdir}/bluetooth/bcmtool_4330b1
%exclude %{_hal_sysconfdir}/bluetooth/bcmtool_4343w
%{_hal_sysconfdir}/bluetooth/bcmtool_4358a1
%{_hal_sysconfdir}/bluetooth/setbd
#%{_hal_sysconfdir}/bluetooth/BT_FW_BCM4330B1_002.001.003.0221.0265.hcd
%{_hal_sysconfdir}/bluetooth/BT_FW_BCM4358A1_001.002.005.0032.0066.hcd
%{_hal_sysconfdir}/bluetooth/bt-dev-end.sh
%{_hal_sysconfdir}/bluetooth/bt-dev-start.sh
%{_hal_sysconfdir}/bluetooth/bt-set-addr.sh

%post exynos3250
rm -rf %{_hal_sysconfdir}/bluetooth/bt-dev-start.sh
ln -s %{_hal_sysconfdir}/bluetooth/bt-dev-start-exynos3250.sh %{_hal_sysconfdir}/bluetooth/bt-dev-start.sh

%files exynos3250
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.APLv2
%{_hal_licensedir}/%{name}/LICENSE.Broadcom
%{_hal_sysconfdir}/bluetooth/bcmtool_4343w
%{_hal_sysconfdir}/bluetooth/setbd
%{_hal_sysconfdir}/bluetooth/BCM4343A1_001.002.009.0035.0096_ORC_Orbis_WC1-S.hcd
%{_hal_sysconfdir}/bluetooth/BCM4343A1_001.002.009.0022.0050_Murata_Type-1FR.hcd
%{_hal_sysconfdir}/bluetooth/bt-dev-end.sh
%{_hal_sysconfdir}/bluetooth/bt-dev-start-exynos3250.sh
%{_hal_sysconfdir}/bluetooth/bt-set-addr.sh

%post artik
rm -rf %{_hal_sysconfdir}/bluetooth/bt-dev-start.sh
ln -s %{_hal_sysconfdir}/bluetooth/bt-dev-start-artik.sh %{_hal_sysconfdir}/bluetooth/bt-dev-start.sh

%files artik
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.APLv2
%{_hal_licensedir}/%{name}/LICENSE.Broadcom
%{_hal_sysconfdir}/bluetooth/brcm_patchram_plus
%{_hal_sysconfdir}/bluetooth/setbd
%{_hal_sysconfdir}/bluetooth/BCM4354_003.001.012.0353.0745_Samsung_Artik_ORC.hcd
%{_hal_sysconfdir}/bluetooth/BCM4345C0_003.001.025.0111.0205.hcd
%{_hal_sysconfdir}/bluetooth/bt-dev-end.sh
%{_hal_sysconfdir}/bluetooth/bt-dev-start-artik.sh
%{_hal_sysconfdir}/bluetooth/bt-set-addr.sh

%post exynos7270
rm -rf %{_hal_sysconfdir}/bluetooth/bt-dev-start.sh
ln -s %{_hal_sysconfdir}/bluetooth/bt-dev-start-exynos7270.sh %{_hal_sysconfdir}/bluetooth/bt-dev-start.sh
rm -rf %{_hal_libdir}/firmware/43012B0.hex
ln -s %{_hal_libdir}/firmware/bcm43012/BCM43012B0_002.001.021.0081.0087.hex %{_hal_libdir}/firmware/43012B0.hex

%files exynos7270
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.APLv2
%{_hal_licensedir}/%{name}/LICENSE.Broadcom
%{_hal_sysconfdir}/bluetooth/setbd
%{_hal_libdir}/firmware/bcm43012/BCM43012B0_002.001.021.0081.0087.hex
%{_hal_sysconfdir}/bluetooth/bt-dev-end.sh
%{_hal_sysconfdir}/bluetooth/bt-dev-start-exynos7270.sh
%{_hal_sysconfdir}/bluetooth/bt-set-addr.sh

%post rpi3
rm -rf %{_hal_sysconfdir}/bluetooth/bt-dev-start.sh
rm -rf %{_hal_sysconfdir}/bluetooth/bt-dev-end.sh
ln -s %{_hal_sysconfdir}/bluetooth/bt-dev-start-rpi3.sh %{_hal_sysconfdir}/bluetooth/bt-dev-start.sh
ln -s %{_hal_sysconfdir}/bluetooth/bt-dev-end-rpi3.sh %{_hal_sysconfdir}/bluetooth/bt-dev-end.sh
mkdir -p %{_hal_libdir}/firmware/brcm
ln -s %{_hal_sysconfdir}/bluetooth/BCM43430A1.hcd %{_hal_libdir}/firmware/brcm/
ln -s %{_hal_sysconfdir}/bluetooth/BCM4345C0.hcd %{_hal_libdir}/firmware/brcm/

%files rpi3
%manifest %{name}.manifest
%{_hal_licensedir}/%{name}/LICENSE.APLv2
%{_hal_licensedir}/%{name}/LICENSE.Broadcom
%{_hal_sysconfdir}/bluetooth/BCM43430A1.hcd
%{_hal_sysconfdir}/bluetooth/BCM4345C0.hcd
%{_hal_sysconfdir}/bluetooth/bt-dev-end-rpi3.sh
%{_hal_sysconfdir}/bluetooth/bt-dev-start-rpi3.sh
%{_hal_libdir}/*.so*
