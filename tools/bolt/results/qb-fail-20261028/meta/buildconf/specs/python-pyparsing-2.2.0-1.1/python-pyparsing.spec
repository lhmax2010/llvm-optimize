#
# spec file for package python-pyparsing
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           python-pyparsing
VCS:            platform/upstream/python-pyparsing#da18def77b1b65452e775fb16cb33727be652ff9
Version:        2.2.0
Release:        1.1
Summary:        Grammar Parser Library for Python
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/pyparsing
Source:         https://files.pythonhosted.org/packages/source/p/pyparsing/pyparsing-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python

BuildArch:      noarch

Provides:       python-parsing = %{version}
Obsoletes:      python-parsing < %{version}

%description
The pyparsing module is an alternative approach to creating and executing
simple grammars, vs. the traditional lex/yacc approach, or the use of regular
expressions. The pyparsing module provides a library of classes that client
code uses to construct the grammar directly in Python code.

%prep
%setup -q -n pyparsing-%{version}

%build
cp %{SOURCE1001} .
%{__python} setup.py build
# Fix wrong EOL encoding:
sed -i 's/\r$//' CHANGES LICENSE README examples/*

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

# ensure egg-info is a directory
rm %{buildroot}%{python_sitelib}/*.egg-info
cp -r pyparsing.egg-info %{buildroot}%{python_sitelib}/pyparsing-%{version}-py%{python_version}.egg-info


%remove_docs

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE
%{python_sitelib}/pyparsing.py*
%{python_sitelib}/pyparsing-%{version}-py*.egg-info/

%changelog

