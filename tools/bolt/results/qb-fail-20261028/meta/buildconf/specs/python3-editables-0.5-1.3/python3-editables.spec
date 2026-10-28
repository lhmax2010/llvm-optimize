Name:           python3-editables
VCS:            platform/upstream/python3-editables#000b5b27a1d65f14ec8080d291380889e5435e65
Version:        0.5
Release:        1.3
Summary:        Editable installations
License:        MIT
URL:            https://github.com/pfmoore/editables
Source0:        editables-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildArch:      noarch

%description
A Python library for creating "editable wheels"

This library supports the building of wheels which, when installed, will expose
packages in a local directory on sys.path in "editable mode". In other words,
changes to the package source will be reflected in the package visible to
Python, without needing a reinstall.

%prep
%setup -q -n editables-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/editables-%{version}-py3-*.whl

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{python3_sitelib}/editables/*.py
%{python3_sitelib}/editables/py.typed
%{python3_sitelib}/editables/__pycache__/*
%{python3_sitelib}/editables-%{version}.dist-info/*
