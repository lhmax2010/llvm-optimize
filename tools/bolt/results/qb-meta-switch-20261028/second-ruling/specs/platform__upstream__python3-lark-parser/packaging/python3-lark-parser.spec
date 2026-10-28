Name:           python3-lark-parser
Version:        1.3.1
Release:        1
Summary:        A modern parsing library
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
BuildRequires:  python3-setuptools_scm

BuildArch:      noarch

%description
A modern parsing library


%prep
%setup -q
cp %{SOURCE1001} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/lark-%{version}-py3-*.whl

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/lark/*
%{python3_sitelib}/lark-%{version}.dist-info/*
