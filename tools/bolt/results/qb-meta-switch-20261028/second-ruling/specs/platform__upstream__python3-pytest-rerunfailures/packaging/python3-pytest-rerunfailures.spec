Name:           python3-pytest-rerunfailures
Version:        16.1
Release:        1
Summary:        pytest-rerunfailures is a plugin for pytest
License:        MPL-2.0
Group:          Development/Languages/Python
Source:         pytest-rerunfailures-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
pytest-rerunfailures is a plugin for pytest that re-runs tests to eliminate intermittent failures.


%prep
%setup -q -n pytest-rerunfailures-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/pytest_rerunfailures.py
%{python3_sitelib}/__pycache__/pytest_rerunfailures.cpython-*.pyc
%{python3_sitelib}/pytest_rerunfailures-%{version}-py%{python3_version}.egg-info/*

