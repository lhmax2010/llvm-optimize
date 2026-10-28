Name:       capi-media-player
Summary:    A Media Player API
Version:    1.0.16
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-media-player.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(muse-client)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(mmsvc-player)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libinput)
# libudev was previously pulled into the build rootstrap transitively through
# the EFL packages. Since those are now conditional, require it explicitly
# (needed by the test suite and mm-navevent-handler).
BuildRequires:  pkgconfig(libudev)
# player_test uses tizen-core-wl. Only the optional player_ecore_test target
# (--define "ecore_test 1") still needs EFL; player_ut (gtests) has been
# migrated to tizen_core_wl and no longer requires it.
%if 0%{?ecore_test:1}
BuildRequires:  pkgconfig(appcore-efl)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(evas)
%endif
# DALi provides native image support in player_test, enabled by default
# (PLAYER_DALI_TEST). Disable with --define "dali_test_disable 1" if unavailable.
%if !0%{?dali_test_disable:1}
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  dali2-adaptor-integration-devel
BuildRequires:  pkgconfig(dali2-toolkit)
%endif

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(jsoncpp)
# Used to fetch contentsInfo.config from the content server. The media files
# themselves are streamed by the player from the URL, not downloaded.
BuildRequires:  pkgconfig(libcurl)
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A Media Player library in Tizen Native API.

%package devel
Summary:  A Media Player library in Tizen Native API (Development)
Group:    Development/Multimedia
Requires: %{name} = %{version}-%{release}

%description devel
%devel_desc

%package utils
Summary: A test app for Media Player API
Group:   Utils/Multimedia
Requires: %{name} = %{version}-%{release}

%description utils
A test app for Media Player API

%if 0%{?gtests:1}
%package ut
Summary: A unittest app for Media Player API
Group:   Utils/Multimedia
Requires: %{name} = %{version}-%{release}

%description ut
A unittest app for Media Player API
%endif

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Player library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a Player library in Tizen native API
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
#export CFLAGS+=" -D_USE_X_DIRECT_"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT -DPATH_LIBDIR=\\\"%{_libdir}\\\""

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
SO_FULLVER=0.4.0
SO_MAJORVER=`echo ${SO_FULLVER} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DSO_FULLVER=${SO_FULLVER} -DSO_MAJORVER=${SO_MAJORVER} \
%if 0%{?ecore_test:1}
  -DPLAYER_ECORE_TEST=YES \
%endif
%if 0%{?dali_test_disable:1}
  -DPLAYER_DALI_TEST=NO \
%endif
%if 0%{?gtests:1}
  -DBUILD_UNITTEST=YES
%else
  -DBUILD_UNITTEST=NO
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
cp test/player_test %{buildroot}/usr/bin
cp test/player_es_push_test %{buildroot}/usr/bin
cp test/player_audio_test %{buildroot}/usr/bin
cp test/player_simple_test %{buildroot}/usr/bin
cp test/player_media_packet_test %{buildroot}/usr/bin
%if 0%{?ecore_test:1}
cp test/player_ecore_test %{buildroot}/usr/bin
%endif

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -not -regex ".*\(test\|internal\|handler\).*$" -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-media-player.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/media/player.h
%{_includedir}/media/player_internal.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-player.so

%files utils
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_bindir}/player_test
%{_bindir}/player_es_push_test
%{_bindir}/player_audio_test
%{_bindir}/player_simple_test
%{_bindir}/player_media_packet_test
%if 0%{?ecore_test:1}
%{_bindir}/player_ecore_test
%endif
%{_libdir}/libmm-navevent-handler.so*

%if 0%{?gtests:1}
%files ut
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_bindir}/player_ut
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
