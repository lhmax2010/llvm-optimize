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

%if "%{?with_abi_check}" == "1"
%define WITH_ABI_CHECK 1
%else
%define WITH_ABI_CHECK 0
%endif

Name:		hal-rootstrap-checker
Summary:	Package for hal rootstrap checker
Version:	1.0.0
Release:	5
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1:	hal-rootstrap-checker.manifest
Source2:	hal-rootstrap-checker.sh
Source4:	macros.hal-rootstrap-checker
Source5:	hal-rootstrap-abi-gate.sh
Source6:	hal-rootstrap-download-rpm.pl

# Disable automatic dependency generation
AutoReqProv:	no

# System ABI tools dependency (controlled by WITH_ABI_CHECK)
%if "%{WITH_ABI_CHECK}" == "1"
Requires:       ctags
Requires:       abi-compliance-checker
Requires:       abi-dumper
Requires:       vtable-dumper
Requires:       abi-tracker
Requires:       perl
%endif

#!BuildIgnore: hal-rootstrap-checker

%description
Package for hal rootstrap checker

%prep
%setup -q
cp %{SOURCE1} .

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/hal/rootstrap
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/hal/rootstrap
install -m 755 %{SOURCE5} %{buildroot}%{_sysconfdir}/hal/rootstrap
install -m 755 %{SOURCE6} %{buildroot}%{_sysconfdir}/hal/rootstrap
mkdir -p %{buildroot}%{_sysconfdir}/hal/rootstrap/rules.d/acr

%if "%{WITH_SR}" == "1"
mkdir -p %{buildroot}%{_sysconfdir}/hal/rootstrap/default.rules.d
install -m 644 rules/default.rules.d/*.yaml %{buildroot}%{_sysconfdir}/hal/rootstrap/default.rules.d
%else
%if "%{WITH_DA}" == "1"
mkdir -p %{buildroot}%{_sysconfdir}/hal/rootstrap/rules.d
install -m 644 rules/da.rules.d/*.yaml %{buildroot}%{_sysconfdir}/hal/rootstrap/rules.d
%else
%if "%{WITH_VD}" == "1"
mkdir -p %{buildroot}%{_sysconfdir}/hal/rootstrap/rules.d
install -m 644 rules/vd.rules.d/*.yaml %{buildroot}%{_sysconfdir}/hal/rootstrap/rules.d
%endif
%endif
%endif

mkdir -p %{buildroot}%{_sysconfdir}/rpm
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/rpm

%files
%manifest %{name}.manifest
%{_sysconfdir}/hal/rootstrap/hal-rootstrap-checker.sh
%{_sysconfdir}/hal/rootstrap/hal-rootstrap-abi-gate.sh
%{_sysconfdir}/hal/rootstrap/hal-rootstrap-download-rpm.pl
%dir %{_sysconfdir}/hal/rootstrap/rules.d/acr
%if "%{WITH_SR}" == "1"
%{_sysconfdir}/hal/rootstrap/default.rules.d/*.yaml
%else
%if "%{WITH_DA}" == "1"
%{_sysconfdir}/hal/rootstrap/rules.d/*.yaml
%else
%if "%{WITH_VD}" == "1"
%{_sysconfdir}/hal/rootstrap/rules.d/*.yaml
%endif
%endif
%endif
%{_sysconfdir}/rpm/macros.hal-rootstrap-checker