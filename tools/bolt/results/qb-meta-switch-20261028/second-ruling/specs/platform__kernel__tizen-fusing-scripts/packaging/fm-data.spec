Name:       fm-data
Summary:    Partition data files for flash manager
Version:    0.0.1
Release:    0
Group:      System/Utilities
License:    MIT
Source0:    %{name}-%{version}.tar.gz
ExclusiveArch: %{arm} aarch64 riscv64

%description
Partition data files for flash manager. This package provides partition
information files for various target boards.

%ifarch %{arm} aarch64
%package rpi3
Summary:	RaspberryPi3 specific data for flash manager
Group:		System/Utilities
Provides:	fm-data

%description rpi3
Provide flash-manager with partition table for flashing image and files of Raspberry Pi 3 board

%package rpi4
Summary:	RaspberryPi4 specific data for flash manager
Group:		System/Utilities
Provides:	fm-data

%description rpi4
Provide flash-manager with partition table for flashing image and files of Raspberry Pi 4 board

%package orinnano
summary:	OrinNano specific data for flash manager
group:		system/utilities
provides:	fm-data

%description orinnano
provide flash-manager with partition table for flashing image and files of Jetson Orin Nano board
%endif

%package generic
Summary:	Generic Image data for flash manager
Group:		System/Utilities
Provides:	fm-data

%description generic
Provide flash-manager with partition table for flashing image and files of common board

%ifarch riscv64
%package visionfive2
Summary:	Visionfive2 specific data for flash manager
Group:		System/Utilities
Provides:	fm-data

%description visionfive2
Provide flash-manager with partition table for flashing image and files of Visionfive2 board

%package lpi4a
Summary:	lpi-4a specific data for flash manager
Group:		System/Utilities
Provides:	fm-data

%description lpi4a
Provide flash-manager with partition table for flashing image and files of lpi-4a board

%package bpif3
Summary:	bpi-f3 specific data for flash manager
Group:		System/Utilities
Provides:	fm-data

%description bpif3
Provide flash-manager with partition table for flashing image and files of bpi-f3 board
%endif

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_hal_licensedir}/fm-data
cp ./LICENSE.MIT %{buildroot}%{_hal_licensedir}/fm-data/

mkdir -p %{buildroot}%{_hal_datadir}
%ifarch %{arm} aarch64
cp ./data/partition_rpi3.info %{buildroot}%{_hal_datadir}/
cp ./data/partition_rpi4.info %{buildroot}%{_hal_datadir}/
cp ./data/partition_orinnano.info %{buildroot}%{_hal_datadir}/
%endif
cp ./data/partition_generic.info %{buildroot}%{_hal_datadir}/
%ifarch riscv64
cp ./data/partition_visionfive2.info %{buildroot}%{_hal_datadir}/
cp ./data/partition_lpi4a.info %{buildroot}%{_hal_datadir}/
cp ./data/partition_bpif3.info %{buildroot}%{_hal_datadir}/
%endif

%ifarch %{arm} aarch64
%post rpi3
mv %{_hal_datadir}/partition_rpi3.info %{_hal_datadir}/partition.info

%post rpi4
mv %{_hal_datadir}/partition_rpi4.info %{_hal_datadir}/partition.info

%post orinnano
mv %{_hal_datadir}/partition_orinnano.info %{_hal_datadir}/partition.info
%endif

%post generic
mv %{_hal_datadir}/partition_generic.info %{_hal_datadir}/partition.info

%ifarch riscv64
%post visionfive2
mv %{_hal_datadir}/partition_visionfive2.info %{_hal_datadir}/partition.info

%post lpi4a
mv %{_hal_datadir}/partition_lpi4a.info %{_hal_datadir}/partition.info

%post bpif3
mv %{_hal_datadir}/partition_bpif3.info %{_hal_datadir}/partition.info
%endif

%ifarch %{arm} aarch64
%postun rpi3
rm -f %{_hal_datadir}/partition.info

%postun rpi4
rm -f %{_hal_datadir}/partition.info

%postun orinnano
rm -f %{_hal_datadir}/partition.info
%endif

%postun generic
rm -f %{_hal_datadir}/partition.info

%ifarch riscv64
%postun visionfive2
rm -f %{_hal_datadir}/partition.info

%postun lpi4a
rm -f %{_hal_datadir}/partition.info

%postun bpif3
rm -f %{_hal_datadir}/partition.info
%endif

%ifarch %{arm} aarch64
%files rpi3
%manifest packaging/fm-data.manifest
%{_hal_licensedir}/fm-data/LICENSE.MIT
%{_hal_datadir}/partition_rpi3.info

%files rpi4
%manifest packaging/fm-data.manifest
%{_hal_licensedir}/fm-data/LICENSE.MIT
%{_hal_datadir}/partition_rpi4.info

%files orinnano
%manifest packaging/fm-data.manifest
%{_hal_licensedir}/fm-data/LICENSE.MIT
%{_hal_datadir}/partition_orinnano.info
%endif

%files generic
%manifest packaging/fm-data.manifest
%{_hal_licensedir}/fm-data/LICENSE.MIT
%{_hal_datadir}/partition_generic.info

%ifarch riscv64
%files visionfive2
%manifest packaging/fm-data.manifest
%{_hal_licensedir}/fm-data/LICENSE.MIT
%{_hal_datadir}/partition_visionfive2.info

%files lpi4a
%manifest packaging/fm-data.manifest
%{_hal_licensedir}/fm-data/LICENSE.MIT
%{_hal_datadir}/partition_lpi4a.info

%files bpif3
%manifest packaging/fm-data.manifest
%{_hal_licensedir}/fm-data/LICENSE.MIT
%{_hal_datadir}/partition_bpif3.info
%endif
