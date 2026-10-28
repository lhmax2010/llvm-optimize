%define udev_dir %{_prefix}/lib/udev
%global _vpath_builddir build

Name:             pulseaudio
Summary:          Improved Linux sound server
Version:          15.0
Release:          50
Group:            Multimedia/Audio
License:          LGPL-2.1
URL:              http://pulseaudio.org
Source0:          http://www.freedesktop.org/software/pulseaudio/releases/%{name}-%{version}.tar.gz
Source1001:       pulseaudio.manifest
BuildRequires:    libtool-ltdl-devel
BuildRequires:    libtool
BuildRequires:    intltool
BuildRequires:    fdupes
BuildRequires:    meson >= 0.50.0
BuildRequires:    pkgconfig(speexdsp)
BuildRequires:    pkgconfig(sndfile)
BuildRequires:    pkgconfig(alsa)
BuildRequires:    pkgconfig(glib-2.0)
%if "%{tizen_profile_name}" != "tv"
BuildRequires:    pkgconfig(sbc)
%endif
BuildRequires:    pkgconfig(dbus-1)
BuildRequires:    pkgconfig(libudev)
BuildRequires:    pkgconfig(openssl3)
BuildRequires:    pkgconfig(json-c)
BuildRequires:    pkgconfig(dlog)
BuildRequires:    pkgconfig(cynara-client)
BuildRequires:    pkgconfig(cynara-creds-socket)
BuildRequires:    pkgconfig(cynara-session)
BuildRequires:    pkgconfig(vconf)
BuildRequires:    systemd-devel
BuildRequires:    libcap-devel
BuildRequires:    doxygen
%if "%{tizen_profile_name}" == "tv"
BuildRequires:    pkgconfig(lwipc)
BuildRequires:    pkgconfig(capi-boost-tv)
BuildRequires:    pkgconfig(capi-system-info)
%endif
Requires:         udev
Requires:         pulseaudio-isu
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
PulseAudio is a sound server for Linux and other Unix like operating
systems. It is intended to be an improved drop-in replacement for the
Enlightened Sound Daemon (ESOUND).

%package -n libpulse
Summary:    PulseAudio client libraries
Group:      Multimedia/Audio

%description -n libpulse
Client libraries used by applications that access a PulseAudio sound server
via PulseAudio's native interface.

%package -n libpulse-mainloop-glib
Summary:        GLIB  2
Group:          Multimedia/Audio

%description -n libpulse-mainloop-glib
pulseaudio is a networked sound server for Linux and other Unix like
operating systems and Microsoft Windows. It is intended to be an
improved drop-in replacement for the Enlightened Sound Daemon (ESOUND).

This package contains the GLIB Main Loop bindings for the PulseAudio
sound server.

%package -n libpulse-devel
Summary:    PulseAudio client development headers and libraries
Group:      Multimedia/Development
Requires:   libpulse = %{version}
Requires:   libpulse-mainloop-glib = %{version}

%description -n libpulse-devel
Headers and libraries for developing applications that access a PulseAudio
sound server via PulseAudio's native interface

%package utils
Summary:    Command line tools for the PulseAudio sound server
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}

%description utils
These tools provide command line access to various features of the
PulseAudio sound server. Included tools are:
pabrowse - Browse available PulseAudio servers on the local network.
paplay - Playback a WAV file via a PulseAudio sink.
pacat - Cat raw audio data to a PulseAudio sink.
parec - Cat raw audio data from a PulseAudio source.
pacmd - Connect to PulseAudio's built-in command line control interface.
pactl - Send a control command to a PulseAudio server.
padsp - /dev/dsp wrapper to transparently support OSS applications.
pax11publish - Store/retrieve PulseAudio default server/sink/source
settings in the X11 root window.

%package module-bluetooth
Summary:    Bluetooth module for PulseAudio sound server
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}

%description module-bluetooth
This module enables PulseAudio to work with bluetooth devices, like headset
or audio gateway

%package config
Summary: PA default configuration
Group: System Environment/Configuration

%description config
Default configuration for PulseAudio.

%package module-raop
Summary: PA module-raop
Group:   Multimedia/Audio

%description module-raop
PulseAudio module-raop.

