Name:       org.tizen.installer
Summary:    application Installer
Version:    0.1.6
Release:    1
Group:      Application Framework/Notifications
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gettext-tools
BuildRequires:  edje-tools
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(ecore-file)
BuildRequires:  pkgconfig(appsvc)
BuildRequires:  pkgconfig(notification)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(elementary)
#BuildRequires:  pkgconfig(ui-extension)
BuildRequires:  pkgconfig(efl-extension)
BuildRequires:	pkgconfig(security-privilege-manager)
BuildRequires:  hash-signer
#Requires(post): signing-client

%description
SLP application Installer


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description devel
Development files for %{name}

%package service
Summary:	installer-service
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%description service
installer-service

%prep
%setup -q

%build
cmake . -DCMAKE_INSTALL_PREFIX=/usr
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
%define tizen_sign 1
%define tizen_sign_base %{_prefix}/apps/%{name}
%define tizen_sign_level platform
%define tizen_author_sign 1
%define tizen_dist_sign 1

%post

%files
%manifest %{name}.manifest
%{_prefix}/apps/%{name}/bin/*
%{_prefix}/apps/%{name}/res/edje/*
%{_prefix}/apps/%{name}/res/locale/*/*/*.mo
%{_datadir}/packages/%{name}.xml
#Signing
%{_prefix}/apps/%{name}/author-signature.xml
%{_prefix}/apps/%{name}/signature1.xml
%license LICENSE
