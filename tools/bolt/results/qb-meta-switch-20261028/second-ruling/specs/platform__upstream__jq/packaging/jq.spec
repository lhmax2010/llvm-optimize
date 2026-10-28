Name:           jq
Version:        1.8.1
Release:        1
Summary:        A lightweight and flexible command-line JSON processor

License:        MIT AND CC-BY-3.0
URL:            https://jqlang.org/
Source0:        %{name}-%{version}.tar.gz
Source1001:        %{name}.manifest

# Build dependencies based on autotools build system
BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make

# Runtime dependencies
Requires:       libjq = %{version}-%{release}

%description
A lightweight and flexible command-line JSON processor. jq is like sed for
JSON data – you can use it to slice and filter and map and transform
structured data with the same ease that sed, awk, grep and friends let
you play with text.

%package -n libjq
Summary:        Library for a lightweight and flexible command-line JSON processor
Group:          System/Libraries

%description -n libjq
Library for a lightweight and flexible command-line JSON processor.
This package contains the shared library for applications that need to
process JSON data programmatically.

%package -n libjq-devel
Summary:        Development files for jq
Group:          Development/Languages/C and C++
Requires:       libjq = %{version}-%{release}
Requires:       pkgconfig

%description -n libjq-devel
Development files (headers and libraries for jq).
This package contains the header files and development libraries needed
to build applications that use the libjq library.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
# Set compiler flags for Tizen
export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"

# Generate configure script
autoreconf -fi

%configure \
  --with-oniguruma=builtin \
  --disable-static \
  --disable-silent-rules \
  --enable-shared

%{make_build}

%install
%{make_install}

# Remove documentation and manual pages (Tizen policy)
%remove_docs


%post -n libjq -p /sbin/ldconfig

%postun -n libjq -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/%{name}
%{_bindir}/onig-config

%files -n libjq
%manifest %{name}.manifest
%license COPYING
%{_libdir}/lib%{name}.so.*
%{_libdir}/libonig.so.*

%files -n libjq-devel
%manifest %{name}.manifest
%license COPYING
%{_includedir}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/libonig.so
%{_libdir}/pkgconfig/*.pc
