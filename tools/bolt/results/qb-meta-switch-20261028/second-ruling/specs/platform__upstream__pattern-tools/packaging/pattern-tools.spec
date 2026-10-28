Summary:	Pattern Tools
Name:		pattern-tools
Version:	001
Release:	1
License:	GPLv2
Group:		System/Base
URL:		http://www.tizen.org
Source:		%{name}-%{version}.tar.bz2
Source1001: 	pattern-tools.manifest
Requires:  libxslt
Requires: python-yaml
Requires: python-lxml

%description
Tools for managing package groups and patterns.

%prep
%setup -q
cp %{SOURCE1001} .

%build
make 

%install
%make_install


%files 
%manifest %{name}.manifest
%{_bindir}/merge-patterns
%{_datadir}/package-groups/stylesheets/*.xsl
