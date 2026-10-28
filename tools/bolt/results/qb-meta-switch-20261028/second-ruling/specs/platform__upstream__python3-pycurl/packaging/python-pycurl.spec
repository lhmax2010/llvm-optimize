Name:           python3-pycurl
Version:        7.45.7
Release:        0
Summary:        PycURL -- cURL library module
License:        LGPL-2.1-or-later AND MIT
URL:            http://pycurl.io/
Source0:         %{name}-%{version}.tar.gz

Source1000:     Fix-build-error-for-python-3.12.patch
Source1001:     disable_randomly_failing_tests.patch

# PATCH-FIX-UPSTREAM handle difference between libssh and libssh2
Source1002:         pycurl-libssh.patch
# PATCH-FIX-OPENSUSE increase_test_timeout.diff -- Increase the timeout in a test so it doesn't fail when obs is overloaded
Source1003:         increase_test_timeout.diff
# PATCH-FIX-OPENSUSE make-leap15-compat.patch mcepl@suse.com
# Make tests passing with Leap 15.2
Source1004:         make-leap15-compat.patch
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libcurl) >= 7.19.0
BuildRequires:  pkgconfig(openssl3)


%description
This module provides bindings for the cURL library.


%prep
%setup -q -n %{name}-%{version}
%{__patch} -p1 < %{SOURCE1000}
%{__patch} -p1 < %{SOURCE1001}
%{__patch} -p1 < %{SOURCE1002}
%{__patch} -p1 < %{SOURCE1003}
%{__patch} -p1 < %{SOURCE1004}

# temporarily remove a failing test-case until the issue is
# fixed in curl: https://github.com/curl/curl/issues/6615
rm -f tests/failonerror_test.py

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
export PYCURL_SSL_LIBRARY=openssl
python3 setup.py build --with-openssl

%install
export PYCURL_SSL_LIBRARY=openssl
python3 setup.py install -O1 --skip-build --root=%{buildroot} --prefix=%{_prefix} --with-openssl

rm -rf %{buildroot}%{_datadir}/doc # Remove wrongly installed junk



%files 
%license COPYING-LGPL COPYING-MIT
%doc AUTHORS ChangeLog README.rst
%{python3_sitearch}/*
