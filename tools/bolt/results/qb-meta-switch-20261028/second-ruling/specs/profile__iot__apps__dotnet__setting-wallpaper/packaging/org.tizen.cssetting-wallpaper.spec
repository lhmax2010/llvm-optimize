Name:		org.tizen.cssetting-wallpaper
summary:	NUI wallpaper setting application
Version:	1.0.1
Release:	1
Provides:	org.tizen.cssetting-wallpaper = %{version}-%{release}
Group:		Applications/Security
License:	Apache-2.0
Source0:    %{name}-%{version}.tar.gz

Requires(post): /usr/bin/pkgcmd
Requires(post): /usr/sbin/cyad

%description
NUI application for managing wallpaper functionalities

%define rpk_pkgid org.tizen.cssetting-wallpaper
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
#pkgcmd -it rpk -p %{preload_rpk_path}/%{rpk_pkgid}-%{version}.rpk

cyad -s -k MANIFESTS_GLOBAL -c User::Pkg::%{rpk_pkgid} -u 5001 -p http://tizen.org/privilege/notexist -t ALLOW

# Uncomment following lines to test preload rpk installation on image creation
#pkg_initdb --ro
#install_preload_pkg

%files
%defattr(-,root,root,-)
%{preload_rpk_path}/*
