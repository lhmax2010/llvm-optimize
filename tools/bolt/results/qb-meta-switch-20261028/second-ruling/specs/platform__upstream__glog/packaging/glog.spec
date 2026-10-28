%define	RELEASE	1
%define	prefix	%{_prefix}
%define NAME    glog
%define VERSION 0.3.5

Name: %NAME
Summary: A C++ application logging library
Version: %VERSION
Release: 1
Group: Development/Libraries
URL: http://github.com/google/glog
License: BSD-3-Clause
Vendor: Google
Packager: Google Inc. <opensource@google.com>
Source: %{name}-%{version}.tar.gz
Patch0: 0001-fix-build-break-on-tizen-gcc13.patch
Patch1: 0002-remove-register-keyword-from-unittest.patch
Distribution: Redhat 7 and above.
Prefix: %prefix

%description
The %name package contains a library that implements application-level
logging.  This library provides logging APIs based on C++-style
streams and various helper macros.

%package devel
Summary: A C++ application logging library
Group: Development/Libraries
Requires: %{NAME} = %{VERSION}

%description devel
The %name-devel package contains static and debug libraries and header
files for developing applications that use the %name package.

%changelog
    * Wed Mar 26 2008 <opensource@google.com>
    - First draft

%prep
%setup

%patch0 -p1
%patch1 -p1

%build
%autogen.sh
./configure
make prefix=%prefix

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix} libdir=$RPM_BUILD_ROOT%{_libdir} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

## Mark all installed files within /usr/share/doc/{package name} as
## documentation.  This depends on the following two lines appearing in
## Makefile.am:
##     docdir = $(prefix)/share/doc/$(PACKAGE)-$(VERSION)
##     dist_doc_DATA = AUTHORS COPYING ChangeLog INSTALL NEWS README
%docdir %{prefix}/share/doc/%{NAME}-%{VERSION}
%{prefix}/share/doc/%{NAME}-%{VERSION}/*
%{_libdir}/libglog.so.0
%{_libdir}/libglog.so.0.0.0

%files devel
%defattr(-,root,root)

%{_includedir}/glog
%{_libdir}/libglog.a
%{_libdir}/libglog.la
%{_libdir}/libglog.so
%{_libdir}/pkgconfig/libglog.pc
