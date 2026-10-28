Name:       capi-media-transporter
Summary:    A Media Transporter library in Tizen Native API
Version:    1.5.2
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
URL:        http://source.tizen.org
Source0:    %{name}-%{version}.tar.gz
Source1001: capi-media-transporter.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-rtsp-server-1.0)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(mm-display-interface)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(tizen-core-wl)
BuildRequires:  pkgconfig(resource-manager)
BuildRequires:  pkgconfig(resource-center-api)
# for test
BuildRequires:  pkgconfig(capi-media-camera)
BuildRequires:  pkgconfig(esplusplayer)
# DALi provides native image support in mtpr_test, enabled by default
# (MTPR_DALI_TEST). Disable with --define "dali_test_disable 1" if unavailable.
%if !0%{?dali_test_disable:1}
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  dali2-adaptor-integration-devel
BuildRequires:  pkgconfig(dali2-toolkit)
%endif
%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%description
A Media Transporter library in Tizen Native API.

%package devel
Summary:    Multimedia Media Transporter Library in Tizen Native API (Development)
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description devel
Media Transporter Library in Tizen Native API (DEV).

%package tool
Summary:  Tizen Media Transporter API testsuite
Requires: %{name} = %{version}-%{release}

%description tool
Tizen Media Transporter API testsuite.

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

%build
export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS="$CXXFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if "%{tizen_profile_name}" == "tv"
-DTIZEN_PROFILE_TV=on \
%else
-DTIZEN_PROFILE_TV=off \
%endif
%if 0%{?dali_test_disable:1}
-DMTPR_DALI_TEST=NO \
%endif
%if 0%{?gtests:1}
-DMTPR_UNITTEST=ON
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_hal_datadir}
cp test/mtpr_test %{buildroot}%{_bindir}

%make_install
mkdir -p %{buildroot}%{_hal_sysconfdir}/multimedia

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

%files tool
%defattr(-,root,root,-)
%{_bindir}/mtpr_test
%if 0%{?gtests:1}
%{_bindir}/mtpr_ut
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
