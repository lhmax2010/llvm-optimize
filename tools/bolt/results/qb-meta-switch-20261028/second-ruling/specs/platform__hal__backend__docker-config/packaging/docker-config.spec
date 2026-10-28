Name:       hal-backend-docker-config
Summary:    Hal backend docker configuration package
Version:    0.1.0
Release:    0
Group:      Tools/Docker
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

%description
Hal backend docker configuration package including json files.

%package rpi4
Summary: Hal backend docker configuration package for rpi4 target
Group: Tools/Docker
License: Apache-2.0

%description rpi4
Hal backend docker configuration package including json files for rpi4 target.

%prep
%setup -q -n %{name}-%{version}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_hal_datadir}

mkdir -p %{buildroot}%{_hal_licensedir}/%{name}-rpi4
cp LICENSE %{buildroot}%{_hal_licensedir}/%{name}-rpi4
mkdir -p %{buildroot}%{_hal_datadir}/%{name}-rpi4
cp -arf %{name}-rpi4/* %{buildroot}%{_hal_datadir}/%{name}-rpi4

%post rpi4
cp -arf %{_hal_datadir}/%{name}-rpi4/* /
rm -rf %{_hal_datadir}/%{name}-rpi4

%preun rpi4
rm -rf %{_hal_sysconfdir}/docker

%postun

%files rpi4
%manifest %{name}-rpi4.manifest
%{_hal_licensedir}/%{name}-rpi4/*
%defattr(-,root,root,-)
%{_hal_datadir}/%{name}-rpi4%{_hal_sysconfdir}/docker/*
