Name:		org.tizen.setting-wifi-direct
summary:	NUI wifi-direct setting application
Version:	1.0.10
Release:	1
Provides:	org.tizen.setting-wifi-direct = %{version}-%{release}
Group:		Applications/Security
License:	Apache-2.0
Source0:    %{name}-%{version}.tar.gz

Requires(post): /usr/bin/pkgcmd
Requires(post): /usr/sbin/cyad

%description
NUI application for managing wifi-direct functionalities

%define rpk_pkgid org.tizen.cssetting-wifi-direct
%define preload_rpk_path /usr/apps/.preload-rpk

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{preload_rpk_path}
install packaging/%{rpk_pkgid}-%{version}.rpk %{buildroot}/%{preload_rpk_path}/

%post
# Uncomment following lines to test rpk installation
#unified-back
#unified-backend --preload -i %{preload_rpk_path}/%{rpk_pkgid}-%{version}.rpk

# Uncomment following lines to test preload rpk installation on image creation
#pkg_initdb --ro
#install_preload_pkg

%files
%defattr(-,root,root,-)
%{preload_rpk_path}/*
