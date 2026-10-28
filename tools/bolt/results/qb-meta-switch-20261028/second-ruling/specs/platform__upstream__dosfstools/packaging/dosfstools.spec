Name:           dosfstools
Version:        4.2
Release:        0
License:        GPL-3.0+
Group:          Base/File Systems
Summary:        Utilities for Making and Checking MS-DOS FAT File Systems on Linux
URL:            http://www.daniel-baumann.ch/software/dosfstools/
Source:         %{name}-%{version}.orig.tar.xz
Source1001:     dosfstools.manifest

%description
The dosfstools package includes the mkdosfs and dosfsck utilities,
which respectively make and check MS-DOS FAT file systems on hard
drives or on floppies.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure \
    --enable-compat-symlinks
%{__make} %{?_smp_mflags} CFLAGS=" -fPIC -pie %{optflags} -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64"

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

rm -rf %{buildroot}%{_datadir}/doc/dosfstools


%docs_package

%files
%manifest %{name}.manifest
%license COPYING
%manifest dosfstools.manifest
%{_sbindir}/dosfsck
%{_sbindir}/dosfslabel
%{_sbindir}/fatlabel
%{_sbindir}/fsck.fat
%{_sbindir}/fsck.msdos
%{_sbindir}/fsck.vfat
%{_sbindir}/mkdosfs
%{_sbindir}/mkfs.fat
%{_sbindir}/mkfs.msdos
%{_sbindir}/mkfs.vfat
%{_mandir}/man8/dosfsck.8%{?ext_man}
%{_mandir}/man8/dosfslabel.8%{?ext_man}
%{_mandir}/man8/fatlabel.8%{?ext_man}
%{_mandir}/man8/fsck.fat.8%{?ext_man}
%{_mandir}/man8/fsck.msdos.8%{?ext_man}
%{_mandir}/man8/fsck.vfat.8%{?ext_man}
%{_mandir}/man8/mkdosfs.8%{?ext_man}
%{_mandir}/man8/mkfs.fat.8%{?ext_man}
%{_mandir}/man8/mkfs.msdos.8%{?ext_man}
%{_mandir}/man8/mkfs.vfat.8%{?ext_man}
