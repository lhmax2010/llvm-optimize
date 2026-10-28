Name:           python3-pytest
Version:        9.0.2
Release:        1
Summary:        The pytest framework makes it easy to write small tests
License:        MIT
Group:          Development/Languages/Python
Source0:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        pytest-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildRequires:  python3-attrs
BuildRequires:  python3-importlib-metadata
BuildRequires:  python3-iniconfig
BuildRequires:  python3-packaging
BuildRequires:  python3-pluggy
BuildRequires:  python3-py
BuildRequires:  python3-pygments
BuildRequires:  python3-toml
BuildRequires:  python3-zipp

Requires:       python3-attrs
Requires:       python3-importlib-metadata
Requires:       python3-iniconfig
Requires:       python3-packaging
Requires:       python3-pluggy
Requires:       python3-py
Requires:       python3-pygments
Requires:       python3-toml
Requires:       python3-zipp

BuildArch:      noarch

%description
The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.


%prep
%setup -q -n pytest-%{version}
cp %{SOURCE1} .

%build

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/py.test
%{_bindir}/pytest
%{python3_sitelib}/*
%{python3_sitelib}/pytest-%{version}.dist-info/*
