#
# spec file for package python-unittest2
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

Name:           python-unittest2
VCS:            platform/upstream/python-unittest2#28cda0acb36d9d81826ae48f80536e188b9caaaa
Version:        1.1.0
Release:        1.1
Url:            http://pypi.python.org/pypi/unittest2
Summary:        The new features in unittest for Python 2.7 backported to Python 2.3+
License:        BSD-3-Clause
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/u/unittest2/unittest2-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python-argparse
BuildRequires:  python-devel
BuildRequires:  python-linecache2
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-traceback2

Requires:       python-argparse
Requires:       python-linecache2
Requires:       python-six
Requires:       python-traceback2

Provides:       python2-unittest2

BuildArch:      noarch

%description
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7. It is tested to run on Python 2.4 - 2.7.

%prep
%setup -q -n unittest2-%{version}

%build
cp %{SOURCE1001} .
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_bindir}/unit2
%{python_sitelib}/unittest2/*
%{python_sitelib}/unittest2/test/*
%{python_sitelib}/unittest2-%{version}-py*.egg-info

%changelog

