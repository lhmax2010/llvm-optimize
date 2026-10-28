%bcond_without wayland
%bcond_with x
# BUILD_TCORE_ENABLE: 0 (default) = ECORE, 1 = TCORE, for Tizen 11 only.
# Example: gbs build ... --define "BUILD_TCORE_ENABLE 1"
# Resolve the backend here for both dependencies and build options.
%{!?BUILD_TCORE_ENABLE:%global BUILD_TCORE_ENABLE 0}
%global tizen_wayland_backend ECORE
%if 0%{?tizen_version_major} == 11
%if "%{BUILD_TCORE_ENABLE}" != "0" && "%{BUILD_TCORE_ENABLE}" != "1"
%{error:BUILD_TCORE_ENABLE must be 0 or 1}
%endif
%if "%{BUILD_TCORE_ENABLE}" == "1"
%global tizen_wayland_backend TCORE
%endif
%endif

Name:    libwidget_viewer_dali
Summary: Library for developing the application
Version: 1.4.12
Release: 1
Group:   System/Libraries
License: Flora-1.1
Source0: %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: gettext-tools
BuildRequires: pkgconfig
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(widget_service)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(dali2-core)
BuildRequires: pkgconfig(dali2-adaptor)
BuildRequires: pkgconfig(dali2-toolkit)
BuildRequires: dali2-integration-devel
BuildRequires: dali2-adaptor-integration-devel
BuildRequires: dali2-toolkit-integration-devel
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-self)
BuildRequires: pkgconfig(wayland-tbm-client)
%if "%{?tizen_wayland_backend}" == "TCORE"
BuildRequires: pkgconfig(screen_connector_watcher_tcore)
%else
BuildRequires: pkgconfig(screen_connector_watcher)
%endif

# For ASAN test
%if "%{vd_asan}" == "1" || "%{asan}" == "1"
BuildRequires: asan-force-options
BuildRequires: asan-build-env
BuildRequires: libasan
%endif

%description
API for creating a new instance of the widget and managing its life-cycle.

##############################
# devel
##############################
%package devel
Summary: Development Library for widget Viewer Dali Application
Group: Development/Building
Requires: %{name} = %{version}-%{release}

%description devel
Header and package configuration files for the widget viewer development

##############################
# Preparation
##############################
%prep
%setup -q

##############################
# Build
##############################
%build

PREFIX="/usr"
CXXFLAGS="$CXXFLAGS -Wall -g -O2 -fPIE -Wl,-z,relro,-z,now -fstack-protector-strong -D_FORTIFY_SOURCE=2"
LDFLAGS="$LDFLAGS -Wl,--rpath=$PREFIX/lib -Wl,--as-needed -pie -Wl,-z,relro,-z,now"

%ifarch %{arm}
CXXFLAGS="$CXXFLAGS -D_ARCH_ARM_"
%endif

%if 0%{?tizen_version_major} >= 7
CXXFLAGS="$CXXFLAGS -DOVER_TIZEN_VERSION_7"
%endif

%if "%{vd_asan}" == "1" || "%{asan}" == "1"
CFLAGS="$CFLAGS -fsanitize=address"
CXXFLAGS="$CXXFLAGS -fsanitize=address"
LDFLAGS="$LDFLAGS -fsanitize=address"
%endif

cd %{_builddir}/%{name}-%{version}/build/tizen

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DWIDGET_ENABLED=On \
	   -DTZ_SYS_SHARE=/usr/share \
       -DFULLVER=%{version} \
       -DMAJORVER=${MAJORVER} \
       -DTIZEN_WAYLAND_BACKEND=%{?tizen_wayland_backend} \
%if 0%{?enable_debug}
      -DCMAKE_BUILD_TYPE=Debug \
%endif
       .

make %{?jobs:-j%jobs}

##############################
# Installation
##############################

%install
rm -rf %{buildroot}
cd build/tizen
%make_install

##############################
# Post Install
##############################

%post
/sbin/ldconfig
exit 0

##############################
# Post Uninstall
##############################

%postun
/sbin/ldconfig
exit 0

##############################
# Files in Binary Packages
##############################

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/%{name}.so*
%license LICENSE
/usr/share/widget_viewer_dali/images/*.png
/usr/share/widget_viewer_dali/locale/*/LC_MESSAGES/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/widget_viewer_dali/*
%{_libdir}/pkgconfig/widget_viewer_dali.pc

# End of a file
