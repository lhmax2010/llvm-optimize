#
# spec file for package python-packaging
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

%if "%{run_tests}" == "1"
    %define __spec_check_pre %___build_pre
    %define check %%check
%endif

%define debug_package %{nil}

Name:           python-packaging
VCS:            platform/upstream/python-packaging#28c0103819c467092050c8f8cdaca57627d51893
Version:        20.8
Release:        1.1
Summary:        Core utilities for Python packages
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            https://github.com/pypa/packaging
Source:         https://pypi.io/packages/source/p/packaging/packaging-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python
BuildRequires:  python-pyparsing
BuildRequires:  python-six

# do not add setuptools dependency, this is now a dependency
# of setuptools. Ensure that all dependencies also don't depend
# on setuptools
# (at the moment, six and pyparsing are ok)

Requires:       python-pyparsing
Requires:       python-six
BuildArch:      noarch

%description
Core utilities for Python packages

%prep
%setup -q -n packaging-%{version}

%build
cp %{SOURCE1001} .
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

# ensure egg-info is a directory
rm %{buildroot}%{python_sitelib}/*.egg-info
cp -r packaging.egg-info %{buildroot}%{python_sitelib}/packaging-%{version}-py%{python_version}.egg-info


%check


%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.APACHE
%{python_sitelib}/packaging
%{python_sitelib}/packaging-%{version}-py*.egg-info/

%changelog
