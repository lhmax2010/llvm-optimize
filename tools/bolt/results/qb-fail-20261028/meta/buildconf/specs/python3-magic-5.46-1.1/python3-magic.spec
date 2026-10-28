Name:           python3-magic
VCS:            platform/upstream/python3-magic#881d3c4f256e656c1ef7595868a87697c724d62e
Version:        5.46
Release:        1.1
Url:            http://www.darwinsys.com/file/
Summary:        Python3 module to use libmagic
License:        BSD-2-Clause
Group:          Platform Development/Python
Source:         ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
Source1001:     python3-magic.manifest
BuildRequires:  findutils
BuildRequires:  libtool
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  zlib-devel

BuildArch:      noarch

%description
This package contains the python3 binding that require the magic "file"
interface.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} ./%{name}.manifest

%build
(cd python &&
%{_bindir}/python3 setup.py build
 )

%install
(cd python &&
%{_bindir}/python3 setup.py install --root=%{buildroot} --prefix=%{_prefix}
 )

%files
%defattr(-,root,root)
%manifest %{name}.manifest
%license python/LICENSE
%{python3_sitelib}/file_magic-*.egg-info/*
%{python3_sitelib}/__pycache__/magic.*
%{python3_sitelib}/magic.*
