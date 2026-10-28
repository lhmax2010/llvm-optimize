# Ignore double dash in version for rpmbuild
%define _wrong_version_format_terminate_build 0

%define config_name tizen_bcm2711_defconfig
%ifarch aarch64
%define buildarch arm64
%else
%define buildarch arm
%endif
%define target_board rpi4
%define variant %{buildarch}-%{target_board}

Name: rpi4-linux-kernel
Summary: The Linux Kernel for Raspberry Pi4
Version: 6.12.80
Release: 0
License: GPL-2.0
ExclusiveArch: %{arm} aarch64
Group: System/Kernel
Vendor: The Linux Community
URL: https://www.kernel.org
Source0:   linux-kernel-%{version}.tar.xz
Source1001: linux-rpi.manifest
BuildRoot: %{_tmppath}/%{name}-%{PACKAGE_VERSION}-root

%define fullVersion %{version}_%{buildarch}_%{target_board}

BuildRequires: bc
BuildRequires: module-init-tools
BuildRequires: bison
BuildRequires: flex
BuildRequires: pkgconfig(openssl3)
BuildRequires: libunwind-devel
BuildRequires: libdw-devel
BuildRequires: libelf-devel
BuildRequires: elfutils
BuildRequires: xz-devel
BuildRequires: binutils-devel
BuildRequires: python3
BuildRequires: rsync
BuildRequires: dwarves

%description
The Linux Kernel, the operating system core itself

# kernel
%package -n %{variant}-linux-kernel
License: GPL-2.0
Summary: Tizen kernel for %{target_board}
Group: System/Kernel
Provides: %{variant}-kernel-uname-r = %{fullVersion}
Provides: linux-kernel = %{version}_%{release}

%description -n %{variant}-linux-kernel
This package contains the Linux kernel for Tizen (arch %{buildarch}, target board %{target_board})

%package -n %{variant}-rt-linux-kernel
License: GPL-2.0
Summary: Tizen kernel for %{target_board}
Group: System/Kernel
Provides: %{variant}-kernel-uname-r = %{fullVersion}_rt
Provides: linux-kernel = %{version}_%{release}_rt

%description -n %{variant}-rt-linux-kernel
This package contains the Linux kernel for Tizen (arch %{buildarch}, target board %{target_board})

# modules

%package -n %{variant}-linux-kernel-modules
Summary: Kernel modules for %{target_board}
Group: System/Kernel
Provides: %{variant}-kernel-modules = %{fullVersion}
Provides: %{variant}-kernel-modules-uname-r = %{fullVersion}

%description -n %{variant}-linux-kernel-modules
Kernel-modules includes the loadable kernel modules(.ko files) for %{target_board}

%package -n %{variant}-rt-linux-kernel-modules
Summary: Kernel modules for %{target_board}
Group: System/Kernel
Provides: %{variant}-kernel-modules = %{fullVersion}_rt
Provides: %{variant}-kernel-modules-uname-r = %{fullVersion}_rt

%description -n %{variant}-rt-linux-kernel-modules
Kernel-modules includes the loadable kernel modules(.ko files) for %{target_board}
with the PREEMPT_RT patch

# devel

%package -n %{variant}-linux-kernel-devel
License: GPL-2.0
Summary: Linux support kernel map and etc for other packages
Group: System/Kernel
Provides: %{variant}-kernel-devel = %{fullVersion}
Provides: %{variant}-kernel-devel-uname-r = %{fullVersion}

%description -n %{variant}-linux-kernel-devel
This package provides kernel map and etc information.

%package -n %{variant}-rt-linux-kernel-devel
License: GPL-2.0
Summary: Linux support kernel map and etc for other packages
Group: System/Kernel
Provides: %{variant}-kernel-devel = %{fullVersion}_rt
Provides: %{variant}-kernel-devel-uname-r = %{fullVersion}_rt

%description -n %{variant}-rt-linux-kernel-devel
This package provides kernel map and etc information.

%package -n %{variant}-linux-kernel-btf-devel
License: GPL-2.0
Summary: Linux kernel BTF header for eBPF development
Group: System/Kernel
Provides: %{variant}-kernel-btf-devel = %{fullVersion}
Provides: %{variant}-kernel-btf-devel-uname-r = %{fullVersion}
Provides: kernel-btf-devel

%description -n %{variant}-linux-kernel-btf-devel
This package provides the vmlinux.h header file generated from the
Linux kernel for eBPF program development. This header contains all the
type definitions needed for BPF CO-RE (Compile Once - Run Everywhere).

