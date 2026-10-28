Name:       org.tizen.MusicPlayer
Summary:    org.tizen.MusicPlayer
Version:    1.0.5
Release:    1
Group:      N/A
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define internal_name org.tizen.MusicPlayer
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk

%description
profile/iot/apps/dotnet/music-player
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
