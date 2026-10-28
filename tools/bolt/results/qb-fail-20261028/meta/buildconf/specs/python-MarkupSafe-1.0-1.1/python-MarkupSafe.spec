#
# spec file for package python-MarkupSafe
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

Name:           python-MarkupSafe
VCS:            platform/upstream/python-MarkupSafe#c79bd7b8b3aa485aa4bad116bb27a9bb6e7c096f
Version:        1.0
Release:        1.1
Url:            http://dev.pocoo.org/
Summary:        Implements a XML/HTML/XHTML Markup safe string for Python
License:        BSD-3-Clause
Group:          Development/Languages/Python
Source:         https://pypi.io/packages/source/M/MarkupSafe/MarkupSafe-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  python-devel
BuildRequires:  python-setuptools

Provides:       python-markupsafe = %{version}
Obsoletes:      python-markupsafe < %{version}

%description
Implements a unicode subclass that supports HTML strings. This can be used to
safely encode strings for dynamically generated web pages.

%prep
%setup -q -n MarkupSafe-%{version}

%build
cp %{SOURCE1001} .
export CFLAGS="%{optflags}"
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --install-lib=%{python_sitelib} --root=%{buildroot}

# Move library
%ifarch x86_64 aarch64 riscv64
mkdir -p %{buildroot}%{_libdir}/python%{python_version}/site-packages/markupsafe
mv %{buildroot}%{python_sitelib}/markupsafe/_speedups.so %{buildroot}%{_libdir}/python%{python_version}/site-packages/markupsafe
%endif

%remove_docs

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{python_sitelib}/markupsafe/
%{python_sitelib}/MarkupSafe-%{version}-py*.egg-info
%{_libdir}/python%{python_version}/site-packages/markupsafe/

%changelog

