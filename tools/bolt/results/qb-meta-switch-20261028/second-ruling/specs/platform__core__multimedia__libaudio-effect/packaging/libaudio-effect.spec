Name:       libaudio-effect
Summary:    audio effect library
Version:    0.0.27
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(speexdsp)
BuildRequires:  pkgconfig(webrtc-audio-processing)
%if "%{tizen_profile_name}" != "tv"
BuildRequires:  pkgconfig(rnnoise)
%endif
BuildRequires:  meson >= 0.53.0

%description
audio effect library

%package devel
Summary:    Audio effect library
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description devel
MMSound development package for audio effect

%prep
%setup -q

%build
%{meson} -Dtizen=enabled \
%if "%{tizen_profile_name}" != "tv"
	-Dns-rnnoise=enabled \
	-Dns-srid=enabled \
%endif
	-Daec-webrtc=enabled \
	-Dagc-speex=enabled \
	-Drefcopy=enabled \
	-Daec-speex=enabled

%{meson_build}

%install
%{meson_install}

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n %{name}
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/*.so.*
%{_libdir}/audio-effect-plugins/*

%files devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_libdir}/*.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
