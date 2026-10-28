Name:           libxml++
Version:        5.6.0
Release:        1
Summary:        C++ interface for XML files
License:        LGPL-2.1-or-later
URL:            https://libxmlplusplus.github.io/libxmlplusplus/
Source0:        %{name}-%{version}.tar.gz
Source1001:        %{name}.manifest

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  glibmm-devel

%description
libxml++ provides a C++ interface for XML files. It presently uses
libxml2 to access the XML files. This is a C++ wrapper for the libxml2
XML parser library.

%package devel
Summary:        Development files for libxml++
Requires:       %{name} = %{version}
Requires:       glibmm-devel

%description devel
This package contains all necessary include files and libraries needed
to develop applications that use libxml++.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
# Meson build with Tizen-specific options
%meson \
    -Dbuild-deprecated-api=true \
    -Dbuild-documentation=false \
    -Dbuild-examples=false \
    -Dbuild-tests=false \
    -Dmaintainer-mode=false \
    -Dwarning_level=1

%meson_build

%install
%meson_install

# Remove static libraries and libtool files
find %{buildroot} -name "*.a" -delete
find %{buildroot} -name "*.la" -delete

# Remove documentation and man pages (Tizen policy)
%remove_docs

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libxml++-5.0.so.*

%files devel
%license COPYING
%{_includedir}/libxml++-5.0/
%{_libdir}/libxml++-5.0/
%{_libdir}/libxml++-5.0/include/libxml++config.h
%{_libdir}/libxml++-5.0.so
%{_libdir}/pkgconfig/libxml++-5.0.pc
