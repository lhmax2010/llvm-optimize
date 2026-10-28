Name:           btrfs-progs
Version:        7.0
Release:        1
Summary:        Userspace programs for btrfs filesystem
Group:		Base/File Systems
License:        GPL-2.0
URL:            https://btrfs.readthedocs.io
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(blkid)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  lzo-devel
BuildRequires:  libxml2-devel
BuildRequires:  python3-devel

%description
Btrfs is a new copy on write filesystem for Linux aimed at implementing
advanced features while focusing on fault tolerance, repair and easy
administration. This package contains the userspace programs for btrfs.

%package devel
Summary:        Development files for btrfs-progs
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains development files for btrfs-progs.

%prep
%setup -q -n %{name}

cp %{SOURCE1001} .

%build
./autogen.sh
export CFLAGS="$CFLAGS -fPIE"
export LDFLAGS="$LDFLAGS -pie -Wl,-z,relro -Wl,-z,now"
%configure \
    --prefix=/usr \
    --bindir=%{_sbindir} \
    --disable-documentation \
    --disable-python \
    --disable-convert \
    --enable-zstd \
    --enable-lzo \
    --disable-zoned \
    --disable-libudev \
    --with-crypto=builtin
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# Remove static libraries
find %{buildroot} -name '*.a' -delete

# Add PATH to shell scripts
if [ -f %{buildroot}%{_sbindir}/fsck.btrfs ]; then
    sed -i '1a PATH=/bin:/usr/bin:/sbin:/usr/sbin' %{buildroot}%{_sbindir}/fsck.btrfs
fi

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README.md
%manifest %{name}.manifest
%{_sbindir}/btrfs
%{_sbindir}/btrfsck
%{_sbindir}/btrfs-find-root
%{_sbindir}/btrfs-image
%{_sbindir}/btrfs-map-logical
%{_sbindir}/btrfs-select-super
%{_sbindir}/btrfstune
%{_sbindir}/fsck.btrfs
%{_sbindir}/mkfs.btrfs
%{_libdir}/libbtrfs.so.*
%{_libdir}/libbtrfsutil.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/btrfs/*
%{_includedir}/btrfsutil.h
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfsutil.so
%{_libdir}/pkgconfig/libbtrfsutil.pc
