Name:           python3-distlib
Version:        0.4.0
Release:        1
Summary:        packaging and distribution of Python software
License:        Python-2.0
Group:          Development/Languages/Python
Source:         distlib-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     Add-setup.py-to-use-setuptools.patch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
Distlib is a library which implements low-level functions that relate to packaging and distribution of Python software.


%prep
%setup -q -n distlib-%{version}
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
rm -f %{buildroot}/%{python3_sitelib}/distlib/*.exe

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{python3_sitelib}/distlib-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/distlib/*.py
%{python3_sitelib}/distlib/__pycache__/*.cpython-*.pyc
