Name:       org.tizen.Apps
Summary:    org.tizen.Apps
Version:    1.0.6
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define apps_name org.tizen.Apps
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk

%description
profile/iot/apps/dotnet/tray
This is the application to access all installed apps in the device

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_tpk_path}
install packaging/%{apps_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/

%post

%files
%defattr(-,root,root,-)
%{preload_tpk_path}/*
%license LICENSE