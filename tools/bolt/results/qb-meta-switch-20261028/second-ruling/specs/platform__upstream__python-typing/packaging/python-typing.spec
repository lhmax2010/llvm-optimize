#
# spec file for package python-typing
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
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


Name:           python-typing
Version:        3.7.4.3
Release:        0
Summary:        Type Hints for Python
License:        Python-2.0
Group:          Development/Languages/Python
# Url:            https://docs.python.org/3.5/library/typing.html
Source:         https://files.pythonhosted.org/packages/source/t/typing/typing-%{version}.tar.gz
BuildRequires:  pkgconfig(python)
BuildRequires:  python-setuptools
BuildRequires:  fdupes
# BuildRequires:  python-rpm-macros

Source1001:     %{name}.manifest

BuildArch:      noarch

%description
Backport of the standard library typing module for Python versions older than 3.5.

%prep
%setup -q -n typing-%{version}

%build
cp %{SOURCE1001} .
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

# %check
# %python_expand $python python_%{$python_bin_suffix}/test_typing.py

%files
%manifest %{name}.manifest
%license LICENSE
%{python_sitelib}/*
