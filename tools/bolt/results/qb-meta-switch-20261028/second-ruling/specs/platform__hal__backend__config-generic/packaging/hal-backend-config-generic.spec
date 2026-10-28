Name:		hal-backend-config-generic
Summary:	Package for hal backend configuration
Version:	0.0.1
Release:	1
License:	Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:	hal-backend-config-generic.manifest
Source2:	hal-backend-manifest.xml

%description
Package for hal backend configuration

%prep
%setup -q
cp %{SOURCE1} .

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_hal_sysconfdir}
cp %{SOURCE2} %{buildroot}%{_hal_sysconfdir}

%files
%manifest %{name}.manifest
%{_hal_sysconfdir}/hal-backend-manifest.xml
