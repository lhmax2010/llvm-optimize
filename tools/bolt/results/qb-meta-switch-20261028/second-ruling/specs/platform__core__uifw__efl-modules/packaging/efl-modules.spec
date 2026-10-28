Name:       efl-modules
Summary:    The EFL Modules
Version:    0.1.1
Release:    1
Provides:   efl-modules = %{version}-%{release}
Group:      System/Libraries
License:    Flora-1.1
URL:        http://www.tizen.org
Source0:    %{name}-%{version}.tar.gz
BuildRequires: elementary-devel, eina-devel
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: libfeedback-devel
BuildRequires: gettext
BuildRequires: tts-devel
BuildRequires: pkgconfig(capi-media-audio-io)
BuildRequires: pkgconfig(capi-media-sound-manager)
BuildRequires: pkgconfig(tzsh-quickpanel)
BuildRequires: pkgconfig(capi-ui-efl-util)
BuildRequires: pkgconfig(efl-extension)

%description
The EFL Modules

%package -n efl-modules-profile_common
Summary: The EFL Modules
License: Flora-1.1

%description -n efl-modules-profile_common
The EFL Modules for common profile.

%package -n efl-modules-profile_tv
Summary: The EFL Modules
License: Flora-1.1

%description -n efl-modules-profile_tv
The EFL Modules for tv profile.

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -fvisibility=hidden -fPIC -Wall -Wno-implicit-function-declaration"
export LDFLAGS="$LDFLAGS -fvisibility=hidden -Wl,--hash-style=both -Wl,--as-needed -Wl,-z,defs"

%define DEF_SUBDIRS clock_input_spinner clock_input_spinner_tv edje_feedback ecore_audio_tizen quickpanel_callback naviframe_effect_mobile  calendar_string access_output_tts


for FILE in %{DEF_SUBDIRS}
do
    cd $FILE
    if [ -f autogen.sh ]
    then
        ./autogen.sh && %configure && make
    else
        make
    fi
    cd ..
done

%install
for FILE in %{DEF_SUBDIRS}
do
        (cd $FILE && PREFIX=%{buildroot}/usr make install DESTDIR=%{buildroot})
done

%files -n efl-modules-profile_common
%defattr(-,root,root,-)
/usr/share/locale/*/LC_MESSAGES/*
%{_libdir}/elementary/modules/calendar_string/*/*.so
%{_libdir}/elementary/modules/clock_input_spinner/*/*.so
%{_libdir}/elementary/modules/naviframe_effect_mobile/*/*.so
%{_libdir}/elementary/modules/quickpanel_callback/*/*.so
%{_libdir}/edje/modules/*/*/*.so
%{_libdir}/ecore_audio/modules/*/*/*.so
%license COPYING
%manifest %{name}.manifest
## Below is not needed except Machintosh
%exclude %{_libdir}/elementary/modules/calendar_string/*/*.la
%exclude %{_libdir}/elementary/modules/clock_input_spinner/*/*.la
%exclude %{_libdir}/elementary/modules/naviframe_effect_mobile/*/*.la
%exclude %{_libdir}/elementary/modules/quickpanel_callback/*/*.la
%exclude %{_libdir}/edje/modules/*/*/*.la
%exclude %{_libdir}/ecore_audio/modules/*/*/*.la

%files -n efl-modules-profile_tv
%defattr(-,root,root,-)
%{_libdir}/elementary/modules/clock_input_spinner_tv/*/*.so
%{_libdir}/elementary/modules/access_output_tts/*/*.so
%{_libdir}/edje/modules/*/*/*.so
%license COPYING
%manifest %{name}.manifest
## Below is not needed except Machintosh
%exclude %{_libdir}/elementary/modules/clock_input_spinner_tv/*/*.la
%exclude %{_libdir}/elementary/modules/access_output_tts/*/*.la
%exclude %{_libdir}/edje/modules/*/*/*.la
