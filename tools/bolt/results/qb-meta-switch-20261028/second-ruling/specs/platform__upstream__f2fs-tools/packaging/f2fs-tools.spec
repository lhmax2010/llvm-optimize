Name:           f2fs-tools
Version:        1.16.0
Release:        0.g4f3af3a2acfe
Summary:        Utilities for the Flash-friendly filesystem (F2FS)
Group:          Base/File Systems
License:        GPL-2.0
Url:            https://git.kernel.org/cgit/linux/kernel/git/jaegeuk/f2fs-tools.git
Source:         %{name}-%{version}.tar.xz
Source1001:     f2fs-tools.manifest
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig
BuildRequires:  xz
BuildRequires:  pkgconfig(blkid)
BuildRequires:  pkgconfig(uuid)

%description
Utilities needed to create and maintain F2FS filesystem.

%package -n libf2fs
Summary:        Library to manipulate F2FS
Group:          Base/File Systems
License:        LGPL-2.1

%description -n libf2fs
This package contains a shared library used for manipulation of F2FS filesystem.

%package -n libf2fs_format
Summary:        Library to create F2FS
Group:          Base/File Systems
License:        LGPL-2.1

%description -n libf2fs_format
This package contains a shared library to format F2FS filesystem.

%package devel
Summary:        Development files for F2FS
Group:          Base/Development
License:        LGPL-2.1
Requires:       libf2fs = %version
Requires:       libf2fs_format = %version

%description devel
This package contains development files for %name.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="${CFLAGS} -fPIE"
export LDFLAGS="${LDFLAGS} -pie"
%autogen
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install
find %buildroot -type f -name "*.la" -delete -print

mkdir -p "%buildroot/%_includedir"
cp -a include/f2fs_fs.h mkfs/f2fs_format_utils.h \
	"%buildroot/%_includedir/"

rm -f %buildroot/usr/share/man/man8/*

%post   -n libf2fs -p /sbin/ldconfig
%postun -n libf2fs -p /sbin/ldconfig
%post   -n libf2fs_format -p /sbin/ldconfig
%postun -n libf2fs_format -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%_sbindir/*

%files -n libf2fs
%manifest %{name}.manifest
%license COPYING
%_libdir/libf2fs.so.*

%files -n libf2fs_format
%manifest %{name}.manifest
%license COPYING
%_libdir/libf2fs_format.so.*

%files devel
%manifest %{name}.manifest
%license COPYING
%_includedir/*.h
%_libdir/libf2fs*.so
