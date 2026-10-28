#
# spec file for package gpgme
#
# Copyright (c) 2025 Tizen Project
#
# License: GPL-2.0-or-later and LGPL-2.1-or-later
# This package contains GPL-2.0-or-later and LGPL-2.1-or-later licensed components
# Tizen Policy: GPL 2.0-or-later and LGPL 2.1-or-later are compatible with Tizen

Name:           gpgme
Version:        1.24.3
Release:        1
Summary:        A Library Designed to Give Applications Easy Access to GnuPG
License:        GPL-2.0-or-later
URL:            http://www.gnupg.org/related_software/gpgme/
Source0:        %{name}-%{version}.tar.bz2
Source1:        %{name}.manifest
Source2:        build_gpgme-config.patch


BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libassuan-devel >= 2.4.2
BuildRequires:  libgpg-error-devel >= 1.36
BuildRequires:  gpg2 >= 2.0.10

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications. It provides a high-level Crypto API for
encryption, decryption, signing, signature verification, and key
management. Currently it uses GnuPG as its back-end, but the API is not
restricted to this engine.

Because the direct use of GnuPG from an application can be a
complicated programming task, it is suggested that all software should
try to use GPGME instead. This way bug fixes or improvements can be
done at a central place and every application benefits from this.
Authors of MUAs should especially consider using GPGME. Creating a set
of standard widgets for common key selection tasks is even planned.

%package -n libgpgme
License:        LGPL-2.1-or-later
Summary:        A Library Designed to give Applications easy Access to GnuPG
Requires:       gpg2

%description -n libgpgme
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications. It provides a high-level Crypto API for
encryption, decryption, signing, signature verification, and key
management. Currently it uses GnuPG as its back-end, but the API is not
restricted to this engine.

Who Should use GPGME?

Because the direct use of GnuPG from an application can be a
complicated programming task, it is suggested that all software should
try to use GPGME instead. This way bug fixes or improvements can be
done at a central place and every application benefits from this.
Authors of MUAs should especially consider using GPGME. Creating a set
of standard widgets for common key selection tasks is even planned.

%package -n libgpgme-devel
Summary:        Development files for GPGME library
Requires:       libgpgme = %{version}-%{release}
Requires:       libgpg-error-devel

%description -n libgpgme-devel
Development files for the GPGME library, including headers and
development libraries needed to build applications that use GPGME.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1} .
%{__patch} -p1 < %{SOURCE2}

%build
export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"
sh autogen.sh
languages="cl cpp"
# Ensure that a (re)build uses fixed binaries with minimum version because
# in case configure picks GnuPG-1.x, e.g. from /usr/local, this would cause
# testsuite failures:
%configure \
    --disable-silent-rules \
    --disable-static \
    --disable-fd-passing \
    --enable-languages="${languages}"

%make_build

%install
%make_install

# Remove static libraries
find %{buildroot} -name "*.a" -delete
find %{buildroot} -name "*.la" -delete

# Remove documentation and manual pages (Tizen policy)
%remove_docs

%post -n libgpgme -p /sbin/ldconfig

%postun -n libgpgme -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/gpgme-*
%{_datadir}/common-lisp

%files -n libgpgme
%manifest %{name}.manifest
%license COPYING.LESSER
%{_libdir}/libgpgme.so.*
%{_libdir}/libgpgmepp.so*

%files -n libgpgme-devel
%license COPYING.LESSER
%manifest %{name}.manifest
%{_libdir}/libgpgme.so
%{_libdir}/libgpgmepp.so
%{_datadir}/aclocal/gpgme.m4
%{_includedir}/gpgme.h
%{_includedir}/gpgme++/*
%{_bindir}/gpgme-config
%{_libdir}/pkgconfig/gpgme*.pc
%{_libdir}/cmake/Gpgmepp/*.cmake
