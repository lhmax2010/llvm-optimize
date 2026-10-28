Name:           libarchive
VCS:            platform/upstream/libarchive#04aeba83d3da60ffb632a552742bebf1e7d919ff
Version:        3.8.1
Release:        2.4
License:        BSD-2-Clause
Summary:        A library for handling streaming archive formats
Url:            https://github.com/libarchive/libarchive
Group:          System/Libraries
Source0:        https://github.com/libarchive/libarchive/archive/refs/tags/v%{version}.tar.gz
Source1001:     libarchive.manifest
Source1002:     disable_man_info.patch
Source1003:     Fix_libcrypto3_confiugre.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  libtool
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(ext2fs)
BuildRequires:  pkgconfig(liblzma)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  gnutar

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.

%package tools
Summary:        Tools based on %{name}
Requires:       %{name} = %{version}
Provides:       /bin/tar
Provides:       /usr/bin/tar

%description tools
Tools based on %{name}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}
Requires:       pkgconfig(openssl3)

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

# bsdtar (the new /usr/bin/tar) links against libarchive.so, which is absent
# from the buildroot while libarchive itself is being built. Use gnutar for
# %setup source extraction to avoid the self-dependency.
%define __tar /usr/bin/gnutar

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}
%{__patch} -p1 < %{SOURCE1003}

%build
%global optflags    %{optflags} -D_REENTRANT -pipe
export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"
autoreconf -fi
%configure --disable-static --enable-bsdcpio
%__make %{?_smp_mflags}

%install
%make_install

find %{buildroot} -name cpio.5 -exec rm -f {} ';'
find %{buildroot} -name mtree.5 -exec rm -f {} ';'
find %{buildroot} -name tar.5 -exec rm -f {} ';'

ln -sf bsdtar %{buildroot}%{_bindir}/tar

%check
# %__make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root,-)
%{_libdir}/*.so.*


%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libarchive.pc

%files tools
%manifest %{name}.manifest
%license COPYING
%{_bindir}/bsdcpio
%{_bindir}/bsdtar
%{_bindir}/tar
%{_bindir}/bsdcat
%{_bindir}/bsdunzip