%package module-augment-properties
Summary: PA module-augment-properties
Group:   Multimedia/Audio

%description module-augment-properties
PulseAudio module-augment-properties.

%package module-dbus-protocol
Summary: PA module-dbus-protocol
Group:   Multimedia/Audio

%description module-dbus-protocol
PulseAudio module-dbus-protocol.

%package module-switch-on-connect
Summary: PA module-swich-on-connect
Group:   Multimedia/Audio

%description module-switch-on-connect
PulseAudio module-swich-on-connect.

%package vala-bindings
Summary:    PA Vala bindings
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}

%description vala-bindings
PulseAudio Vala bindings.

%package realtime-scheduling
Summary:    PA realtime scheduling
Group:      Multimedia/Audio
Requires:   %{name} = %{version}-%{release}
Requires:   libcap-tools

%description realtime-scheduling
PulseAudio realtime-scheduling.

%prep
%setup -q -T -b0
echo "%{version}" > .tarball-version
cp %{SOURCE1001} .
%if "%{tizen_profile_name}" == "tv"
cp src/daemon/systemd/system/pulseaudio-tv.service.in src/daemon/systemd/system/pulseaudio.service.in
%endif

%build
export CFLAGS="%{optflags} -fno-strict-aliasing -D__TIZEN__ -DTIZEN_BT_A2DP_MULTISTREAM -D__TIZEN_BT__ -D__TIZEN_LOG__ %{?asan:-ldl -fPIC }"
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS+=" -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

%if "%{tizen_profile_name}" == "mobile"
echo "tizen profile mobile"
export CFLAGS+=" -DTIZEN_PROFILE_MOBILE "
%endif

%if "%{tizen_profile_name}" == "wearable"
echo "tizen profile wearable"
export CFLAGS+=" -DTIZEN_PROFILE_WEARABLE"
%endif

%if "%{tizen_profile_name}" == "tv"
echo "tizen profile tv"
export CFLAGS+=" -DTIZEN_TV_PROD "
%endif

export LD_AS_NEEDED=0

mkdir -p %{_vpath_builddir}
%meson --auto-features=auto \
    -Dhal-datadir=%{_hal_datadir} \
    -Dhal-sysconfdir=%{_hal_sysconfdir} \
    -Dtests=false \
    -Ddatabase=simple \
    -Dbluez5-native-headset=false \
    -Dgsettings=disabled \
    -Dhal-compat=false \
    -Dipv6=false \
%if "%{tizen_profile_name}" == "tv"
    -Dprelink=true \
    -Dlwipc=true \
    -Dbluez5=false \
    -Dcpu-boosting=true \
%endif
    -Diconv=disabled \
    -Doss-output=disabled \
    -Dudevrulesdir=%{udev_dir}/rules.d \
    -Dpkg_version=%{version}

%meson_build

%install
%meson_install
%find_lang %{name}

rm -rf  %{buildroot}%{_sysconfdir}/xdg/autostart/pulseaudio-kde.desktop
rm -rf  %{buildroot}%{_bindir}/start-pulseaudio-kde
rm -rf  %{buildroot}%{_bindir}/start-pulseaudio-x11
rm -rf  %{buildroot}%{_libdir}/pulse-%{version}/modules/module-device-manager.so
rm -rf  %{buildroot}%{_libdir}/pulse-%{version}/modules/module-systemd-login.so
mkdir -p %{buildroot}%{_includedir}/pulsecore/filter
cp %{buildroot}%{_includedir}/pulsecore/lfe-filter.h %{buildroot}%{_includedir}/pulsecore/filter

%if "%{tizen_profile_name}" == "tv"
mkdir -p %{buildroot}%{_unitdir}/sysinit.target.wants/
ln -s  ../pulseaudio.service  %{buildroot}%{_unitdir}/sysinit.target.wants/pulseaudio.service
%else
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants/
ln -s  ../pulseaudio.service  %{buildroot}%{_unitdir}/multi-user.target.wants/pulseaudio.service
%endif

fdupes  %{buildroot}%{_hal_datadir}
fdupes  %{buildroot}%{_includedir}

