%define keepstatic 1
Name:           pcre
VCS:            platform/upstream/pcre#feba6a19627f5d6e74d551ef2fc8b33af0547780
Version:        8.45
Release:        1.14
License:        BSD-3-Clause
Summary:        A library for Perl-compatible regular expressions
Url:            ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
Group:          System/Libraries
Source:         ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source10:       add_pie_compile_option.patch
Source1001: 	pcre.manifest
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pkg-config

%description
The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

%package        devel
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries
Requires:       libpcre = %{version}
Requires:       libpcrecpp = %{version}
Requires:       libpcreposix = %{version}
Requires:       libstdc++-devel

%description devel
The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

%package        devel-static
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries
Requires:       pcre-devel = %{version}

%description devel-static
The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.
This package contains static versions of the PCRE libraries.

%package -n libpcre
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries
Provides:       %{name} = %{version}
Obsoletes:      %{name} < %{version}

%description -n libpcre
The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

%package -n libpcreposix
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries

%description -n libpcreposix
The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

%package -n libpcrecpp
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries

%description -n libpcrecpp
The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

%package doc
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries
BuildArch:      noarch

%description doc
The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

%package tools
Summary:        A library for Perl-compatible regular expressions
Group:          System/Libraries

%description tools
The PCRE library is a set of functions that implement regular
expression pattern matching using the same syntax and semantics
as Perl 5.

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE10}

%build
export CFLAGS="${CFLAGS} -fPIC"

# Available JIT archs see sljit/sljitConfig.h
autoreconf -fiv
%configure \
%ifarch %ix86 x86_64 %arm ppc ppc64 mips
	    --enable-jit \
%endif
	    --enable-static \
	    --with-link-size=2 \
	    --with-match-limit=10000000 \
	    --enable-newline-is-lf \
	    --enable-utf8 \
        --enable-unicode-properties
make %{?_smp_mflags}


# %check
# export LANG=POSIX
# make check || exit 0

%install
%make_install
mkdir -p %{buildroot}/%{_defaultdocdir}
mv %{buildroot}/usr/share/doc/pcre %{buildroot}/%{_defaultdocdir}/pcre-doc
rm -f %{buildroot}%{_libdir}/*.la
%{remove_docs}

%post -n libpcre -p /sbin/ldconfig

%postun -n libpcre -p /sbin/ldconfig

%post -n libpcrecpp -p /sbin/ldconfig

%postun -n libpcrecpp -p /sbin/ldconfig

%post -n libpcreposix -p /sbin/ldconfig

%postun -n libpcreposix -p /sbin/ldconfig

%files -n libpcre
%manifest %{name}.manifest
%license LICENCE
%{_libdir}/libpcre.so.*

%files -n libpcrecpp
%manifest %{name}.manifest
%license LICENCE
%{_libdir}/libpcrecpp.so.*

%files -n libpcreposix
%manifest %{name}.manifest
%license LICENCE
%{_libdir}/libpcreposix.so.*

%files tools
%manifest %{name}.manifest
%license LICENCE
%{_bindir}/pcregrep
%{_bindir}/pcretest

%files devel
%license LICENCE
%manifest %{name}.manifest
%{_bindir}/pcre-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libpcre.pc
%{_libdir}/pkgconfig/libpcrecpp.pc
%{_libdir}/pkgconfig/libpcreposix.pc

%files devel-static
%license LICENCE
%manifest %{name}.manifest
%{_libdir}/*.a

