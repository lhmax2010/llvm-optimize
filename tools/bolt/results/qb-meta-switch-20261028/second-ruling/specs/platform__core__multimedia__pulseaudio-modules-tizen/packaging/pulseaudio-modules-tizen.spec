%define module_ver 15.0

Name:             pulseaudio-modules-tizen
Summary:          Pulseaudio modules for Tizen
Version:          15.0.96
Release:          0
Group:            Multimedia/Audio
License:          LGPL-2.1+
Source0:          %{name}-%{version}.tar.gz
Source1:          pulseaudio.conf
Source2:          pulseaudio-modules.cfg
Source3:          pulseaudio-module-acm.cfg
BuildRequires:    libtool-ltdl-devel
BuildRequires:    libtool
BuildRequires:    intltool
BuildRequires:    pkgconfig(dbus-1)
BuildRequires:    pkgconfig(iniparser)
BuildRequires:    pkgconfig(json-c)
BuildRequires:    pkgconfig(vconf)
%if "%{tizen_profile_name}" == "tv"
BuildRequires:    pkgconfig(glib-2.0)
%endif
BuildRequires:    pkgconfig(libpulse)
BuildRequires:    pkgconfig(pulsecore)
BuildRequires:    pkgconfig(libsystemd)
BuildRequires:    pkgconfig(dns_sd)
BuildRequires:    pkgconfig(hal-api-audio)
BuildRequires:    pkgconfig(speexdsp)
BuildRequires:    pkgconfig(libaudio-effect)
BuildRequires:    pulseaudio
BuildRequires:    m4
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
This package contains pulseaudio modules for tizen audio system.

%package -n pulseaudio-module-acm
Summary: PA module-acm-sink
Group:   Multimedia/Audio

%description -n pulseaudio-module-acm
PulseAudio module-acm-sink for sending PCM data to ACM core.

%prep
%setup -q

%build
export CFLAGS="%{optflags} -fno-strict-aliasing -D__TIZEN__ -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\" -fPIC -Wno-unused-function"
%if "%{tizen_profile_name}" == "tv"
export CFLAGS+=" -DTIZEN_TV -D__TIZEN_TV_EXTERNAL_BT_SCO__ -D__TIZEN_TV_BUILTIN_MIC__ -D__TIZEN_TV_EXTERNAL_TV_SOURCE__ -D__TIZEN_TV_DISABLE_AUTO_ALL__";
%endif

export LD_AS_NEEDED=0
%reconfigure --prefix=%{_prefix} \
        --disable-static \
        --enable-acm \
        --enable-preprocessor \
%if "%{tizen_profile_name}" == "tv"
        --enable-vconf-helper
%endif
#        --enable-haltc

%__make %{?_smp_mflags} V=1

LIB_DIR=%{_libdir}
MODULE_VER=%{module_ver}

%install
%make_install

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE1 %{buildroot}%{_tmpfilesdir}/pulseaudio.conf

mkdir -p %{buildroot}/etc/isu/pulseaudio/isu.cfg.d
cp %SOURCE2 %{buildroot}/etc/isu/pulseaudio/isu.cfg.d/pulseaudio-modules.cfg
cp %SOURCE3 %{buildroot}/etc/isu/pulseaudio/isu.cfg.d/pulseaudio-module-acm.cfg
sed -i -e "s,##LIBDIR##,%{_libdir},g" \
       -e "s,##MODULE_VER##,%{module_ver},g" \
       %{buildroot}/etc/isu/pulseaudio/isu.cfg.d/pulseaudio-modules.cfg \
       %{buildroot}/etc/isu/pulseaudio/isu.cfg.d/pulseaudio-module-acm.cfg

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.LGPL-2.1+
%{_libdir}/pulse-%{module_ver}/modules/module-poweroff.so
%{_libdir}/pulse-%{module_ver}/modules/module-sound-player.so
%{_libdir}/pulse-%{module_ver}/modules/module-tone-player.so
%{_libdir}/pulse-%{module_ver}/modules/module-tizenaudio-policy.so
%{_libdir}/pulse-%{module_ver}/modules/module-tizenaudio-sink.so
%{_libdir}/pulse-%{module_ver}/modules/module-tizenaudio-source.so
%{_libdir}/pulse-%{module_ver}/modules/module-tizenaudio-sink2.so
%{_libdir}/pulse-%{module_ver}/modules/module-tizenaudio-source2.so
%{_libdir}/pulse-%{module_ver}/modules/module-tizenaudio-discover.so
%{_libdir}/pulse-%{module_ver}/modules/module-tizenaudio-publish.so
%{_libdir}/pulse-%{module_ver}/modules/module-tizenaudio-preprocessor.so
%{_libdir}/pulse-%{module_ver}/modules/libprocessor.so
%{_libdir}/pulse-%{module_ver}/modules/libtizenaudio-util.so
%{_libdir}/pulse-%{module_ver}/modules/libhal-interface.so
%{_libdir}/pulse-%{module_ver}/modules/libcommunicator.so
%{_tmpfilesdir}/pulseaudio.conf
%if "%{tizen_profile_name}" == "tv"
%{_libdir}/pulse-%{module_ver}/modules/module-vconf.so
%{_libexecdir}/pulse/vconf-helper
%endif
%{_libdir}/ladspa/*.so
%{_datadir}/sounds/mm-sound/*
/etc/isu/pulseaudio/isu.cfg.d/pulseaudio-modules.cfg

%files -n pulseaudio-module-acm
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE.LGPL-2.1+
%{_libdir}/pulse-%{module_ver}/modules/module-acm-sink.so
/etc/isu/pulseaudio/isu.cfg.d/pulseaudio-module-acm.cfg