# get rid of *.la files
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/pulseaudio/*.la

rm -rf %{buildroot}/%{_hal_sysconfdir}
rm -rf %{buildroot}/%{_hal_datadir}

%package isu
Summary: ISU pacakge for pulseaudio
Group:   Multimedia/Audio

%description isu
Configuration files to generate the ISU (Individual Service Upgrade) pack

%post
/sbin/ldconfig

%preun

%postun -p /sbin/ldconfig

%post   -n libpulse -p /sbin/ldconfig
%postun -n libpulse -p /sbin/ldconfig

%post   -n libpulse-mainloop-glib -p /sbin/ldconfig
%postun -n libpulse-mainloop-glib -p /sbin/ldconfig

%post   realtime-scheduling
#setcap cap_sys_nice+ep /usr/bin/pulseaudio

%postun realtime-scheduling
#setcap -r /usr/bin/pulseaudio

%lang_package

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE LGPL
%{_bindir}/pulseaudio
%{_libdir}/pulseaudio/libpulsecore-%{version}.so
%{udev_dir}/rules.d/90-pulseaudio.rules
%config(noreplace) /etc/dbus-1/system.d/pulseaudio-system.conf
# list all modules
%{_libdir}/pulse-%{version}/modules/libalsa-util.so
%{_libdir}/pulse-%{version}/modules/libcli.so
%{_libdir}/pulse-%{version}/modules/libprotocol-cli.so
%{_libdir}/pulse-%{version}/modules/libprotocol-http.so
%{_libdir}/pulse-%{version}/modules/libprotocol-native.so
%{_libdir}/pulse-%{version}/modules/libprotocol-simple.so
%{_libdir}/pulse-%{version}/modules/librtp.so
%{_libdir}/pulse-%{version}/modules/module-allow-passthrough.so
%{_libdir}/pulse-%{version}/modules/module-alsa-card.so
%{_libdir}/pulse-%{version}/modules/module-alsa-sink.so
%{_libdir}/pulse-%{version}/modules/module-alsa-source.so
%{_libdir}/pulse-%{version}/modules/module-always-sink.so
%{_libdir}/pulse-%{version}/modules/module-always-source.so
%{_libdir}/pulse-%{version}/modules/module-card-restore.so
%{_libdir}/pulse-%{version}/modules/module-cli-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-cli-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-cli.so
%{_libdir}/pulse-%{version}/modules/module-combine.so
%{_libdir}/pulse-%{version}/modules/module-combine-sink.so
%{_libdir}/pulse-%{version}/modules/module-console-kit.so
%{_libdir}/pulse-%{version}/modules/module-default-device-restore.so
%{_libdir}/pulse-%{version}/modules/module-detect.so
%{_libdir}/pulse-%{version}/modules/module-device-restore.so
%{_libdir}/pulse-%{version}/modules/module-echo-cancel.so
%{_libdir}/pulse-%{version}/modules/module-filter-apply.so
%{_libdir}/pulse-%{version}/modules/module-filter-heuristics.so
%{_libdir}/pulse-%{version}/modules/module-http-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-http-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-intended-roles.so
%{_libdir}/pulse-%{version}/modules/module-ladspa-sink.so
%{_libdir}/pulse-%{version}/modules/module-loopback.so
%{_libdir}/pulse-%{version}/modules/module-match.so
%{_libdir}/pulse-%{version}/modules/module-mmkbd-evdev.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-fd.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-native-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-null-sink.so
%{_libdir}/pulse-%{version}/modules/module-null-source.so
%{_libdir}/pulse-%{version}/modules/module-pipe-sink.so
%{_libdir}/pulse-%{version}/modules/module-pipe-source.so
%{_libdir}/pulse-%{version}/modules/module-position-event-sounds.so
%{_libdir}/pulse-%{version}/modules/module-remap-sink.so
%{_libdir}/pulse-%{version}/modules/module-remap-source.so
%{_libdir}/pulse-%{version}/modules/module-rescue-streams.so
%{_libdir}/pulse-%{version}/modules/module-role-ducking.so
%{_libdir}/pulse-%{version}/modules/module-role-cork.so
%{_libdir}/pulse-%{version}/modules/module-rtp-recv.so
%{_libdir}/pulse-%{version}/modules/module-rtp-send.so
%{_libdir}/pulse-%{version}/modules/module-rygel-media-server.so
%{_libdir}/pulse-%{version}/modules/module-simple-protocol-tcp.so
%{_libdir}/pulse-%{version}/modules/module-simple-protocol-unix.so
%{_libdir}/pulse-%{version}/modules/module-sine.so
%{_libdir}/pulse-%{version}/modules/module-sine-source.so
%{_libdir}/pulse-%{version}/modules/module-stream-restore.so
%{_libdir}/pulse-%{version}/modules/module-suspend-on-idle.so
%{_libdir}/pulse-%{version}/modules/module-switch-on-port-available.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-sink.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-sink-new.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-source.so
%{_libdir}/pulse-%{version}/modules/module-tunnel-source-new.so
%{_libdir}/pulse-%{version}/modules/module-udev-detect.so
%{_libdir}/pulse-%{version}/modules/module-virtual-sink.so
%{_libdir}/pulse-%{version}/modules/module-virtual-source.so
%{_libdir}/pulse-%{version}/modules/module-volume-restore.so


%exclude %{_bindir}/pulseaudio
%exclude %{_unitdir_user}/pulseaudio.service
%exclude %{_unitdir_user}/pulseaudio.socket
%exclude %{_unitdir_user}/pulseaudio-x11.service
%exclude %{_unitdir}/pulseaudio.service
%if "%{tizen_profile_name}" == "tv"
%exclude %{_unitdir}/sysinit.target.wants/pulseaudio.service
%else
%exclude %{_unitdir}/multi-user.target.wants/pulseaudio.service
%endif

%files -n libpulse
%manifest %{name}.manifest
%license LICENSE LGPL
%defattr(-,root,root,-)
%{_libdir}/libpulse.so.*
%{_libdir}/libpulse-simple.so.*
%{_libdir}/pulseaudio/libpulsecommon-*.so

%files -n libpulse-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/pulse/*
%{_includedir}/pulsecore/*
%{_includedir}/pulsecore/filter/*
%{_libdir}/libpulse.so
%{_libdir}/libpulse-simple.so
%{_libdir}/libpulse-mainloop-glib.so
%{_libdir}/pkgconfig/libpulse*.pc
%{_libdir}/pkgconfig/pulsecore.pc
# cmake stuff
%{_libdir}/cmake/PulseAudio/PulseAudioConfig.cmake
%{_libdir}/cmake/PulseAudio/PulseAudioConfigVersion.cmake

%files -n libpulse-mainloop-glib
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libpulse-mainloop-glib.so.*

%files utils
%manifest %{name}.manifest
%license LICENSE LGPL
%defattr(-,root,root,-)
%doc %{_mandir}/man1/*
%doc %{_mandir}/man5/*
%{_bindir}/pacat
%{_bindir}/pacmd
%{_bindir}/pactl
%{_bindir}/paplay
%{_bindir}/parec
%{_bindir}/pamon
%{_bindir}/parecord
%{_bindir}/pasuspender
%exclude %{_bindir}/pa-info

%files module-bluetooth
%manifest %{name}.manifest
%license LICENSE LGPL
%if "%{tizen_profile_name}" != "tv"
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-bluetooth-discover.so
%{_libdir}/pulse-%{version}/modules/module-bluetooth-policy.so
%{_libdir}/pulse-%{version}/modules/module-bluez5-discover.so
%{_libdir}/pulse-%{version}/modules/module-bluez5-device.so
%{_libdir}/pulse-%{version}/modules/libbluez5-util.so
%endif

%files module-raop
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/libraop.so
%{_libdir}/pulse-%{version}/modules/module-raop*.so

%files module-augment-properties
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-augment-properties.so

%files module-dbus-protocol
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-dbus-protocol.so

%files module-switch-on-connect
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/pulse-%{version}/modules/module-switch-on-connect.so

%files config
%manifest %{name}.manifest
%defattr(-,root,root,-)

%files vala-bindings
%manifest %{name}.manifest
%defattr(-,root,root,-)

%files realtime-scheduling
%defattr(-,root,root,-)

%docs_package

%files isu
/etc/isu/pulseaudio/isu.cfg
/etc/isu/pulseaudio/system-services/pulseaudio.service
