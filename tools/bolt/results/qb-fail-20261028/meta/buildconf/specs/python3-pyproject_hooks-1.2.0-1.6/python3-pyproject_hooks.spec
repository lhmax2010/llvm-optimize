Name:           python3-pyproject_hooks
VCS:            platform/upstream/python3-pyproject_hooks#60db7b32f2a6fbba841617c13fb4ff2a419fda7d
Version:        1.2.0
Release:        1.6
Summary:        Wrappers to call pyproject.toml-based build backend hooks
License:        MIT
URL:            https://github.com/pypa/pyproject-hooks
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
Source2:        pyproject_hooks-%{version}-py3-none-any.whl

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
This is a low-level library for calling build-backends in ``pyproject.toml``-based project.
It provides the basic functionality to help write tooling that generates distribution files from Python projects.

If you want a tool that builds Python packages, you'll want to use https://github.com/pypa/build instead.
This is an underlying piece for `pip`, `build` and other "build frontends" use to call "build backends" within them.

Note: The ``pep517`` project has been replaced by this project (low level) and the ``build`` project (high level).

%prep
%setup -q -n pyproject_hooks-%{version}
cp %{SOURCE1} .

%build
#%%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} %{SOURCE2}

%files 
%license LICENSE
%{python3_sitelib}/pyproject_hooks/*
%{python3_sitelib}/pyproject_hooks-%{version}.dist-info/*
