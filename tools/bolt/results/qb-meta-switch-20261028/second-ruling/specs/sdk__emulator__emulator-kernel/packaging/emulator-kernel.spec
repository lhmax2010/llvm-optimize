%define buildarch    x86_64
%define config_name  tizen_emul_defconfig
%define target_board emulator

# Want to enable initramfs facility to hand modulable kernel (e.g., file systems)?
%define with_initramfs 1

Name:          emulator-kernel
Summary:       The Linux Kernel for Tizen Studio Emulator
Version:       6.18.2.tizen
Release:       0
License:       GPL-2.0
Group:         System/Kernel
URL:           https://www.kernel.org
Distribution:  Tizen
Vendor:        Tizen
Source0:       %{name}-%{version}.tar.gz
Source1001:    %{name}.manifest
%define fullVersion %{version}-%{buildarch}_%{target_board}

ExclusiveArch: x86_64
BuildRequires: binutils
BuildRequires: bc
BuildRequires: flex
BuildRequires: bison
BuildRequires: rsync
BuildRequires: coreutils
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(libelf)
BuildRequires: glibc-devel
BuildRequires: kmod kmod-compat module-init-tools
BuildRequires: dwarves
BuildRequires: python3

Provides: %{name} = %{fullVersion}
Provides: %{name}-uname-r = %{fullVersion}

%description
This package provides the Linux kernel (vmlinuz,bzImage), the core of any
Linux-based operating system. The kernel handles the basic functions
of the OS: memory allocation, process allocation, device I/O, etc.
This package contains the Linux kernel for Tizen (arch %{buildarch},
target board %{target_board})

%package devel
License: GPL-2.0
Summary: Linux support kernel map and etc for other packages
Group: System/Kernel
Provides: %{name}-devel = %{fullVersion}
Provides: %{name}-devel-uname-r = %{fullVersion}
Provides: linux-kernel-modulebuild = %{fullVersion}

%description devel
This package provides the kernel header files and makefiles
sufficient to build modules against the kernel package.

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

%package btf-devel
License: GPL-2.0
Summary: Linux kernel BTF header for eBPF development
Group: System/Kernel
Provides: %{name}-btf-devel = %{fullVersion}
Provides: %{name}-btf-devel-uname-r = %{fullVersion}
Provides: kernel-btf-devel

%description btf-devel
This package provides the vmlinux.h header file generated from the
Linux kernel for eBPF program development. This header contains all the
type definitions needed for BPF CO-RE (Compile Once - Run Everywhere).

%package user-headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Provides: %{name}-user-headers = %{fullVersion}
Provides: %{name}-user-headers-uname-r = %{fullVersion}
Provides: linux-kernel-modulebuild-header = %{fullVersion}

%description user-headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%prep
%setup -q -n emulator-kernel-%{version}
cp %{SOURCE1001} .

%build
%{?asan:/usr/bin/gcc-unforce-options}
%{?ubsan:/usr/bin/gcc-unforce-options}

%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
%endif
}

# Make sure EXTRAVERSION says what we want it to say
sed -i "s/^EXTRAVERSION.*/EXTRAVERSION = -%{buildarch}/" Makefile

# 1.1 build: set config file
%if "%{dev_wos}" == "1"
# build as permissive mode
./scripts/config --file arch/x86/configs/%{config_name} -u CONFIG_SECURITY_SMACK -u CONFIG_SECURITY_SMACK_APPEND_SIGNALS -e CONFIG_DEFAULT_SECURITY_DAC --set-str CONFIG_LSM ""
%endif

make %{?_smp_mflags} ARCH=%{buildarch} %{config_name}

./scripts/config --set-str CONFIG_INITRAMFS_SOURCE ramfs/initramfs.%{buildarch}

# To prevent the script scripts/setlocalversion to append the "+" to the end of
# the kernel local version, we create an empty .scmversion file in the root of the kernel source.
touch .scmversion

# 1.2 build: generate uapi headers
make %{?_smp_mflags} ARCH=%{buildarch} headers_install

# 1.3 build: generate bzImage for x86 and x86_64
make %{?_smp_mflags} ARCH=%{buildarch} bzImage

