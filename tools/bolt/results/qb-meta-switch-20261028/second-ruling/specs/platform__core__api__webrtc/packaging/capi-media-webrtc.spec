Name:       capi-media-webrtc
Summary:    A WebRTC library in Tizen Native API
Version:    1.3.8
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
URL:        http://source.tizen.org
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-test.manifest
Source1003: %{name}-test-headless.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-webrtc-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-allocators-1.0)
BuildRequires:  pkgconfig(tizen-core-wl)
%if "%{without_dali_test}" != "1"
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  dali2-adaptor-integration-devel
BuildRequires:  pkgconfig(dali2-toolkit)
%endif
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(libtbm)
%if "%{without_signaling}" != "1"
BuildRequires:  pkgconfig(libsoup-2.4)
BuildRequires:  pkgconfig(libwebsockets)
%endif
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(mm-fileinfo)
%if "%{without_snapshot}" != "1"
BuildRequires:  pkgconfig(mmutil-common)
BuildRequires:  pkgconfig(mmutil-imgp)
BuildRequires:  pkgconfig(mmutil-jpeg)
BuildRequires:  pkgconfig(mmutil-magick)
%endif
%if "%{without_dns}" != "1"
BuildRequires:  pkgconfig(dns_sd)
%endif
%if "%{tizen_profile_name}" != "tv"
BuildRequires:  pkgconfig(resource-manager)
BuildRequires:  pkgconfig(resource-center-api)
BuildRequires:  pkgconfig(capi-system-sensor)
BuildRequires:  pkgconfig(sensor)
BuildRequires:  pkgconfig(esplusplayer)
%endif

%description
A WebRTC library in Tizen Native API.

%package devel
Summary:    Multimedia WebRTC Library in Tizen Native API (Development)
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description devel
WebRTC Library in Tizen Native API (DEV).

%package test
Summary:    Testsuite of Tizen Native WebRTC API
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description test
Testsuite of Tizen Native WebRTC API.

%if "%{test_espp_render}" != "1"
%package test-headless
Summary:    Testsuite of Tizen Native WebRTC API (For headless target)
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description test-headless
Testsuite of Tizen Native WebRTC API for headless target.
%endif

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage files
Group: Development/Multimedia

%description gcov
Collection of files related to line coverage using gcov.
%endif

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .

%build
export CFLAGS+=" -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS+=" -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

export CFLAGS+=" -DSUPPORT_FILESRC_AUDIO_FORMAT_CHANGE"

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if "%{tizen_profile_name}" == "tv"
-DTIZEN_PROFILE_TV=on \
%else
-DTIZEN_PROFILE_TV=off \
%endif
%if "%{test_espp_render}" == "1"
-DTIZEN_FEATURE_ESPP=on \
%else
-DTIZEN_FEATURE_ESPP=off \
%endif
%if "%{without_ui}" == "1"
-DTIZEN_FEATURE_UI=off \
%else
-DTIZEN_FEATURE_UI=on \
%endif
%if "%{without_dns}" == "1"
-DTIZEN_FEATURE_DNS=off \
%else
-DTIZEN_FEATURE_DNS=on \
%endif
%if "%{without_snapshot}" == "1"
-DTIZEN_FEATURE_SNAPSHOT=off \
%else
-DTIZEN_FEATURE_SNAPSHOT=on \
%endif
%if "%{without_signaling}" == "1"
-DTIZEN_FEATURE_SIGNALING=off \
%else
-DTIZEN_FEATURE_SIGNALING=on \
%endif
%if "%{without_dali_test}" == "1"
-DWEBRTC_DALI_TEST=off \
%else
-DWEBRTC_DALI_TEST=on \
%endif
-DAPI_VERSION=%{version}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%{_libdir}/lib%{name}.so.*
%license LICENSE.APLv2

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib%{name}.so

%if "%{without_signaling}" != "1"
%files test
%manifest %{name}-test.manifest
%{_bindir}/webrtc_test
%license LICENSE.APLv2
%endif

%if "%{test_espp_render}" != "1" && "%{without_signaling}" != "1"
%files test-headless
%manifest %{name}-test-headless.manifest
%{_bindir}/webrtc_test_headless
%license LICENSE.APLv2
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
