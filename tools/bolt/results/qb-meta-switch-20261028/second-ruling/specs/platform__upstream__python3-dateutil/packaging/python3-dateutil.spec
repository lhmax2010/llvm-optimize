Name:           python3-dateutil
Version:        2.9.0.post0
Release:        1
Summary:        Extensions to the standard Python datetime module
License:        Apache-2.0 or BSD-3-Clause
Group:          Development/Languages/Python
Source:         python-dateutil-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildArch:      noarch

%description
Extensions to the standard Python datetime module

%prep
%setup -q -n python-dateutil-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/dateutil/*.py
%{python3_sitelib}/dateutil/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/dateutil/parser/*.py
%{python3_sitelib}/dateutil/parser/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/dateutil/tz/*.py
%{python3_sitelib}/dateutil/tz/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/dateutil/zoneinfo/*.py
%{python3_sitelib}/dateutil/zoneinfo/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/dateutil/zoneinfo/dateutil-zoneinfo.tar.gz
%{python3_sitelib}/python_dateutil-*-py%{python3_version}.egg-info
