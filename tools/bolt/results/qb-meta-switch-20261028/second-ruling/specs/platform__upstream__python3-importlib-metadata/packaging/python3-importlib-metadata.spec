Name:           python3-importlib-metadata
Version:        8.7.1
Release:        1
Summary:        Read metadata from pyhon packages
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        LICENSE.Apache-2.0
Source3:        importlib_metadata-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-zipp

BuildArch:      noarch

%description
Read metadata from pyhon packages


%prep
%setup -q -n importlib_metadata-%{version}
cp %{SOURCE1} .
cp %{SOURCE2} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE3}

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{python3_sitelib}/importlib_metadata/*
%{python3_sitelib}/importlib_metadata-%{version}.dist-info/*
