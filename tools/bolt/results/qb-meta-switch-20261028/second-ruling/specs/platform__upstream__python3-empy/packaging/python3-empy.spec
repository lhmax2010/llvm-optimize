Name:       python3-empy
Summary:    A powerful and robust template system for Python
Version:    4.2
Release:    0
License:    BSD-3-Clause
Group:      Development/Languages
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
EmPy is a system for embedding Python expressions and statements in template
text; it takes an EmPy source file, processes it, and produces output.


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
%license LICENSE.md
%{_bindir}/*.py
%{python3_sitelib}/__pycache__/*.pyc
%{python3_sitelib}/*.py
%{python3_sitelib}/empy-%{version}-py%{python3_version}.egg-info/*

