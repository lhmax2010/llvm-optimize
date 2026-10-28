%if %{defined profile}
%define _profile %profile
%else
%define _profile base
%endif

%if "%{?profile}" == "mobile" || "%{?profile}" == "wearable" || "%{?profile}"=="tv" || "%{?profile}" == "ivi" || "%{?profile}" == "common"
%define _with_legacy_imageconfig 1
%endif
%bcond_with legacy_imageconfig

Summary:	Tizen Package Groups
Name:		package-groups
Version:	103
Release:	1
License:	GPL-2.0
Group:		System/Base
URL:		http://www.tizen.org
Source:		%{name}-%{version}.tar.bz2
Source1001: 	package-groups.manifest
BuildRequires:	meta-generic
%if %{with legacy_imageconfig}
BuildRequires:	meta-%{_profile}
%else
BuildRequires:	meta-common
%endif
BuildRequires:	pattern-tools
BuildRequires:	python
BuildRequires:	xsltproc


%description
Tizen Package Groups

%prep
%setup -q
cp %{SOURCE1001} .

%build
%ifarch %{arm}
%define __arch arm
%else
%define __arch i586
%endif

mkdir -p input output
%if %{with legacy_imageconfig}
for pp in generic %_profile; do
	test -d %{_datadir}/package-groups/$pp && cp %{_datadir}/package-groups/$pp/*.yaml input
done
%else
for pp in generic common; do
	test -d %{_datadir}/package-groups/$pp && cp %{_datadir}/package-groups/$pp/*.yaml input
done
%endif

merge-patterns -a %__arch --pattern-dir=input/ --output-dir=output/
xsltproc /usr/share/package-groups/stylesheets/comps.xsl output/patterns.xml > output/group.xml


%install
install -d %{buildroot}/usr/share/package-groups
install -m 644 output/patterns.xml %{buildroot}/usr/share/package-groups
install -m 644 output/group.xml %{buildroot}/usr/share/package-groups

%files
%manifest %{name}.manifest
%{_datadir}/package-groups/*.xml

