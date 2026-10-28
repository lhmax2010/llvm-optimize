Name:           libtheora
Version:        1.1.1
Release:        14
License:        BSD-2.0
Summary:        Free Video Codec
Url:            http://www.theora.org/
Group:          Multimedia/Video
%define pkg_version %{version}
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	libtheora.manifest
BuildRequires:  gcc-c++
BuildRequires:  libogg-devel
BuildRequires:  libtool
BuildRequires:  libvorbis-devel
BuildRequires:  pkg-config
BuildRequires:  python

%description
Theora is a free video codec based on VP3. The package contains the
library that can decode and encode Theora streams. Theora is also able
to playback VP3 streams.

%package devel
License:        BSD-3-Clause
Summary:        Free Video Codec
Group:          Development/Libraries
Requires:       libogg-devel
Requires:       libtheora = %{version}

%description devel
Theora is a free video codec based on VP3. The package contains the
library that can decode and encode Theora streams. Theora is also able
to playback VP3 streams.

%prep
%setup -q -n %{name}-%{pkg_version}
cp %{SOURCE1001} .

%build
ACLOCAL="aclocal -I m4" autoreconf -f -i
%configure --disable-examples \
    --disable-static \
    --with-pic
make %{?_smp_mflags} docdir=%{_docdir}/%{name}

%check
make check

%install
%make_install
install -d %{buildroot}%{_bindir}

rm -rf %{buildroot}/%{_datadir}/doc/%{name}-%{version}/*

%post  -p /sbin/ldconfig

%postun  -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING LICENSE
%{_libdir}/libtheora.so.0*
%{_libdir}/libtheoradec.so.1*
%{_libdir}/libtheoraenc.so.1*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/theora
%{_libdir}/*.so
%{_libdir}/pkgconfig/theoradec.pc
%{_libdir}/pkgconfig/theoraenc.pc
%{_libdir}/pkgconfig/theora.pc
