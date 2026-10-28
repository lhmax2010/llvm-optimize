Name:       python3-idna
Summary:    Internationalized Domain Names in Applications (IDNA)
Version:    3.11
Release:    0
License:    BSD-3-Clause
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildArch:      noarch

%description
A library to support the Internationalised Domain Names in
Applications (IDNA) protocol as specified in RFC 5891
http://tools.ietf.org/html/rfc5891. This version of the protocol
is often referred to as \A1\B0IDNA2008\A1\B1 and can produce different
results from the earlier standard from 2003.

The library is also intended to act as a suitable drop-in replacement
for the \A1\B0encodings.idna\A1\B1 module that comes with the Python standard
library but currently only supports the older 2003 specification.


%prep
%setup -q
cp %{SOURCE1001} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/idna-%{version}-py3-*.whl

%clean

%files
%manifest %{name}.manifest
%license LICENSE.md
%{python3_sitelib}/idna/*
%{python3_sitelib}/idna-%{version}.dist-info/*


