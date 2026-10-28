Name:       org.tizen.notifications
Summary:    org.tizen.notifications
Version:    1.0.4
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define app_name org.tizen.notifications
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk

%description
profile/iot/apps/dotnet/notifications
This is the application to show the current notifications on the device

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_tpk_path}
install packaging/%{app_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/

%post

%files
%defattr(-,root,root,-)
%{preload_tpk_path}/*
%license LICENSE