#headers
%package -n %{variant}-linux-kernel-headers
License: GPL-2.0
Summary: Linux support headers for userspace development
Group: System/Kernel
Provides: kernel-headers-tizen-dev

%description -n %{variant}-linux-kernel-headers
This package provides userspaces headers from the Linux kernel. These
headers are used by the installed headers for GNU glibc and other system
 libraries.

%package -n linux-kernel-perf
Summary: The perf performance counter tool
Group: System/Kernel
Provides: perf = %{version}

%description -n linux-kernel-perf
This package provides the "perf" tool that can be used to monitor performance
counter events as well as various kernel internal events.

%package -n linux-kernel-bpftool
Summary: The bpftool utility
Group: System/Kernel
Provides: bpftool = %{version}

%description -n linux-kernel-bpftool
This package provides bpftool. Bpftool is a command-line utility designed
for managing, inspecting, debugging, and generating skeletons for eBPF
programs within the Linux kernel. Its skeleton generation feature
("bpftool gen skeleton") enables easier integration of compiled BPF
objects with user-space applications, making bpftool a critical component
for building and running eBPF-based monitoring and instrumentation.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%{?asan:/usr/bin/gcc-unforce-options}
%{?ubsan:/usr/bin/gcc-unforce-options}

%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
%endif
}

# LSM configuration fragment selection
%if "%{?dev_sel}" == "1"
%define lsm_fragment kernel/configs/selinux.config
%else
%if "%{?dev_wos}" == "1"
%define lsm_fragment kernel/configs/nosmack.config
%endif
%endif

for target in %{variant} %{variant}-rt; do
    echo "-${target}" > localversion-tizen

    # extract uapi headers
    make O=build/${target} headers_install %{?_smp_mflags}

    # Set config file
    BASE_CONFIG="arch/%{buildarch}/configs/%{config_name}"
    EXTRA_FRAGMENTS=""

    case $target in
	%{variant})
	    EXTRA_FRAGMENTS="%{?lsm_fragment}"
	;;
	%{variant}-rt)
	    EXTRA_FRAGMENTS="kernel/configs/rt.config %{?lsm_fragment}"
	;;
    esac

    mkdir -p build/${target}
    ./scripts/kconfig/merge_config.sh -m -O build/${target} ${BASE_CONFIG} ${EXTRA_FRAGMENTS}
    make O=build/${target} olddefconfig %{?_smp_mflags}

    if [ "${target}" = "%{variant}" ]; then
        # Build perf
        # WERROR=0 make O=build/${target} -s -C tools/lib/traceevent %{?_smp_mflags}
        WERROR=0 make O=build/${target} -s -C tools/perf EXTRA_CFLAGS="-fPIE" %{?_smp_mflags} NO_LIBTRACEEVENT=1 NO_JEVENTS=1

        # Build bpftool
        WERROR=0 make O=build/${target} -s -C tools/bpf/bpftool %{?_smp_mflags}
    fi

    # Build Image/Image.gz
    make O=build/${target} %{?_smp_mflags}

    # Build dtbs
    make O=build/${target} dtbs %{?_smp_mflags}

    # Build modules
    make O=build/${target} modules %{?_smp_mflags}

    if [ "${target}" = "%{variant}" ]; then
       # Create directory for BTF data
       mkdir -p build/${target}/btf

       # Generate vmlinux.h from vmlinux binary
       ./build/${target}/bpftool btf dump file build/${target}/vmlinux format c > build/${target}/btf/vmlinux.h
    fi

done

%install
QA_SKIP_BUILD_ROOT="DO_NOT_WANT"; export QA_SKIP_BUILD_ROOT

%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
%endif
}

# Destination directories
mkdir -p %{buildroot}/boot
mkdir -p %{buildroot}/lib/modules

# Install boot binary files
%ifarch aarch64
install -m 644 rpi/boot/config_64bit.txt %{buildroot}/boot/config.txt
%else
install -m 644 rpi/boot/config.txt %{buildroot}/boot/
%endif
install -m 644 rpi/boot/LICENCE.broadcom %{buildroot}/boot/
install -m 644 rpi/boot/start*.elf %{buildroot}/boot/
install -m 644 rpi/boot/fixup*.dat %{buildroot}/boot/

