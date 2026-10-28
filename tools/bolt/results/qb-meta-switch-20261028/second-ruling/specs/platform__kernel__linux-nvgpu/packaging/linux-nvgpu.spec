%define kernel_dir /boot/kernel/devel/kernel-devel-jetson

Name:           linux-nvgpu
Version:        36.4.4
Release:        0
License:        GPL-2.0
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.manifest
Summary:        NVIDIA GPU driver
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
NVIDIA GPU driver.

%package devel
License: GPL-2.0
Summary: Header files for linux-nvgpu development
Group: System/Kernel
Provides: linux-nvgpu-devel = %{version}-%{release}

%description devel
This package contains the necessary header files for developing modules
that use the linux-nvgpu kernel driver.

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

# linux-nvgpu build
make ARCH=arm64 -C %{kernel_dir} \
	srctree.nvconftest=%{_builddir} \
	srctree.nvidia=/boot/kernel/devel/linux-nv-oot \
	srctree.nvidia-oot=/boot/kernel/devel/linux-nv-oot \
	CONFIG_TEGRA_OOT_MODULE=m \
	KBUILD_EXTRA_SYMBOLS=/boot/kernel/devel/linux-nv-oot/Module.symvers \
	M=%{_builddir}/%{name}-%{version}/drivers/gpu/nvgpu \
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
	M=%{_builddir}/%{name}-%{version}/drivers/gpu/nvgpu modules_install

mkdir -p %{buildroot}/lib/modules
find lib/modules -name "nvgpu.ko" -exec cp -a --parents {} %{buildroot}/ \;

rm -rf %{_builddir}/%{name}-%{version}/lib/modules/$RELEASEVERSION

mkdir -p %{buildroot}/boot/kernel/devel/linux-nvgpu
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
	./ %{buildroot}/boot/kernel/devel/linux-nvgpu

mkdir -p %{buildroot}/lib/modules/modules-load.d
install -m 644 conf/nv-modules.conf %{buildroot}/lib/modules/modules-load.d/

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
/lib/modules/*-jetson/updates/nvgpu.ko
/lib/modules/modules-load.d/nv-modules.conf

%files devel
/boot/kernel/devel/linux-nvgpu/
