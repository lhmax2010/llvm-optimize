Name:           python3-zipp
Version:        3.23.0
Release:        1
Summary:        Backport of pathlib-compatible object wrapper for zip files
License:        MIT
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        zipp-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-pip

BuildArch:      noarch

%description
Backport of pathlib-compatible object wrapper for zip files


%prep
%setup -q -n zipp-%{version}
cp %{SOURCE1} .

%build

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/zipp/*
%{python3_sitelib}/zipp-%{version}.dist-info/*
