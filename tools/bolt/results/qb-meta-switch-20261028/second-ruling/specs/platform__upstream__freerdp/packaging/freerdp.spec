%bcond_with x
%bcond_with wayland

Name:           freerdp
Version:        2.3.2
Release:        0
Summary:        Remote Desktop Protocol functionality
License:        Apache-2.0
Group:          Graphics & UI Framework/Development
Url:            http://www.freerdp.com/

Source0:         %name-%version.tar.xz
Source1: 	freerdp.manifest
BuildRequires:	cmake
BuildRequires:  libtool >= 2.2
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  libopenssl3-devel
%if %{with wayland}
BuildRequires:  pkgconfig(wayland-client)
%endif
%if %{with x}
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xv)
%endif

%description
FreeRDP is a free implementation of the Remote Desktop Protocol (RDP)
according to the Microsoft Open Specifications.

%package devel
Summary: Development files for package %{name}
Group:   Graphics & UI Framework/Development
Requires: freerdp = %{version}-%{release}
%description devel
This package provides header files and other developer related files
for package %{name}.

%prep
%setup -q
cp %{SOURCE1} .

%build
cmake \
        -DWITH_CLIENT:BOOL=ON \
%if %{with wayland}
        -DWITH_WAYLAND:BOOL=ON \
%else
        -DWITH_WAYLAND:BOOL=OFF \
%endif
%if %{with x}
        -DWITH_X11:BOOL=ON \
%else
        -DWITH_X11:BOOL=OFF \
%endif
%ifarch aarch64
        -DWITH_NEON:BOOL=OFF \
%endif
        -DWITH_SERVER:BOOL=ON \
        -DWITH_ALSA:BOOL=ON \
        -DWITH_SSE2:BOOL=OFF \
        -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON \
	-DCMAKE_INSTALL_PREFIX:PATH=/usr \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp
cp include/freerdp/*.h $RPM_BUILD_ROOT/usr/include/freerdp
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/cache
cp include/freerdp/cache/*.h $RPM_BUILD_ROOT/usr/include/freerdp/cache
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/channels
cp include/freerdp/channels/*.h $RPM_BUILD_ROOT/usr/include/freerdp/channels
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/client
cp include/freerdp/client/*.h $RPM_BUILD_ROOT/usr/include/freerdp/client
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/codec
cp include/freerdp/codec/*.h $RPM_BUILD_ROOT/usr/include/freerdp/codec
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/crypto
cp include/freerdp/crypto/*.h $RPM_BUILD_ROOT/usr/include/freerdp/crypto
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/gdi
cp include/freerdp/gdi/*.h $RPM_BUILD_ROOT/usr/include/freerdp/gdi
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/locale
cp include/freerdp/locale/*.h $RPM_BUILD_ROOT/usr/include/freerdp/locale
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/server
cp include/freerdp/server/*.h $RPM_BUILD_ROOT/usr/include/freerdp/server
mkdir -p $RPM_BUILD_ROOT/usr/include/freerdp/utils
cp include/freerdp/utils/*.h $RPM_BUILD_ROOT/usr/include/freerdp/utils

mkdir -p $RPM_BUILD_ROOT/usr/include/winpr
cp winpr/include/winpr/*.h $RPM_BUILD_ROOT/usr/include/winpr
mkdir -p $RPM_BUILD_ROOT/usr/include/winpr/tools
cp winpr/include/winpr/tools/makecert.h $RPM_BUILD_ROOT/usr/include/winpr/tools


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
%{_libdir}/lib*.so.*
%{_bindir}/freerdp-proxy*
%{_bindir}/freerdp-shadow-cli*
%{_bindir}/winpr-hash*
%{_bindir}/winpr-makecert*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/freerdp*.pc
%{_libdir}/pkgconfig/winpr*.pc
%{_includedir}/freerdp
%{_includedir}/winpr

%changelog
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0
