Name:       libsrtp
Summary:    This package provides an implementation of the Secure Real-time Transport Protocol (SRTP)
Version:    2.3.0
Release:    2
Group:      Multimedia/Libraries
License:    BSD-3-Clause
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)

%description
This package provides an implementation of the Secure Real-time Transport Protocol

%package devel
Summary:    libsrtp headers and libraries for development.
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
libsrtp headers and libraries for development.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%cmake . -DFULLVER=%{version}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}

%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/*.so

%files devel
%manifest %{name}.manifest
%{_includedir}/srtp2/*
%{_libdir}/pkgconfig/*.pc

