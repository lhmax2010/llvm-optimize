%define major 0
%define libname %{name}%{major}
Name:           libdeflate
Version:        1.25
Release:        0
Summary:        Library for DEFLATE/zlib/gzip compression and decompression
License:        MIT
URL:            https://github.com/ebiggers/libdeflate
Source:         %{name}-%{version}.tar.gz
Source1001:	%{name}.manifest
BuildRequires:  cmake
BuildRequires:  zlib-devel

%description
libdeflate is a library for whole-buffer DEFLATE-based compression
and decompression. It supports raw, zlib-wrapped and gzip-wrapped DEFLATE.
It is significantly faster than zlib and gzip (+72-187%%).
In addition, libdeflate provides optional high compression modes
above zlib's "level 9".

%package -n    %{libname}
Summary:        Library for DEFLATE/zlib/gzip compression and decompression

%description -n    %{libname}
libdeflate is a library for whole-buffer DEFLATE-based compression
and decompression. It supports raw, zlib-wrapped and gzip-wrapped DEFLATE.
It is significantly faster than the zlib library:

 - decompression speedup over gzip-1.10 is 2.28x (generic), 2.87x (AVX2)
 - compression speedup over gzip is 1.72x (generic), 2.23x (AVX2)

In addition, libdeflate provides optional high compression modes
above zlib's "level 9".

%package tools
Summary:        File compression utility

%description tools
A gzip implementation that uses libdeflate which is significantly
faster than the GNU gzip implementation (+72-187%%).

%package devel
Summary:        Development files for %{name}
Requires:       %{libname} = %{version}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1
cp %{SOURCE1001} .

%build
%cmake \
  -DLIBDEFLATE_BUILD_STATIC_LIB=ON \
  -DLIBDEFLATE_BUILD_TESTS=ON
%make_build

%install
%make_install

# Delete libdeflate-gunzip and replace with symlink libdeflate-gzip to fix dwz break with hardlink.
# boo#1180984
rm %{buildroot}%{_bindir}/libdeflate-gunzip
ln -s ./libdeflate-gzip %{buildroot}%{_bindir}/libdeflate-gunzip

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files tools
%manifest %{name}.manifest
%license COPYING
%{_bindir}/libdeflate-gzip
%{_bindir}/libdeflate-gunzip

%files -n %{libname}
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libdeflate.so.%{major}

%files devel
%license COPYING
%doc README.md
%manifest %{name}.manifest
%{_includedir}/libdeflate.h
%{_libdir}/libdeflate.so
%{_libdir}/cmake/libdeflate
%{_libdir}/pkgconfig/libdeflate.pc

%changelog
