%global majorversion 1
%global minorversion 6
%global microversion 0
%global apiversion   0.3
%global spaversion   0.2
%global soversion    0

# Build conditions for various features
%define support_alsa 1
%define support_vulkan 0
%define support_v4l2 0
%define support_x11 0
%define support_ffado 0
%define installed_tests 1

Name:           pipewire
Summary:        Media Sharing Server
Version:        %{majorversion}.%{minorversion}.%{microversion}
Release:        15
License:        MIT
URL:            https://pipewire.org/
Source0:        https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/%{version}/pipewire-%{version}.tar.gz
Source1:	tizen-audio-service.conf
Source2:        pipewire_keytone.conf
Source3:        %{name}.manifest
BuildRequires:  gettext
BuildRequires:  meson >= 0.59.0
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-allocators-1.0) >= 1.10.0
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(security-manager)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(hal-api-common)
BuildRequires:  pkgconfig(hal-api-audio)
BuildRequires:  pkgconfig(hal-api-camera)
BuildRequires:  libusb-devel
BuildRequires:  readline-devel
Requires:       %{name}-utils%{?_isa} = %{version}-%{release}

Requires(pre):  shadow-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       systemd

%description
PipeWire is a multimedia server for Linux and other Unix like operating
systems.

%package libs
Summary:        Libraries for PipeWire clients
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PipeWire media server.

%package devel
Summary:        Headers and libraries for PipeWire client development
License:        MIT
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Headers and libraries for developing applications that can communicate with
a PipeWire media server.

%package utils
Summary:        PipeWire media server utilities
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description utils
This package contains command line utilities for the PipeWire media server.

%if %{support_vulkan}
%package plugin-vulkan
Summary:        PipeWire media server vulkan support
License:        MIT
BuildRequires:  pkgconfig(vulkan)
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description plugin-vulkan
This package contains the PipeWire spa plugin for vulkan.
%endif

%if %{support_v4l2}
%package v4l2
Summary:        PipeWire media server v4l2 LD_PRELOAD support
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description v4l2
This package contains an LD_PRELOAD library that redirects v4l2 applications to
PipeWire.
%endif

%package module-x11
Summary:        PipeWire media server x11 support
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description module-x11
This package contains X11 bell support for PipeWire.

%if %{support_ffado}
%package module-ffado
Summary:        PipeWire media server ffado support
License:        MIT
BuildRequires:  libffado-devel
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description module-ffado
This package contains the FFADO support for PipeWire.
%endif

%prep
%autosetup -p1 %{?snapdate:-n %{name}-%{gitcommit}}

%build

%if "%{tizen_profile_name}" == "tv"
export CFLAGS+=" -w -Os -ffunction-sections -fdata-sections"
export CXXFLAGS+=" -w -Os -ffunction-sections -fdata-sections"
export LDFLAGS+=" -Wl,--gc-sections -Wl,--as-needed"
%endif

%{meson}									\
    --buildtype=minsize								\
    --wrap-mode=forcefallback							\
    -D sdl2=disabled								\
    -D videotestsrc=disabled -D videoconvert=enabled				\
    -D volume=disabled -D bluez5-codec-aptx=disabled 		  		\
    -D bluez5=disabled								\
    -D bluez5-codec-lc3plus=disabled -D bluez5-codec-lc3=disabled		\
    -D bluez5-codec-ldac=disabled						\
    -D rtprio-server=60 -D rtprio-client=55 -D rlimits-rtprio=70		\
    -D raop=disabled								\
    -D snap=disabled								\
    -D pipewire-jack=disabled -D jack=disabled -D jack-devel=false		\
    -D libcamera=disabled			 				\
    -D vulkan=disabled								\
    -D libmysofa=disabled							\
    -D lv2=disabled								\
    -D roc=disabled								\
    -D libffado=disabled							\
    -D selinux=disabled								\
    -D avahi=disabled								\
    -D x11=disabled -D x11-xfixes=disabled					\
    -D libcanberra=disabled							\
    -D echo-cancel-webrtc=disabled						\
    -D v4l2=disabled								\
    -D avb=disabled								\
    -D gsettings-pulse-schema=disabled						\
    -D gsettings=disabled							\
    -D pipewire-v4l2=disabled							\
    -D gstreamer=enabled							\
    -D udev=enabled -D libusb=enabled						\
    -D libsystemd=disabled							\
    -D systemd-system-service=disabled -D systemd-user-service=disabled		\
    -D pw-cat-ffmpeg=disabled							\
    -D audiotestsrc=enabled							\
    -D logind=disabled -D compress-offload=disabled -D flatpak=disabled		\
    -D dbus=enabled								\
    -D ebur128=disabled								\
    -D fftw=disabled								\
    -D onnxruntime=disabled							\
    -D libpulse=disabled							\
%if 0%{?support_alsa}
    -D pipewire-alsa=enabled							\
    -D alsa=enabled								\
%else
    -D pipewire-alsa=disabled							\
    -D alsa=disabled								\
%endif
    -D tizen=enabled                                                          \
    -D tizen-privilege=true                                                   \
    -D tizen-hal-utils=true                                                   \
    -D tizen-audio-hal=enabled                                                        \
    -D tizen-camera-hal=enabled                                                       \
    -D optimize-size=true							\
    -D dlog=enabled								\
%if 0%{?installed_tests}
    -D installed_tests=enabled							\
%endif
    -D tizen-spa-audio-max-channels=16						\
    %{nil}

%{meson_build}

%install
%{meson_install}

# Copy manifest file to build directory
install -m 0644 %SOURCE3 .

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE2 %{buildroot}%{_tmpfilesdir}/pipewire_keytone.conf

#mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
#ln -s  ../pipewire.socket %{buildroot}%{_unitdir}/sockets.target.wants/pipewire.socket

