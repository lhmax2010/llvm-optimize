# Prevent creating debug package
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

%define config_name tizen_qcom_defconfig
%define target_board rubikpi3

Name: linux-qc
Summary: Tizen kernel for %{target_board}
Version: 6.6.52
Release: 0
License: GPL-2.0
ExclusiveArch: aarch64
Group: System/Kernel
Vendor: The Linux Community
Source0:   linux-kernel-%{version}.tar.xz
Source1:   %{name}.manifest
BuildRoot: %{_tmppath}/%{name}-%{PACKAGE_VERSION}-root

BuildRequires: bc
BuildRequires: module-init-tools
BuildRequires: bison
BuildRequires: flex
BuildRequires: libopenssl3-devel
BuildRequires: openssl3
BuildRequires: rsync
BuildRequires: python3

Provides: linux-kernel = %{version}-%{release}

%description
This package contains the Linux kernel for Tizen (%{target_board} board)

%package modules
Summary: Kernel modules for %{target_board}
Group: System/Kernel
Provides: linux-kernel-modules-%{target_board} = %{version}-%{release}

%description modules
Kernel-modules includes the loadable kernel modules(.ko files) for %{target_board}

%package devel
License: GPL-2.0
Summary: Linux support kernel map and etc for other packages for %{target_board}
Group: System/Kernel
Provides: linux-kernel-devel-%{target_board} = %{version}-%{release}

%description devel
This package provides kernel map and etc information for %{target_board}.

%package dtbs
License: BSD-3-Clause
Summary: %{target_board} device tree blobs from the Linux kernel
Group: System/Kernel
Provides: linux-kernel-dtbs-%{target_board} = %{version}-%{release}

%description dtbs
This package provides %{target_board} device tree blobs (DTBs) extracted
 from the Linux kernel.

%package kernel-headers
License: GPL-2.0
Summary: Linux support headers for userspace development
Group: System/Kernel
Provides: kernel-headers-tizen-dev

%description kernel-headers
This package provides userspaces headers from the Linux kernel. These
headers are used by the installed headers for GNU glibc and other system
 libraries.

%prep
%setup -q
cp %{SOURCE1} ./

%build
%{?asan:/usr/bin/gcc-unforce-options}
%{?ubsan:/usr/bin/gcc-unforce-options}

# 0. extract uapi headers
make headers_install %{?_smp_mflags}

# 1-1. Set config file
make %{config_name} %{?_smp_mflags}
if ! grep -q "^CONFIG_LOCALVERSION=\"-%{target_board}" .config; then
    ./scripts/config --set-str CONFIG_LOCALVERSION "-%{target_board}$(eval $(grep ^CONFIG_LOCALVERSION= .config); echo $CONFIG_LOCALVERSION)"
fi

# 1-2. Build Image
make %{?_smp_mflags}

# 1-3. Build modules
make modules %{?_smp_mflags}

# 1-4. Change permission of singing key files
chmod 644 certs/signing_key.pem
chmod 644 certs/signing_key.x509

%install
QA_SKIP_BUILD_ROOT="DO_NOT_WANT"; export QA_SKIP_BUILD_ROOT

# 2-1. Destination directories
mkdir -p %{buildroot}/boot
mkdir -p %{buildroot}/lib/modules
mkdir -p %{buildroot}/dtbs

# 2-2. Install kernel image
install -m 644 arch/arm64/boot/Image %{buildroot}/boot/

# 2-3 Install prebuilt files
cp -rf  tizen/boot/loader %{buildroot}/boot/

# 2-4 Install dtbs
install -m 644 arch/arm64/boot/dts/qcom/rubikpi3-6490.dtb %{buildroot}/dtbs/combined-dtb.dtb
install -m 644 arch/arm64/boot/dts/qcom/rubikpi3-6490.dtb %{buildroot}/boot/rubikpi3-6490.dtb

# 2-5. Install modules
make INSTALL_MOD_STRIP=1 INSTALL_MOD_PATH=%{buildroot} modules_install

# 2-6. Install kernel headers
make headers_install %{?_smp_mflags} INSTALL_HDR_PATH=%{buildroot}/usr

# 2-7. Remove conflicts headers with glibc-devel
rm -rf %{buildroot}/usr/include/scsi

# 3. Copy files for devel package
mkdir -p %{buildroot}/boot/kernel/devel/kernel-devel-%{target_board}
rsync -rl \
    --exclude "/debug*.list" \
    --exclude "/documentation.list" \
    --exclude "/*.manifest" \
    --exclude "/packaging/" \
    --exclude "/.gbs.conf" \
    --exclude "/.git**" \
    --exclude ".gitignore" \
    --exclude ".tmp_vmlinux*" \
    --exclude ".*dtb*tmp" \
    --exclude ".*dtb" \
    --exclude ".*dtbo*tmp" \
    --exclude ".*dtbo" \
    --exclude "*.*tmp" \
    --exclude "Image" \
    --exclude "Image.gz" \
    --exclude "*.cmd" \
    --exclude "*.ko" \
    --exclude "*.o" \
    --exclude "*.S" \
    --exclude "*.HEX" \
%{_builddir}/%{name}-%{version}/ %{buildroot}/boot/kernel/devel/kernel-devel-%{target_board}

%clean
rm -rf %{buildroot}

%files
%manifest %{name}.manifest
%license COPYING
/boot/Image
/boot/loader/*
/boot/rubikpi3-6490.dtb

%files modules
%manifest %{name}.manifest
/lib/modules/*

%files devel
/boot/kernel/devel/*

%files kernel-headers
/usr/include/*

%files dtbs
/dtbs/combined-dtb.dtb

