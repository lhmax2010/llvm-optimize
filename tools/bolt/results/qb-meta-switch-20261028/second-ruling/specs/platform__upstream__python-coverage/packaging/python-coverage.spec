Name:           python-coverage
Version:        3.6
Release:        0
Summary:        Code coverage measurement for Python
Url:            http://nedbatchelder.com/code/coverage
License:        BSD-3-Clause
Group:          Platform Development/Python
Source:         coverage-%{version}.tar.gz
Source1001: 	python-coverage.manifest
BuildRequires:  python-devel
BuildRequires:  python-distribute
BuildRequires:  python-xml
Requires:       python-xml

%description
Coverage.py measures code coverage, typically during test execution. It uses
the code analysis tools and tracing hooks provided in the Python standard
library to determine which lines are executable, and which have been executed.

%prep
%setup -q -n coverage-%{version}
cp %{SOURCE1001} .

%build
%{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%{_bindir}/coverage*
%{py_sitedir}/*
