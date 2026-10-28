Name:       org.tizen.askuser-popup-profile_iot
Summary:    Askuser privacy popup for IoT
Version:    3.0.0
Release:    0
Group:      Applications/Security
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires: pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define tpk_name org.tizen.askuser-privacy-popup
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk

%description
Application providing ui for requesting privacy permission from the user.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_tpk_path}

install %{tpk_name}-%{version}.tpk %{buildroot}/%{preload_tpk_path}/

%files
%defattr(-,root,root,-)
%{preload_tpk_path}/*
%license LICENSE
