Name:           python3-hatch-fancy-pypi-readme
Version:        25.1.0
Release:        1
Summary:        Hatch plugin for writing fancy PyPI readmes
License:        MIT
URL:            https://github.com/hynek/hatch-fancy-pypi-readme
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildRequires:  python3-hatchling

%description
This provides a Hatch metadata plugin for everyone who cares about the
first impression of their projectâ€™s PyPI landing page. It allows you to
define your PyPI project description in terms of concatenated fragments
that are based on static strings, files, and most importantly: parts of
files defined using cut-off points or regular expressions.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/hatch_fancy_pypi_readme-%{version}-*.whl

%remove_docs

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{_bindir}/hatch-fancy-pypi-readme
%{python3_sitelib}/hatch_fancy_pypi_readme/*
%{python3_sitelib}/hatch_fancy_pypi_readme-%{version}.dist-info/*

