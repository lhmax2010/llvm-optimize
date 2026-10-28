Name:       python3-cffi
Summary:    Foreign Function Interface for Python calling C code
Version:    2.0.0
Release:    0
License:    MIT
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools
BuildRequires:  python3-pycparser
BuildRequires:  pkgconfig(libffi)

Requires:       python3-pycparser

%description
Foreign Function Interface for Python calling C code. The aim of this project
is to provide a convenient and reliable way of calling C code from Python.


%prep
%setup -q
cp %{SOURCE1001} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitearch}/_cffi_backend.cpython-*.so
%{python3_sitearch}/cffi-%{version}-py%{python3_version}.egg-info/*
%{python3_sitearch}/cffi/*.h
%{python3_sitearch}/cffi/*.py
%{python3_sitearch}/cffi/__pycache__/*.cpython-*.pyc
