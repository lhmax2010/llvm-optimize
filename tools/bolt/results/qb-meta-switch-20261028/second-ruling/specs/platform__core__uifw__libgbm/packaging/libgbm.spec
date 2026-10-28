%define MAJOR_VER	1
%define MINOR_VER	1

Summary:	Wayland GBM for TIZEN
Name:		libgbm
Version:	%{MAJOR_VER}.%{MINOR_VER}.1
Release:	1
Group:		System/Libraries
License:	MIT
Source:		%{name}-%{version}.tar.gz

BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: systemd-devel
BuildRequires: pkgconfig(libdrm)

%description
Wayland Generic Buffer Management for TIZEN

%package devel
Summary:    Development header files for use with GBM
Group:      System/Libraries
Requires:   %{name}

%description devel
Development header files for use with Wayland GBM

%prep
%setup -q -n %{name}

%build
%reconfigure --disable-static \
            --with-backends-path=%{_hal_libdir}/gbm \
            CFLAGS="${CFLAGS} -Wall -Werror" LIBDIR=%{_libdir}
make libdir=%{_libdir} major_ver=%{MAJOR_VER} minor_ver=%{MINOR_VER}

%install
%makeinstall major_ver=%{MAJOR_VER} minor_ver=%{MINOR_VER}
rm -f %{buildroot}/%{_libdir}/*.la

ln -sf libgbm.so.%{MAJOR_VER}.%{MINOR_VER}.0	%{buildroot}%{_libdir}/libgbm.so.%{MAJOR_VER}
ln -sf libgbm.so.%{MAJOR_VER}			%{buildroot}%{_libdir}/libgbm.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest packaging/libgbm.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/libgbm.so*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gbm.h
%{_includedir}/gbmint.h
%{_libdir}/pkgconfig/gbm.pc
%{_libdir}/libgbm.so
