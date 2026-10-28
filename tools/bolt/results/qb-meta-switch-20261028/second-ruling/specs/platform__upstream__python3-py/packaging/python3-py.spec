Name:           python3-py
Version:        1.11.0
Release:        1
Summary:        library with cross-python path, ini-parsing, io, code, log facilities
License:        MIT
Group:          Development/Languages/Python
Source:         py-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     py-1.11.0-py2.py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-build
BuildRequires:  python3-pip
BuildRequires:  python3-packaging
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildArch:      noarch

%description
library with cross-python path, ini-parsing, io, code, log facilities


%prep
%setup -q -n py-%{version}
cp %{SOURCE1001} .

%build
# %%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE1002}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/py/*.py
%{python3_sitelib}/py/*.pyi
%{python3_sitelib}/py/*.typed
%{python3_sitelib}/py/__pycache__/*
%{python3_sitelib}/py/_code/*
%{python3_sitelib}/py/_io/*
%{python3_sitelib}/py/_log/*
%{python3_sitelib}/py/_path/*
%{python3_sitelib}/py/_process/*
%{python3_sitelib}/py/_vendored_packages/*.py
%{python3_sitelib}/py/_vendored_packages/__pycache__/*
%{python3_sitelib}/py/_vendored_packages/apipkg/*
%{python3_sitelib}/py/_vendored_packages/apipkg-*.dist-info/*
%{python3_sitelib}/py/_vendored_packages/iniconfig/*
%{python3_sitelib}/py/_vendored_packages/iniconfig-*.dist-info/*
%{python3_sitelib}/py-%{version}.dist-info/*
