Name:       python3-pathlib2
Summary:    Object-oriented filesystem paths
Version:    2.3.7.post1
Release:    0
License:    MIT
Group:      devel/python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

Requires:       python3-six

%description
pathlib2 offers a set of classes to handle filesystem paths in an
object-oriented fashion. This is a backport of the Python 3.4+ pathlib
module for older Python versions.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --root=%{buildroot} --prefix=%{_prefix}

# Remove documentation and manual pages
%remove_docs

%files
%manifest %{name}.manifest
%license LICENSE.rst
%{python3_sitelib}/pathlib2/*
%{python3_sitelib}/pathlib2-%{version}-py%{python3_version}.egg-info/*

