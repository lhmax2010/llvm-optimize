Name:           python3-hatch-vcs
Version:        0.5.0
Release:        1
Summary:        Hatch plugin for versioning with your preferred VCS
License:        MIT
URL:            https://github.com/ofek/hatch-vcs
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildRequires:  python3-hatchling
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-packaging
BuildRequires:  python3-pathspec
BuildRequires:  python3-pluggy
BuildRequires:  python3-trove_classifiers

%description
This provides a plugin for Hatch that uses your preferred version control
system (like Git) to determine project versions.

%prep
%setup -q -n hatch_vcs-%{version}
cp %{SOURCE1} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/hatch_vcs-%{version}-*.whl

# Remove documentation and manual pages
%remove_docs

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{python3_sitelib}/hatch_vcs/*
%{python3_sitelib}/hatch_vcs-%{version}.dist-info/*