# 1.4 build: build bpftool from kernel source
make %{?_smp_mflags} ARCH=%{buildarch} -C tools/bpf/bpftool

# 1.5 build: generate vmlinux.h from vmlinux binary
mkdir -p btf
./tools/bpf/bpftool/bpftool btf dump file vmlinux format c > btf/vmlinux.h

%install
QA_SKIP_BUILD_ROOT="DO_NOT_WANT"; export QA_SKIP_BUILD_ROOT

%{?_toolchain:
%if %{toolchain_is clang}
export LLVM=1
%endif
}

# 2.1 Install user-headers
make INSTALL_PATH=%{buildroot} INSTALL_MOD_PATH=%{buildroot} INSTALL_HDR_PATH=%{buildroot}/usr headers_install

# 2.2 install: installing bzImage(vmlinuz), config, System.map, and initramfs
mkdir -p %{buildroot}/boot

install -m 644 arch/%{buildarch}/boot/bzImage %{buildroot}/boot/bzImage.%{buildarch}
install -m 644 .config %{buildroot}/boot/config-%{version}-%{buildarch}
install -m 644 System.map %{buildroot}/boot/System.map-%{version}-%{buildarch}

%if %{with_initramfs}
install -m 644 ramfs/initramfs.%{buildarch} %{buildroot}/boot/
%endif

# 2.3 install: Install bpftool binary
mkdir -p %{buildroot}/usr/sbin
install -m 755 tools/bpf/bpftool/bpftool %{buildroot}/usr/sbin/bpftool

# 2.4 install: Install vmlinux.h BTF header for eBPF development
mkdir -p %{buildroot}/usr/include/bpf
install -m 644 btf/vmlinux.h %{buildroot}/usr/include/bpf/vmlinux.h

# 2.5 install: remove unnecessary files before generating a devel package
find %{_builddir}/emulator-kernel-%{version} -name ".tmp_vmlinux*" -delete
find %{_builddir}/emulator-kernel-%{version} -name ".gitignore" -delete
find %{_builddir}/emulator-kernel-%{version} -name "\.*dtb*tmp" -delete
find %{_builddir}/emulator-kernel-%{version} -name "\.*dtb" -delete
find %{_builddir}/emulator-kernel-%{version} -name "*\.*tmp" -delete
find %{_builddir}/emulator-kernel-%{version} -name "Image" -delete
find %{_builddir}/emulator-kernel-%{version} -name "Image.gz" -delete
find %{_builddir}/emulator-kernel-%{version} -name "*.cmd" -delete
find %{_builddir}/emulator-kernel-%{version} -name "*\.ko" -delete
find %{_builddir}/emulator-kernel-%{version} -name "*\.o" -delete
find %{_builddir}/emulator-kernel-%{version} -name "*\.S" -delete
find %{_builddir}/emulator-kernel-%{version} -name "*\.HEX" -type f -delete
find %{_builddir}/emulator-kernel-%{version} -name "*\.c" -not -path "%{_builddir}/emulator-kernel-%{version}/scripts/*" -delete

# 2.6 install: move filted files into /boot/kernel/devel/ for devel package
mkdir -p %{buildroot}/boot/kernel/devel
cp -arf %{_builddir}/emulator-kernel-%{version} %{buildroot}/boot/kernel/devel/

# let's make /usr/src/linux-headers as a symbolc linke for compatibility
mkdir -p %{buildroot}/usr/src
ln -s /boot/kernel/devel/emulator-kernel-%{version} %{buildroot}/usr/src/linux-headers-%{version}
ln -s /boot/kernel/devel/emulator-kernel-%{version} %{buildroot}/usr/src/linux-headers

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license COPYING
/boot/bzImage*
/boot/config-*
/boot/System.map-*
%if %{with_initramfs}
/boot/initramfs.%{buildarch}
%endif

%files devel
%defattr(-,root,root,-)
/boot/kernel/devel/*
/usr/src/*

%files -n linux-kernel-bpftool
%defattr(-,root,root,-)
/usr/sbin/bpftool

%files btf-devel
%defattr(-,root,root,-)
/usr/include/bpf/vmlinux.h

%files user-headers
%defattr(-,root,root,-)
/usr/include
