Name:           speex
Version:        1.2.1
Release:        10
License:        BSD-3-Clause
Summary:        An Open Source, Patent Free Speech Codec
Url:            http://www.speex.org/
Group:          Multimedia/Audio
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Source1001: 	speex.manifest
BuildRequires:  libogg-devel
BuildRequires:  libtool
BuildRequires:  pkgconfig

%description
Speex is a patent free audio codec designed especially for voice
(unlike Vorbis which targets general audio) signals and providing good
narrowband and wideband quality. This project aims to be complementary
to the Vorbis codec.

%package -n libspeex
License:        BSD-3-Clause
Summary:        An Open Source, Patent Free Speech Codec Library
Group:          Multimedia/Audio

%description -n libspeex
Speex is a patent free audio codec designed especially for voice
(unlike Vorbis which targets general audio) signals and providing good
narrowband and wideband quality. This project aims to be complementary
to the Vorbis codec.

%package -n libspeex-devel
License:        BSD-3-Clause
Summary:        Development package for SpeeX
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       libogg-devel
Requires:       libspeex = %{version}

%description -n libspeex-devel
This package contains the files needed to compile programs that use the
Speex library.

%package -n libspeexdsp
License:        BSD-3-Clause
Summary:        An Open Source, Patent Free Speech Codec Library
Group:          Multimedia/Audio

%description -n libspeexdsp
Speex is a patent free audio codec designed especially for voice
(unlike Vorbis which targets general audio) signals and providing good
narrowband and wideband quality. This project aims to be complementary
to the Vorbis codec.

%package -n libspeexdsp-devel
License:        BSD-3-Clause
Summary:        Development package for SpeexDSP
Group:          Development/Libraries
Requires:       glibc-devel
Requires:       libspeexdsp = %{version}

%description -n libspeexdsp-devel
This package contains the files needed to compile programs that use the
SpeexDSP library.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
autoreconf -fi
%configure \
    --disable-static \
	--disable-binaries
make %{?_smp_mflags}

cd libspeexdsp
autoreconf -fi
%configure \
    --disable-static \
	--disable-examples
make %{?_smp_mflags}
cd -

%install
%make_install

cd libspeexdsp
%make_install
cd -

# remove duped documents
rm -rf %{buildroot}%{_datadir}/doc/speex*

%post -n libspeex -p /sbin/ldconfig
%postun -n libspeex -p /sbin/ldconfig

%post -n libspeexdsp -p /sbin/ldconfig
%postun -n libspeexdsp -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING

%files -n libspeex
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%{_libdir}/libspeex.so.*

%files -n libspeex-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/speex/speex.h
%{_includedir}/speex/speex_bits.h
%{_includedir}/speex/speex_callbacks.h
%{_includedir}/speex/speex_config_types.h
%{_includedir}/speex/speex_header.h
%{_includedir}/speex/speex_stereo.h
%{_includedir}/speex/speex_types.h
%{_datadir}/aclocal/speex.m4
%{_libdir}/pkgconfig/speex.pc
%{_libdir}/libspeex.so

%files -n libspeexdsp
%manifest %{name}.manifest
%license COPYING
%defattr(-,root,root)
%{_libdir}/libspeexdsp.so.*

%files -n libspeexdsp-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/speex/speexdsp_config_types.h
%{_includedir}/speex/speexdsp_types.h
%{_includedir}/speex/speex_echo.h
%{_includedir}/speex/speex_jitter.h
%{_includedir}/speex/speex_preprocess.h
%{_includedir}/speex/speex_resampler.h
%{_libdir}/pkgconfig/speexdsp.pc
%{_libdir}/libspeexdsp.so

%changelog
