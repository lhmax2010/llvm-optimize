Name:           python3-jinja2
Version:        3.1.3
Release:        1
Summary:        A syntax highlighting engine written in Python3
Group:          Development/Libraries
License:        BSD-3-Clause
URL:            https://jinja.palletsprojects.com/
Source0:        %{name}-%{version}.tar.gz
Source1001:     python3-jinja2.manifest

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-MarkupSafe
Requires:       python3-setuptools

BuildArch:      noarch

%description
Jinja is a fast, expressive, extensible templating engine. Special
placeholders in the template allow writing code similar to Python
syntax. Then the template is passed data to render the final document.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install -O1 --skip-build --root %{buildroot} --prefix=%{_prefix}

%files
%manifest %{name}.manifest
%license LICENSE.rst
%{python3_sitelib}/*
