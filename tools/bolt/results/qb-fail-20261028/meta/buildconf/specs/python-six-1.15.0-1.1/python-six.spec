#
# spec file for package python-six
#
# Copyright (c) 2016 SUSE LINUX GmbH, Nuernberg, Germany.
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

Name:           python-six
VCS:            platform/upstream/python-six#96f094858c3aab8ff5b2827ebf861a7e3abbc77c
Version:        1.15.0
Release:        1.1
Url:            http://pypi.python.org/pypi/six/
Summary:        Python 2 and 3 compatibility utilities
License:        MIT
Group:          Development/Libraries/Python
Source:         http://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python-devel

BuildArch:      noarch

%description
Six is a Python 2 and 3 compatibility library. It provides utility
functions for smoothing over the differences between the Python
versions with the goal of writing Python code that is compatible on
both Python versions. See the documentation for more information on
what is provided.

%prep
%setup -q -n six-%{version}

%build
cp %{SOURCE1001} .
%{__python} setup.py build
# due to cyclic requirements between Sphinx and six,
# documentation is build in its own package <hpj@urpla.net>

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

# Run tests in -doc package to avoid dependency loop
# %check
# %{__python} test_six.py

%pre
# previous versions of the package installed .egg-info as a directory,
# the new update now installs it as a file. Clean out the directory, should it exist.
if [ -d %{python_sitelib}/six-%{version}-py%{py_ver}.egg-info ]; then
  rm -rf %{python_sitelib}/six-%{version}-py%{py_ver}.egg-info
fi

%files
%manifest %{name}.manifest
%license LICENSE
%{python_sitelib}/six.py*
%{python_sitelib}/six-%{version}-py*.egg-info

%changelog
