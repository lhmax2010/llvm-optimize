Summary:	Tizen Package Groups and Images Configurations
Name:		meta-generic
Version:	0
Release:	0
License:	GPL-2.0
Group:		Base/Configuration
URL:		http://www.tizen.org
Source:		%{name}-%{version}.tar.bz2
Source1001: 	meta-generic.manifest
BuildArch:      noarch

%description
Tizen Package Groups and Image Configurations for Base OS


%package adaptation
Summary:  Hardware adataption configuration files
BuildArch:      noarch

%description adaptation
Hardware adaptation tweaks to ship inside image

%prep
%setup -q
cp %{SOURCE1001} .

%build
make

%install
%make_install


%files
%manifest %{name}.manifest
%attr(644,-,-) %{_datadir}/package-groups/generic/*.yaml
%{_datadir}/image-configurations/generic/scripts


%files adaptation
%{_sysconfdir}/profile.d/generic-adaptation.sh

