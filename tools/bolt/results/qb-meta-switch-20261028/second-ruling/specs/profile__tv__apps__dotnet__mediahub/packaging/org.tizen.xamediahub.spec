Name:       org.tizen.xamediahub
Summary:    mediahub application
Version:    1.0.0
Release:    1
Group:      Applications
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(libtzplatform-config)
Requires(post):  /usr/bin/tpk-backend

%define internal_name org.tizen.xamediahub
%define preload_tpk_path %{TZ_SYS_RO_APP}/.preload-tpk

%define build_mode %{nil}

%ifarch arm armv7l
%define target arm
%endif
%ifarch aarch64
%define target aarch64
%endif
%ifarch x86_64
%define target x86_64
%endif
%ifarch i386 i486 i586 i686
%define target i386
%endif
%description
This is a container package which includes preloaded application package as the TPK file format.
During installation of this package, the preloaded application package would be dropped into a specific folder.
The folder will be searched by the system and the system will install the TPK files in the folder automatically.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{preload_tpk_path}
install TVMediaHub/TVMediaHub.Tizen/bin/Debug/TVMediaHub.Tizen.tpk %{buildroot}%{preload_tpk_path}/

%post

%files
%defattr(-,root,root,-)
%{preload_tpk_path}/*.tpk
