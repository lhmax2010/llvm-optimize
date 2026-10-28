Name:       gtest
Summary:    Google C++ Testing Framework
Version:    1.15.2
Release:    0

# ==========================================================
License:    BSD-3-Clause
# ==========================================================

Group:      Definition/Libraries/C and C++
Source0:    %{name}-%{version}.tar.gz
Source1:    Fix-build-error-at-cmake.patch
Source1001: %{name}.manifest

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires:  cmake
Provides:   libgtest_main.so.0 libgtest.so.0
Provides:   libgmock_main.so.0 libgmock.so.0

%description
Google's framework for writing C++ tests on a variety of platforms (Linux, Mac
OS X, Windows, Cygwin, Windows CE, and Symbian). Based on the xUnit
architecture. Supports automatic test discovery, a rich set of assertions,
user-defined assertions, death tests, fatal and non-fatal failures, value- and
type-parameterized tests, various options for running the tests, and XML test
report generation.


%package devel
Summary:    Google C++ Testing Framework
Requires:   %{name} = %{version}

%description devel
Google C++ Testing Framework


%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1}

# ==========================================================
# build section
# how to actually build the software we are packaging
# ==========================================================
%build
mkdir -p build
cd build
%{cmake} ..
%{__make} %{?_smp_mflags}
cd -


# ==========================================================
# install section
# how to actually build the software we are packaging
# ==========================================================
%install
cd build
%{make_install}
cd -

rm -f %{buildroot}/%{_includedir}/gmock/internal/custom/README.md
rm -f %{buildroot}/%{_includedir}/gtest/internal/custom/README.md

%clean

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

# ==========================================================
# files section
# The list of files that will be installed in the end
# user’s system.
# ==========================================================
%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/*.so.*
%{_libdir}/*.so

%files devel
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/pkgconfig/gtest_main.pc
%{_libdir}/pkgconfig/gtest.pc
%{_libdir}/pkgconfig/gmock_main.pc
%{_libdir}/pkgconfig/gmock.pc
%{_includedir}/gmock/*.h
%{_includedir}/gmock/internal/*.h
%{_includedir}/gmock/internal/custom/*.h
%{_includedir}/gtest/*.h
%{_includedir}/gtest/internal/*.h
%{_includedir}/gtest/internal/custom/*.h
%{_libdir}/cmake/GTest/*.cmake
