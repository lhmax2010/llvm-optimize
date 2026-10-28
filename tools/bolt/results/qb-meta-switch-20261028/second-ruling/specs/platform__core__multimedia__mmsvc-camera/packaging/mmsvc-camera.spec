%if "%{tizen_profile_name}" == "tv"
%define profile_tv 1
%if "%{sec_buildconf_ir_touch_detection_support}" == "1"
%define buildconf_ir_touch_detection_support 1
%endif
%endif

Name:       mmsvc-camera
Summary:    A Camera module for muse server
Version:    1.5.1
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(muse-server)
BuildRequires:  pkgconfig(mm-camcorder)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libtbm)
%if "%{gtests}" == "1"
BuildRequires:  pkgconfig(gmock)
%endif
%if 0%{?profile_tv}
BuildRequires:  pkgconfig(capi-boost-tv)
BuildRequires:  pkgconfig(capi-system-info)
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
A Camera module for muse server and native camera API.


%package devel
Summary:  A Camera module for muse server (Development)
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(libtbm)

%description devel
Development related files of a Camera module for muse server.


%prep
%setup -q

%if 0%{?profile_tv}
echo "BUILD CONFIG: Profile TV"
%if 0%{?buildconf_ir_touch_detection_support}
echo "BUILD CONFIG: IR Touch Detection Support"
%endif
%endif

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS+=" -DTIZEN_DEBUG_ENABLE"
%endif
%if 0%{?profile_tv}
export CFLAGS+=" -DTIZEN_FEATURE_USE_PROD_FEATURE_AND_PRIVILEGE"
export CFLAGS+=" -DTIZEN_FEATURE_BOOST"
%if 0%{?buildconf_ir_touch_detection_support}
export CFLAGS+=" -DTIZEN_FEATURE_MEMORY_POOL"
%endif
%endif
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
%if "%{gtests}" == "1"
	-DENABLE_GTESTS=On\
%else
	-DENABLE_GTESTS=Off\
%endif
%if 0%{?profile_tv}
	-DENABLE_PROFILE_TV=On\
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix}\
	-DFULLVER=%{version}\
	-DMAJORVER=${MAJORVER}\
	-DLIBDIR=%{_libdir}


make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
%make_install


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig

%files
%manifest mmsvc-camera.manifest
%license LICENSE.APLv2
%{_libdir}/liblegacy-camera.so
%{_libdir}/libmuse-camera.so
%if "%{gtests}" == "1"
%{_bindir}/gtests-*
%endif

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
