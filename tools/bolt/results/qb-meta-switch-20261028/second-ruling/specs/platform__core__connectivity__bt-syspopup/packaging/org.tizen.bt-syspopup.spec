Name: org.tizen.bt-syspopup
Summary: Bluetooth System Popup application
Version: 1.0.0
Release: 1
Group: App/Bluetooth
License: Flora-1.1
Source0: %{name}-%{version}.tar.gz

%description
Bluetooth System Popup application
Handles Bluetooth-related system popups including:
PIN request, passkey confirmation, device authorization,
visibility mode, and Bluetooth enable/reset requests.

%package profile_common
Provides: %{name}-compat = %{version}-%{release}
Summary: bt-syspopup binary for common

%description profile_common
Bluetooth System Popup application
Handles Bluetooth-related system popups including:
PIN request, passkey confirmation, device authorization,
visibility mode, and Bluetooth enable/reset requests.

%define tpk_pkgid org.tizen.bt-syspopup
%define preload_tpk_path /usr/apps/.preload-tpk

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{preload_tpk_path}
install packaging/%{tpk_pkgid}-%{version}.tpk %{buildroot}%{preload_tpk_path}/

%files
%defattr(-,root,root,-)
%{preload_tpk_path}/*
%license LICENSE

%files profile_common
