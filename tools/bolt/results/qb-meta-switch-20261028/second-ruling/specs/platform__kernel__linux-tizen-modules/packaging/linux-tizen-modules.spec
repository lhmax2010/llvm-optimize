%define KMOD_PATH /lib/modules

%ifarch aarch64
%define buildarch arm64
%endif
%ifarch %{arm}
%define buildarch arm
%endif
%ifarch riscv64
%define buildarch riscv
%endif

Name:           linux-tizen-modules
Version:        11.0.0
Release:        0
License:        GPL-2.0+
Source0:        %{name}-%{version}.tar.xz
Source1:        %{name}.manifest
Summary:        Tizen-specific kernel modules
Group:          System/Kernel
ExclusiveArch:  %{arm} aarch64 riscv64
BuildRequires:  dwarves
BuildRequires:  kmod
BuildRequires:  linux-tizen-modules-source
%ifarch aarch64
BuildRequires:  linux-kernel-devel-amlogic-kvim
BuildRequires:  linux-kernel-modules-amlogic-kvim
BuildRequires:  linux-kernel-devel-amlogic-odroid
BuildRequires:  linux-kernel-modules-amlogic-odroid
BuildRequires:  %{buildarch}-rpi4-linux-kernel-devel
BuildRequires:  %{buildarch}-rpi4-linux-kernel-modules
BuildRequires:  %{buildarch}-rpi4-rt-linux-kernel-devel
BuildRequires:  %{buildarch}-rpi4-rt-linux-kernel-modules
BuildRequires:  linux-qc-devel
BuildRequires:  jetson-linux-kernel-devel
%endif
%ifarch %{arm}
BuildRequires:  %{buildarch}-rpi4-linux-kernel-devel
BuildRequires:  %{buildarch}-rpi4-linux-kernel-modules
BuildRequires:  %{buildarch}-rpi4-rt-linux-kernel-devel
BuildRequires:  %{buildarch}-rpi4-rt-linux-kernel-modules
%endif
%ifarch riscv64
BuildRequires: riscv-qemu-linux-kernel-devel
BuildRequires: riscv-qemu-linux-kernel-modules
BuildRequires: riscv-visionfive2-linux-kernel-devel
BuildRequires: riscv-visionfive2-linux-kernel-modules
BuildRequires: riscv-lpi4a-linux-kernel-devel
BuildRequires: riscv-lpi4a-linux-kernel-modules
BuildRequires: riscv-bpif3-linux-kernel-devel
BuildRequires: riscv-bpif3-linux-kernel-modules
%endif
%description

%ifarch aarch64
%package        amlogic-kvim
Summary:        Tizen modules for Amlogic Khadas VIM3 boards
AutoReqProv:    no
Requires:       linux-kernel-modules-amlogic-kvim
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
Provides:       stability-monitor-kernel-module
%description    amlogic-kvim

%package        amlogic-odroid
Summary:        Tizen modules for Amlogic Odroid boards
AutoReqProv:    no
Requires:       linux-kernel-modules-amlogic-odroid
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
Provides:       stability-monitor-kernel-module
%description    amlogic-odroid

%package        rubikpi3
Summary:        Tizen modules for Qcom RubikPi3 board
AutoReqProv:    no
Requires:       linux-qc-modules
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
%description    rubikpi3

%package        orinnano
Summary:        Tizen modules for Nvidia orinnano board
AutoReqProv:    no
Requires:       jetson-linux-kernel-modules
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
%description    orinnano
%endif

%ifarch %{arm} aarch64
%package        rpi4
Summary:        Tizen modules for RaspberryPI 4
AutoReqProv:    no
Requires:       %{buildarch}-rpi4-linux-kernel-modules
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
Provides:       stability-monitor-kernel-module
%description    rpi4

%package        rpi4-rt
Summary:        Tizen modules for RaspberryPI 4 RT (real-time)
AutoReqProv:    no
Requires:       %{buildarch}-rpi4-rt-linux-kernel-modules
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
Provides:       stability-monitor-kernel-module
%description    rpi4-rt
%endif

