#
# spec file for package python-ZSI
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#

Name:           python-ZSI
Version:        2.1.a1
Release:        0
Url:            http://pywebsvcs.sf.net
Summary:        Zolera SOAP Infrastructure
License:        Python
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/Z/ZSI/ZSI-2.1-a1.tar.gz
Source1001: 	python-ZSI.manifest
BuildRequires:  python-devel
BuildRequires:  fdupes
BuildArch:      noarch
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%description
ZSI, the Zolera SOAP Infrastructure, is a pure-Python module that
provides an implementation of SOAP messaging, as described in SOAP 1.1
Specification (see http://www.w3.org/TR/soap).  It can also be used to
build applications using SOAP Messages with Attachments (see
http://www.w3.org/TR/SOAP-attachments).  ZSI is intended to make it
easier to write web services in Python.

In particular, ZSI parses and generates SOAP messages, and converts
between native Python datatypes and SOAP syntax. Simple dispatch and
invocation methods are supported.  There are no known bugs.  Its only
known limitation is that it cannot handle multi-dimensional arrays.

%prep
%setup -q -n ZSI-2.1-a1
cp %{SOURCE1001} .
find doc -type f -name .cvsignore -exec rm {} \; # Remove CVS files
#sed -i '1d' ZSI/{auth,client,digest_auth,dispatch,fault,generate/wsdl2dispatch,__init__,parse,resolvers,schema,ServiceContainer,TCapache,TCcompound,TCnumbers,TC,TCtimes,writer,wstools/c14n,wstools/__init__}.py # Remove she-bang line
#chmod -x doc/guide02-wsdl2py.tex # Remove executable bit from tex file

%build
%{__python} setup.py build
%fdupes -s doc

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
#%{_bindir}/wsdl2dispatch
%{_bindir}/wsdl2py
%{python_sitelib}/*

%changelog
