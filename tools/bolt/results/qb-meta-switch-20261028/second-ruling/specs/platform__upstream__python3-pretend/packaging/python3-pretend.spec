Name:       python3-pretend
Summary:    A library for stubbing in Python
Version:    1.0.9
Release:    0
License:    BSD-3-Clause
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
Pretend is a library to make stubbing with Python easier.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean

%files
%manifest %{name}.manifest
%license LICENSE.rst
%{python3_sitelib}/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/pretend-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/pretend.py
