Name:		default-ac-domains
VCS:   platform/core/security/default-ac-domains#ece8b054ef76fd0e60f1fd3b0166caf3523abb62
Version:	0.2
Release:	1.1
Group:		Security/Access Control
License:	GPL-2.0
Summary:	The definition of default ac domains
Source0:	%{name}-%{version}.tar.gz
Source1001:	default-ac-domains.manifest
Source1002:	default-ac-domains-uid-app-sandboxing.manifest

%description
The package provides a definition for the default set of ac domains
with the corresponding Smack rules between them

%prep
%setup -q

%build
%if "%{?uid_app_sandboxing}" == "1"
cp %{SOURCE1002} ./default-ac-domains.manifest
%else
cp %{SOURCE1001} .
%endif

%install

%files
%defattr(-,root,root)
%manifest default-ac-domains.manifest
%license COPYING

%changelog
* Tue Jun  4 2013 Elena Reshetova <elena.reshetova@intel.com>
- Initial package creation for domains System and User
