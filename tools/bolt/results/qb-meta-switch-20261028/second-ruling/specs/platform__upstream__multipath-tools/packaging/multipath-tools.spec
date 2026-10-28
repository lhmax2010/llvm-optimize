Name:           multipath-tools
Url:            http://christophe.varoqui.free.fr/
Version:        0.13.0
Release:        0
Summary:        Tools to Manage Multipathed Devices with the device-mapper
License:        GPL-2.0-or-later and GPL-2.0-or-later
Group:          System/Base
Source:         multipath-tools-%{version}.tar.bz2
Source1001: 	multipath-tools.manifest

BuildRequires:  device-mapper-devel
BuildRequires:  libaio-devel
BuildRequires:  readline-devel

Requires:       device-mapper
Requires:       kpartx
Requires(pre):  coreutils grep

%description
This package provides the tools to manage multipathed devices by
instructing the device-mapper multipath module what to do. The tools
are:

- multipath: scans the system for multipathed devices, assembles
   them, and updates the device-mapper's maps

- multipathd: waits for maps events then execs multipath

- devmap-name: provides a meaningful device name to udev for devmaps

- kpartx: maps linear devmaps to device partitions, which makes
multipath maps partionable



%package -n kpartx
Summary:        Manages partition tables on device-mapper devices
Group:          System/Base
Requires:       device-mapper

%description -n kpartx
The kpartx program maps linear devmaps to device partitions, which
makes multipath maps partionable.

Authors:
--------
    Christophe Varoqui <christophe.varoqui@free.fr>

%prep
%setup -q -n multipath-tools-%{version}
cp %{SOURCE1001} .
%build
%{__make} -f create-config.mk

cd kpartx
export CFLAGS=$(echo ${CFLAGS} | sed -E "s/-Wp\,-D_FORTIFY_SOURCE=[0-9]//g")
export CXXFLAGS=$(echo ${CXXFLAGS} | sed -E "s/-Wp\,-D_FORTIFY_SOURCE=[0-9]//g")
export RPM_OPT_FLAGS=$(echo ${RPM_OPT_FLAGS} | sed -E "s/-Wp\,-D_FORTIFY_SOURCE=[0-9]//g")
%{__make} CC="%__cc" OPTFLAGS="$RPM_OPT_FLAGS" LIB=%_libdir

%install
( cd kpartx && %{__make} DESTDIR=$RPM_BUILD_ROOT LIB=%_libdir install )

%{remove_docs}


%clean
rm -rf $RPM_BUILD_ROOT;

%files
%manifest %{name}.manifest
%defattr(-,root,root)

%files -n kpartx
%manifest %{name}.manifest
%license COPYING
%config /usr/lib/udev/rules.d/*.rules
/sbin/kpartx
%dir /usr/lib/udev
/usr/lib/udev/kpartx_id
