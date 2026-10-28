%define _unpackaged_files_terminate_build 0

Name:       pcsc-lite
Summary:    pcsc-lite
Version:    0.1.2
Release:    0
Group:      Network & Connectivity/Common
License:    3-clause BSD License
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(udev)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
pcsc-lite Usb driver

%package devel
Summary:  pcsc-lite API library (development library)
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the development files for %{name} API library.

%prep
%setup -q
chmod 644 %{SOURCE0}
cp %{SOURCE1} ./%{name}.manifest

%build

aclocal
autoconf
automake
./configure --prefix=/usr --with-systemdsystemunitdir=%{_unitdir}
make %{?_smp_mflags}

%install

%make_install

mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants

cp etc/pcscd.service %{buildroot}%{_unitdir}/basic.target.wants
cp etc/pcscd.socket %{buildroot}%{_unitdir}/sockets.target.wants


mkdir -p %{buildroot}%{_sbindir}/
cp src/pcscd %{buildroot}%{_sbindir}/

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp src/libpcsclite.pc %{buildroot}%{_libdir}/pkgconfig

mkdir -p %{buildroot}%{_includedir}/PCSC/
cp src/PCSC/*.h %{buildroot}%{_includedir}/PCSC/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root,-)
%attr(644,-,-) /usr/lib/libpcsclite.so.*
%{_sbindir}/pcscd
%{_unitdir}/*

%files devel
%defattr(-,root,root,-)
%attr(644,-,-) /usr/lib/libpcsclite.so
%{_libdir}/pkgconfig/libpcsclite.pc
%{_includedir}/PCSC/*.h
