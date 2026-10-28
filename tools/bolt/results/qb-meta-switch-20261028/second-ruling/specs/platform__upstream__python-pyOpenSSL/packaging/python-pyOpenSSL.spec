#
# spec file for package python-pyOpenSSL
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

Name:           python-pyOpenSSL
Version:        19.0.0.0
Release:        0
Url:            https://github.com/pyca/pyopenssl
Summary:        Python wrapper module around the OpenSSL library
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         https://files.pythonhosted.org/packages/source/p/pyOpenSSL/pyOpenSSL-%{version}.tar.gz
Source1001: 	python-pyOpenSSL.manifest
#BuildRequires:  libopenssl1.1-devel
BuildRequires:  python-setuptools
BuildRequires:  python-devel
BuildRequires: openssl3
BuildArch:      noarch
#comment the below line. if add the below line, compile failed, python setup.py install will use /usr/lib/python2.7 for x86_64 arch. the below is /usr/lib64/python2.7
#%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description
High-level wrapper around a subset of the OpenSSL library, includes
 * SSL.Connection objects, wrapping the methods of Python's portable
   sockets
 * Callbacks written in Python
 * Extensive error-handling mechanism, mirroring OpenSSL's error codes
...  and much more ;)

%prep
%setup -q -n pyOpenSSL-%{version}
cp %{SOURCE1001} .

%build
CFLAGS="%{optflags} -fno-strict-aliasing" %{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%doc *.rst
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
