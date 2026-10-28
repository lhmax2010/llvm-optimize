Name:           python3-pytest-repeat
Version:        0.9.4
Release:        1
Summary:        pytest-repeat is a plugin for pytest
License:        MPL-2.0
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        pytest_repeat-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildRequires:  python3-pytest
BuildRequires:  python3-hatchling
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildArch:      noarch

%description
pytest-repeat is a plugin for pytest that makes it easy to repeat a single test, or multiple tests, a specific number of times.


%prep
%setup -q -n pytest-repeat-%{version}
cp %{SOURCE1} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/*.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/pytest_repeat-%{version}.dist-info/*