%ifarch riscv64
%package        rv64qemu
Summary:        Tizen modules for RISCV QEMU
Requires:       %{buildarch}-qemu-linux-kernel-modules
AutoReqProv:    no
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
%description    rv64qemu

%package        visionfive2
Summary:        Tizen modules for VisionFive2
Requires:       %{buildarch}-visionfive2-linux-kernel-modules
AutoReqProv:    no
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
%description    visionfive2

%package        lpi4a
Summary:        Tizen modules for LicheePi4A
Requires:       %{buildarch}-lpi4a-linux-kernel-modules
AutoReqProv:    no
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
%description    lpi4a

%package        bpif3
Summary:        Tizen modules for BananaPiF3
Requires:       %{buildarch}-bpif3-linux-kernel-modules
AutoReqProv:    no
Requires(post): /bin/sh
Requires(post): coreutils
Requires(post): findutils
Requires(post): kmod-compat
%description    bpif3
%endif

%prep
%setup -q
cp %{SOURCE1} ./%{name}.manifest
cp -a /usr/src/linux-tizen-modules-source ./kernel
mkdir -p ./%{KMOD_PATH}
find %{KMOD_PATH} -type f -not -name "*.ko" -exec cp --parents {} . \;

%build
# Force not to build with sanitizers because this is kernel
%{?asan:/usr/bin/gcc-unforce-options}
%{?ubsan:/usr/bin/gcc-unforce-options}

# Default buffer sizes to compile in. [kB]
export LOGGER_MAIN_BUFFER_SIZE=256
export LOGGER_EVENTS_BUFFER_SIZE=256
export LOGGER_RADIO_BUFFER_SIZE=256
export LOGGER_SYSTEM_BUFFER_SIZE=256

export TIZEN_INFORM_PATH="/mnt/inform/reboot-param.bin"

%ifarch aarch64
# KVIM
export BUILD_dm_bow=n
export BUILD_extcon_usb_fixed=m
export BUILD_inform_reboot=n
export BUILD_kdbus=n
export BUILD_logger=m
export BUILD_proc_tsm=m
export BUILD_zlogger=n

export THREAD_GROUP_CPUTIME_SUPPORT=1

make -C kernel clean KERNELDIR=/boot/kvim/kernel/devel/
make -C kernel KERNELDIR=/boot/kvim/kernel/devel/
make -C kernel modules_install KERNELDIR=/boot/kvim/kernel/devel/ INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra

# Odroid (Amlogic)
export BUILD_dm_bow=n
export BUILD_extcon_usb_fixed=m
export BUILD_inform_reboot=n
export BUILD_kdbus=n
export BUILD_logger=m
export BUILD_proc_tsm=m
export BUILD_zlogger=n

export THREAD_GROUP_CPUTIME_SUPPORT=1

make -C kernel clean KERNELDIR=/boot/odroid/kernel/devel/
make -C kernel KERNELDIR=/boot/odroid/kernel/devel/
make -C kernel modules_install KERNELDIR=/boot/odroid/kernel/devel/ INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra

# RubikPi3 (Qcom)
export BUILD_dm_bow=n
export BUILD_extcon_usb_fixed=m
export BUILD_inform_reboot=n
export BUILD_kdbus=n
export BUILD_logger=m
export BUILD_proc_tsm=n
export BUILD_zlogger=n

make -C kernel clean KERNELDIR=/boot/kernel/devel/kernel-devel-rubikpi3/
make -C kernel KERNELDIR=/boot/kernel/devel/kernel-devel-rubikpi3/
make -C kernel modules_install KERNELDIR=/boot/kernel/devel/kernel-devel-rubikpi3/ INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra

# OrinNano (Nvidia)
export BUILD_dm_bow=n
export BUILD_extcon_usb_fixed=m
export BUILD_inform_reboot=n
export BUILD_kdbus=n
export BUILD_logger=m
export BUILD_proc_tsm=n
export BUILD_zlogger=n

%{?_toolchain:
%if %{toolchain_is clang}
# Only apply LLVM build to RPI kernel module
export LLVM=1
# Remove LLVM unrecognized flags
find kernel -name Makefile -exec sed -i "s/-Wno-error=missing-attributes//g" {} \;
%endif
}

