Name:           python3-sqlite
Version:        0.5.4
Release:        0
Summary:        DB-API 2.0 interface for SQLite 3.x
License:        Zlib
Group:          Platform Development/Python
Url:            https://github.com/coleifer/pysqlite3
Source:         %{name}-%{version}.tar.gz
Source1001: 	python3-sqlite.manifest

BuildRequires:  pkgconfig(python3)
BuildRequires:  sqlite3-devel
BuildRequires:  python3-setuptools

Requires:       sqlite3

%description
Python3 interface to SQLite 3
pysqlite is an interface to the SQLite 3.x embedded relational database engine.
It is almost fully compliant with the Python3 database API version 2.0 also
exposes the unique features of SQLite.

%prep
%setup -q -n pysqlite3-%{version}
cp %{SOURCE1001} .

%build
export CFLAGS="%{optflags}"
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
rm -rf %{buildroot}%{_prefix}/pysqlite3-doc # Remove wrongly installed junk

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitearch}/pysqlite3/
%{python3_sitearch}/pysqlite3-%{version}-py*.egg-info
