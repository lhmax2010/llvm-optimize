#
# spec file for package python-pysqlite
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           python-sqlite
Version:        2.6.3
Release:        0
Url:            http://pysqlite.googlecode.com/
Summary:        DB-API 2.0 interface for SQLite 3.x
License:        Zlib
Group:          Platform Development/Python
Source:         http://pysqlite.googlecode.com/files/pysqlite-%{version}.tar.gz
Source1001: 	python-sqlite.manifest
BuildRequires:  python-devel
BuildRequires:  sqlite3-devel
Requires:       sqlite3

%description
Python interface to SQLite 3

pysqlite is an interface to the SQLite 3.x embedded relational database engine.
It is almost fully compliant with the Python database API version 2.0 also
exposes the unique features of SQLite.

%prep
%setup -q -n pysqlite-%{version}
cp %{SOURCE1001} .

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}
rm -rf %{buildroot}%{_prefix}/pysqlite2-doc # Remove wrongly installed junk

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{python_sitearch}/*

%changelog
