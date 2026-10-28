#
# spec file for package libmd
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           libmd
VCS:            platform/upstream/libmd#982f43d0d75d238712bd35b8a142d3412a91afbf
Version:        1.1.0
Release:        1.1
Summary:        Message digest functions from BSD systems
License:        BSD-2-Clause OR BSD-3-Clause OR ISC OR SUSE-Public-Domain
URL:            https://www.hadrons.org/software/libmd/
Source:         libmd-%{version}.tar.xz
Source1001:     %{name}.manifest 

BuildRequires:  autoconf

%description
The libmd library provides a few message digest ("hash") functions, as
found on various BSDs on a library with the same name and with a compatible
API.

Digests supported: MD2/4/5, RIPEMD160, SHA1, SHA2-256/384/512.

%package devel
Summary:        Provides message digest functions from BSD systems
Requires:       %{name} = %{version}

%description devel
The libmd library provides a few message digest ("hash") functions, as
found on various BSDs on a library with the same name and with a compatible
API.

Digests supported: MD2/4/5, RIPEMD160, SHA1, SHA2-256/384/512.

%prep
%setup -q
cp %{SOURCE1001} .

%build
./autogen
%configure \
  --disable-static \
  --disable-silent-rules
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%remove_docs

%check
%make_build check

%files
%manifest %{name}.manifest
%license COPYING
%{_libdir}/%{name}.so.*

%files devel
%manifest %{name}.manifest
%license COPYING
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/libmd.pc
