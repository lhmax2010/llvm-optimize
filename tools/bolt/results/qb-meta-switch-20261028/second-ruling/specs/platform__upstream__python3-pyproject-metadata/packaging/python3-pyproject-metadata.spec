Name:           python3-pyproject-metadata
Version:        0.10.0
Release:        0
Summary:        PEP 621 metadata parsing
License:        MIT
URL:            https://github.com/FFY00/python-pyproject-metadata
Source0:        pyproject-metadata-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildArch:      noarch

%description
Dataclass for PEP 621 metadata with support for core metadata generation.

This project does not implement the parsing of pyproject.toml containing PEP
621 metadata.  Instead, given a Python data structure representing PEP 621
metadata (already parsed), it will validate this input and generate a PEP
643-compliant metadata file (e.g. PKG-INFO).

%prep
%setup -q -n pyproject-metadata-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/pyproject_metadata-%{version}-py3-*.whl

%files 
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/pyproject_metadata/*
%{python3_sitelib}/pyproject_metadata-%{version}.dist-info/*
