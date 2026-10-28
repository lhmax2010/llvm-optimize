%if 0%{?debug:1}
%define debug_package %{nil}
%define __debug_install_post %{nil}
%endif

Name:       libnice
Summary:    Library for implementing Interactive Connectivity Establishment (ICE) standard (RFC 5245 & RFC 8445)
Version:    0.1.22
Release:    2
Group:      Multimedia/Libraries
License:    LGPL-2.1
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: meson >= 0.52.0
BuildRequires: pkgconfig(glib-2.0) >= 2.32.0
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(dlog)

%description
Library for implementing Interactive Connectivity Establishment (ICE) standard (RFC 5245 & RFC 8445)

%package devel
Summary:    nice headers and libraries for development.
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
nice headers and libraries for development.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
meson --auto-features=disabled --prefix=/usr --libdir=%{_libdir} --datadir=%{_datadir} build
ninja -C build

%install
rm -rf %{buildroot}
export DESTDIR=%{buildroot}
ninja -C build install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
#enable below if 'stun_tools' meson option is enabled
#%{_bindir}/*
%{_libdir}/*.so.*
%license COPYING.LGPL

%files devel
%manifest %{name}.manifest
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/nice/*.h
%{_includedir}/stun/*.h
%{_includedir}/stun/usages/*.h
%exclude /usr/include/stun/win32_common.h
