Name:           python3-rosdep
Version:        0.26.0
Release:        1
Summary:        rosdep is a command-line tool for installing system dependencies.
License:        BSD-3-Clause 
Group:          Development/Languages/Python
Source:         rosdep-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

Requires:  python3-PyYAML
Requires:  python3-rospkg
Requires:  python3-catkin-pkg
Requires:  python3-rosdistro
Requires:  python3-distro
Requires:  python3-dateutil
Requires:  python3-docutils

BuildArch:      noarch

%description
rosdep is a command-line tool for installing system dependencies.


%prep
%setup -q -n rosdep-%{version}

%build
cp %{SOURCE1001} .
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/rosdep
%{_bindir}/rosdep-source
%{python3_sitelib}/rosdep-%{version}-py%{python3_version}.egg-info/*
%{python3_sitelib}/rosdep2/*.py
%{python3_sitelib}/rosdep2/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/rosdep2/ament_packages/*.py
%{python3_sitelib}/rosdep2/ament_packages/__pycache__/*.cpython-*.pyc
%{python3_sitelib}/rosdep2/platforms/*.py
%{python3_sitelib}/rosdep2/platforms/__pycache__/*.cpython-*.pyc
