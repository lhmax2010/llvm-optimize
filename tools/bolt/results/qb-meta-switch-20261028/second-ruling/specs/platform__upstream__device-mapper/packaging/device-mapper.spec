%define libdevice_mapper_version 1.02.196
%define lvm2_version 2_03_22

Name:           device-mapper
Version:        %{libdevice_mapper_version}
Release:        1
License:        GPL-2.0+
Summary:        Device mapper utility
Url:            http://sources.redhat.com/dm
Group:          Base/Device Management
Source0:        ftp://sources.redhat.com/pub/lvm2/lvm2-v%{lvm2_version}.tar.gz
Source101:      99-dm-tizen.rules
Source1001:     device-mapper.manifest
BuildRequires:  pkgconfig(libsystemd)

%description
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%package devel
License:        LGPL-2.1+
Summary:        Development libraries and headers for device-mapper
Group:          Development/Libraries
Requires:       libdevmapper = %{libdevice_mapper_version}-%{release}

%description devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%package -n libdevmapper
License:        LGPL-2.1+
Summary:        Device-mapper shared library
Group:          Base/Device Management
Obsoletes:      device-mapper < 1.02.17-6

%description -n libdevmapper
This package contains the device-mapper shared library, libdevmapper.

%global udev_dir %{_prefix}/lib/udev/rules.d

%prep
%setup -q -n lvm2-v2_03_22
cp %{SOURCE101} .
cp %{SOURCE1001} .

%build
%define _exec_prefix ""
%configure --with-user= \
           --with-group= \
           --with-device-uid=0 \
           --with-device-gid=6 \
           --with-device-mode=0660 \
           --enable-pkgconfig \
           --enable-udev_rules \
           --with-udevdir=%{udev_dir} \
           --enable-udev_sync

%define _exec_prefix /
make CFLAGS+=" -fPIC " LDFLAGS+=" -pie " V=1 \
     device-mapper

%install
make install_device-mapper DESTDIR=%{buildroot} usrlibdir=%{buildroot}/usr/%{_lib}
sed -i 's/ (.*)//g' %{buildroot}%{_libdir}/pkgconfig/*.pc
install -m644 99-dm-tizen.rules %{buildroot}/%{udev_dir}/99-dm-tizen.rules
rm -rf %{buildroot}/usr/share/man


%post -n libdevmapper -p /sbin/ldconfig

%postun -n libdevmapper -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING COPYING.LIB
%attr(755,root,root) %{_sbindir}/dmsetup
%attr(755,root,root) %{_sbindir}/blkdeactivate
%attr(755,root,root) %{_sbindir}/dmstats
%attr(644,-,-) %{udev_dir}/*.rules

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/*.pc

%files -n libdevmapper
%manifest %{name}.manifest
%license COPYING.LIB
%attr(755,root,root) %{_libdir}/libdevmapper.so.*
