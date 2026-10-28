# Ignore double dash in version for rpmbuild
%define _wrong_version_format_terminate_build 0

%ifarch aarch64
%define buildarch arm64
%define KERNEL_IMAGE Image.gz
%else
%define buildarch arm
%define KERNEL_IMAGE zImage
%endif

%define CHIPSET amlogic
%define TARGET_ODROIDS odroid
%define ODROIDS_DT_PREFIX meson64_odroid
%define TARGET_VIMS kvim
%define VIMS_DT_PREFIX kvim
%define TARGETS %{TARGET_ODROIDS} %{TARGET_VIMS}

Name: linux-amlogic
Summary: The Linux Kernel for amlogic boards
Version: 4.9.241
Release: 0
License: GPL-2.0
ExclusiveArch: %{arm} aarch64
Group: System/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source0: %{name}-%{version}.tar.xz

BuildRequires: bc
BuildRequires: module-init-tools
BuildRequires: bison
BuildRequires: flex
BuildRequires: pkgconfig(openssl3)
BuildRequires: rsync

%description
The Linux Kernel, the operating system core itself

## Start of Packages lists
# kernel-headers package for all amlogic targets both for arm and arm64
%package -n kernel-headers-amlogic
License: GPL-2.0
Summary: Linux support headers for amlogic userspace development
Group: System/Kernel
Provides: kernel-headers-tizen-dev
Provides: kernel-headers-amlogic-odroid = %{version}_%{CHIPSET}_odroid
Provides: kernel-headers-amlogic-kvim = %{version}_%{CHIPSET}_kvim

%description -n kernel-headers-amlogic
This package provides userspaces headers from the Linux kernel for Amlogic.
These headers are used by the installed headers for GNU glibc and other
system libraries.

# ARM64 Build result pagckages for each target
%ifarch aarch64
%package -n linux-kernel-amlogic-odroid
License: GPL-2.0
Summary: Tizen kernel for amlogic odroid boards
Group: System/Kernel
Provides: linux-amlogic-odroid = %{version}_%{CHIPSET}_odroid

%description -n linux-kernel-amlogic-odroid
This package contains the Tizen Linux kernel for amlogic odroid boards

%package -n linux-kernel-modules-amlogic-odroid
Summary: Kernel modules for amlogic odroid boards
Group: System/Kernel
Provides: linux-kernel-modules-amlogic-odroid = %{version}_%{CHIPSET}_odroid

%description -n linux-kernel-modules-amlogic-odroid
Kernel-modules includes the loadable kernel modules(.ko files) for amlogic odroid

%package -n linux-kernel-devel-amlogic-odroid
License: GPL-2.0
Summary: Linux support kernel map and etc for other packages
Group: System/Kernel
Provides: linux-kernel-devel-amlogic-odroid = %{version}_%{CHIPSET}_odroid

%description -n linux-kernel-devel-amlogic-odroid
This package provides kernel map and etc information.

%package -n linux-kernel-firmware-amlogic-odroid
License: GPL-2.0
Summary: firmware files for the amlogic Odroid Linux kernel
Group: System/Kernel

%description -n linux-kernel-firmware-amlogic-odroid
This package provides firmware files for the amlogic Odroid Linux kernel.

%package -n linux-kernel-amlogic-kvim
License: GPL-2.0
Summary: Tizen kernel for amlogic kadas vim3/vim3l boards
Group: System/Kernel
Provides: linux-amlogic-kvim = %{version}_%{CHIPSET}_kvim

%description -n linux-kernel-amlogic-kvim
This package contains the Tizen Linux kernel for amlogic khadas vim3/vim3l boards

%package -n linux-kernel-modules-amlogic-kvim
Summary: Kernel modules for amlogic khadas vim3/vim3l boards
Group: System/Kernel
Provides: linux-kernel-modules-amlogic-kvim = %{version}_%{CHIPSET}_kvim

%description -n linux-kernel-modules-amlogic-kvim
Kernel-modules includes the loadable kernel modules(.ko files) for amlogic khadas vim3/vim3l

%package -n linux-kernel-devel-amlogic-kvim
License: GPL-2.0
Summary: Linux support kernel map and etc for other packages
Group: System/Kernel
Provides: linux-kernel-devel-amlogic-kvim = %{version}_%{CHIPSET}_kvim

%description -n linux-kernel-devel-amlogic-kvim
This package provides kernel map and etc information.
%endif
## End of Packages lists

%prep
%setup -q

%build
%{?asan:/usr/bin/gcc-unforce-options}
%{?ubsan:/usr/bin/gcc-unforce-options}

## Start of Build steps