make -C kernel clean KERNELDIR=/boot/kernel/devel/kernel-devel-jetson/
make -C kernel KERNELDIR=/boot/kernel/devel/kernel-devel-jetson/
make -C kernel modules_install KERNELDIR=/boot/kernel/devel/kernel-devel-jetson/ INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra

unset LLVM
%endif

%ifarch %{arm} aarch64
# RPI4
export BUILD_dm_bow=m
export BUILD_extcon_usb_fixed=m
export BUILD_inform_reboot=m
export BUILD_kdbus=m
export BUILD_logger=m
export BUILD_proc_tsm=m
export BUILD_zlogger=m

export THREAD_GROUP_CPUTIME_SUPPORT=1

%{?_toolchain:
%if %{toolchain_is clang}
# Only apply LLVM build to RPI kernel module
export LLVM=1
# Remove LLVM unrecognized flags
find kernel -name Makefile -exec sed -i "s/-Wno-error=missing-attributes//g" {} \;
%endif
}

make -C kernel clean KERNELDIR=/boot/kernel/devel/kernel-devel-%{buildarch}-rpi4
make -C kernel KERNELDIR=/boot/kernel/devel/kernel-devel-%{buildarch}-rpi4
make -C kernel modules_install KERNELDIR=/boot/kernel/devel/kernel-devel-%{buildarch}-rpi4 INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra

make -C kernel clean KERNELDIR=/boot/kernel/devel/kernel-devel-%{buildarch}-rpi4-rt
make -C kernel KERNELDIR=/boot/kernel/devel/kernel-devel-%{buildarch}-rpi4-rt
make -C kernel modules_install KERNELDIR=/boot/kernel/devel/kernel-devel-%{buildarch}-rpi4-rt INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra
%endif

unset LLVM

%ifarch riscv64
# QEMU-RISCV64
export BUILD_dm_bow=n
export BUILD_extcon_usb_fixed=n
export BUILD_inform_reboot=n
export BUILD_kdbus=n
export BUILD_logger=m
export BUILD_proc_tsm=n
export BUILD_zlogger=m

make -C kernel clean KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-qemu
make -C kernel KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-qemu
make -C kernel modules_install KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-qemu INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra

# VisionFive2
export BUILD_dm_bow=m
export BUILD_extcon_usb_fixed=m
export BUILD_inform_reboot=m
export BUILD_kdbus=n
export BUILD_logger=m
export BUILD_proc_tsm=n
export BUILD_zlogger=m

make -C kernel clean KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-visionfive2
make -C kernel KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-visionfive2
make -C kernel modules_install KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-visionfive2 INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra

# Licheepi4A
export BUILD_dm_bow=m
export BUILD_extcon_usb_fixed=n
export BUILD_inform_reboot=m
export BUILD_kdbus=n
export BUILD_logger=m
export BUILD_proc_tsm=n
export BUILD_zlogger=m

make -C kernel clean KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-lpi4a
make -C kernel KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-lpi4a
make -C kernel modules_install KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-lpi4a INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra

# BPI-F3
export BUILD_dm_bow=m
export BUILD_extcon_usb_fixed=m
export BUILD_inform_reboot=m
export BUILD_kdbus=n
export BUILD_logger=m
export BUILD_proc_tsm=n
export BUILD_zlogger=m

make -C kernel clean KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-bpif3
make -C kernel KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-bpif3
make -C kernel modules_install KERNELDIR=/boot/kernel/devel/kernel-devel-riscv-bpif3 INSTALL_MOD_STRIP=1 INSTALL_MOD_DIR=extra
%endif

%install
mkdir -p %{buildroot}/%{KMOD_PATH}

cd lib/modules
find -name "*.ko" -exec cp -a --parents {} %{buildroot}/%{KMOD_PATH}/ \;
cd -

%ifarch aarch64
# module load config
mkdir -p %{buildroot}/%{KMOD_PATH}/modprobe.d
install -m 644 conf/tizen-modprobe-amlogic.conf %{buildroot}/%{KMOD_PATH}/modprobe.d

