%define sover 5
Name:           libzip
Version:        1.11.4
Release:        1
Summary:        C library for reading, creating, and modifying zip archives
License:        BSD-3-Clause
URL:            https://libzip.org/
Source0:        https://libzip.org/download/libzip-%{version}.tar.gz
Source1001:        libzip.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(bzip2)

Provides:       libzip-util = %{version}
Obsoletes:      libzip-util < %{version}

%description
libzip is a C library for reading, creating, and modifying zip
archives. Files can be added from data buffers, files, or compressed. This
package contains a set of small utilities built using libzip
 * zipmerge - merge source zip archives into the target one
 * zipcmp - compares the zip archives and check if they contains same files

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
libzip is a C library for reading, creating, and modifying zip
archives. This package contains devel files.

%package tools
Summary:        Utilities from the libzip project
Obsoletes:      libzip < %{version}
Provides:       libzip = %{version}

%description tools
This subpackage contains zipcmp and zipmerge, for comparison of two
archives, and merging multiple archives together, respectively.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%cmake . \
    -DDOCUMENTATION_FORMAT=man \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_FLAGS="%{optflags} -fPIC" \
    -DCMAKE_EXE_LINKER_FLAGS=" -pie" \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DBUILD_TOOLS=ON \
    -DBUILD_REGRESS=OFF \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_DOC=OFF \
    -DENABLE_OPENSSL=ON \
    -DENABLE_BZIP2=ON \
    -DENABLE_ZSTD=OFF \
    -DENABLE_LZMA=OFF \
    -DENABLE_MBEDTLS=OFF \
    -DENABLE_GNUTLS=OFF \
    -DENABLE_COMMONCRYPTO=OFF

%__make %{?_smp_mflags}

%install
%make_install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/libzip.la
%remove_docs

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libzip.so.%{sover}*

%files devel
%manifest %{name}.manifest
%license LICENSE
%{_includedir}/zip.h
%{_includedir}/zipconf.h
%{_libdir}/libzip.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/*.cmake
%{_libdir}/cmake/%{name}/modules/*.cmake

%files tools
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/zipcmp
%{_bindir}/zipmerge
%{_bindir}/ziptool

