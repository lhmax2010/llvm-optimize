Name:           webrtc-audio-processing
Version:        0.3.1
Release:        2
Summary:        Library for echo cancellation
License:        BSD-3-Clause
URL:            http://www.freedesktop.org/software/pulseaudio/webrtc-audio-processing/
Source0:        http://freedesktop.org/software/pulseaudio/webrtc-audio-processing/%{name}-%{version}.tar.xz
Source1:        %{name}.manifest

%description
%{name} is a library derived from Google WebRTC project that
provides echo cancellation functionality. This library is used by for example
PulseAudio to provide echo cancellation.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header
files for developing applications that use %{name}.

%prep
%setup -q
cp %{SOURCE1} .

%build
%if "%{tizen_profile_name}" == "tv"
export CFLAGS="$CFLAGS -Wno-error=shadow -Wno-error=missing-field-initializers -Wno-error=class-memaccess"
export CXXFLAGS="$CXXFLAGS -Wno-error=shadow -Wno-error=missing-field-initializers -Wno-error=class-memaccess"
%endif

./autogen.sh

%ifarch %{arm}
%global neon --enable-neon=no
%endif

%configure \
  %{?neon} \
  --disable-silent-rules \
  --disable-static

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

rm -fv %{buildroot}%{_libdir}/lib*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libwebrtc_audio_processing.so.1*
%license COPYING

%files devel
%{_libdir}/libwebrtc_audio_processing.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/webrtc_audio_processing/

