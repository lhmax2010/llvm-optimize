%define kernel_dir /boot/kernel/devel/kernel-devel-jetson

Name:           linux-nv-oot
Version:        36.4.4
Release:        0
License:        GPL-2.0
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.manifest
Summary:        NVIDIA OOT driver
Group:          System/Kernel
ExclusiveArch:  aarch64
BuildRequires:  jetson-linux-kernel-devel
BuildRequires:  jetson-linux-kernel-modules
BuildRequires:  linux-hwpm
BuildRequires:  linux-hwpm-devel
BuildRequires:  nvethernetrm-devel
BuildRequires:  kmod-compat
BuildRequires:  rsync
BuildRequires:  bc
AutoreqProv:    no
Requires:       linux-hwpm
Requires(post): kmod-compat

%description
NVIDIA OOT driver.

%package devel
License: GPL-2.0
Summary: Header files for NVIDIA OOT development
Group: System/Kernel
Provides: linux-nv-oot-devel = %{version}-%{release}

%description devel
This package contains the necessary header files for developing modules
that use the linux-nv-oot kernel driver.

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
export CLANG_KCFLAGS="\
    -Wno-unknown-warning-option \
    -Wno-error=frame-larger-than \
    -Wno-error=implicit-function-declaration \
    -Wno-error=incompatible-function-pointer-types \
    -Wno-error=default-const-init-var-unsafe \
    -Wno-error=int-conversion"
%else
export CLANG_KCFLAGS=""
%endif
}

# conftest setup
mkdir -p %{_builddir}/nvidia
cp -av %{kernel_dir}/nvidia/conftest/* %{_builddir}/nvidia/

make ARCH=arm64 src=%{_builddir}/nvidia obj=%{_builddir}/nvidia \
	NV_KERNEL_SOURCES=%{kernel_dir} \
	NV_KERNEL_OUTPUT=%{kernel_dir} \
	-f %{_builddir}/nvidia/Makefile %{?_smp_mflags}

# nvidia-oot build
mkdir -p %{_builddir}/%{name}-%{version}/drivers/net/ethernet/nvidia/nvethernet
cp -r /boot/kernel/devel/nvethernetrm \
	%{_builddir}/%{name}-%{version}/drivers/net/ethernet/nvidia/nvethernet

make ARCH=arm64 -C %{kernel_dir} \
	KCFLAGS="-Wno-error=address ${CLANG_KCFLAGS}" \
	srctree.nvconftest=%{_builddir} \
	srctree.nvidia-oot=%{_builddir}/%{name}-%{version} \
	srctree.hwpm=/boot/kernel/devel/linux-hwpm \
	CONFIG_TEGRA_OOT_MODULE=m \
	KBUILD_EXTRA_SYMBOLS=/boot/kernel/devel/linux-hwpm/drivers/tegra/hwpm/Module.symvers \
	M=%{_builddir}/%{name}-%{version} modules %{?_smp_mflags}

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
	M=%{_builddir}/%{name}-%{version} modules_install

rm -rf %{_builddir}/%{name}-%{version}/lib/modules/$RELEASEVERSION/kernel
rm -f %{_builddir}/%{name}-%{version}/lib/modules/$RELEASEVERSION/updates/nvhwpm.ko

mkdir -p %{buildroot}/lib/modules
find lib/modules -name "*.ko" -exec cp -a --parents {} %{buildroot}/ \;

mkdir -p %{buildroot}/boot/kernel/devel/linux-nv-oot
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
	./ %{buildroot}/boot/kernel/devel/linux-nv-oot

mkdir -p %{buildroot}/lib/modules/modules-load.d
install -m 644 conf/orinnano-tfm-modules.conf %{buildroot}/lib/modules/modules-load.d/

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
/lib/modules/*-jetson/updates/
/lib/modules/modules-load.d/orinnano-tfm-modules.conf

%files devel
/boot/kernel/devel/linux-nv-oot/
