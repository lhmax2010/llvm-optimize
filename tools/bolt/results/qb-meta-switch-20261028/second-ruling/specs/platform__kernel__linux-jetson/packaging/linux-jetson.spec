# Ignore double dash in version for rpmbuild
%define _wrong_version_format_terminate_build 0

%define config_name tizen_orin_defconfig
%define buildarch arm64
%define variant jetson

Name: jetson-linux-kernel
Summary: The Linux Kernel for NVIDIA Jetson Orin(Tegra)
Version: 5.15.148
Release: 0
License: GPL-2.0
ExclusiveArch: aarch64
Group: System/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source0: linux-kernel-%{version}.tar.xz
Source1001: linux-jetson.manifest
BuildRoot: %{_tmppath}/%{name}-%{PACKAGE_VERSION}-root

%define fullVersion %{version}_%{buildarch}_jetson

BuildRequires: bc
BuildRequires: module-init-tools
BuildRequires: bison
BuildRequires: flex
BuildRequires: pkgconfig(openssl3)
BuildRequires: openssl3
BuildRequires: python3
BuildRequires: rsync

Provides: jetson-kernel-uname-r = %{fullVersion}
Provides: linux-kernel = %{version}_%{release}

%description
The Linux Kernel, the operating system core itself

# modules
%package -n jetson-linux-kernel-modules
Summary: Kernel modules for jetson
Group: System/Kernel
Provides: jetson-kernel-modules = %{fullVersion}
Provides: jetson-kernel-modules-uname-r = %{fullVersion}

%description -n jetson-linux-kernel-modules
Kernel-modules includes the loadable kernel modules(.ko files) for jetson

%package -n jetson-linux-kernel-devel
License: GPL-2.0
Summary: Linux support kernel map and etc for other packages
Group: System/Kernel
Provides: jetson-kernel-devel = %{fullVersion}
Provides: jetson-kernel-devel-uname-r = %{fullVersion}

%description -n jetson-linux-kernel-devel
This package provides kernel map and etc information.

#headers
%package -n jetson-linux-kernel-headers
License: GPL-2.0
Summary: Linux support headers for userspace development
Group: System/Kernel
Provides: kernel-headers-tizen-dev

%description -n jetson-linux-kernel-headers
This package provides userspaces headers from the Linux kernel. These
headers are used by the installed headers for GNU glibc and other system
 libraries.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%{?asan:/usr/bin/gcc-unforce-options}
%{?ubsan:/usr/bin/gcc-unforce-options}

%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
export CFLAGS_KERNEL="${CFLAGS_KERNEL} -Wno-error=incompatible-pointer-types-discards-qualifiers"
export KCFLAGS="${KCFLAGS} -Wno-error=incompatible-pointer-types-discards-qualifiers"
%endif
}

# extract uapi headers
make headers_install %{?_smp_mflags}

# Set config file
make %{config_name} %{?_smp_mflags}
if ! grep -q "^CONFIG_LOCALVERSION=\"-%{variant}" .config; then
    ./scripts/config --set-str CONFIG_LOCALVERSION "-%{variant}$(eval $(grep ^CONFIG_LOCALVERSION= .config); echo $CONFIG_LOCALVERSION)"
fi

# Build Image
make %{?_smp_mflags}

# Build modules
make modules %{?_smp_mflags}

# Change permission of signing key
chmod a+r certs/signing_key.pem

%install
QA_SKIP_BUILD_ROOT="DO_NOT_WANT"; export QA_SKIP_BUILD_ROOT

%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
export CFLAGS_KERNEL="${CFLAGS_KERNEL} -Wno-error=incompatible-pointer-types-discards-qualifiers"
export KCFLAGS="${KCFLAGS} -Wno-error=incompatible-pointer-types-discards-qualifiers"
%endif
}

# Destination directories
mkdir -p %{buildroot}/boot/boot
mkdir -p %{buildroot}/boot/boot/extlinux
mkdir -p %{buildroot}/esp/EFI/BOOT
mkdir -p %{buildroot}/lib/modules

# Install kernel headers
make headers_install %{?_smp_mflags} INSTALL_HDR_PATH=%{buildroot}/usr

# Install kernel binary
install -m 644 arch/%{buildarch}/boot/Image %{buildroot}/boot/boot/Image
install -m 644 tizen/boot/extlinux/extlinux.conf %{buildroot}/boot/boot/extlinux/
install -m 644 tizen/boot/initrd %{buildroot}/boot/boot/
install -m 644 tizen/EFI/BOOT/BOOTAA64.efi %{buildroot}/esp/EFI/BOOT/

# Install modules
make INSTALL_MOD_STRIP=1 INSTALL_MOD_PATH=%{buildroot} modules_install

# Install modules-load conf file
mkdir -p %{buildroot}/lib/modules/modules-load.d
install -m 644 conf/tegra-tfm-modules.conf %{buildroot}/lib/modules/modules-load.d/

# Copy files for devel package
mkdir -p %{buildroot}/boot/kernel/devel/kernel-devel-jetson
rsync -r \
	--include "/scripts/**.c" \
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
	--exclude "Image" \
	--exclude "zImage" \
	--exclude "Image.gz" \
	--exclude "*.cmd" \
	--exclude "*.ko" \
	--exclude "*.o" \
	--exclude "*.S" \
	--exclude "*.HEX" \
	--exclude "arch/*/kernel/vdso*/*.so" \
	--exclude "arch/*/kernel/vdso*/*.so.dbg" \
	./ %{buildroot}/boot/kernel/devel/kernel-devel-jetson

%clean
rm -rf %{buildroot}

%files -n jetson-linux-kernel-modules
/lib/modules/*

%files -n jetson-linux-kernel-devel
/boot/kernel/devel/*jetson/

%files -n jetson-linux-kernel
%license COPYING
/boot/boot/Image
/boot/boot/initrd
/boot/boot/extlinux/extlinux.conf
/esp/EFI/BOOT/BOOTAA64.efi

%files -n jetson-linux-kernel-headers
/usr/include/*
