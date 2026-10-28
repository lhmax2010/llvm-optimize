Name:       libmm-sound
Summary:    MMSound Package contains client lib and focus server binary
Version:    0.21.3
Release:    0
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source4:    focus-server.service
Source5:    focus-server.path
Source6:    focus-server.conf
Requires: security-config
%if "%{tizen_profile_name}" == "tv"
Source7:    focus-server-tv.service
Source9:    focus-server-tv.path
%endif
Source8:    focus.conf
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(mm-common)
%if "%{tizen_profile_name}" == "tv"
BuildRequires: pkgconfig(lwipc)
%endif
BuildRequires: meson

# tests build option
%define tests_enabled 1


%description
MMSound package contains focus-server and client interfaces connected to audio system

%package devel
Summary: MMSound development package
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:  pkgconfig(mm-sound)
Provides:  pkgconfig(mm-keysound)
Provides:  pkgconfig(mm-bootsound)
Provides:  pkgconfig(mm-msgbox)
Provides:  pkgconfig(mm-pairbox)
Provides:  pkgconfig(mm-workloop)
Provides:  pkgconfig(mm-audio-conf)
Provides:  pkgconfig(mm-list)

%description devel
MMSound development package for sound system

%package sdk-devel
Summary: MMSound development package
Group:      Development/Libraries
Requires:   %{name}-devel = %{version}-%{release}

%description sdk-devel
MMSound development package for sound system

%package tool
Summary: MMSound utility package - contains test tools
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description tool
MMSound utility package - contains test tools for sound system

%prep
%setup -q


%build

CFLAGS="%{optflags} -D_TIZEN_PUBLIC_" ;export CFLAGS
CXXFLAGS="%{optflags}" ;export CXXFLAGS

export CFLAGS="${CFLAGS} -DUSE_DLOG"
export CXXFLAGS="${CXXFLAGS} -DUSE_DLOG"

%if "%{tizen_profile_name}" == "tv"
        CFLAGS="${CFLAGS} -DTIZEN_TV";export CFLAGS
%endif

# Size/dead-code trim: minsize gives -Os; add per-function/data sections so the
# linker can gc unreferenced code, and drop unused DT_NEEDED with --as-needed.
export CFLAGS="${CFLAGS} -ffunction-sections -fdata-sections"
export CXXFLAGS="${CXXFLAGS} -ffunction-sections -fdata-sections"
export LDFLAGS="${LDFLAGS} -Wl,--gc-sections -Wl,--as-needed"

%if 0%{?gcov:1}
export CFLAGS="${CFLAGS} -fprofile-arcs -ftest-coverage -DUSE_GCOV"
export CXXFLAGS="${CXXFLAGS} -fprofile-arcs -ftest-coverage "
export LDFLAGS="${LDFLAGS} -lgcov "
%endif

%{meson} \
    --buildtype=minsize \
    -Dversion=%{version} \
    -Dpc_requires_mm_common=true \
%if %{tests_enabled}
        -Dtests=true \
%else
        -Dtests=false \
%endif
%if "%{tizen_profile_name}" == "tv"
        -Dlwipc=true \
%endif
        %{nil}

%{meson_build}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/dbus-1/system.d/
cp %{SOURCE6} %{buildroot}/etc/dbus-1/system.d/focus-server.conf
%if "%{tizen_profile_name}" == "tv"
cp %{SOURCE7} %{SOURCE4}
cp %{SOURCE9} %{SOURCE5}
%endif
mkdir -p %{buildroot}/usr/share/dbus-1/system-services/

%{meson_install}

install -d %{buildroot}%{_unitdir}/paths.target.wants
install -m0644 %{SOURCE4} %{buildroot}%{_unitdir}/
install -m0644 %{SOURCE5} %{buildroot}%{_unitdir}/
ln -sf ../focus-server.path %{buildroot}%{_unitdir}/paths.target.wants/focus-server.path

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE8 %{buildroot}%{_tmpfilesdir}/focus.conf

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest libmm-sound.manifest
%defattr(-,root,root,-)
%{_bindir}/focus_server
%{_libdir}/libmmfsound.so*
%{_libdir}/libmmfkeysound.so*
%{_libdir}/libmmfbootsound.so*
%{_libdir}/libmmfmsgbox.so*
%{_libdir}/libmmfpairbox.so*
%{_libdir}/libmmfworkloop.so*
%{_libdir}/libmmfaudioconf.so*
%{_unitdir}/paths.target.wants/focus-server.path
%{_unitdir}/focus-server.service
%{_unitdir}/focus-server.path
%{_tmpfilesdir}/focus.conf

%license LICENSE.APLv2
/etc/dbus-1/system.d/focus-server.conf

%files devel
%defattr(-,root,root,-)
%{_libdir}/libmmfsound.so
%{_libdir}/libmmfkeysound.so
%{_libdir}/libmmfbootsound.so
%{_libdir}/libmmfmsgbox.so
%{_libdir}/libmmfpairbox.so
%{_libdir}/libmmfworkloop.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/mmf/*.h

%files sdk-devel
%defattr(-,root,root,-)

%files tool
%manifest libmm-sound-tool.manifest
%defattr(-,root,root,-)
%{_bindir}/mm_list_test
%{_bindir}/mm_msgbox_test
%{_bindir}/mm_pairbox_test
%{_bindir}/mm_sound_keysound_stress_test
%{_bindir}/mm_keytone_test
%{_bindir}/mm_audio_conf_test
%license LICENSE.APLv2
