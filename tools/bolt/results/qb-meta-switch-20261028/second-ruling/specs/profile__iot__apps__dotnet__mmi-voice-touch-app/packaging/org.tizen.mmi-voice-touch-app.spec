Name:       org.tizen.mmi-voice-touch-app
Summary:    org.tizen.mmi-voice-touch-app
Version:    1.0.1
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define internal_name org.tizen.voice-touch
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk

%description
This application is a mmi-voice-touch-app which is NUI reference application

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
%license COPYING
%{preload_tpk_path}/*