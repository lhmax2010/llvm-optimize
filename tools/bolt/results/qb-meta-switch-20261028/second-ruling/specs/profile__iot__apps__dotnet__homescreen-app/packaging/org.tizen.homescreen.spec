Name:       org.tizen.homescreen
Summary:    org.tizen.homescreen
Version:    1.0.0
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 riscv64

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define internal_name org.tizen.homescreen
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk


%description
This application is used to set homescreen wallpaper for the system.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_tpk_path}
mkdir -p %{buildroot}/%{TZ_SYS_DATA}/settings/

%ifarch %{ix86} riscv64
install packaging/%{internal_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/
%endif

%ifarch x86_64
install packaging/x64/%{internal_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/
%endif

%ifarch %{arm}
install packaging/arm/%{internal_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/
%endif

%ifarch aarch64
install packaging/arm64/%{internal_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/
%endif

cp -r packaging/media/settings %{buildroot}%{TZ_SYS_DATA}/

%files
%defattr(-,root,root,-)
%{preload_tpk_path}/*
%{TZ_SYS_DATA}/settings/*
%license LICENSE