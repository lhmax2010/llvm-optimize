Name:           python-cython
Version:        0.29.21
Release:        0
Url:            http://www.cython.org
Summary:        The Cython compiler for writing C extensions for the Python language
License:        Apache-2.0
Group:          Development/Languages/Python

Source:         %{name}-%{version}.tar.gz
BuildRequires:  fdupes
BuildRequires:  python-devel
BuildRequires:  python-xml
BuildRequires:  python-libxml2
BuildRequires:  python-lxml
Provides:       python-cython = %{version}
Obsoletes:      python-cython < %{version}
Requires:       python-xml
Requires:       python-libxml2
Requires:       python-lxml


%description
The Cython language makes writing C extensions for the Python language as
easy as Python itself.  Cython is a source code translator based on the
well-known Pyrex, but supports more cutting edge functionality and
optimizations.

The Cython language is very close to the Python language (and most Python
code is also valid Cython code), but Cython additionally supports calling C
functions and declaring C types on variables and class attributes. This
allows the compiler to generate very efficient C code from Cython code.

This makes Cython the ideal language for writing glue code for external C
libraries, and for fast C modules that speed up the execution of Python
code.

%prep
%setup -q -n cython-%{version}

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}
%fdupes -s %{buildroot}%{python_sitearch} %{buildroot}%{_docdir}
%remove_docs

%files
%license LICENSE.txt
%{_bindir}/cygdb
%{_bindir}/cython
%{_bindir}/cythonize
%{python_sitearch}/Cython*
%{python_sitearch}/cython.py*
%{python_sitearch}/pyximport/
