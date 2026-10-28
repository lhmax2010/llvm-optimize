Name:           python3-rospkg
Version:        1.6.1
Release:        1
Summary:        ROS package library
License:        BSD-4-Clause
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        LICENSE.BSD-3-Clause

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildArch:      noarch

%description
ROS package library


%prep
%setup -q -n rospkg-%{version}

%build
cp %{SOURCE1} .
cp %{SOURCE2} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE.BSD-3-Clause
%{_bindir}/rosversion
%{python3_sitelib}/rospkg-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/rospkg/*.py
%{python3_sitelib}/rospkg/__pycache__/*.cpython-*.pyc
