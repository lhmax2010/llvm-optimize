Name:           libsigc++
Version:        2.12.1
Release:        1
Summary:        Typesafe Signal Framework for C++
License:        LGPL-2.1-or-later
URL:            https://github.com/libsigcplusplus/libsigcplusplus
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  meson
BuildRequires:  pkg-config
BuildRequires:  mm-common
BuildRequires:  libxslt-tools
BuildRequires:  doxygen
BuildRequires:  m4
BuildRequires:  python3

%description
This library implements a full callback system for use in widget
libraries, abstract interfaces, and general programming. It is the most
complete library of its kind with the ability to connect an abstract
callback to a class method, function, or function object. It contains
adaptor classes for connection of dissimilar callbacks and has an ease
of use unmatched by other C++ callback libraries.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Development files and headers for %{name}.
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
%meson \
    -Dmaintainer-mode=true \
    -Dbuild-deprecated-api=true \
    -Dbuild-documentation=false \
    -Dbuild-examples=false \
    -Dbuild-tests=false \
    -Dbenchmark=false \
    -Dwarning_level=1

%meson_build

%install
%meson_install

# Remove static libraries and libtool files
find %{buildroot} -type f -name "*.a" -delete -print
find %{buildroot} -type f -name "*.la" -delete -print

%remove_docs

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libsigc-2.0.so.*

%files devel
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libsigc-2.0.so
%{_libdir}/pkgconfig/sigc++-2.0.pc
%{_libdir}/sigc++-2.0/include/
%{_includedir}/sigc++-2.0/
