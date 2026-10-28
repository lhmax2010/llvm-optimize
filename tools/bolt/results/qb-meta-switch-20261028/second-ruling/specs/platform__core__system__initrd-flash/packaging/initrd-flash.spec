Name:       initrd-flash
Summary:    Advanced flash-manager, package for building ramdisk-recovery.img
Version:    0.0.13
Release:    0
Group:      System/Utilities
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
ExclusiveArch: %{arm} aarch64 riscv64
BuildRequires: cmake
BuildRequires: libblkid-devel
BuildRequires: pkgconfig(libusbgx)
BuildRequires: pkgconfig(hal-api-device)

Requires: util-linux
Requires: /bin/sh
Requires: initrd-recovery
Requires: module-init-tools
Requires: libusbgx

%description
Provide kernel-based target image downloader.
This package would be included in partition image for RAMDISK2 (ramdisk-recovery.img)

%package test
Summary:    Test package for initrd-flash
Group:      Development/Tools
Requires:   initrd-flash

%description test
Test package for initrd-flash that provides a safe testing environment
without affecting real partitions. Includes test server and client programs
for testing THOR protocol functionality.

%define init_script_dir %{_libdir}/initrd-recovery/flash
%define initrd_recovery_install_dropin_dir %{_datadir}/initrd-recovery/initrd.list.d

%prep
%setup -q

%build

%cmake . --no-warn-unused-cli \
	 -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	 -DINITRD_FLASH_VERSION=%{version} \
	 -DINITRD_FLASH_LIBEXEC_DIR=%{init_script_dir} \
	 -DINITRD_FLASH_PARTITION_DATA_DIR=%{_hal_datadir} \
	 -DINITRD_FLASH_HAL_LIB_DIR=%{_hal_libdir} \
	 -DINITRD_RECOVERY_INSTALL_DROPIN_DIR=%{initrd_recovery_install_dropin_dir}

make %{?jobs:-j%jobs}

%install

%make_install

%post

%postun

%files
%manifest initrd-flash.manifest
%license LICENSE
%attr(775,root,root) %{_bindir}/flash-manager
%attr(775,root,root) %{init_script_dir}/*.sh
%{initrd_recovery_install_dropin_dir}/*.list

%files test
%manifest initrd-flash.manifest
%attr(775,root,root) %{_bindir}/tfm-test-server
%attr(775,root,root) %{_bindir}/tfm-test-client
%{_datadir}/initrd-flash-test/partition_test.info
%{_datadir}/initrd-flash-test/partition_test.info.old
%{_datadir}/initrd-flash-test/test.ext4
