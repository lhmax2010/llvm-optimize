%define target_board rubikpi3

Name:    qc-graphics-kernel
Summary: QCOM Graphics drivers
Version: 1.0
Release: 2
License: GPL-2.0-only
ExclusiveArch: aarch64
Group  : System/Kernel
Vendor:  Qualcomm Technologies
URL:     https://git.codelinaro.org/clo/le/platform/vendor/qcom/opensource/graphics-kernel
Source:  %{name}-%{version}.tar.xz
Source1: %{name}.manifest

AutoReqProv:   no
BuildRequires: linux-qc-devel
BuildRequires: module-init-tools
BuildRequires: openssl3

%description
QCOM Graphics drivers

%package rubikpi3
License: GPL-2.0-only
Summary: QCOM Graphics drivers for RUBIK Pi 3 board
Group  : System/Kernel
Requires: linux-qc-modules
Requires(post): module-init-tools

%description rubikpi3
QCOM Graphics drivers for RUBIK Pi 3 board

%prep
%setup -q
cp %{SOURCE1} .

%build
rm -f %{_builddir}/kernel-build-artifacts
ln -sf /boot/kernel/devel/kernel-devel-%{target_board} %{_builddir}/kernel-build-artifacts

export ROOT_DIR=%{_builddir}
export KERNEL_SRC=%{_builddir}/kernel-build-artifacts
export KERNEL_DIR=kernel-build-artifacts
export M=%{_builddir}/%{name}-%{version}
export _smp_mflags=%{?_smp_mflags}

make modules

%install
export ROOT_DIR=%{_builddir}
export KERNEL_SRC=%{_builddir}/kernel-build-artifacts
export KERNEL_DIR=kernel-build-artifacts
export M=%{_builddir}/%{name}-%{version}
export _smp_mflags=%{?_smp_mflags}

mkdir -p %{buildroot}/lib/modules
make modules_install INSTALL_MOD_STRIP=1 INSTALL_MOD_PATH=%{buildroot}

# remove conflict files with linux-qc-modules
find %{buildroot}/lib/modules -name "modules.*" -exec rm -f {} \;

%clean
rm -rf %{buildroot}

%files rubikpi3
%manifest %{name}.manifest
%license GPL-2.0-only
/lib/modules/*

%post rubikpi3
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name updates | head -1`))
/sbin/depmod -a $RELEASEVERSION
/usr/bin/chsmack -a "_" /lib/modules/${RELEASEVERSION}/modules.*
