%define modname distribute
%define mod2nam setuptools
Name:           python-%{modname}
Version:        0.6.32
Release:        0
Url:            http://packages.python.org/distribute
Summary:        Easily download, build, install, upgrade, and uninstall Python packages
License:        Python-2.0 or ZPL-2.0
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/d/%{modname}/%{modname}-%{version}.tar.gz
Source1001:     python-distribute.manifest
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python-devel

#Provides:       python-setuptools = %{version}
#Obsoletes:      python-setuptools < %{version}

BuildArch:      noarch
%py_requires

%description
Distribute is a fork of the Setuptools project.

Distribute is intended to replace Setuptools as the standard method for working
with Python module distributions.

%prep
%setup -q -n %{modname}-%{version}
cp %{SOURCE1001} .
rm -f %{modname}.egg-info/*.orig
chmod -x ./*.txt docs/*.txt # Fix executable bits for documentation

%build
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}
rm -rf %{buildroot}%{python_sitelib}/%{mod2nam}/tests # Don't install tests
rm -rf %{buildroot}%{python_sitelib}/%{mod2nam}/*.exe # Remove unneeded files

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/easy_install
%{_bindir}/easy_install-%{py_ver}
%{python_sitelib}/easy_install.py*
%{python_sitelib}/pkg_resources.py*
%{python_sitelib}/_markerlib/
%{python_sitelib}/%{mod2nam}.pth
%{python_sitelib}/%{mod2nam}/
%{python_sitelib}/site.py*
%{python_sitelib}/%{modname}-%{version}-py%{py_ver}.egg-info/
%{python_sitelib}/%{mod2nam}-*-py%{py_ver}.egg-info
