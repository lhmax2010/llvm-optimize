Name:           libaio
Version:        0.3.113
Release:        0
Summary:        Linux-Native Asynchronous I/O Access Library
License:        LGPL-2.1+
Group:          Development/Libraries
Url:            http://kernel.org/pub/linux/libs/aio/
Source:         libaio-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	libaio.manifest

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has
a richer API and capability set than the simple POSIX async I/O
facility. This library provides the Linux-native API for async I/O. The
POSIX async I/O facility requires this library to provide
kernel-accelerated async I/O capabilities, as do applications that
require the Linux-native async I/O API.


%package devel
Summary:        Development Files for Linux-native Asynchronous I/O Access
Group:          Development/Libraries/C and C++
Requires:       %name = %version, glibc-devel

%description devel
This package provides header files to include, and libraries to link
with, for the Linux-native asynchronous I/O facility ("async I/O", or
"aio").

%prep
%setup -q
cp %{SOURCE1001} .

%build
#diable asan check option.
%{?asan:/usr/bin/gcc-unforce-options}
%__make %{?_smp_mflags} CC="%__cc" OPTFLAGS="$RPM_OPT_FLAGS"

%install
%__make install prefix=%{buildroot}/usr libdir=%{buildroot}/%{_libdir}

rm -f "%buildroot/%_libdir"/*.a

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%_libdir/libaio.so.*

%files devel
%manifest %{name}.manifest
/usr/include/libaio.h
%_libdir/libaio.so
