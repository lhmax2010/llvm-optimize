Name:           python3-iniconfig
Version:        2.3.0
Release:        1
Summary:        brain-dead simple config-ini parsing
License:        MIT
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        iniconfig-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildArch:      noarch

%description
brain-dead simple config-ini parsing


%prep
%setup -q -n iniconfig-%{version}
cp %{SOURCE1} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/iniconfig/*
%{python3_sitelib}/iniconfig-%{version}.dist-info/*

