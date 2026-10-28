Name:           libgcrypt
VCS:            platform/upstream/libgcrypt#3b573f07a66551205be98c50519cef2849c83095
Version:        1.11.0
Release:        1.1
License:        LGPL-2.1+
Summary:        The GNU Crypto Library
%define libsoname %{name}
Url:            http://directory.fsf.org/wiki/Libgcrypt
Group:          Security/Crypto Libraries
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	libgcrypt.manifest
BuildRequires:  libgpg-error-devel >= 1.8
BuildRequires:  libtool

%description
Libgcrypt is a general purpose crypto library based on the code used in
GnuPG (alpha version).

%package devel
License:        GPL-2.0+ and GPL-3.0+ and LGPL-2.1+ and X11 and BSD-2.0 and IETF
Summary:        The GNU Crypto Library
Group:          Development/Libraries
Requires:       %{libsoname} = %{version}
Requires:       glibc-devel
Requires:       libgpg-error-devel >= 1.8

%description devel
Libgcrypt is a general purpose crypto library based on the code used in
GnuPG (alpha version).

This package contains needed files to compile and link against the
library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%ifarch %arm
%{?asan:/usr/bin/gcc-unforce-options}
%endif
# define ciphers to build
ENABLE_CIPHER="arcfour blowfish cast5 des aes twofish serpent rfc2268 seed camellia chacha20"
ENABLE_PUBKEY="dsa elgamal rsa ecc"
ENABLE_DIGEST="crc md4 md5 rmd160 sha1 sha256 sha512 sha3 tiger whirlpool blake2"
#
autoreconf -fi

export CFLAGS="$(echo ${CFLAGS} | sed 's/-mthumb/-marm/g')"
export CFLAGS="$(echo ${CFLAGS} | sed 's/-mimplicit-it=thumb/-mimplicit-it=arm/g')"

# keep using libgcrypt-config instead gpgrt_config
# When gpgrt_config is used & ac_cv_path_GPG_ERROR_CONFIG="no", libgcrypt_config will not be installed
export ac_cv_path_GPG_ERROR_CONFIG="yes"

%configure --with-pic \
		--enable-noexecstack \
		--disable-static \
		--enable-ciphers="$ENABLE_CIPHER" \
		--enable-pubkey-ciphers="$ENABLE_PUBKEY" \
		--enable-digests="$ENABLE_DIGEST" \
		--disable-doc
make %{?_smp_mflags}

%check
# Nice idea. however this uses /dev/random, which hangs
# on hardware without random feeds.
#make check

%install
%make_install

%post  -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING.LIB
%{_libdir}/%{name}.so.20*

%files devel
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_bindir}/mpicalc
%{_bindir}/%{name}-config
%{_libdir}/%{name}.so
%{_includedir}/gcrypt*.h
%{_datadir}/aclocal/%{name}.m4
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Mar 18 2013 Anas Nashif <anas.nashif@intel.com> submit/trunk/20130318.041041@26faab0
- Fixed package groups and move package to security domain
* Sun Mar 17 2013 Anas Nashif <anas.nashif@intel.com> upstream/1.5.0@6c03acd
- Update package groups
