Name:       python3-more-itertools
Summary:    More routines for operating on iterables, beyond itertools
Version:    10.8.0
Release:    0
License:    MIT
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3
BuildRequires:  python3-build
BuildRequires:  python3-flit_core
BuildRequires:  python3-pip

BuildArch:      noarch

%description
I love itertools; it's one of the most beautiful, composable standard libs.
Whenever I have an iteration problem, there's almost always an itertools
routine that fits it perfectly. Sometimes, however, neither itertools nor the
recipes included in its docs do quite what I need.

Here I've collected several routines I've reached for but not found. Since
they are deceptively tricky to get right, I've wrapped them up into a library.
We've also included implementations of the recipes from the itertools
documentation. Enjoy! Any additions are welcome; just file a pull request.


%prep
%setup -q
cp %{SOURCE1} .

%build
%{_bindir}/python3 -m build -n

%install
%{_bindir}/python3 -m pip install --root %{buildroot} ./dist/more_itertools-%{version}-py3-*.whl

%clean

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/more_itertools/*
%{python3_sitelib}/more_itertools-%{version}.dist-info/*

