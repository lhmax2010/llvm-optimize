Name:           python3-argcomplete
Version:        3.6.3
Release:        1
Summary:        Bash tab completion for argparse
License:        Apache-2.0
Group:          Development/Languages/Python
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        argcomplete-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-pip

BuildRequires:  python3-hatchling

BuildArch:      noarch

%description
Bash tab completion for argparse


%prep
%setup -q -n argcomplete-%{version}

%build
cp %{SOURCE1} .
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files
%manifest %{name}.manifest
%license LICENSE.rst
%{_bindir}/activate-global-python-argcomplete
%{_bindir}/python-argcomplete-check-easy-install-script
%{_bindir}/register-python-argcomplete
%{python3_sitelib}/argcomplete/*
%{python3_sitelib}/argcomplete-%{version}.dist-info/*
