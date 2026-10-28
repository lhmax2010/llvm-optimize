#%bcond_with : disable ESPLUSPLAYER_UT by default, %bcond_without : enable ESPLUSPLAYER_UT
%bcond_without TIZEN_PUBLIC
%bcond_without TIZEN_PUBLIC_DRM
# ecore is enabled by default; disable with: gbs build --define "ecore 0"
%{!?ecore:%define ecore 1}

%if ("%{_vd_cfg_product_type}" != "AUDIO")
%bcond_without ESPLUSPLAYER_UT
%else
%bcond_with ESPLUSPLAYER_UT
%endif
#echo "Product Type: %{_vd_cfg_product_type}"

Name:       esplusplayer
Summary:    new multimedia streaming player
Version:    1.4.4
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: esplusplayer.manifest
BuildRequires:  cmake
BuildRequires:  curl
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(boost)
BuildRequires:  pkgconfig(tizen-core-wl)
%if %{with TIZEN_PUBLIC}
BuildRequires:  pkgconfig(libtrackrenderer)
BuildRequires:  pkgconfig(capi-media-sound-manager)
# for test
BuildRequires:  pkgconfig(capi-mediademuxer)
%else
BuildRequires:  pkgconfig(tv-resource-manager)
BuildRequires:  pkgconfig(drmdecrypt)
BuildRequires:  pkgconfig(context-aware-api)
%if ("%{_vd_cfg_product_type}" != "AUDIO")
BuildRequires:  pkgconfig(graphics-control)
%endif
BuildRequires:  pkgconfig(capi-trackrenderer-tv)
BuildRequires:  pkgconfig(logger)
%endif

BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(jsoncpp)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libtbm)

BuildRequires:  pkgconfig(capi-system-info)

%if (("%{sec_buildconf_product_lite_tizen}" == "n") || %{with TIZEN_PUBLIC})
# for ut
BuildRequires:  gtest-devel
%endif

%define _packagedir /usr
%define _bindir %{_packagedir}/bin
%define _includedir %{_packagedir}/include
%define _pkgconfigdir %{_libdir}/pkgconfig
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%description
new multimedia player, object-oriented model

%package devel
Summary:    Developement for multimedia player
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%package config
Summary:    Configuration for multimedia player
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
%devel_desc

%description config

#################################################
# gcov
#################################################
%if 0%{?vd_gcov:1}
%package gcov
Summary: gcov enabled package
Group: gcov package

%description gcov
This package is gcov package for coverage measurement.
%endif

%if %{with TIZEN_PUBLIC}
%package tool
Summary:  Esplusplayer API testsuite with mediademuxer
Requires: %{name} = %{version}-%{release}

%description tool
Esplusplayer API testsuite with mediademuxer
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%if ("%{sec_buildconf_product_lite_tizen}" == "n")
%if ("%{_vd_cfg_product_type}" != "AUDIO")
%{?!TOMATO: %define TOMATO n}

%define _tomatoname esplusplayer
%define _tomatodir  /opt/usr/apps/tomato/testcase/%{name}
%define _tomatobin /opt/usr/apps/tomato/testcase/%{name}/bin

%package ut-component-tomato
Summary: Test package with TOMATO
BuildRequires:  gtest-devel
%if %{without TIZEN_PUBLIC}
BuildRequires:  pkgconfig(video-capture)
BuildRequires:  pkgconfig(audio-control)
BuildRequires:  pkgconfig(video-sink)
%endif
BuildRequires:  libjpeg-turbo-devel

#BuildRequires:  pkgconfig(capi-system-info)
Requires: %{name} = %{version}-%{release}

%description ut-component-tomato
This package is for test