mkdir -p %{buildroot}/%{KMOD_PATH}/modules-load.d
install -m 644 conf/tizen-modules-amlogic.conf %{buildroot}/%{KMOD_PATH}/modules-load.d
install -m 644 conf/tizen-modules-rubikpi3.conf %{buildroot}/%{KMOD_PATH}/modules-load.d
install -m 644 conf/tizen-modules-orinnano.conf %{buildroot}/%{KMOD_PATH}/modules-load.d
%endif

%ifarch %{arm} aarch64
# module load config
mkdir -p %{buildroot}/%{KMOD_PATH}/modprobe.d
install -m 644 conf/tizen-modprobe-rpi4.conf %{buildroot}/%{KMOD_PATH}/modprobe.d

mkdir -p %{buildroot}/%{KMOD_PATH}/modules-load.d
install -m 644 conf/tizen-modules-rpi4.conf %{buildroot}/%{KMOD_PATH}/modules-load.d
%endif

%ifarch riscv64
mkdir -p %{buildroot}/%{KMOD_PATH}/modules-load.d
install -m 644 conf/tizen-modules-lpi4a.conf %{buildroot}/%{KMOD_PATH}/modules-load.d
install -m 644 conf/tizen-modules-visionfive2.conf %{buildroot}/%{KMOD_PATH}/modules-load.d
install -m 644 conf/tizen-modules-bpif3.conf %{buildroot}/%{KMOD_PATH}/modules-load.d
%endif

%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}-%{version}/lib

%ifarch aarch64
%post amlogic-kvim
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION

%post amlogic-odroid
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION

%post rubikpi3
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION

%post orinnano
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION
%endif

%ifarch %{arm} aarch64
%post rpi4
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION

%post rpi4-rt
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION
%endif

%ifarch riscv64
%post visionfive2
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION

%post lpi4a
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION

%post bpif3
RELEASEVERSION=$(basename $(dirname `find /lib/modules -name extra | head -1`))
/sbin/depmod -a $RELEASEVERSION
%endif

