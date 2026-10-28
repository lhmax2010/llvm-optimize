Name:       org.tizen.systemui
Summary:    org.tizen.systemui
Version:    1.0.4
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend
Requires(post):  /usr/bin/unified-backend

%define systemui_name org.tizen.systemui
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk
%define popup_gadget_name org.tizen.SystemPopupGadget
%define popup_gadget_version 1.0.0
%define appselector_gadget_name org.tizen.app-selector
%define appselector_gadget_version 1.0.0
%define preload_rpk_path %{TZ_SYS_RO_APP}/.preload-rpk

%description
profile/iot/apps/dotnet/systemui
This is the application to access all installed apps in the device

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_tpk_path}
install packaging/%{systemui_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/
mkdir -p %{buildroot}/%{preload_rpk_path}
install packaging/%{popup_gadget_name}-%{popup_gadget_version}.rpk %{buildroot}/%{preload_rpk_path}/
install packaging/%{appselector_gadget_name}-%{appselector_gadget_version}.rpk %{buildroot}/%{preload_rpk_path}/

%post

%files
%defattr(-,root,root,-)
%{preload_tpk_path}/*
%{preload_rpk_path}/*
%license LICENSE
