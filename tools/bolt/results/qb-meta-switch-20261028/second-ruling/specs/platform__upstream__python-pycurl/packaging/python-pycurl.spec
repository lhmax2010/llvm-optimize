%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-pycurl
Version:        7.19.0
Release:        0
Summary:        A Python interface to libcurl
Group:          Platform Development/Python
License:        LGPL-2.1+ or MIT/X11
URL:            http://pycurl.sourceforge.net/
Source0:        pycurl-%{version}.tar.gz
Source1001:     python-pycurl.manifest
BuildRequires:  python-devel
BuildRequires:  curl-devel >= 7.19.0
BuildRequires:   pkgconfig(openssl3)
BuildRequires:  pkgconfig(libcares)
Requires:	libcurl
Provides:       pycurl = %{version}-%{release}

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup -q -n pycurl-%{version}
chmod a-x examples/*

%build
cp %{SOURCE1001} .
export CFLAGS="%{optflags} -DHAVE_CURL_OPENSSL"
%{__python} setup.py build

%check
export PYTHONPATH=$PWD/build/lib*
%{__python} tests/test_internals.py -q

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot} --prefix=%{_prefix}


%remove_docs

%files
%manifest %{name}.manifest
%license COPYING
%manifest python-pycurl.manifest
%{python_sitearch}/curl/*
%{python_sitearch}/pycurl*
