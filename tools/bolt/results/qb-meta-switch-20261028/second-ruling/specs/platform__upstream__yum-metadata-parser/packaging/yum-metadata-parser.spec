%{!?python_sitelib_platform: %define python_sitelib_platform %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           yum-metadata-parser
Version:        1.1.4
Release:        0
License:        GPL-2.0
Summary:        A fast metadata parser for yum
Url:            http://linux.duke.edu/projects/yum/
Group:          Development/Libraries
Source0:        http://linux.duke.edu/projects/yum/download/%{name}/%{name}-%{version}.tar.gz
Source1001: 	yum-metadata-parser.manifest
BuildRequires:  pkgconfig
BuildRequires:  sqlite-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(python-2.7)
Requires:       glib2 >= 2.15
Conflicts: yum < 3.2.0

%description
Fast metadata parser for yum implemented in C.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --root=%{buildroot}

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{python_sitelib_platform}/_sqlitecache.so
%{python_sitelib_platform}/sqlitecachec.py
%{python_sitelib_platform}/sqlitecachec.pyc
%{python_sitelib_platform}/sqlitecachec.pyo

%{python_sitelib_platform}/*egg-info

%changelog
