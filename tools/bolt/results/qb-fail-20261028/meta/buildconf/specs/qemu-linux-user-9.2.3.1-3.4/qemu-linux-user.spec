#
# spec file for package qemu
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


# !! IMPORTANT !! See README.PACKAGING before modifying package in any way

%define summary_string Machine emulator and virtualizer

%define qemuver 9.2.3.1
%define srcver  9.2.3.1
%define sbver   1.14.0_0_g155821a
%define srcname qemu
Name:           qemu-linux-user
VCS:            platform/upstream/qemu#1b431ba0f3c634c2b5e0105311a3401be61a2f8d
URL:            https://www.qemu.org/
Summary:        %{summary_string}
License:        BSD-2-Clause AND BSD-3-Clause AND GPL-2.0-only AND GPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
Group:          System/Emulators/PC
Version:        %qemuver
Release:        3.4
Source:         https://wiki.qemu.org/download/%{srcname}-%{srcver}.tar.xz
Source1001:     qemu-linux-user-9.2.3-160000.1.1.x86_64.rpm

ExclusiveArch:  %{ix86} x86_64

# Common BuildRequires listed here:
%if 0%{?qemu_user_space_build:1}
#!BuildIgnore:  post-build-checks
%endif
#!BuildIgnore:  build-compare

%description
QEMU provides CPU emulation along with other related capabilities. This package
provides programs to run user space binaries and libraries meant for another
architecture. The syscall interface is intercepted and execution below the
syscall layer occurs on the native hardware and operating system.

%prep
%setup -q
%ifarch x86_64
rpm2cpio %{SOURCE1001} | cpio -idv
%endif

%build

%check

%install
mkdir -p %{buildroot}%_bindir
cp -r usr/bin/* %{buildroot}%_bindir/
mkdir -p %{buildroot}%_sbindir
cp -r usr/sbin/* %{buildroot}%_sbindir/

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc COPYING COPYING.LIB Changelog README VERSION
%license COPYING COPYING.LIB LICENSE
%_bindir/qemu-aarch64
%_bindir/qemu-aarch64_be
%_bindir/qemu-alpha
%_bindir/qemu-arm
%_bindir/qemu-armeb
%_bindir/qemu-hppa
%_bindir/qemu-i386
%_bindir/qemu-m68k
%_bindir/qemu-microblaze
%_bindir/qemu-microblazeel
%_bindir/qemu-mips
%_bindir/qemu-mips64
%_bindir/qemu-mips64el
%_bindir/qemu-mipsel
%_bindir/qemu-mipsn32
%_bindir/qemu-mipsn32el
%_bindir/qemu-or1k
%_bindir/qemu-ppc
%_bindir/qemu-ppc64
%_bindir/qemu-ppc64le
%_bindir/qemu-riscv32
%_bindir/qemu-riscv64
%_bindir/qemu-s390x
%_bindir/qemu-sh4
%_bindir/qemu-sh4eb
%_bindir/qemu-sparc
%_bindir/qemu-sparc32plus
%_bindir/qemu-sparc64
%_bindir/qemu-x86_64
%_bindir/qemu-xtensa
%_bindir/qemu-xtensaeb
%ifarch x86_64
%_bindir/qemu-hexagon
%_bindir/qemu-loongarch64
%endif
%_bindir/qemu-binfmt
%_bindir/qemu-*-binfmt
# add compatibility symlinks
%_bindir/qemu-arm64
%_bindir/qemu-*-static
%_sbindir/qemu-binfmt-conf.sh

