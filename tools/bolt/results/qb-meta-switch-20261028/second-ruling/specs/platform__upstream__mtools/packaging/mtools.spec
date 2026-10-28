Name:           mtools
Version:        4.0.49
Release:        0
License:        GPL-3.0+
Summary:        Access Files on an MS-DOS File System
Url:            http://mtools.linux.lu/
Group:          System/File Systems
Source:         %{name}-%{version}.tar.bz2
Source1001:     mtools.manifest
BuildRequires:  autoconf
BuildRequires:  makeinfo

%description
Mtools allows uncomplicated access to an MS-DOS file system on disk
without mounting it. It includes commands for working with MS-DOS
files: mdir, mcd, mcopy, and mformat.

XDF support for OS/2 is also provided.

%package doc
License:        GPL-3.0+ and GFDL-1.3
Summary:        Access Files on an MS-DOS File System
Group:          System/File Systems
Requires:       %{name} = %{version}

%description doc
Mtools allows uncomplicated access to an MS-DOS file system on disk
without mounting it. It includes commands for working with MS-DOS
files: mdir, mcd, mcopy, and mformat.

XDF support for OS/2 is also provided.

%prep
%setup -q
cp %{SOURCE1001} .

%build
autoconf --force
export INSTALL_PROGRAM="install"
export CPPFLAGS="$CPPFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"
%configure \
    --includedir=/usr/src/linux/include

%install
install -d -m 755 %{buildroot}%{_sysconfdir}
%make_install
cp -p mtools.conf %{buildroot}%{_sysconfdir}

rm -rf %{buildroot}%{_mandir}/man?*/f*
rm -rf %{buildroot}%{_bindir}/f*

%docs_package

%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%config %{_sysconfdir}/mtools.conf
%{_bindir}/*
