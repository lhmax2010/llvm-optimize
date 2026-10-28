Name:           python3-docutils
Version:        0.22.4
Release:        1
Summary:        Python documentation utilities
License:        PD and BSD-2-Clause and GPL-3.0
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

Requires:       python3-importlib-metadata

BuildArch:      noarch

%description
Python documentation utilities


%prep
%setup -q -n docutils-%{version}
cp %{SOURCE1001} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/docutils-%{version}-py3-*.whl

%files
%manifest %{name}.manifest
%license ./licenses/*.rst
%license ./licenses/*.txt
%{_bindir}/*
%{python3_sitelib}/docutils/*
%{python3_sitelib}/docutils-%{version}.dist-info/*
