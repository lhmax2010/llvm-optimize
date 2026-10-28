Name:       resource-manager
Summary:    Resource manager
Version:    0.1
Release:    7
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(resource-information)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(boost)
BuildRequires:  pkgconfig(gmock)

%define _pkgconfigdir %{_libdir}/pkgconfig
%define _packagedir %{_libdir}/%{name}
%define _includedir %{_libdir}/%{name}
%define _bindir %{_packagedir}

%define _utname resource-manager-ut

%description
This package manages the resources of Tizen device.

%package devel
Summary: Resource manager header files, static libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and static libraries
for Resource manager.

%prep

%setup -q

export EVK_TV=n
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

cmake . \
    -DCMAKE_INSTALL_PREFIX=%{_packagedir} \
    -DPACKAGE_NAME=%{name} \
    -DBINDIR=%{_bindir} \
    -DINCLUDEDIR=%{_includedir} \
    -DPKGCONFIG_INSTALL_DIR=%{_pkgconfigdir} \
    -DVERSION=%{version} \
    -DMAJORVERSION=${MAJORVER} \
    -DLIBDIR=%{_libdir} \
	-DRSCMGRPKGNAME=%{_utname} \
    -DTZ_SYS_RW_APP=%{TZ_SYS_RW_APP} \
	-DUNIT_TEST=1

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_bindir}/*
%manifest resource-manager.manifest
%license LICENSE.APLv2

%files devel
%defattr(-,root,root,-)
%{_pkgconfigdir}/resource-manager.pc
%{_includedir}/*.h
%{_libdir}/*.so
