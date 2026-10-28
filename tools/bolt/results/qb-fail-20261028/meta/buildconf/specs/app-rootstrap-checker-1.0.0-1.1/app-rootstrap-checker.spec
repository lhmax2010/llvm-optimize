%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

%if "%{tizen_profile_name}" == "tv"
%define WITH_VD 1
%else
%define WITH_VD 0
%endif

%if "%{WITH_VD}" == "0" && "%{WITH_DA}" == "0"
%define WITH_SR 1
%else
%define WITH_SR 0
%endif

Name:		app-rootstrap-checker
VCS:   platform/core/system/app-rootstrap-checker#104e9b3bbb999761e89e337c391975438a55b608
Summary:	Package for app rootstrap checker
Version:	1.0.0
Release:	1.1
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1:	app-rootstrap-checker.manifest
Source2:	app-rootstrap-checker.sh
Source4:	macros.app-rootstrap-checker

#!BuildIgnore: app-rootstrap-checker

%description
Package for app rootstrap checker

%prep
%setup -q
cp %{SOURCE1} .

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/app-rootstrap
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/app-rootstrap

%if "%{WITH_SR}" == "1"
mkdir -p %{buildroot}%{_sysconfdir}/app-rootstrap/default.rules.d
install -m 644 rules/default.rules.d/*.yaml %{buildroot}%{_sysconfdir}/app-rootstrap/default.rules.d
%else
%if "%{WITH_DA}" == "1"
mkdir -p %{buildroot}%{_sysconfdir}/app-rootstrap/rules.d
install -m 644 rules/da.rules.d/*.yaml %{buildroot}%{_sysconfdir}/app-rootstrap/rules.d
%else
%if "%{WITH_VD}" == "1"
mkdir -p %{buildroot}%{_sysconfdir}/app-rootstrap/rules.d
ls rules/vd.rules.d/*.yaml >/dev/null 2>&1 && install -m 644 rules/vd.rules.d/*.yaml %{buildroot}%{_sysconfdir}/app-rootstrap/rules.d
%endif
%endif
%endif

mkdir -p %{buildroot}%{_sysconfdir}/rpm
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/rpm

%files
%manifest %{name}.manifest
%{_sysconfdir}/app-rootstrap/app-rootstrap-checker.sh
%if "%{WITH_SR}" == "1"
%{_sysconfdir}/app-rootstrap/default.rules.d/*.yaml
%else
%if "%{WITH_DA}" == "1"
%{_sysconfdir}/app-rootstrap/rules.d/*.yaml
%else
%if "%{WITH_VD}" == "1"
%{_sysconfdir}/app-rootstrap/rules.d
%endif
%endif
%endif
%{_sysconfdir}/rpm/macros.app-rootstrap-checker
