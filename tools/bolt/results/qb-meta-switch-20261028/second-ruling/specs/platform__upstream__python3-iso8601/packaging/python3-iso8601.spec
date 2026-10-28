Name:       python3-iso8601
Summary:    Simple module to parse ISO 8601 dates
Version:    2.1.0
Release:    0
License:    MIT
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    iso8601-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildArch:      noarch

%description
Simple module to parse ISO 8601 dates

This module parses the most common forms of ISO 8601 date strings (e.g.
2007-01-14T20:34:22+00:00) into datetime objects.


%prep
%setup -q
cp %{SOURCE1} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%clean

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/iso8601/*
%{python3_sitelib}/iso8601-%{version}.dist-info/*