%ifarch aarch64
%files amlogic-kvim
%manifest %{name}.manifest
%license COPYING
%{KMOD_PATH}/*-amlogic-kvim/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*-amlogic-kvim/extra/proc-tsm.ko
%{KMOD_PATH}/*-amlogic-kvim/extra/logger.ko
%{KMOD_PATH}/modprobe.d/tizen-modprobe-amlogic.conf
%{KMOD_PATH}/modules-load.d/tizen-modules-amlogic.conf

%files amlogic-odroid
%manifest %{name}.manifest
%license COPYING
%{KMOD_PATH}/*-amlogic-odroid/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*-amlogic-odroid/extra/proc-tsm.ko
%{KMOD_PATH}/*-amlogic-odroid/extra/logger.ko
%{KMOD_PATH}/modprobe.d/tizen-modprobe-amlogic.conf
%{KMOD_PATH}/modules-load.d/tizen-modules-amlogic.conf

%files rubikpi3
%manifest %{name}.manifest
%license COPYING
%{KMOD_PATH}/*-rubikpi3/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*-rubikpi3/extra/logger.ko
%{KMOD_PATH}/modules-load.d/tizen-modules-rubikpi3.conf

%files orinnano
%manifest %{name}.manifest
%license COPYING
%{KMOD_PATH}/*-jetson/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*-jetson/extra/logger.ko
%{KMOD_PATH}/modules-load.d/tizen-modules-orinnano.conf
%endif

%ifarch %{arm} aarch64
%files rpi4
%manifest %{name}.manifest
%license COPYING
%ifarch aarch64
%{KMOD_PATH}/*rpi4-v8/extra/dm-bow.ko
%{KMOD_PATH}/*rpi4-v8/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*rpi4-v8/extra/proc-tsm.ko
%{KMOD_PATH}/*rpi4-v8/extra/inform-reboot.ko
%{KMOD_PATH}/*rpi4-v8/extra/kdbus/kdbus.ko
%{KMOD_PATH}/*rpi4-v8/extra/logger.ko
%{KMOD_PATH}/*rpi4-v8/extra/zlogger/zlogger.ko
%else
%{KMOD_PATH}/*rpi4-v7l/extra/dm-bow.ko
%{KMOD_PATH}/*rpi4-v7l/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*rpi4-v7l/extra/proc-tsm.ko
%{KMOD_PATH}/*rpi4-v7l/extra/inform-reboot.ko
%{KMOD_PATH}/*rpi4-v7l/extra/kdbus/kdbus.ko
%{KMOD_PATH}/*rpi4-v7l/extra/logger.ko
%{KMOD_PATH}/*rpi4-v7l/extra/zlogger/zlogger.ko
%endif
%{KMOD_PATH}/modprobe.d/tizen-modprobe-rpi4.conf
%{KMOD_PATH}/modules-load.d/tizen-modules-rpi4.conf

%files rpi4-rt
%manifest %{name}.manifest
%license COPYING
%ifarch aarch64
%{KMOD_PATH}/*rpi4-rt-v8/extra/dm-bow.ko
%{KMOD_PATH}/*rpi4-rt-v8/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*rpi4-rt-v8/extra/proc-tsm.ko
%{KMOD_PATH}/*rpi4-rt-v8/extra/inform-reboot.ko
%{KMOD_PATH}/*rpi4-rt-v8/extra/kdbus/kdbus.ko
%{KMOD_PATH}/*rpi4-rt-v8/extra/logger.ko
%{KMOD_PATH}/*rpi4-rt-v8/extra/zlogger/zlogger.ko
%else
%{KMOD_PATH}/*rpi4-rt-v7l/extra/dm-bow.ko
%{KMOD_PATH}/*rpi4-rt-v7l/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*rpi4-rt-v7l/extra/proc-tsm.ko
%{KMOD_PATH}/*rpi4-rt-v7l/extra/inform-reboot.ko
%{KMOD_PATH}/*rpi4-rt-v7l/extra/kdbus/kdbus.ko
%{KMOD_PATH}/*rpi4-rt-v7l/extra/logger.ko
%{KMOD_PATH}/*rpi4-rt-v7l/extra/zlogger/zlogger.ko
%endif
%{KMOD_PATH}/modprobe.d/tizen-modprobe-rpi4.conf
%{KMOD_PATH}/modules-load.d/tizen-modules-rpi4.conf
%endif

%ifarch riscv64
%files rv64qemu
%manifest %{name}.manifest
%license COPYING
%{KMOD_PATH}/*-riscv-qemu/extra/logger.ko
%{KMOD_PATH}/*-riscv-qemu/extra/zlogger/zlogger.ko

%files visionfive2
%manifest %{name}.manifest
%license COPYING
%{KMOD_PATH}/*-riscv-visionfive2/extra/dm-bow.ko
%{KMOD_PATH}/*-riscv-visionfive2/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*-riscv-visionfive2/extra/logger.ko
%{KMOD_PATH}/*-riscv-visionfive2/extra/inform-reboot.ko
%{KMOD_PATH}/*-riscv-visionfive2/extra/zlogger/zlogger.ko
%{KMOD_PATH}/modules-load.d/tizen-modules-visionfive2.conf

%files lpi4a
%manifest %{name}.manifest
%license COPYING
%{KMOD_PATH}/*-riscv-lpi4a/extra/dm-bow.ko
%{KMOD_PATH}/*-riscv-lpi4a/extra/logger.ko
%{KMOD_PATH}/*-riscv-lpi4a/extra/inform-reboot.ko
%{KMOD_PATH}/*-riscv-lpi4a/extra/zlogger/zlogger.ko
%{KMOD_PATH}/modules-load.d/tizen-modules-lpi4a.conf

%files bpif3
%manifest %{name}.manifest
%license COPYING
%{KMOD_PATH}/*-riscv-bpif3/extra/dm-bow.ko
%{KMOD_PATH}/*-riscv-bpif3/extra/extcon-usb-fixed.ko
%{KMOD_PATH}/*-riscv-bpif3/extra/logger.ko
%{KMOD_PATH}/*-riscv-bpif3/extra/inform-reboot.ko
%{KMOD_PATH}/*-riscv-bpif3/extra/zlogger/zlogger.ko
%{KMOD_PATH}/modules-load.d/tizen-modules-bpif3.conf

%endif
