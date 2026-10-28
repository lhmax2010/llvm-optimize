Name:       python3-pycparser
Summary:    C parser in Python
Version:    2.23
Release:    0
License:    BSD-3-Clause
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

%description
pycparser is a complete parser of the C language, written in pure Python using
the PLY parsing library. It parses C code into an AST and can serve as a
front-end for C compilers or analysis tools.


%prep
%setup -q
cp %{SOURCE1001} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/pycparser-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/pycparser/*.py
%{python3_sitelib}/pycparser/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/pycparser/_c_ast.cfg
%{python3_sitelib}/pycparser/ply/*.py
%{python3_sitelib}/pycparser/ply/__pycache__/*.cpython-*.pyc

