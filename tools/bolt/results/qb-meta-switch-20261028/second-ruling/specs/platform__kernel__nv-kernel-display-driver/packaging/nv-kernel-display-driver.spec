%define kernel_dir /boot/kernel/devel/kernel-devel-jetson

Name:           nv-kernel-display-driver
Version:        36.4.4
Release:        0
License:        GPL-2.0 OR MIT
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.manifest
Summary:        NVIDIA kernel display driver
Group:          System/Kernel
ExclusiveArch:  aarch64
BuildRequires:  jetson-linux-kernel-devel
BuildRequires:  jetson-linux-kernel-modules
BuildRequires:  linux-hwpm
BuildRequires:  linux-nv-oot
BuildRequires:  linux-nv-oot-devel
BuildRequires:  kmod-compat
BuildRequires:  rsync
BuildRequires:  bc
AutoreqProv:    no
Requires:       linux-nv-oot
Requires(post): kmod-compat

%description
NVIDIA kernel display driver

%package devel
License: GPL-2.0
Summary: Header files for nv-kernel-display-driver development
Group: System/Kernel
Provides: nv-kernel-display-driver-devel = %{version}-%{release}

%description devel
This package contains the necessary header files for developing modules
that use the nv-kernel-display-driver kernel driver.

%prep
%setup -q
cp %{SOURCE1} .
mkdir -p lib/modules
find /lib/modules -type f -not -name "*.ko" -exec cp --parents {} . \;

%build
# Force not to build with sanitizers because this is kernel
%{?asan:/usr/bin/gcc-unforce-options}
%{?ubsan:/usr/bin/gcc-unforce-options}

%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
%endif
}

# conftest setup
mkdir -p %{_builddir}/nvidia
cp -av %{kernel_dir}/nvidia/conftest/* %{_builddir}/nvidia/
make ARCH=arm64 src=%{_builddir}/nvidia obj=%{_builddir}/nvidia \
	NV_KERNEL_SOURCES=%{kernel_dir} \
	NV_KERNEL_OUTPUT=%{kernel_dir} \
	-f %{_builddir}/nvidia/Makefile %{?_smp_mflags}

# nv-kernel-display-driver build
sed -i '$a EXTRA_CFLAGS += -w -fpermissive' \
	%{_builddir}/%{name}-%{version}/kernel-open/Kbuild

mkdir -p %{_builddir}/%{name}-%{version}/nvidia-linux-header
cp -LR %{kernel_dir}/* %{_builddir}/%{name}-%{version}/nvidia-linux-header
cp -LR /boot/kernel/devel/linux-nv-oot/include/* \
	%{_builddir}/%{name}-%{version}/nvidia-linux-header/include/
cat %{kernel_dir}/Module.symvers /boot/kernel/devel/linux-nv-oot/Module.symvers \
	> %{_builddir}/%{name}-%{version}/nvidia-linux-header/Module.symvers

make TARGET_ARCH=aarch64 \
	-C %{_builddir}/%{name}-%{version} \
        LOCALVERSION= NV_VERBOSE=0 KERNELRELEASE="" \
        SYSSRC=%{_builddir}/%{name}-%{version}/nvidia-linux-header \
        SYSOUT=%{_builddir}/%{name}-%{version}/nvidia-linux-header \
        SYSSRCHOST1X=%{_builddir}/%{name}-%{version}/drivers/gpu/host1x/include \
	modules %{?_smp_mflags}

%install
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name updates | head -1`))
cp -r /lib/modules/$RELEASEVERSION %{_builddir}/%{name}-%{version}/lib/modules/

%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
%endif
}

make ARCH=arm64 INSTALL_MOD_PATH=%{_builddir}/%{name}-%{version} \
	INSTALL_MOD_STRIP=1 -C %{kernel_dir} \
	M=%{_builddir}/%{name}-%{version}/kernel-open modules_install

mkdir -p %{buildroot}/lib/modules
find lib/modules -name "nvidia-drm.ko" -exec cp -a --parents {} %{buildroot}/ \;
find lib/modules -name "nvidia-modeset.ko" -exec cp -a --parents {} %{buildroot}/ \;
find lib/modules -name "nvidia.ko" -exec cp -a --parents {} %{buildroot}/ \;

rm -rf %{_builddir}/%{name}-%{version}/lib/modules/$RELEASEVERSION
rm -rf %{_builddir}/%{name}-%{version}/nvidia-linux-header

mkdir -p %{buildroot}/boot/kernel/devel/nv-kernel-display-driver
rsync -r \
	--exclude "/lib/modules" \
	--exclude "/*.manifest" \
	--exclude "/packaging/" \
	--exclude "/.gbs.conf" \
	--exclude "/.git**" \
	--exclude ".gitignore" \
	--exclude "*\.c" \
	--exclude "*.*tmp" \
	--exclude "*.cmd" \
	--exclude ".*.d" \
	--exclude "*.ko" \
	--exclude "*.o" \
	--exclude "*.S" \
	--exclude "*.HEX" \
	./ %{buildroot}/boot/kernel/devel/nv-kernel-display-driver

mkdir -p %{buildroot}/lib/modules/modprobe.d
install -m 644 conf/nvidia-display.conf %{buildroot}/lib/modules/modprobe.d/

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-%{version}/lib
rm -rf %{_builddir}/nvidia

%post
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name updates | head -1`))
/sbin/depmod -a $RELEASEVERSION

%files
%manifest %{name}.manifest
%license COPYING
/lib/modules/*-jetson/updates/nvidia-drm.ko
/lib/modules/*-jetson/updates/nvidia-modeset.ko
/lib/modules/*-jetson/updates/nvidia.ko
/lib/modules/modprobe.d/nvidia-display.conf

%files devel
/boot/kernel/devel/nv-kernel-display-driver/
