Name:           python3-colcon-cd
Version:        0.1.1
Release:        1
Summary:        A shell function for colcon to change the current working directory.
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         colcon-cd-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

Requires:       python3-colcon-core
Requires:       python3-colcon-package-information

BuildArch:      noarch

%description
A shell function for colcon to change the current working directory.

%prep
%setup -q -n colcon-cd-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/colcon_cd-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/colcon_cd/*.py
%{python3_sitelib}/colcon_cd/__pycache__/*.cpython-*.pyc
%{_datadir}/colcon_cd/function/colcon_cd.sh
