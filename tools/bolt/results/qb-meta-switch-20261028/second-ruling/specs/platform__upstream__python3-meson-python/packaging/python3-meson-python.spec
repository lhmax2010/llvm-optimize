Name:           python3-meson-python
Version:        0.18.0
Release:        0
Summary:        Meson Python build backend (PEP 517)
License:        MIT
URL:            https://github.com/mesonbuild/meson-python
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        meson_python-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildRequires:  meson
BuildRequires:  python3-pyproject-metadata

BuildArch:      noarch

%description
meson-python is a Python build backend built on top of the Meson build system.
It enables to use Meson for the configuration and build steps of Python
packages. Meson is an open source build system meant to be both extremely fast,
and, even more importantly, as user friendly as possible. meson-python is best
suited for building Python packages containing extension modules implemented in
languages such as C, C++, Cython, Fortran, Pythran, or Rust. Consult the
documentation for more details.

%prep
%setup -q -n meson-python-%{version}
cp %{SOURCE1} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files 
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/mesonpy/*
%{python3_sitelib}/meson_python-%{version}.dist-info/*
