Name:           python3-packaging
VCS:            platform/upstream/python3-packaging#9650bb69dd9e2ac7e91e86c251b7ab80f90fd80e
Version:        25.0
Release:        1.8
Summary:        Core utilities for Python3 packages
License:        Apache-2.0
Group:          Development/Languages/Python3
Url:            https://github.com/pypa/packaging
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        packaging-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-pip
BuildRequires:  python3-flit_core

BuildRequires:  python3-pyparsing
BuildRequires:  python3-six

Requires:       python3-pyparsing
Requires:       python3-six

BuildArch:      noarch

%description
Core utilities for Python3 packages

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .

%build

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files
%manifest %{name}.manifest
%license LICENSE.APACHE
%{python3_sitelib}/packaging/*
%{python3_sitelib}/packaging-%{version}.dist-info/*
