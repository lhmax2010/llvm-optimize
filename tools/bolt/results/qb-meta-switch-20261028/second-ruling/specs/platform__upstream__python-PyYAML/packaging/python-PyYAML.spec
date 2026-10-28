Name:           python-PyYAML
Version:        3.10
Release:        0
Url:            http://pyyaml.org/wiki/PyYAML
Summary:        YAML parser and emitter for Python
License:        MIT
Group:          Development/Languages/Python
Source:         http://pypi.python.org/packages/source/P/PyYAML/PyYAML-%{version}.tar.gz
Source1001: 	python-PyYAML.manifest
Source1002: 	Migration_for_python_3.11.patch
BuildRequires:  python-devel
BuildRequires:  python-nose
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
Provides:       python-yaml = %{version}
Obsoletes:      python-yaml < %{version}

%description
YAML is a data serialization format designed for human readability
and interaction with scripting languages.  PyYAML is a YAML parser
and emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%package -n python3-PyYAML
Summary:	YAML parser and emitter for Python3
Provides:	python3-yaml = %{version}
Obsoletes:	python3-yaml < %{version}

%description -n python3-PyYAML
PyYAML for Python3

YAML is a data serialization format designed for human readability
and interaction with scripting languages.  PyYAML is a YAML parser
and emitter for Python.

PyYAML features a complete YAML 1.1 parser, Unicode support, pickle
support, capable extension API, and sensible error messages.  PyYAML
supports standard YAML tags and provides Python-specific tags that
allow to represent an arbitrary Python object.

PyYAML is applicable for a broad range of tasks from complex
configuration files to object serialization and persistance.

%prep
%setup -q -n PyYAML-%{version}
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
CFLAGS="%{optflags}" %{__python} setup.py build
CFLAGS="%{optflags}" python3 setup.py build
find examples -type f | xargs chmod -x # Fix example permissions

%check
%{__python} setup.py test


%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc LICENSE
%{python_sitearch}/*

%define python3_sitearch %(/usr/bin/python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

%files -n python3-PyYAML
%manifest %{name}.manifest
%defattr(-,root,root,-)
%doc LICENSE
%{python3_sitearch}/*

%changelog
