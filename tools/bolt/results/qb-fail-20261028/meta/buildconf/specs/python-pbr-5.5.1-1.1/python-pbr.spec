#
# spec file for package python-pbr
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


# NOTE(saschpe): git invocation and pythonpath issues with testrepository
# enable testing with a build conditional (off by default):

Name:           python-pbr
VCS:            platform/upstream/python-pbr#13505c4ed32c4009ad345709de74394dc7cd66c7
Version:        5.5.1
Release:        1.1
Summary:        Python Build Reasonableness
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            http://pypi.python.org/pypi/pbr
Source:         https://pypi.python.org/packages/c3/2c/63275fab26a0fd8cadafca71a3623e4d0f0ee8ed7124a5bb128853d178a7/pbr-%{version}.tar.gz
Source1001:     %{name}.manifest

#BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools

#BuildRequires:  python-pip >= 1.4
#BuildRequires:  fdupes
#BuildRequires:  python-rpm-macros

Requires:       python-setuptools

BuildArch:      noarch

%description
PBR is a library to automatically do a bunch of standard
things you want in your setup.py without you having to repeat
them every time. It will set versions, process requirements
files and generate AUTHORS and ChangeLog file all from git
information.


%prep
%setup -q -n pbr-%{version}
# Get rid of ugly build-time deps that require network:
sed -i "s/, 'sphinx\.ext\.intersphinx'//" doc/source/conf.py

%build
cp %{SOURCE1001} .
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%if %{with test}
%check
%{__python} %{_bindir}/testr init
%{__python} %{_bindir}/testr run --parallel
%endif

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/pbr
%{python_sitelib}/pbr
%{python_sitelib}/pbr-%{version}-py%{python_version}.egg-info

%changelog
