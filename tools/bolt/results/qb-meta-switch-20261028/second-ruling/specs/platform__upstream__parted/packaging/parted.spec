%define _sbindir /sbin

Name:           parted
Version:        3.6
Release:        1
License:        GPL-3.0+
Summary:        The GNU disk partition manipulation program
Url:            http://www.gnu.org/software/parted
Group:          Applications/System

Source0:        %{name}-%{version}.tar.gz
Source1001: 	parted.manifest

BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  libuuid-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  texinfo
BuildRequires:  pkgconfig(ext2fs)

%description
The GNU Parted program allows you to create, destroy, resize, move,
and copy hard disk partitions. Parted can be used for creating space
for new operating systems, reorganizing disk usage, and copying data
to new hard disks.

%package devel
Summary:        Files for developing apps which will manipulate disk partitions
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       pkgconfig

%description devel
The GNU Parted library is a set of routines for hard disk partition
manipulation. If you want to develop programs that manipulate disk
partitions and filesystems using the routines provided by the GNU
Parted library, you need to install this package.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"
%configure --disable-static --disable-device-mapper --with-readline --with-libdir=%{_libdir} --exec-prefix=/usr
make %{?_smp_mflags}

%install
%make_install

%find_lang %{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%lang_package

%docs_package

%files
%manifest %{name}.manifest
%license COPYING
%{_sbindir}/parted
%{_sbindir}/partprobe
%{_libdir}/libparted*.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/parted
%{_libdir}/libparted.so
%{_libdir}/libparted-fs-resize.so
%{_libdir}/pkgconfig/libparted.pc
%{_libdir}/pkgconfig/libparted-fs-resize.pc
