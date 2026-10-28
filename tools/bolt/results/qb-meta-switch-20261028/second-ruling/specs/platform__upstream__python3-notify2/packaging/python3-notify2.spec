Name:           python3-notify2
Version:        0.3.1
Release:        1
Summary:        Python interface to DBus notifications
License:        BSD-2-Clause
Group:          Development/Languages/Python
Source:         notify2-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
Python interface to DBus notifications


%prep
%setup -q -n notify2-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/notify2-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/*.py
