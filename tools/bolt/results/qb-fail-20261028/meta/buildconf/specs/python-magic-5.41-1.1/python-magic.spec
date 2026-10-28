Name:           python-magic
VCS:            platform/upstream/python-magic#4e7fcf573530b8d84bfb63b36d1fe24eadb0e156
Version:        5.41
Release:        1.1
Url:            http://www.darwinsys.com/file/
Summary:        Python module to use libmagic
License:        BSD-2-Clause
Group:          Platform Development/Python
Source:         ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
Source1001:     python-magic.manifest
BuildRequires:  findutils
BuildRequires:  libtool
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  zlib-devel

BuildArch:      noarch

%description
This package contains the python binding that require the magic "file"
interface.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} ./%{name}.manifest

%build
(cd python &&
%{__python} setup.py build
 )

%install
(cd python &&
%{__python} setup.py install --root=%{buildroot} \
                        --prefix=%{_prefix}
 )

%files
%defattr(-,root,root)
%manifest %{name}.manifest
%license python/LICENSE
%{python_sitelib}/file_magic-*.egg-info/*
%{python_sitelib}/magic.*
