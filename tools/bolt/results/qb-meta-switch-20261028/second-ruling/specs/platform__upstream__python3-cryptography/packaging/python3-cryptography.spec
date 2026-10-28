Name:       python3-cryptography
Summary:    PyCA's cryptography library
Version:    2.3
Release:    0
License:    Apache-2.0 or BSD-3-Clause
Group:      Development/Libraries
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  python3-pytest

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.


%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -Wno-error=incompatible-pointer-types"
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.APACHE LICENSE.BSD
%{python3_sitearch}/cryptography-%{version}-py%{python3_version}.egg-info/*
%{python3_sitearch}/cryptography/*.py
%{python3_sitearch}/cryptography/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/*.py
%{python3_sitearch}/cryptography/hazmat/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/backends/*.py
%{python3_sitearch}/cryptography/hazmat/backends/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/backends/openssl/*.py
%{python3_sitearch}/cryptography/hazmat/backends/openssl/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/bindings/*.py
%{python3_sitearch}/cryptography/hazmat/bindings/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/bindings/_constant_time.abi3.so
%{python3_sitearch}/cryptography/hazmat/bindings/_openssl.abi3.so
%{python3_sitearch}/cryptography/hazmat/bindings/_padding.abi3.so
%{python3_sitearch}/cryptography/hazmat/bindings/openssl/*.py
%{python3_sitearch}/cryptography/hazmat/bindings/openssl/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/primitives/*.py
%{python3_sitearch}/cryptography/hazmat/primitives/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/primitives/asymmetric/*.py
%{python3_sitearch}/cryptography/hazmat/primitives/asymmetric/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/primitives/ciphers/*.py
%{python3_sitearch}/cryptography/hazmat/primitives/ciphers/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/primitives/kdf/*.py
%{python3_sitearch}/cryptography/hazmat/primitives/kdf/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/hazmat/primitives/twofactor/*.py
%{python3_sitearch}/cryptography/hazmat/primitives/twofactor/__pycache__/*.cpython-*.pyc
%{python3_sitearch}/cryptography/x509/*.py
%{python3_sitearch}/cryptography/x509/__pycache__/*.cpython-*.pyc