# Build for each target for arm64
%ifarch aarch64
for target_board in %{TARGETS}; do
	%define variant TIZEN-%{CHIPSET}-${target_board}

	mkdir -p %{_builddir}/build/${target_board}
	echo "-%{variant}" > %{_builddir}/build/${target_board}/localversion-tizen

	case $target_board in
	%{TARGET_ODROIDS})
		CONFIG_NAME=odroidg12
		DT_PREFIX=%{ODROIDS_DT_PREFIX}
	;;
	%{TARGET_VIMS})
		CONFIG_NAME=kvims
		DT_PREFIX=%{VIMS_DT_PREFIX}
	;;
	esac

	# Set defconfig file
	rm -f %{_builddir}/build/${target_board}/.config
	make O=%{_builddir}/build/${target_board} tizen_${CONFIG_NAME}_defconfig

	# Build kernel image, dtb and modules
	make O=%{_builddir}/build/${target_board} %{KERNEL_IMAGE} %{?_smp_mflags}
	make O=%{_builddir}/build/${target_board} dtbs %{?_smp_mflags}
	make O=%{_builddir}/build/${target_board} modules %{?_smp_mflags}
done
%endif
## End of Build steps

%install
## Start of install steps
QA_SKIP_BUILD_ROOT="DO_NOT_WANT"; export QA_SKIP_BUILD_ROOT

rm -f localversion*

# Install files for arm64

# Install uapi headers
make headers_install %{?_smp_mflags} INSTALL_HDR_PATH=%{buildroot}/usr
find %{buildroot}/usr \( -name .install -o -name ..install.cmd \) -delete
make mrproper

%ifarch aarch64
# Install files
for target_board in %{TARGETS}; do
	case $target_board in
	%{TARGET_ODROIDS})
		DT_PREFIX=%{ODROIDS_DT_PREFIX}
		;;
	%{TARGET_VIMS})
		DT_PREFIX=%{VIMS_DT_PREFIX}
		;;
	esac

	mkdir -p %{buildroot}/boot/${target_board}/kernel/devel/

	install -m 644 %{_builddir}/build/${target_board}/arch/%{buildarch}/boot/%{KERNEL_IMAGE} %{buildroot}/boot/${target_board}/
	install -m 644 %{_builddir}/build/${target_board}/arch/%{buildarch}/boot/dts/amlogic/${DT_PREFIX}*.dtb %{buildroot}/boot/
	make O=%{_builddir}/build/${target_board} INSTALL_MOD_STRIP=1 INSTALL_MOD_PATH=%{buildroot} modules_install

	rsync -lr \
	      --include "/scripts/**.c" \
	      --exclude ".install" \
	      --exclude "..install.cmd" \
	      --exclude "/debug*.list" \
	      --exclude "/documentation.list" \
	      --exclude "/*.manifest" \
	      --exclude "/packaging/" \
	      --exclude "/.gbs.conf" \
	      --exclude "/.git**" \
	      --exclude ".gitignore" \
	      --exclude "*\.c" \
	      --exclude ".tmp_vmlinux*" \
	      --exclude ".*dtb*tmp" \
	      --exclude ".*dtb" \
	      --exclude "*.*tmp" \
	      --exclude "vmlinux" \
	      --exclude "Image" \
	      --exclude "zImage" \
	      --exclude "Image.gz" \
	      --exclude "*.cmd" \
	      --exclude "*.ko" \
	      --exclude "*.o" \
	      --exclude "*.S" \
	      --exclude "*.HEX" \
	      ./ %{_builddir}/build/${target_board}/ %{buildroot}/boot/${target_board}/kernel/devel/

	rm -f %{buildroot}/lib/modules/*${target_board}*/build \
	      %{buildroot}/lib/modules/*${target_board}*/source \
              %{buildroot}/boot/${target_board}/kernel/devel/source

	# Replace #!/bin/bash and #! /bin/bash with #!/bin/sh for dash compatibility
	find %{buildroot}/boot/${target_board}/kernel/devel/ -type f \
	  -exec grep -qlE '^#! ?/bin/bash' {} \; -exec sed -i -E 's|^#! ?/bin/bash|#!/bin/sh|g' {} \;
done
%endif
# End of install steps

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/usr
rm -rf %{_builddir}/boot
rm -rf %{_builddir}/lib

## Start of rpm pack
# uapi headers
%files -n kernel-headers-amlogic
/usr/include/*

# ARM64 Build result pagckages for each target
%ifarch aarch64
%files -n linux-kernel-amlogic-odroid
%license COPYING
/boot/%{ODROIDS_DT_PREFIX}*.dtb
/boot/%{TARGET_ODROIDS}/%{KERNEL_IMAGE}

%files -n linux-kernel-modules-amlogic-odroid
/lib/modules/*%{TARGET_ODROIDS}/*

%files -n linux-kernel-devel-amlogic-odroid
/boot/%{TARGET_ODROIDS}/kernel/*

%files -n linux-kernel-firmware-amlogic-odroid
/lib/firmware/*

%files -n linux-kernel-amlogic-kvim
%license COPYING
/boot/%{VIMS_DT_PREFIX}*.dtb
/boot/%{TARGET_VIMS}/%{KERNEL_IMAGE}

%files -n linux-kernel-modules-amlogic-kvim
/lib/modules/*%{TARGET_VIMS}/*

%files -n linux-kernel-devel-amlogic-kvim
/boot/%{TARGET_VIMS}/kernel/*
%endif
## End of rpm pack
