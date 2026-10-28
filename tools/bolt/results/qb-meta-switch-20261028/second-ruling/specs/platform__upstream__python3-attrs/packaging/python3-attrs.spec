Name:           python3-attrs
Version:        25.4.0
Release:        1
Summary:        Classes Without Boilerplate
License:        MIT
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        attrs-%{version}-py3-none-any.whl

BuildRequires:  python3
BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-build
BuildRequires:  python3-pip

BuildArch:      noarch

%description
Classes Without Boilerplate


%prep
%setup -q -n attrs-%{version}
cp %{SOURCE1} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/attr/*
%{python3_sitelib}/attrs/*
%{python3_sitelib}/attrs-%{version}.dist-info/*
