Name:           python3-pytest-cov
Version:        7.0.0
Release:        1
Summary:        Pytest plugin for measuring coverage.
License:        MIT
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools

BuildRequires:  python3-pytest
BuildRequires:  python3-coverage
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-fancy-pypi-readme

BuildArch:      noarch

%description
Pytest plugin for measuring coverage.


%prep
%setup -q -n pytest-cov-%{version}
cp %{SOURCE1001} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/pytest_cov-%{version}-*.whl

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/pytest_cov/*
%{python3_sitelib}/pytest_cov-%{version}.dist-info/*