# TODO: /sysinit.target.wants/ for TV
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants/
ln -s  ../pipewire.service %{buildroot}%{_unitdir}/multi-user.target.wants/pipewire.service

install -d -m 0755 %{buildroot}%{_datadir}/pipewire/pipewire.conf.d/
install -d -m 0755 %{buildroot}%{_datadir}/pipewire/client.conf.d/

%if %{support_alsa}
mkdir -p %{buildroot}%{_sysconfdir}/alsa/conf.d/
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/50-pipewire.conf
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf

%endif

# rates config
ln -s ../pipewire.conf.avail/10-rates.conf \
		%{buildroot}%{_datadir}/pipewire/pipewire.conf.d/10-rates.conf

# Tizen Camera HAL SPA factory mapping
ln -s ../pipewire.conf.avail/10-tizen-camera-hal.conf \
		%{buildroot}%{_datadir}/pipewire/pipewire.conf.d/10-tizen-camera-hal.conf

# Tizen Audio HAL SPA factory mapping
ln -s ../pipewire.conf.avail/10-tizen-audio-hal.conf \
		%{buildroot}%{_datadir}/pipewire/pipewire.conf.d/10-tizen-audio-hal.conf

# upmix config
ln -s ../pipewire.conf.avail/20-upmix.conf \
		%{buildroot}%{_datadir}/pipewire/pipewire.conf.d/20-upmix.conf
ln -s ../client.conf.avail/20-upmix.conf \
		%{buildroot}%{_datadir}/pipewire/client.conf.d/20-upmix.conf

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE1 %{buildroot}%{_tmpfilesdir}/tizen-audio-service.conf

%find_lang %{name}

%post
/sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE COPYING
%dir %{_datadir}/pipewire/
%dir %{_datadir}/pipewire/pipewire.conf.d/
%{_bindir}/pipewire*
%{_datadir}/pipewire/*.conf
%{_datadir}/pipewire/pipewire.conf.avail/10-rates.conf
%{_datadir}/pipewire/pipewire.conf.avail/10-tizen-camera-hal.conf
%{_datadir}/pipewire/pipewire.conf.avail/10-tizen-audio-hal.conf
%{_datadir}/pipewire/pipewire.conf.avail/20-upmix.conf
%{_datadir}/pipewire/client.conf.avail/20-upmix.conf
%{_datadir}/pipewire/pipewire.conf.d/10-rates.conf
%{_datadir}/pipewire/pipewire.conf.d/10-tizen-camera-hal.conf
%{_datadir}/pipewire/pipewire.conf.d/10-tizen-audio-hal.conf
%{_datadir}/pipewire/pipewire.conf.d/20-upmix.conf
%{_datadir}/pipewire/client.conf.d/20-upmix.conf
%{_datadir}/pipewire/filter-chain/*.conf
%{_unitdir}/pipewire.service
%{_unitdir}/multi-user.target.wants/pipewire.service
%{_tmpfilesdir}/pipewire_keytone.conf
%{_datadir}/pipewire/pipewire.conf.avail/50-raop.conf
%config(noreplace) %{_sysconfdir}/security/limits.d/*.conf
%exclude %{_datadir}/pipewire/pipewire-pulse.conf.avail/20-upmix.conf
%exclude %{_datadir}/locale/*

%files libs -f %{name}.lang
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE COPYING
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/libpipewire-tizen-privilege.so.*
%{_libdir}/libpipewire-tizen-hal-utils.so.*
%{_libdir}/pipewire-%{apiversion}/libpipewire-*.so
%dir %{_datadir}/alsa-card-profile/
%dir %{_datadir}/alsa-card-profile/mixer/
%dir %{_datadir}/pipewire/client.conf.d/
%dir %{_libdir}/spa-%{spaversion}
%{_prefix}/lib/udev/rules.d/90-pipewire-alsa.rules
%{_libdir}/gstreamer-1.0/libgstpipewire.*
%{_libdir}/spa-%{spaversion}/*
%{_datadir}/pipewire/client.conf
%{_datadir}/alsa-card-profile/mixer/paths/
%{_datadir}/alsa-card-profile/mixer/profile-sets/
%{_tmpfilesdir}/*

%if %{support_alsa}
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pipewire.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%endif

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/pipewire-%{apiversion}/
%{_includedir}/spa-%{spaversion}/
%{_libdir}/libpipewire-%{apiversion}.so
%{_libdir}/libpipewire-tizen-privilege.so
%{_libdir}/libpipewire-tizen-hal-utils.so
%{_libdir}/pkgconfig/libpipewire-%{apiversion}.pc
%{_libdir}/pkgconfig/libpipewire-tizen-privilege.pc
%{_libdir}/pkgconfig/libpipewire-tizen-hal-utils.pc
%{_libdir}/pkgconfig/libspa-%{spaversion}.pc

%files utils
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/pw-*
%{_bindir}/spa-*
%if %{installed_tests}
%{_libexecdir}/installed-tests/*
%{_datadir}/installed-tests/*
%endif

%if %{support_vulkan}
%files plugin-vulkan
%{_bindir}/pipewire-vulkan
%{_libdir}/spa-%{spaversion}/vulkan/
%{_datadir}/pipewire/pipewire-vulkan.conf
%endif

%if %{support_v4l2}
%files v4l2
%{_bindir}/pw-v4l2
%{_libdir}/pipewire-%{apiversion}/v4l2/libpw-v4l2.so
%endif

%if %{support_x11}
%files module-x11
%{_libdir}/pipewire-%{apiversion}/libpipewire-module-x11-bell.so
%endif

%if %{support_ffado}
%files module-ffado
%{_libdir}/pipewire-%{apiversion}/libpipewire-module-ffado-driver.so
%endif
