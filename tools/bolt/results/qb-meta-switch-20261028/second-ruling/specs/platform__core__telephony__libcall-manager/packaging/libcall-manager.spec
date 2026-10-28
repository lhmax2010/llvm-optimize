%define major 0
%define minor 6
%define patchlevel 0
%define ext_feature 0

Name:           libcall-manager
Version:        %{major}.%{minor}.%{patchlevel}
Release:        1
License:        Apache-2.0
Summary:        Call Manager library
Group:          System/Libraries
Source0:        %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(capi-system-device)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-info)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Call Manager Library

%package devel
Summary: Call Manager API library (devel)
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Call Manager API library (devel)

%prep
%setup -q

%build
export LDFLAGS+=" -Wl,-z,nodelete "

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DVERSION=%{version} \
-DLIB_INSTALL_DIR=%{_libdir} \
%if 0%{?ext_feature}
-D_ENABLE_EXT_FEATURE:BOOL=ON \
%else
-D_ENABLE_EXT_FEATURE:BOOL=OFF \
%endif

make %{?_smp_mflags}

%install
%make_install

# Provides so file of 2.4 to support backward compatibility
ln -s libcall-manager.so %{buildroot}%{_libdir}/libcallmgr_client.so

%post

%postun -p /sbin/ldconfig

%files
%manifest libcall-manager.manifest
%defattr(644,root,root,-)
%license LICENSE
##%attr(755,root,root) %{_bindir}/cm-test
%{_libdir}/*.so.*
%{_libdir}/libcallmgr_client.so

%files devel
# callmgr client
%defattr(644,root,root,-)
%{_libdir}/libcall-manager.so
%{_libdir}/libcallmgr_client.so
%{_includedir}/call-manager/*
%{_libdir}/pkgconfig/callmgr_client.pc

