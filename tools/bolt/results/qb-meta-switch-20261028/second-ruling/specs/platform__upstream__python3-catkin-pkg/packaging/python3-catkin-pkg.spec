Name:           python3-catkin-pkg
Version:        1.1.0
Release:        1
Summary:        catkin package library
License:        BSD
Group:          Development/Languages/Python
Source:         catkin_pkg-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

BuildArch:      noarch

Provides: python3-catkin_pkg

%description
The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries.


%prep
%setup -q -n catkin_pkg-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
# %license LICENSE
%{_bindir}/catkin_create_pkg
%{_bindir}/catkin_find_pkg
%{_bindir}/catkin_generate_changelog
%{_bindir}/catkin_package_version
%{_bindir}/catkin_prepare_release
%{_bindir}/catkin_tag_changelog
%{_bindir}/catkin_test_changelog
%{python3_sitelib}/catkin_pkg-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/catkin_pkg/*.py
%{python3_sitelib}/catkin_pkg/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/catkin_pkg/cli/*.py
%{python3_sitelib}/catkin_pkg/cli/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/catkin_pkg/templates/CMakeLists.txt.in
%{python3_sitelib}/catkin_pkg/templates/metapackage.cmake.in
%{python3_sitelib}/catkin_pkg/templates/package.xml.in
