Name:           python3-setuptools_scm
VCS:            platform/upstream/python3-setuptools_scm#cadd1a03612b29b5c62bdb175d3f62e91d478263
Version:        9.2.2
Release:        1.3
Summary:        setuptools_scm handles managing your Python package versions
License:        MIT
Group:          Development/Languages/Python
Source:         setuptools_scm-%{version}.tar.gz
Source1:     %{name}.manifest
Source2:     setuptools_scm-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-pip

BuildRequires:  python3-setuptools
BuildRequires:  python3-packaging
BuildRequires:  python3-typing_extensions

Requires:       python3-packaging
Requires:       python3-typing_extensions

BuildArch:      noarch

%description
setuptools_scm handles managing your Python package versions in SCM metadata instead of declaring them as the version argument or in a SCM managed file.

%prep
%setup -q -n setuptools_scm-%{version}
cp %{SOURCE1} .

%build

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2} 
rm -f %{buildroot}/%{python3_sitelib}/setuptools_scm/.git_archival.txt

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/setuptools-scm
%{python3_sitelib}/setuptools_scm/*
%{python3_sitelib}/setuptools_scm-%{version}.dist-info/*
