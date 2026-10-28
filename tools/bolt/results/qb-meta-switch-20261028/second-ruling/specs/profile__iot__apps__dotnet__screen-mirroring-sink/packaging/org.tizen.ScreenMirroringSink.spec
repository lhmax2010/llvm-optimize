Name:       org.tizen.ScreenMirroringSink
Summary:    org.tizen.ScreenMirroringSink
Version:    1.0.0
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz


BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define internal_name org.tizen.ScreenMirroringSink
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk

%description
profile/iot/apps/dotnet/screen-mirroring-sink
This is a container package which have preload TPK/WGT files

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

