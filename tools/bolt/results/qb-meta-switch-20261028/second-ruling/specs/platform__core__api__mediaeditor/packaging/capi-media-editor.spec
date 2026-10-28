Name:       capi-media-editor
Summary:    A Tizen Media Editor API
Version:    0.1.3
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gst-editing-services-1.0)
BuildRequires:  pkgconfig(boost)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  gtest-devel
BuildRequires:  gtest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
%if "%{tizen_profile_name}" != "tv"
BuildRequires:  pkgconfig(resource-manager)
BuildRequires:  pkgconfig(resource-information)
BuildRequires:  pkgconfig(resource-center-api)
%endif

%description
A Media Editor library in Tizen Native API.

%package devel
Summary:  A Media Editor API (Development)
Requires: %{name} = %{version}-%{release}

%description devel
Development related files for a Media Editor library in Tizen Native API.

%package tool
Summary:  A Media Editor API testsuite with gtest
Requires: %{name} = %{version}-%{release}
BuildRequires: gtest-devel
BuildRequires: gtest

%description tool
Tizen Native Media Editor API testsuite with gtest.

%files tool
%defattr(-,root,root,-)
%{_bindir}/mediaeditor_ut

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Media Editor library in Tizen Native API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a Media Editor library in Tizen native API
%endif

%prep
%setup -q

%build
export CFLAGS="${CFLAGS} -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS="${CXXFLAGS} -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="${CFLAGS} -DTIZEN_DEBUG_ENABLE"
%endif

%if 0%{?gcov:1}
export CFLAGS="${CFLAGS} -fprofile-arcs -ftest-coverage"
export CXXFLAGS="${CXXFLAGS} -fprofile-arcs -ftest-coverage"
export LDFLAGS="${LDFLAGS} -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if "%{tizen_profile_name}" == "tv"
-DTIZEN_PROFILE_TV=on
%else
-DTIZEN_PROFILE_TV=off
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp test/media_editor_test %{buildroot}%{_bindir}

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
%manifest capi-media-editor.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-media-editor.so.*

%files devel
%{_includedir}/media/media_editor.h
%{_includedir}/media/media_editor_internal.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-editor.so

%files tool
%manifest capi-media-editor-tool.manifest
%license LICENSE.APLv2
%{_bindir}/*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
