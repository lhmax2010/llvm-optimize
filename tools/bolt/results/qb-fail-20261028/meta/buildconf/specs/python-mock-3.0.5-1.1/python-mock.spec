#
# spec file for package python-mock
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

Name:           python-mock
VCS:            platform/upstream/python-mock#6039934960f0ee950415edc545ba139162a456f0
Version:        3.0.5
Release:        1.1
Url:            http://www.voidspace.org.uk/python/mock/
Summary:        A Python Mocking and Patching Library for Testing
License:        BSD-2-Clause
Group:          Development/Languages/Python
Source:         https://pypi.io/packages/source/m/mock/mock-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python-pbr
BuildRequires:  python-setuptools >= 17.1
BuildRequires:  python-six
BuildRequires:  python-funcsigs
BuildRequires:  python-unittest2

Requires:       python-funcsigs >= 1
Requires:       python-pbr
Requires:       python-six >= 1.9

BuildArch:      noarch

%description
mock is a Python module that provides a core Mock class. It removes the need
to create a host of stubs throughout your test suite. After performing an
action, you can make assertions about which methods / attributes were used and
arguments they were called with. You can also specify return values and set
needed attributes in the normal way.

%prep
%setup -q -n mock-%{version}
# remove test runner which causes test failure all by itself
rm mock/tests/__main__.py
rm mock/tests/testhelpers_py3.py

%build
cp %{SOURCE1001} .
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
%{__python} setup.py test

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{python_sitelib}/*

%changelog
