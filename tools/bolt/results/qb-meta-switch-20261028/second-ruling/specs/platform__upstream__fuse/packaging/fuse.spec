Name:           fuse
Summary:        User space File System
License:        GPL-2.0 and LGPL-2.1
Group:          System/Libraries
Version:        2.9.9
Release:        0
Source:         %{name}-%{version}.tar.gz
Source2:        fuse.rpmlintrc
Source98:       baselibs.conf
Source1001: 	fuse.manifest
Url:            http://fuse.sourceforge.net
Requires:       util-linux >= 2.18
Requires:       which
BuildRequires:  pkgconfig
BuildRequires:  gettext
Supplements:    filesystem(fuse)

%description
With FUSE, a user space program can export a file system through the
kernel-default (Linux kernel).

User space file systems which are implemented using FUSE are provided
by the following packages:

- curlftpfs (mount FTP servers),

- encfs (layered file encryption),

- fuseiso (mount iso, img, bin, mdf and nrg CD-ROM images),

- fusepod (mount iPods),

- fusesmb (mount a fully browseable network neighborhood),

- gphotofs (mount gphoto-supported cameras),

- ntfs-3g (mount NTFS volumes read-write),

- obexfs (mount of bluetooth devices),

- sshfs (mount over ssh),

- wdfs (mount of WebDAV shares)

This package contains the mount binaries for fuse (might not be needed
by some FUSE filesystems like ntfs-3g) and the documentation for FUSE.

After installing fuse-devel, administrators can compile and install
other user space file systems which can be found at
http://fuse.sourceforge.net/wiki

%package -n libulockmgr
Summary:        Library of FUSE, the User space File System for GNU/Linux and BSD
License:        LGPL-2.1

%description -n libulockmgr
With FUSE, a user space program can export a file system through the
kernel-default (Linux kernel).

%package -n libfuse
Summary:        Library of FUSE, the User space File System for GNU/Linux and BSD
License:        LGPL-2.1

%description -n libfuse
With FUSE, a user space program can export a file system through the
kernel-default (Linux kernel).

A FUSE file system which only needs libfuse is ntfs-3g, other FUSE
file systems might need the fuse package in addition to have fusermount
and /sbin/mount.fuse.

After installing fuse-devel, administrators can compile and install
other user space file systems which can be found at
http://fuse.sourceforge.net/wiki

%package devel
Summary:        Development package for FUSE (userspace filesystem) modules
License:        LGPL-2.1
Requires:       fuse = %{version}
Requires:       glibc-devel
Requires:       libfuse = %{version}
Requires:       libulockmgr = %{version}

%description devel
This package contains all include files, libraries and configuration
files needed to develop programs that use the fuse (FUSE) library to
implement kernel-default (Linux) file systems in user space.

With fuse-devel, administrators can compile and install other user
space file systems which can be found at
http://fuse.sourceforge.net/wiki

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$RPM_OPT_FLAGS -g -fno-strict-aliasing"
export MOUNT_FUSE_PATH=%{_sbindir}
autoreconf -fi
%configure --with-pic \
    --with-pkgconfigdir=%{_libdir}/pkgconfig \
    --enable-lib \
    --disable-example \
    --enable-static
make %{?_smp_mflags}

%install
%make_install
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/init.d

%post -n libfuse -p /sbin/ldconfig

%postun -n libfuse -p /sbin/ldconfig

%post -n libulockmgr -p /sbin/ldconfig

%postun -n libulockmgr -p /sbin/ldconfig


%docs_package

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING*
%verify(not mode) %attr(4755,root,root) %{_bindir}/fusermount
%{_sbindir}/mount.fuse
%{_bindir}/ulockmgr_server
/etc/udev/rules.d/99-fuse.rules

%files -n libfuse
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING.LIB
%{_libdir}/libfuse.so.2*

%files -n libulockmgr
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING.LIB
%{_libdir}/libulockmgr.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING.LIB
%{_libdir}/libfuse.so
%{_libdir}/libulockmgr.so
%{_includedir}/fuse.h
%{_includedir}/fuse
%{_libdir}/pkgconfig/*.pc
%{_includedir}/ulockmgr.h
