Name:           python3-distro
Version:        1.9.0
Release:        1
Summary:        Distro - an OS platform infomation API
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     distro-1.9.0-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-pip

BuildArch:      noarch

%description
Distro - an OS platform infomation API


%prep
%setup -q -n distro-%{version}
cp %{SOURCE1001} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root=%{buildroot} %{SOURCE1002}

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/distro
%{python3_sitelib}/distro/*
%{python3_sitelib}/distro-%{version}.dist-info/*
