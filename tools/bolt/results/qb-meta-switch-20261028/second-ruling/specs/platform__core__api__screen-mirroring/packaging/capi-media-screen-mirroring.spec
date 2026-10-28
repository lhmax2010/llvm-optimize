Name:       capi-media-screen-mirroring
Summary:    A screen mirroring library in Tizen C API
Version:    0.5.0
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-rtsp-server-1.0)
BuildRequires:  pkgconfig(capi-network-wifi-direct)
BuildRequires:  pkgconfig(mm-wfd)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(tizen-core-wl)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A screen mirrroing library in Tizne native API

%package devel
Summary:  A Screen Mirroring library in Tizen C API (Development)
Group:    Development/Multimedia
Requires: %{name} = %{version}-%{release}

%description devel
Development related files for a screen mirrroring library in Tizen native API

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Screen Mirroring library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a screen mirroring library in Tizen native API
%endif

%package tool
Summary: Test related files for Screen Mirroring library in Tizen native API
Group: Development/Multimedia

%description tool
Collection of files related to test of Screen Mirroring. It has test suites of Source and Sink of Screen Mirroring.

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -Wextra -Wno-array-bounds"
export CFLAGS="$CFLAGS -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow"
export CFLAGS="$CFLAGS -Wwrite-strings -Wno-deprecated-declarations -Wno-deprecated"
export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
#export CFLAGS+="-Wswitch-default"
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

%cmake . \
         -DFULLVER=%{version} \
         -DMAJORVER=${MAJORVER} \
         -DTZ_SYS_BIN=%TZ_SYS_BIN \
         -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE \
         -DTZ_SYS_RO_ETC=%TZ_SYS_RO_ETC \
%if "%{tizen_profile_name}" == "tv"
  -DTIZEN_FEATURE_MM_DISPLAY_TYPE=NO
%else
  -DTIZEN_FEATURE_MM_DISPLAY_TYPE=YES
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{TZ_SYS_RO_SHARE}/dbus-1/system-services/
install -m 644 org.tizen.scmirroring.server.service %{buildroot}%{TZ_SYS_RO_SHARE}/dbus-1/system-services/
mkdir -p %{buildroot}%{_unitdir}
install -m 644 packaging/scmirroring.server.service %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/dbus-1/system.d/
cp -rf %{_builddir}/%{name}-%{version}/packaging/org.tizen.scmirroring.server.conf %{buildroot}/etc/dbus-1/system.d/
%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -not -regex ".*\(primary\|secondary\|internal\|ini\|_src\|util\|test\|miracast\).*$" -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest capi-media-screen-mirroring.manifest
%{_libdir}/libcapi-media-screen-mirroring.so.*
%{_libdir}/libmiracast_server_lib.so.*
%{_unitdir}/scmirroring.server.service
%{_datadir}/dbus-1/system-services/org.tizen.scmirroring.server.service
#License
%license LICENSE.APLv2.0
%{_bindir}/miracast_server
/etc/dbus-1/system.d/org.tizen.scmirroring.server.conf

%files devel
%{_includedir}/media/scmirroring_src.h
%{_includedir}/media/scmirroring_sink.h
%{_includedir}/media/scmirroring_primary_sink.h
%{_includedir}/media/scmirroring_secondary_sink.h
%{_includedir}/media/scmirroring_type.h
%{_includedir}/media/scmirroring_type_internal.h
%{_includedir}/media/scmirroring_src_ini.h
%{_includedir}/media/scmirroring_internal.h
%{_includedir}/media/miracast_server.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-screen-mirroring.so
%{_libdir}/libmiracast_server_lib.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files tool
%manifest capi-media-screen-mirroring.manifest
%{_bindir}/scmirroring_test
%{_bindir}/scmirroring_sink_test
