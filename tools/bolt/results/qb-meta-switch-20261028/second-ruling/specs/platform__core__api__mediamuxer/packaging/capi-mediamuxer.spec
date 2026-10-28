Name:       capi-mediamuxer
Summary:    A Media Muxer library in Tizen Native API
Version:    0.2.3
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(iniparser)
#BuildRequires:  pkgconfig(capi-media-codec)
#BuildRequires:  pkgconfig(capi-mediademuxer)

%description
A Media Muxer library in Tizen Native API

%package devel
Summary:    Multimedia Framework Muxer Library (DEV)
Group:      Multimedia/API
Requires:   %{name} = %{version}-%{release}

%description devel
A Media Muxer library in Tizen Native API (Developement)

%package tools
Summary:    A test app for Media Muxer library in Tizen Native API
Group:      Developmenet/Tools
Requires:   %{name} = %{version}-%{release}

%description tools
A test app for Media Muxer library in Tizen Native API

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Media Muxer library in Tizen Native API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is tested as gcov for a media muxer library in Tizen native API
%endif

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
%ifarch %{arm}
export CFLAGS="$CFLAGS -DENABLE_FFMPEG_CODEC"
%endif
export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_sysconfdir}\\\" "

%if 0%{?gcov:1}
export CFLAGS+=" -DTIZEN_EXCLUDE_COVERAGE -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -DTIZEN_EXCLUDE_COVERAGE -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -DTIZEN_EXCLUDE_COVERAGE -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER}


make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp test/mediamuxer_test %{buildroot}%{_bindir}

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
%manifest capi-mediamuxer.manifest
%{_libdir}/libcapi-mediamuxer.so.*
%license LICENSE.APLv2

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-mediamuxer.so

%files tools
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_bindir}/*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
