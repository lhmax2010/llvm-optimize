Name:           python3-coverage
Version:        7.13.1
Release:        1
Summary:        Code coverage measurement for Python
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools

%description
Code coverage measurement for Python


%prep
%setup -q -n coverage-%{version}
cp %{SOURCE1001} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/coverage-%{version}-*.whl

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{_bindir}/coverage*
%{python3_sitearch}/*.pth
%{python3_sitearch}/coverage/*
%{python3_sitearch}/coverage-%{version}.dist-info/*
