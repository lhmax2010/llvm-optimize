Name:           libphonenumber
Version:        7.0.6
Release:        1
License:        Apache-2.0 and BSD-3-Clause
Summary:        A library for manipulating international phone numbers
Url:            http://code.google.com/p/libphonenumber/
Group:          Social & Content/Libraries
Source:         libphonenumber-%{version}.tgz

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  gtest-devel
BuildRequires:  re2-devel
BuildRequires:  pkgconfig(protobuf-lite)
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(icu-i18n)

%description
Google's common Java, C++ and Javascript library for parsing,
formatting, storing and validating international phone numbers. The
Java version is optimized for running on smartphones, and is used by
the Android framework since 4.0 (Ice Cream Sandwich).

%package devel
Summary:        Devel package for library
Group:          Social & Content/Libraries
Requires:       libphonenumber = %{version}
Requires:       protobuf-devel

%description devel
Google's common Java, C++ and Javascript library for parsing,
formatting, storing and validating international phone numbers. The
Java version is optimized for running on smartphones, and is used by
the Android framework since 4.0 (Ice Cream Sandwich).

%prep
%setup -q -n libphonenumber

%build
export LDFLAGS="-Wl,--copy-dt-needed-entries -Wl,--as-needed"
cmake -DCMAKE_SKIP_RPATH=ON -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_INSTALL_LIBDIR=%{_libdir} cpp

# Parallel builds are broken and/or not supported by upstream, don't
# use them. The generated Makefile lacks the geocoding_data.cc ->
# generate_geocoding_data dependency and thus code generator may still
# be producing the file when the C++ compiler is already parsing it.
%{__make}

%install
%{__make} DESTDIR=%{buildroot} install
rm %{buildroot}/%{_libdir}/*.a
# Exported header has dependency on lock_posix.h but lock_posix.h is not installed.
cp cpp/src/phonenumbers/base/synchronization/lock_posix.h %{buildroot}/%{_includedir}/phonenumbers/base/synchronization/

%post   -n libphonenumber -p /sbin/ldconfig

%postun -n libphonenumber -p /sbin/ldconfig


%files -n libphonenumber
%defattr(-, root, root, -)
%doc AUTHORS
%license LICENSE
%{_libdir}/libphonenumber.so.*
%{_libdir}/libgeocoding.so.*

%files devel
%defattr(-, root, root, -)
%{_includedir}/phonenumbers
%{_libdir}/libphonenumber.so
%{_libdir}/libgeocoding.so
