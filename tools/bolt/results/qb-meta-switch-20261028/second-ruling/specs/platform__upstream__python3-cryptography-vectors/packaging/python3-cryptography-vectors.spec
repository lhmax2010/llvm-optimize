Name:       python3-cryptography-vectors
Summary:    Test vectors for the cryptography package
Version:    2.3
Release:    0
License:    Apache-2.0 OR BSD-3-Clause
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
Vectors for testing of the python cryptography package.


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
%license LICENSE.APACHE LICENSE.BSD
%{python3_sitelib}/cryptography_vectors-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/cryptography_vectors/*
%{python3_sitelib}/cryptography_vectors/*/*
%{python3_sitelib}/cryptography_vectors/*/*/*


