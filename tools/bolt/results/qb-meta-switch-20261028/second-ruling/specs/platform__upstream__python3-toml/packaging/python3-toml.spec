Name:           python3-toml
Version:        0.10.2
Release:        1
Summary:        Python Library for Tom's Obvious, Minimal Language
License:        MIT
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
Python Library for Tom's Obvious, Minimal Language


%prep
%setup -q -n toml-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/toml/*
%{python3_sitelib}/toml-%{version}-py%{python3_version}.egg-info/*
