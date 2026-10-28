Name:           flac
BuildRequires:  gcc-c++
BuildRequires:  gettext-tools
BuildRequires:  libogg-devel
BuildRequires:  libtool
BuildRequires:  pkg-config
%ifarch %{ix86}
BuildRequires:  nasm
%endif
Version:        1.3.0
Release:        0
License:        BSD-3-Clause
Summary:        Free Lossless Audio Codec
Url:            http://flac.sourceforge.net/
#X-Vcs-Url:     https://git.xiph.org/flac.git
Group:          Multimedia / Audio FW
Source:         %{name}-%{version}.tar.bz2
Source1001:     flac.manifest

%description
FLAC is an open source lossless audio codec developed by Josh Coalson.

%package -n libflac
Summary:        Free Lossless Audio Codec Library

%description -n libflac
This package contains the library for FLAC (Free Lossless Audio Codec)
developed by Josh Coalson.

%package -n libflac++
Summary:        Free Lossless Audio Codec Library

%description -n libflac++
This package contains the C++ library for FLAC (Free Lossless Audio
Codec) developed by Josh Coalson.

%package devel
Summary:        FLAC Library Development Package
Requires:       glibc-devel
Requires:       libflac = %{version}-%{release}
Requires:       libflac = %{version}-%{release}
Requires:       libstdc++-devel

%description devel
This package contains the files needed to compile programs that use the
FLAC library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%autogen
%define warn_flags -O3 -W -Wall -Wstrict-prototypes -Wformat-security
export CFLAGS="%{optflags} %{warn_flags}"
export CXXFLAGS="$CFLAGS"
%configure  --disable-thorough-tests --disable-exhaustive-tests\
            --disable-xmms-plugin \
            --disable-static \
            --disable-rpath \
            --with-pic \
            --enable-sse

%__make %{?_smp_mflags}

%install
%make_install
rm -rf %{buildroot}%{_datadir}/doc/%{name}-%{version}

%post -n libflac -p /sbin/ldconfig

%postun -n libflac -p /sbin/ldconfig

%post -n libflac++ -p /sbin/ldconfig

%postun -n libflac++ -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%license  COPYING.*
%{_bindir}/*
%{_mandir}/man*/*

%files -n libflac
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libFLAC.so.8*

%files -n libflac++
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/libFLAC++.so.6*

%files devel
%manifest %{name}.manifest
%defattr(-, root, root)
%{_libdir}/lib*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
