%define debug_package %{nil}
Name:           hwdata
Version:        0.260
Release:        1
License:        GPL-2.0+
Summary:        Hardware identification and configuration data
Group:          System/Base
Source0:        %{name}-%{version}.tar.bz2
Url:            http://git.fedorahosted.org/git/hwdata.git
BuildArch:      noarch
Provides:	pciutils-ids
Source1001: 	hwdata.manifest

%package ivi
Summary:  IVI platform specific configurations files
Requires: %{name}


%description 
This package contains various platform specific configuration files.

%description ivi
This package contains various IVI specific configuration files.

%prep
%setup -q -n hwdata-%{version}-1

%build
%configure
cp %{SOURCE1001} .


%install
%make_install
%{__mkdir_p} %{buildroot}%{_sysconfdir}/modprobe.d
mv %{buildroot}%{_libdir}/modprobe.d/dist-blacklist.conf \
   %{buildroot}%{_sysconfdir}/modprobe.d/blacklist.conf
rm -rf %{buildroot}%{_libdir}
install -m644 blacklist.conf %{buildroot}/%{_sysconfdir}/modprobe.d
install -m644 video.conf %{buildroot}/%{_sysconfdir}/modprobe.d


%files
%manifest %{name}.manifest
%license COPYING
%config(noreplace) %{_sysconfdir}/modprobe.d/blacklist.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files ivi
%config(noreplace)%{_sysconfdir}/modprobe.d/video.conf
