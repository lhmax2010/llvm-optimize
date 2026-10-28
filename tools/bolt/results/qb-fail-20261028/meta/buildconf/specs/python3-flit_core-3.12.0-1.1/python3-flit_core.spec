Name:           python3-flit_core
VCS:            platform/upstream/python3-flit_core#6b0507b1d45f14a92d480929ab5ca149118a86d6
Version:        3.12.0
Release:        1.1
Summary:        Distribution-building parts of Flit
License:        BSD-3-Clause AND MIT
URL:            https://github.com/pypa/flit
Source0:        flit_core-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)

BuildArch:      noarch

%description
This provides a PEP 517 build backend for packages using Flit.
The only public interface is the API specified by PEP 517, at flit_core.buildapi.

%prep
%setup -q -n flit_core-%{version}

%build
cp %{SOURCE1001} .
python3 -m flit_core.wheel

%install
python3 bootstrap_install.py ./dist/flit_core-%{version}-py3-none-any.whl -i%{buildroot}%{python3_sitelib}
rm -rf %{buildroot}%{python3_sitelib}/flit_core/tests

%files 
%license LICENSE
%{python3_sitelib}/flit_core/*.py
%{python3_sitelib}/flit_core/vendor/*
%{python3_sitelib}/flit_core-%{version}.dist-info/*
