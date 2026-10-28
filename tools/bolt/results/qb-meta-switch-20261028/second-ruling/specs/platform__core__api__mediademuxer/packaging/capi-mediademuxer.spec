Name:       capi-mediademuxer
Summary:    A Media Demuxer library in Tizen Native API
Version:    0.2.4
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
#BuildRequires:  pkgconfig(capi-media-codec)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(iniparser)

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%description
A Media Demuxer library in Tizen Native API

%package devel
Summary:    Multimedia Framework Demuxer Library (DEV)
Group:      Multimedia/API
Requires:   %{name} = %{version}-%{release}

%description devel
A Media Demuxer library in Tizen Native API (Developement)

%package tools
Summary:    A test app for Media Demuxer library in Tizen Native API
Group:      Developmenet/Tools
Requires:   %{name} = %{version}-%{release}

%description tools
A test app for Media Demuxer library in Tizen Native API

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Media Demuxer library in Tizen Native API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is tested as gcov for a media demuxer library in Tizen native API
%endif

%if 0%{?gtests:1}
%package ut
Summary: A unittest app for Media Demuxer API
Group:   Utils/Multimedia
Requires: %{name} = %{version}-%{release}

%description ut
A unittest app for Media Demuxer API
%endif

%prep
%setup -q


%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
%ifarch %{arm} riscv64
export CFLAGS="$CFLAGS -DENABLE_FFMPEG_CODEC"
%endif
export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_sysconfdir}\\\" -DTIZEN_FEATURE_GST_UPSTREAM"

%if 0%{?gcov:1}
export CFLAGS+=" -DTIZEN_EXCLUDE_COVERAGE -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -DTIZEN_EXCLUDE_COVERAGE -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -DTIZEN_EXCLUDE_COVERAGE -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if 0%{?gtests:1}
  -DBUILD_UNITTEST=YES
%else
  -DBUILD_UNITTEST=NO
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp test/mediademuxer_test %{buildroot}%{_bindir}

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
%manifest capi-mediademuxer.manifest
%{_libdir}/libcapi-mediademuxer.so.*
%license LICENSE.Apache-2.0

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-mediademuxer.so

%files tools
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_bindir}/mediademuxer_test

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%if 0%{?gtests:1}
%files ut
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_bindir}/mediademuxer_ut
%endif
