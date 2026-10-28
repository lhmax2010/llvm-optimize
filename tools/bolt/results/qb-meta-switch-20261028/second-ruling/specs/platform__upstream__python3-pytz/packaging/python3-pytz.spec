Name:       python3-pytz 
Summary:    World timezone definitions, modern and historical
Version:    2025.2
Release:    0
License:    MIT 
Group:      Development/Libraries
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

%description
python-tz brings the Olson tz database into Python.
This library allows accurate and cross platform timezone calculations
using Python 2.3 or higher. It also solves the issue of ambiguous times
at the end of daylight savings, which you can read more about in
the Python Library Reference (datetime.tzinfo).

%prep
%setup -q
cp %{SOURCE1} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean  

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.txt 
%{python3_sitelib}/pytz/*
%{python3_sitelib}/pytz-%{version}-py%{python3_version}.egg-info/*
