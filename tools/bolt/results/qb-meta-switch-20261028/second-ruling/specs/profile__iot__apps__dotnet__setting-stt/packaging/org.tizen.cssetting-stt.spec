Name:       org.tizen.cssetting-stt
Summary:    org.tizen.cssetting-stt
Version:    1.0.0
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 riscv64

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/unified-backend

%define internal_name org.tizen.cssetting-stt
%define preload_rpk_path %{TZ_SYS_RO_APP}/.preload-rpk

%description
This application is a NUI STT setting gadget.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_rpk_path}
install packaging/%{name}-%{version}.rpk %{buildroot}/%{preload_rpk_path}/

%post

%files
%license LICENSE
%defattr(-,root,root,-)
%{preload_rpk_path}/*
