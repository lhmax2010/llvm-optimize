# Do not create provides fro extension-tm1 because the main package
# should anchor any reverse-dependencies
%global __provides_exclude_from ^(.*\\.tm1)$

Name:       capi-media-codec
Summary:    A Media Codec library in Tizen Native API
Version:    1.2.9
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
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-app-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gstreamer-allocators-1.0)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(iniparser)
%if "%{tizen_profile_name}" != "tv"
BuildRequires:  pkgconfig(resource-center-api)
BuildRequires:  pkgconfig(resource-manager)
%endif
#BuildRequires:  pkgconfig(capi-media-camera)
#BuildRequires:  pkgconfig(capi-mediademuxer)
#BuildRequires:  pkgconfig(capi-mediamuxer)


%description
A Media Codec library in Tizen Native API


%package devel
Summary:  A Media Codec library in Tizen Native API (Development)
Group:    Multimedia/API
Requires: %{name} = %{version}-%{release}

%description devel


%package tools
Summary:  A Media Codec library in Tizen Native API (Tools)
Group:    Multimedia/API
Requires: %{name} = %{version}-%{release}

%description tools


%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Media Codec library in Tizen Native API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is tested as gcov for a media codec library in Tizen native API
%endif

%prep
%setup -q


%build

export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
SO_FULLVER=0.7.0
SO_MAJORVER=`echo ${SO_FULLVER} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=/usr -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DSO_FULLVER=${SO_FULLVER} -DSO_MAJORVER=${SO_MAJORVER} \
%if "%{tizen_profile_name}" == "tv"
  -DRMC=NO
%else
  -DRMC=YES
%endif

make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/bin
cp test/media_codec_test %{buildroot}/usr/bin

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -not -regex ".*\(test\|internal\|bitstream\|port\|ini\|util\).*$" -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif


%post
/sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest capi-media-codec.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-media-codec.so.*

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-codec.so

%files tools
%manifest %{name}-tools.manifest
%license LICENSE.APLv2
%{_bindir}/*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

