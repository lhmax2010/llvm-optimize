Name:       org.tizen.volume
Summary:    org.tizen.volume
Version:    2.0.4
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/unified-backend

%define apps_name org.tizen.VolumeGadget
%define preload_rpk_path %{TZ_SYS_RO_APP}/.preload-rpk

%description
profile/iot/apps/dotnet/volume-app
This is the application to control the system volume.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_rpk_path}
install packaging/%{apps_name}-%{version}.rpk %{buildroot}/%{preload_rpk_path}/

%post

%files
%defattr(-,root,root,-)
%{preload_rpk_path}/*
%license LICENSE
