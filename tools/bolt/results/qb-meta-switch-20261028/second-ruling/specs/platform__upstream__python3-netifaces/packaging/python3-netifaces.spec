Name:       python3-netifaces
Summary:    Portable network interface information
Version:    0.11.0
Release:    0
License:    MIT
Group:      Development/Languages/Python
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest


BuildRequires:  pkgconfig(python3)
BuildRequires:  python3-setuptools

%description
netifaces provides a (hopefully portable-ish) way for Python programmers to
get access to a list of the network interfaces on the local machine, and to
obtain the addresses of those network interfaces.

The package has been tested on Mac OS X, Windows XP, Windows Vista, Linux and
Solaris. On Windows, it is currently not able to retrieve IPv6 addresses,
owing to shortcomings of the Windows API.

It should work on other UNIX-like systems provided they implement either
getifaddrs() or support the SIOCGIFxxx socket options, although the data
provided by the socket options is normally less complete.


%prep
%setup -q
cp %{SOURCE1001} .

%build
%{_bindir}/python3 setup.py build

%install
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{python3_sitearch}/netifaces-%{version}-py%{python3_version}.egg-info/*
%{python3_sitearch}/netifaces.cpython-*.so
