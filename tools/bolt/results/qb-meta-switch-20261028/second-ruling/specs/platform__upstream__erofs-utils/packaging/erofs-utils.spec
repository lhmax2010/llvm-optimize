Name: erofs-utils
Version: 1.8.10
Release: 0
Summary: Utilities for the Extendable Read-Only Filesystem (EROFS)
License: GPL-2.0
Group: System/Kernel
URL: https://git.kernel.org
Source0: %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
%if "%{tizen_profile_name}" == "tv"
Patch1: 0001-erofs-utils-lib-Support-zlib-wrapped-compression-for.patch
Patch2: 0002-erofs-utils-lib-apply-capability-support-uncondition.patch
Patch3: 0003-erofs-utils-mkfs-fix-potential-overflow-in-dest-size.patch
Patch4: 0004-erofs-utils-fsck-extract-blocks-info-while-verifying.patch
Patch5: 0005-erofs-utils-fsck-Add-support-decompression-for-zlib.patch
Patch6: 0006-erofs-utils-mkfs-Create-image-with-4k-aligned-decomp.patch
Patch7: 0007-erofs-utils-Add-new-option-hw-auth-align-for-creatin.patch
Patch8: 0008-erofs-utils-fsck-apply-xattrs-after-attributes-to-pr.patch
Patch9: 0009-erofs-utils-lib-fix-4k-alignment-dropping-a-full-pag.patch
Patch10: 0010-erofs-utils-fsck-emit-canonical-blocks_info-for-hw-a.patch
Patch11: 0011-erofs-utils-mkfs-index-hw-auth-extents-by-physical-a.patch
Patch12: 0012-erofs-utils-lib-reimplement-the-zlib-compressor-on-t.patch
Patch13: 0013-erofs-utils-mkfs-fold-the-HW-authentication-switch-i.patch
Patch14: 0014-erofs-utils-mkfs-inline-the-encoded-length-and-hash-.patch
Patch15: 0015-erofs-utils-mkfs-keep-the-compression-queue-moving-a.patch
%endif
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  lz4-devel
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:	libzstd-devel
BuildRequires:  m4
BuildRequires:  pkg-config
BuildRequires:  xz
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(blkid)

%description
mkfs.erofs is a user-space tool to create erofs filesystem images. It
can create two main types of erofs images, compressed and
uncompressed:

* For compressed images, it is able to integrate several compression
  algorithms, LZ4 is supported according to the current erofs kernel
  implementation.
* For uncompressed images, it can decide whether the last page of a
  file should be inlined or not properly.

%prep
%autosetup -p1
cp %{SOURCE1001} .

%build
export CFLGAS="${CFLAGS} -fPIE"
export LDFLAGS="${LDFLAGS} -fPIE"
autoreconf -fiv
%configure --bindir="%_sbindir" --enable-lzma --enable-lz4 --with-zlib --with-libzstd
%make_build

%install
%make_install
rm -rf %{buildroot}/usr/share/man/man1/*

%files
%manifest %{name}.manifest
%license COPYING
%_sbindir/*erofs
