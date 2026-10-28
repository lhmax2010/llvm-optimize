Name:       capi-network-mdg
Summary:    Multi Device Group CAPI
Version:    0.1.1
Release:    0
Group:      Network & Connectivity/Other
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(capi-system-info)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Multi Device Group API library
Group:    Network & Connectivity/Other
Requires: %{name} = %{version}-%{release}

%package devel
Summary:  Multi Device Group API library (development library)
Group:    Network & Connectivity/Other
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the development files for %{name} API library.

%prep
%setup #-q
chmod g-w %_sourcedir/*
cp %{SOURCE1} ./%{name}.manifest

%build
CFLAGS=$(echo $CFLAGS | sed 's/-O2/-O0/' | sed 's/-O1/-O0/' | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')
CXXFLAGS=$(echo $CXXFLAGS | sed 's/-O2/-O0/' | sed 's/-O1/-O0/' | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%define NETWORK_FW_DATADIR %{TZ_SYS_GLOBALUSER_DATA}/network
%define DBDIR %{TZ_SYS_GLOBALUSER_DATA}/

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DBIN_INSTALL_DIR=%{_bindir} \
	-DINCLUDE_INSTALL_DIR=%{_includedir} \
	-DLIB_PATH=%{_lib} \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DNETWORK_FW_DATADIR=%{NETWORK_FW_DATADIR} \
	-DDBDIR=%{DBDIR} \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}/BUILD/%{name}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.APLv2
%attr(644,-,-) %{_libdir}/lib%{name}.so*

%files devel
%defattr(-,root,root,-)
%attr(644,-,-) %{_libdir}/lib%{name}.so*
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*.h
%attr(777,network_fw,network_fw) %{_bindir}/mdg-test
