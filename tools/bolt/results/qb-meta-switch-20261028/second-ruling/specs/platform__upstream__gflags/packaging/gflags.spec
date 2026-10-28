Name: gflags
Summary: A commandline flags library that allows for distributed flags
Version: 2.2.1
Release: 1
Group: Development/Libraries
URL: http://code.google.com/p/gflags
License: BSD
Vendor: Google Inc. and others
Packager: Google Inc. and others <google-gflags@googlegroups.com>
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.manifest
Distribution: Redhat 7 and above.

BuildRequires: cmake
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
The %name package contains a library that implements commandline flags
processing.  As such it's a replacement for getopt().  It has increased
flexibility, including built-in support for C++ types like string, and
the ability to define flags in the source file in which they're used.

%package devel
Summary: A commandline flags library that allows for distributed flags
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
The %name-devel package contains static and debug libraries and header
files for developing applications that use the %name package.

%prep
%setup -q
cp %{SOURCE1} .

%build
mkdir -p build
cd build
%cmake .. -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_libdir}
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

# Remove unnecessary files
rm -rf %{buildroot}%{_libdir}/cmake
rm -rf %{buildroot}/home/abuild

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%manifest %{name}.manifest
%{_libdir}/*.so.*
%{_bindir}/gflags_completions.sh

%files devel
%defattr(-,root,root)
%{_includedir}/gflags
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
