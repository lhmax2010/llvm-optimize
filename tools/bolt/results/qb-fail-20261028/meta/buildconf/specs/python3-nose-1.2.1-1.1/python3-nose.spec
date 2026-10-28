Name:           python3-nose
VCS:            platform/upstream/python-nose#09d23d3a89279bfee2c34999b69c0a8ae7bf5089
Version:        1.2.1
Release:        1.1
Url:            http://readthedocs.org/docs/nose/
Summary:        Nose extends unittest to make testing easier
License:        LGPL-2.0+
Group:          Platform Development/Python
Source:         http://pypi.python.org/packages/source/n/nose/nose-%{version}.tar.gz
Source1001:     %{name}.manifest
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3-setuptools
Requires:       python3-xml
BuildArch:      noarch

%description
Nose extends the test loading and running features of unittest, making
it easier to write, find and run tests.

By default, nose will run tests in files or directories under the current
working directory whose names include "test" or "Test" at a word boundary
(like "test_this" or "functional_test" or "TestClass" but not
"libtest"). Test output is similar to that of unittest, but also includes
captured stdout output from failing tests, for easy print-style debugging.

These features, and many more, are customizable through the use of
plugins. Plugins included with nose provide support for doctest, code
coverage and profiling, flexible attribute-based test selection,
output capture and more.

%prep
%setup -q -n nose-%{version}
cp %{SOURCE1001} .
sed -i 's,man/man1,share/man/man1,' setup.py

%build
/usr/bin/python3 setup.py build

%check
# python3 setup.py test

%install
/usr/bin/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc NEWS README.txt lgpl.txt
%{_bindir}/nosetests*
%{_mandir}/man*/nosetests*
%{python3_sitelib}/*