%files ut-component-tomato
%defattr(-,root,root,-)
%{_bindir}/esplusplayer_ut
%{_tomatodir}/*

%endif
%endif

%build
export CFLAGS+=" -Wno-deprecated-declarations"
export CXXFLAGS+=" -Wno-deprecated-declarations"

%if %{with TIZEN_PUBLIC}
export CFLAGS+=" -DTIZEN_FEATURE_PUBLIC -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS+=" -DTIZEN_FEATURE_PUBLIC -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

%if %{with TIZEN_PUBLIC_DRM}
export CFLAGS+=" -DTIZEN_FEATURE_PUBLIC_DRM"
export CXXFLAGS+=" -DTIZEN_FEATURE_PUBLIC_DRM"
%endif

%define TIZEN_PUBLIC ON
%define USE_MIXER no
%else
%if ("%{_vd_cfg_product_type}" == "AUDIO")
export CFLAGS+=" -DIS_AUDIO_PRODUCT"
export CXXFLAGS+=" -DIS_AUDIO_PRODUCT"
%define PRODUCT_TYPE_AUDIO yes
%define USE_MIXER no
%else
export CFLAGS+=" -DUSE_MIXER"
export CXXFLAGS+=" -DUSE_MIXER"
%define PRODUCT_TYPE_AUDIO no
%define USE_MIXER yes
%endif
%define TIZEN_PUBLIC OFF
%endif

#TODO: check AV type is used or not
%if ("%{_vd_cfg_product_type}" == "AV")
export CFLAGS+=" -DIS_AV_PRODUCT"
export CXXFLAGS+=" -DIS_AV_PRODUCT"
%endif

#TODO: AUDIO type is used to enable fmm mode API impl.
%if ("%{_vd_cfg_product_type}" == "AUDIO")
export CFLAGS+=" -DSOUNDBAR_PRODUCT"
export CXXFLAGS+=" -DSOUNDBAR_PRODUCT"
%define _support_soundbar -DSUPPORT_SOUNDBAR=ON
%endif

%if 0%{?vd_gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
#export CFLAGS+=" -DIS_TOMATO"
#export CXXFLAGS+=" -DIS_TOMATO"
%endif

export CXXFLAGS+=" -Wno-pessimizing-move"

%ifarch aarch64
export CXXFLAGS+=" -DDRM_MAPI_AARCH_64"
%endif

%if 0%{?ecore}
%define HAVE_ECORE ON
%else
%define HAVE_ECORE OFF
%endif

%if %{with ESPLUSPLAYER_UT}
%cmake . -DESPLUSPLAYER_BUILD_UT=ON -DPRODUCT_TYPE_AUDIO=%PRODUCT_TYPE_AUDIO -DUSE_MIXER=%USE_MIXER -DTIZEN_PUBLIC=%TIZEN_PUBLIC -DHAVE_ECORE=%HAVE_ECORE
%else
%cmake . -DPRODUCT_TYPE_AUDIO=%PRODUCT_TYPE_AUDIO -DUSE_MIXER=%USE_MIXER -DTIZEN_PUBLIC=%TIZEN_PUBLIC -DHAVE_ECORE=%HAVE_ECORE
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%if ("%{sec_buildconf_product_lite_tizen}" == "n")
mkdir -p %{buildroot}%{_tomatodir}
mkdir -p %{buildroot}%{_tomatodir}/log
mkdir -p %{buildroot}%{_tomatodir}/result
mkdir -p %{buildroot}%{_tomatodir}/tc
cp -rf tomato/tc/* %{buildroot}%{_tomatodir}/tc
%endif

%make_install
%if %{without TIZEN_PUBLIC}
mkdir -p %{buildroot}%TZ_SYS_RO_ETC/multimedia
%endif
#mkdir -p %{buildroot}%TZ_SYS_RW_APP/multimedia
#mkdir -p %{buildroot}/opt
#mkdir -p %{buildroot}/opt/usr
#mkdir -p %{buildroot}/opt/usr/home
#mkdir -p %{buildroot}/opt/usr/home/owner
#mkdir -p %{buildroot}/opt/usr/home/owner/models
%if %{without TIZEN_PUBLIC}
cp -rf config/esplusplayer.ini %{buildroot}%TZ_SYS_RO_ETC/multimedia/esplusplayer.ini
%endif

%if 0%{?vd_gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj
find . \( -name '*.gcno' -o -name '*.cpp' -o -name '*.c' -o -name '*.hpp' -o -name '*.h' \) ! -path "./ut/*" ! -path "./test/*" ! -path "*/CompilerIdCXX/*" -exec cp --parents -r '{}' %{buildroot}%{_datadir}/gcov/obj ';'
%endif

%files
%defattr(-,root,root,-)
%manifest esplusplayer.manifest
%license LICENSE.APLv2
%{_libdir}/libespplayer-core.so
%{_libdir}/libesplusplayer.so
%if ("%{USE_MIXER}" == "yes")
%{_libdir}/libmixer.so
%endif

%if %{without TIZEN_PUBLIC}
%TZ_SYS_RO_ETC/multimedia/esplusplayer.ini
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/esplusplayer/*.h
%{_includedir}/esplusplayer/types/*.h
%{_includedir}/esplusplayer_capi/*.h
%{_includedir}/mixer/*.h
%{_includedir}/mixer_capi/*.h
%{_pkgconfigdir}/esplusplayer.pc

%files config
%defattr(-,root,root,-)
%manifest esplusplayer.manifest
%license LICENSE.APLv2
%if %{without TIZEN_PUBLIC}
%TZ_SYS_RO_ETC/multimedia/esplusplayer.ini
%attr(0775, owner,users) %TZ_SYS_RO_ETC/multimedia
%endif

%if 0%{?vd_gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%if %{with TIZEN_PUBLIC}
%files tool
%defattr(-,root,root,-)
%{_bindir}/esplusplayer_test
%if %{with ESPLUSPLAYER_UT}
%{_bindir}/esplusplayer_ut
%endif
%defattr(-,root,root,-)
%endif
