%if "%{tizen_profile_name}" == "tv"
%define profile_tv 1
%if "%{sec_buildconf_ir_touch_detection_support}" == "1"
%define buildconf_ir_touch_detection_support 1
%endif
%endif

Name:       capi-media-camera
Summary:    A Camera API
Version:    1.7.0
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(muse-client)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(mm-camcorder)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(mmsvc-camera)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  dali2-adaptor-integration-devel
BuildRequires:  pkgconfig(dali2-toolkit)
%if 0%{?profile_tv}
BuildRequires:  pkgconfig(capi-boost-tv)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(capi-system-resource)
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A Camera library in Tizen Native API.


%package devel
Summary:  A Camera API (Development)
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(libtbm)
Requires: pkgconfig(capi-media-tool)

%description devel
Development related files for a Camera library in Tizen Native API.


%package test-headed
Summary:  A Camera API testsuite for headed target
Requires: %{name} = %{version}-%{release}

%description test-headed
Tizen Native camera API testsuite for headed target.

%package test-headless
Summary:  A Camera API testsuite for headless target
Requires: %{name} = %{version}-%{release}

%description test-headless
Tizen Native camera API testsuite for headless target.


%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Camera library in Tizen Native API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a camera library in Tizen native API
%endif


%prep
%setup -q

%if 0%{?profile_tv}
echo "BUILD CONFIG: Profile TV"
%if 0%{?buildconf_ir_touch_detection_support}
echo "BUILD CONFIG: IR Touch Detection Support"
%endif
mv include/camera_tv.h include/camera.h
%else
rm include/camera_tv.h
%endif


%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
%if !0%{?profile_tv}
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_NO_TIMEOUT_FOR_PREVIEW"
%else
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_BOOST"
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_LAZY_SYMBOL_RESOLUTION"
%if 0%{?buildconf_ir_touch_detection_support}
export CFLAGS="$CFLAGS -DTIZEN_FEATURE_MEMORY_POOL"
%endif
%endif
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif
export CFLAGS="$CFLAGS -DPATH_LIBDIR=\\\"%{_libdir}\\\""
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
SO_FULLVER=0.5.0
SO_MAJORVER=`echo ${SO_FULLVER} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
%if 0%{?profile_tv}
    -DENABLE_PROFILE_TV=on \
%endif
%if 0%{?buildconf_ir_touch_detection_support}
    -DENABLE_TIZEN_FEATURE_MEMORY_POOL=on \
%endif
    -DFULLVER=%{version} \
    -DMAJORVER=${MAJORVER} \
    -DSO_FULLVER=${SO_FULLVER} \
    -DSO_MAJORVER=${SO_MAJORVER}

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

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%manifest capi-media-camera.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-media-camera.so.*

%files devel
%{_includedir}/media/camera.h
%{_includedir}/media/camera_internal.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-camera.so

%files test-headed
%manifest capi-media-camera-test-headed.manifest
%license LICENSE.APLv2
%{_bindir}/camera_test_headed
%{_bindir}/camera_test_headed2

%files test-headless
%manifest capi-media-camera-test-headless.manifest
%license LICENSE.APLv2
%{_bindir}/camera_test_headless

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

