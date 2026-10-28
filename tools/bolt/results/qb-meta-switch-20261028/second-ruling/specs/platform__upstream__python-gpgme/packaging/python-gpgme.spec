#
# spec file for package python-gpgme
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


Name:           python-gpgme
Version:        0.1
Release:        0
Summary:        A Python module for working with OpenPGP messages
License:        LGPL-2.1+
Group:          Platform Development/Python
Url:            http://pypi.python.org/pypi/pygpgme
Source:         pygpgme-%{version}.tar.bz2
Source1001: 	python-gpgme.manifest
BuildRequires:  libgpgme-devel
BuildRequires:  python-devel

%description
PyGPGME is a Python module that lets you sign, verify, encrypt and
decrypt messages using the OpenPGP format.

It is built on top of the GNU Privacy Guard and the GPGME library.


%prep
%setup -q -n pygpgme-%{version}
cp %{SOURCE1001} .

%build

%install
%{__python} setup.py install --root $RPM_BUILD_ROOT --prefix=%{_prefix}
# No need to ship the tests
rm -rf $RPM_BUILD_ROOT%{py_sitedir}/gpgme/tests/


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc README PKG-INFO
%{py_sitedir}/*

%changelog
