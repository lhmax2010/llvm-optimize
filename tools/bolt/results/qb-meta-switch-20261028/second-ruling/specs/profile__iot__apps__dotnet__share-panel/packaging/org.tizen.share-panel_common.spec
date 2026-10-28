Name:       org.tizen.share-panel_common
Summary:    org.tizen.share-panel
Version:    2.0.1
Release:    0
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 riscv64

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define internal_name org.tizen.share-panel_common
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk

%description
profile/iot/apps/dotnet/share-panel
This application is used to share files through bluetooth.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_tpk_path}
install packaging/%{internal_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/

%post

%files
%defattr(-,root,root,-)
%{preload_tpk_path}/*
%license LICENSE
