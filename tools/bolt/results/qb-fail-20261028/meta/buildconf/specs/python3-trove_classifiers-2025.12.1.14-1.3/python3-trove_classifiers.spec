Name:           python3-trove_classifiers
VCS:            platform/upstream/python3-trove_classifiers#9ea041f558c730695419f17c463d800598b49812
Version:        2025.12.1.14
Release:        1.3
Summary:        Canonical source for classifiers on PyPI
License:        Apache-2.0
URL:            https://github.com/pypa/trove-classifiers
Source0:        trove_classifiers-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-build
BuildRequires:  python3-pip

BuildRequires:  python3-setuptools
BuildRequires:  python3-calver

BuildArch:      noarch

%description
Classifiers categorize projects per PEP 301. Use this package to validate classifiers in packages for PyPI upload or download.

%prep
%setup -q -n trove_classifiers-%{version}
cp %{SOURCE1001} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/trove_classifiers-%{version}-py3-none-any.whl 

%files 
%license LICENSE
%{_bindir}/trove-classifiers
%{python3_sitelib}/trove_classifiers/*
%{python3_sitelib}/trove_classifiers-%{version}.dist-info/*
