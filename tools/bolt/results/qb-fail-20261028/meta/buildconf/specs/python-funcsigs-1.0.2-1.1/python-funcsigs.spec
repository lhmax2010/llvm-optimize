#
# spec file for package python-funcsigs
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

%define debug_package %{nil}

Name:           python-funcsigs
VCS:            platform/upstream/python-funcsigs#bddecfe0f589554e922e5972ec92871a73f44970
Version:        1.0.2
Release:        1.1
Summary:        Python function signatures from PEP362
License:        Apache-2.0
Group:          Development/Languages/Python
Url:            http://funcsigs.readthedocs.org
Source:         https://pypi.io/packages/source/f/funcsigs/funcsigs-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-unittest2

BuildArch:      noarch

%description
funcsigs is a backport of the PEP 362 function signature features from
Python 3.3's inspect module. The backport is compatible with Python 2.6, 2.7
as well as 3.2 and up.

%prep
%setup -q -n funcsigs-%{version}

%build
cp %{SOURCE1001} .
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
%{__python} setup.py test

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{python_sitelib}/*

%changelog
