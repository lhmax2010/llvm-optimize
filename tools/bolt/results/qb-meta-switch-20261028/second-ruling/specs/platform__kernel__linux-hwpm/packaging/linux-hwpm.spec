%define kernel_dir /boot/kernel/devel/kernel-devel-jetson

Name:           linux-hwpm
Version:        36.4.4
Release:        0
License:        GPL-2.0
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.manifest
Summary:        Nvidia hwpm driver modules for Jetson
Group:          System/Kernel
ExclusiveArch:  aarch64
BuildRequires:  jetson-linux-kernel-devel
BuildRequires:  jetson-linux-kernel-modules
BuildRequires:  kmod-compat
BuildRequires:  rsync
AutoreqProv:    no
Requires:       jetson-linux-kernel-modules
Requires(post): kmod-compat

%description
NVIDIA Hardware Performance Monitor driver.

%package devel
License: GPL-2.0
Summary: Header files for NVIDIA Hardware Performance Monitor development
Group: System/Kernel
Provides: linux-hwpm-devel = %{version}-%{release}

%description devel
This package contains the necessary header files for developing modules that use the linux-hwpm kernel driver.

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

# hwpm build
make ARCH=arm64 -C %{kernel_dir} \
	srctree.nvconftest=%{_builddir} CONFIG_TEGRA_OOT_MODULE=m \
	M=%{_builddir}/%{name}-%{version}/drivers/tegra/hwpm modules %{?_smp_mflags}

%install
%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
%endif
}

make ARCH=arm64 INSTALL_MOD_PATH=%{_builddir}/%{name}-%{version} INSTALL_MOD_STRIP=1 \
	-C %{kernel_dir} M=%{_builddir}/%{name}-%{version}/drivers/tegra/hwpm modules_install

mkdir -p %{buildroot}/lib/modules
find lib/modules -name "*.ko" -exec cp -a --parents {} %{buildroot}/ \;

mkdir -p %{buildroot}/boot/kernel/devel/linux-hwpm
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
	./ %{buildroot}/boot/kernel/devel/linux-hwpm

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
/lib/modules/*-jetson/updates/nvhwpm.ko

%files devel
/boot/kernel/devel/linux-hwpm/
