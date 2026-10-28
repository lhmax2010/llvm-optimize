Name:           python3-six
VCS:            platform/upstream/python3-six#50c7e708bf7558d20db9f2e6f95ccfc273ca8adb
Version:        1.17.0
Release:        1.1
Summary:        Python 2 and 3 compatibility utilities
License:        MIT
Group:          Development/Libraries/Python
Url:            http://pypi.python.org/pypi/six/
Source:         %{name}-%{version}.tar.gz
Source1:        %{name}.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

BuildArch:      noarch

%description
Six is a Python 2 and 3 compatibility library. It provides utility
functions for smoothing over the differences between the Python
versions with the goal of writing Python code that is compatible on
both Python versions. See the documentation for more information on
what is provided.

%prep
%setup -q -n six-%{version}
cp %{SOURCE1} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

# %check
# python test_six.py

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitelib}/six.py*
%{python3_sitelib}/six-%{version}-py*.egg-info
%{python3_sitelib}/__pycache__/six.*
