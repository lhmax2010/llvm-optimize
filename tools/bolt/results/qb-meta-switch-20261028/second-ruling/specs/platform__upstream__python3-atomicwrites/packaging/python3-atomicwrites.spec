Name:       python3-atomicwrites 
Summary:    Atomic file writes for Python
Version:    1.4.1 
Release:    0
License:    MIT
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

%description
Atomic file writes for python3.
Features that distinguish it from other similar libraries:

- Race-free assertion that the target file doesn't yet exist. This can be
  controlled with the 'overwrite' parameter.

- High-level API that wraps a very flexible class-based API


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
%{python3_sitelib}/atomicwrites-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/atomicwrites/*.py
%{python3_sitelib}/atomicwrites/__pycache__/*.cpython-*.pyc