# Install kernel DTB
install -m 644 build/%{variant}/arch/%{buildarch}/boot/dts/broadcom/bcm*.dtb %{buildroot}/boot/
mkdir -p %{buildroot}/boot/overlays
install -m 644 build/%{variant}/arch/%{buildarch}/boot/dts/overlays/*.dtb* %{buildroot}/boot/overlays/

# Install kernel headers
make O=build/%{variant} headers_install %{?_smp_mflags} INSTALL_HDR_PATH=%{buildroot}/usr

for target in %{variant} %{variant}-rt; do
    # Install kernel binary
    case $target in
	%{variant})
%ifarch aarch64
            install -m 644 build/${target}/arch/%{buildarch}/boot/Image %{buildroot}/boot/Image
%else
            install -m 644 build/${target}/arch/%{buildarch}/boot/zImage %{buildroot}/boot/zImage
%endif

            # Install perf
            WERROR=0 make O=build/${target} -s -C tools/perf EXTRA_CFLAGS="-fPIE" DESTDIR=%{buildroot}/usr install NO_LIBTRACEEVENT=1 NO_JEVENTS=1

	    # Install bpftool
            mkdir -p %{buildroot}/usr/sbin
            install -m 755 build/${target}/bpftool %{buildroot}/usr/sbin/

	    # Install vmlinux.h header
            mkdir -p %{buildroot}/usr/include/bpf
            install -m 644 build/${target}/btf/vmlinux.h %{buildroot}/usr/include/bpf/vmlinux.h

	    rm -rf %{buildroot}/usr/etc
            rm -rf %{buildroot}/usr/lib/debug
            rm -rf %{buildroot}/usr/lib/perf
            rm -rf %{buildroot}/usr/share
            find %{buildroot}/usr/libexec/ -type f -exec grep -ql '^#!/bin/bash' {} \; -exec rm -f {} \;

	;;
	%{variant}-rt)
%ifarch aarch64
            install -m 644 build/${target}/arch/%{buildarch}/boot/Image %{buildroot}/boot/Image_rt
%else
            install -m 644 build/${target}/arch/%{buildarch}/boot/zImage %{buildroot}/boot/zImage_rt
%endif
	;;
    esac

    # Install modules
    make O=build/${target} INSTALL_MOD_STRIP=1 INSTALL_MOD_PATH=%{buildroot} modules_install

    # Copy files for devel package
    mkdir -p %{buildroot}/boot/kernel/devel/kernel-devel-${target}
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
	  --exclude "/build/" \
	  ./ build/${target}/ %{buildroot}/boot/kernel/devel/kernel-devel-${target}

    # Replace #!/bin/bash and #! /bin/bash with #!/bin/sh for dash compatibility
    find %{buildroot}/boot/kernel/devel/kernel-devel-${target} -type f \
      -exec grep -qlE '^#! ?/bin/bash' {} \; -exec sed -i -E 's|^#! ?/bin/bash|#!/bin/sh|g' {} \;
done

%clean
rm -rf %{buildroot}

%post -n %{variant}-rt-linux-kernel
%ifarch aarch64
mv /boot/Image_rt /boot/Image
%else
mv /boot/zImage_rt /boot/zImage
%endif

%preun -n %{variant}-rt-linux-kernel
%ifarch aarch64
mv /boot/Image /boot/Image_rt
%else
mv /boot/zImage /boot/zImage_rt
%endif

%files -n %{variant}-linux-kernel-modules
%ifarch aarch64
/lib/modules/*%{variant}-v8/
%else
/lib/modules/*%{variant}-v7l/
%endif

%files -n %{variant}-rt-linux-kernel-modules
%ifarch aarch64
/lib/modules/*%{variant}-rt-v8/
%else
/lib/modules/*%{variant}-rt-v7l/
%endif

%files -n %{variant}-linux-kernel-devel
/boot/kernel/devel/*%{variant}/

%files -n %{variant}-rt-linux-kernel-devel
/boot/kernel/devel/*%{variant}-rt/

%files -n %{variant}-linux-kernel-btf-devel
/usr/include/bpf/vmlinux.h

%files -n %{variant}-linux-kernel
%license COPYING
%ifarch aarch64
/boot/Image
%else
/boot/zImage
%endif
/boot/bcm*.dtb
/boot/overlays/*.dtb*
/boot/config.txt
/boot/LICENCE.broadcom
/boot/start*.elf
/boot/fixup*.dat

%files -n %{variant}-rt-linux-kernel
%license COPYING
%ifarch aarch64
/boot/Image_rt
%else
/boot/zImage_rt
%endif
/boot/bcm*.dtb
/boot/overlays/*.dtb*
/boot/config.txt
/boot/LICENCE.broadcom
/boot/start*.elf
/boot/fixup*.dat

%files -n %{variant}-linux-kernel-headers
/usr/include/*

%files -n linux-kernel-perf
%manifest linux-rpi.manifest
%license COPYING
/usr/bin/*
/usr/libexec/*

%files -n linux-kernel-bpftool
%manifest linux-rpi.manifest
%license COPYING
/usr/sbin/bpftool
