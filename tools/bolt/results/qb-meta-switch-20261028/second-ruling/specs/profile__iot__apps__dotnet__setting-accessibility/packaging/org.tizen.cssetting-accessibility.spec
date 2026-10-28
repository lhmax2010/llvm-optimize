Name:       org.tizen.cssetting-accessibility
Summary:    org.tizen.cssetting-accessibility
Version:    1.1.0
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 riscv64

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define preload_rpk_path %{TZ_SYS_RO_APP}/.preload-rpk

%description
NUI Setting Application for Accessibility.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_rpk_path}
install packaging/%{name}-%{version}.rpk %{buildroot}/%{preload_rpk_path}/

%post

%files
%defattr(-,root,root,-)
%{preload_rpk_path}/*
