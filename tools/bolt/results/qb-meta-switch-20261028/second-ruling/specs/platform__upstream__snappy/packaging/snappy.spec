#
# spec file for package snappy
#
# Copyright (c) 2015 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define lib_name libsnappy1
Name:           snappy
Version:        1.1.7
Release:        0
Summary:        A fast compressor/decompressor library
License:        BSD-3-Clause
Group:          Development/Libraries/C and C++
Url:            https://github.com/google/snappy/
Source0:        %{name}-%{version}.tar.gz
Source1001:	snappy.manifest
BuildRequires:  autoconf
BuildRequires:	cmake
BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  lzo-devel
BuildRequires:  pkg-config
BuildRequires:  zlib-devel

%description
Snappy is a compression/decompression library. It does not aim for maximum
compression, or compatibility with any other compression library; instead, it
aims for very high speeds and reasonable compression. For instance, compared to
the fastest mode of zlib, Snappy is an order of magnitude faster for most
inputs, but the resulting compressed files are anywhere from 20% to 100%
bigger. On a single core of a Core i7 processor in 64-bit mode, Snappy
compresses at about 250 MB/sec or more and decompresses at about
500 MB/sec or more.

%package -n %{lib_name}
Summary:        Shared library from snappy
Group:          Development/Libraries/C and C++

%description -n %{lib_name}
Snappy is a compression/decompression library. It does not aim for maximum compression,
or compatibility with any other compression library; instead, it aims for very high
speeds and reasonable compression. For instance, compared to the fastest mode of zlib,
Snappy is an order of magnitude faster for most inputs, but the resulting compressed
files are anywhere from 20% to 100% bigger. On a single core of a Core i7 processor
in 64-bit mode, Snappy compresses at about 250 MB/sec or more and decompresses at about
500 MB/sec or more.

This package holds the shared library of snappy.

%package devel
Summary:        Development files for snappy
Group:          Development/Libraries/C and C++
Requires:       %{lib_name} = %{version}

%description devel
Snappy is a compression/decompression library. It does not aim for maximum
compression, or compatibility with any other compression library; instead, it
aims for very high speeds and reasonable compression. For instance, compared to
the fastest mode of zlib, Snappy is an order of magnitude faster for most
inputs, but the resulting compressed files are anywhere from 20% to 100%
bigger. On a single core of a Core i7 processor in 64-bit mode, Snappy
compresses at about 250 MB/sec or more and decompresses at about
500 MB/sec or more.

This package holds the development files for snappy.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%cmake
make %{?_smp_mflags}

%install
%make_install
#find %{buildroot} -type f -name "*.la" -delete -print
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}
install -p -m 0644 COPYING %{buildroot}%{_defaultdocdir}/%{name}/COPYING
rm -Rf %{buildroot}%{_libdir}/cmake

%post   -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root,-)
%doc %{_defaultdocdir}/%{name}/COPYING
%{_libdir}/libsnappy.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/snappy*.h
%{_libdir}/libsnappy.so
%doc %{_defaultdocdir}/%{name}
%exclude %{_defaultdocdir}/%{name}/COPYING
