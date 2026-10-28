Name:           libdatrie
Version:        0.2.13
Release:        0
License:        LGPL-2.1-or-later
Summary:        Double-Array Trie Library
Url:            http://linux.thai.net/~thep/datrie/datrie.html
Group:          System/Libraries
Source:         %{name}-%{version}.tar.gz
Source1:        Add-pie-compile-option.patch
Source2:        Fix_AC_MSG_RESULT_undefied.patch
Source99:       baselibs.conf
Source1001: 	libdatrie.manifest

BuildRequires:  pkg-config

%description
This is an implementation of double-array structure for representing
trie, as proposed by Junichi Aoe.

Summary:        Double-Array Trie Library
Group:          Development/Libraries/C and C++

%package devel
Summary:        Double-Array Trie Library (development)
Group:          Development/Libraries/C and C++
Requires:       libdatrie = %{version}

%description devel
This is an implementation of double-array structure for representing
trie, as proposed by Junichi Aoe.

This package contains the development files for libdatrie.

%prep
%setup -q
cp %{SOURCE1001} .
%__patch -p1 < %{SOURCE1}
%__patch -p1 < %{SOURCE2}

%build
autoreconf -fi

chmod +x ./configure
%configure \
        --disable-static --with-pic \
        --disable-doxygen-doc
%__make %{?_smp_mflags}

%check
# %__make check || exit 0

%install
%make_install
%remove_docs

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libdatrie.so.1*

%files devel
%manifest %{name}.manifest
%license COPYING
%{_bindir}/trietool
%{_bindir}/trietool-0.2
%{_includedir}/datrie/
%{_libdir}/libdatrie.so
%{_libdir}/pkgconfig/datrie-0.2.pc
