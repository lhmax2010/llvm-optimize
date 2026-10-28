#
# spec file for package python-iniparse
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           python-iniparse
Version:        0.4
Release:        0
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
License:        MIT
Group:          Platform Development/Python
Url:            http://code.google.com/p/iniparse/
Source0:        http://iniparse.googlecode.com/files/iniparse-%{version}.tar.gz
Source1001: 	python-iniparse.manifest
BuildRequires:  python-distribute
BuildRequires:  python-devel
BuildArch:      noarch

%description
iniparse is an INI parser for Python which is API compatible with the
standard library's ConfigParser, preserves structure of INI files
(order of sections & options, indentation, comments, and blank lines
are preserved when data is updated), and is more convenient to use.

%prep
%setup -q -n iniparse-%{version}
cp %{SOURCE1001} .
chmod 644 html/index.html

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root %{buildroot} --prefix=%{_prefix}
rm -rf %{buildroot}%{_datadir}/doc/iniparse-%{version} # Remove unwanted stuff

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE LICENSE-PSF 
%{python_sitelib}/*

%changelog
