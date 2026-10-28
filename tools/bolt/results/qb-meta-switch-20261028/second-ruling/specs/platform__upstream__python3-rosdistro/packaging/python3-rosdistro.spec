Name:           python3-rosdistro
Version:        1.0.1
Release:        1
Summary:        A tool to work with rosdistro files
License:        BSD and MIT
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     LICENSE.bsd
Source1003:     LICENSE.MIT

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
A tool to work with rosdistro files


%prep
%setup -q -n rosdistro-%{version}

%build
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%license LICENSE.bsd
%license LICENSE.MIT
%{_bindir}/rosdistro_*
%{python3_sitelib}/rosdistro/*
%{python3_sitelib}/rosdistro-%{version}-py%{python3_version}.egg-info/*
