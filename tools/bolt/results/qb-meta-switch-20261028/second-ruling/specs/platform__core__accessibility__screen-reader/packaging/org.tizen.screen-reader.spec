%{!?unittest:%global unittest 0}
%{!?compile_commands:%global compile_commands 0}
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

Name:       org.tizen.screen-reader
Summary:    Screen Reader Assistive Technology
Version:    0.0.8
Release:    1
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  at-spi2-core
BuildRequires:  at-spi2-core-devel
BuildRequires:  cmake
BuildRequires:  pkgconfig(appcore-common)
%if "%{tizen_wayland_backend}" == "TCORE"
BuildRequires:  pkgconfig(tizen-core)
%else
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(eina)
BuildRequires:  pkgconfig(eldbus)
%endif
BuildRequires:  pkgconfig(mm-sound)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  tts
BuildRequires:  tts-devel
BuildRequires:  vconf
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(capi-network-bluetooth)
BuildRequires:  pkgconfig(notification)
BuildRequires:  pkgconfig(capi-network-wifi-manager)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(tapi)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(appsvc)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(gio-2.0)
Provides:       %{name}-profile_common = %{version}-%{release}
Provides:       %{name}-profile_mobile = %{version}-%{release}
Provides:       %{name}-profile_wearable = %{version}-%{release}
Provides:       %{name}-profile_ivi = %{version}-%{release}

%description
An utility library for developers of the menu screen.

%package extension-no-tapi
Summary:        Screen Reader Assistive Technology without TAPI (for TV profile)
Requires:       %{name}
Provides:       %{name}-profile_tv = %{version}-%{release}
%description extension-no-tapi
An extension for profile TV.
This extension removes the usage of tapi.

%if %{unittest}
%package unittests
Summary:        Screen Reader unittests and libraries.
License:        Flora-1.1 and Apache-2.0 and BSD-3-Clause and BSD-2-Clause
%description unittests
Screen Reader unittests and libraries required to correctly run them.
%endif

%prep
%setup -q

%build
%define DataDir %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:/usr/share}
%define AppDir %{TZ_SYS_RO_APP}/%{name}
%define Exec screen-reader

rm -rf CMakeFiles CMakeCache.txt

%if "%{tizen_wayland_backend}" == "TCORE"
export CFLAGS="$CFLAGS -DUSE_TCORE_BACKEND"
%else
export CFLAGS="$CFLAGS -DECORE"
%endif

%if "%{?profile}" == "tv"
        export FEATURE_MULTI_WIN_NAV_ENABLE="1"
%else
%if 0%{?_with_da_profile:1} || "%{?profile}" == "mobile" || "%{?profile}" == "wearable" || "%{?profile}" == "ivi"
        export FEATURE_MULTI_WIN_NAV_ENABLE="0"
%else
        export FEATURE_MULTI_WIN_NAV_ENABLE="1"
%endif
%endif

# For build optimization for mobile/wearable
# In the unified build, this should be always true
%if "%{?profile}"!="mobile" && "%{?profile}"!="wearable"
mkdir -p build_no_tapi
_screen_reader_builddir=$(pwd)
cd build_no_tapi
	export SEC_FEATURE_TAPI_ENABLE="0"
cmake .. -DCMAKE_INSTALL_PREFIX="%{AppDir}" \
	-DCMAKE_TARGET="%{Exec}" \
	-DCMAKE_PACKAGE="%{name}" \
	-DTZ_SYS_RO_APP=%{TZ_SYS_RO_APP} \
	-DTZ_SYS_RO_PACKAGES=%{TZ_SYS_RO_PACKAGES} \
	-DSEC_FEATURE_TAPI_ENABLE=${SEC_FEATURE_TAPI_ENABLE} \
	-DFEATURE_MULTI_WIN_NAV_ENABLE=${FEATURE_MULTI_WIN_NAV_ENABLE} \
	-DTIZEN_WAYLAND_BACKEND=%{tizen_wayland_backend}

make %{?jobs:-j%jobs} \
2>&1 | sed \
-e 's%^.*: error: .*$%\x1b[37;41m&\x1b[m%' \
-e 's%^.*: warning: .*$%\x1b[30;43m&\x1b[m%'
export LD_LIBRARY_PATH=/emul/ia32-linux/lib:/emul/ia32-linux/usr/lib:$LD_LIBRARY_PATH
export CTEST_OUTPUT_ON_FAILURE=1
make test
cd "$_screen_reader_builddir"
%endif

# For build optimization for TV
# In the unified build, this should be always true
%if "%{profile}" != "tv"
        export SEC_FEATURE_TAPI_ENABLE="1"
        export CFLAGS="$CFLAGS -DELM_ACCESS_KEYBOARD"

cmake . -DCMAKE_INSTALL_PREFIX="%{AppDir}" \
        -DCMAKE_TARGET="%{Exec}" \
        -DCMAKE_PACKAGE="%{name}" \
        -DTZ_SYS_RO_APP=%{TZ_SYS_RO_APP} \
        -DTZ_SYS_RO_PACKAGES=%{TZ_SYS_RO_PACKAGES} \
        -DSEC_FEATURE_TAPI_ENABLE=${SEC_FEATURE_TAPI_ENABLE} \
	-DFEATURE_MULTI_WIN_NAV_ENABLE=${FEATURE_MULTI_WIN_NAV_ENABLE} \
        -DCOMPILE_COMMANDS=%{compile_commands} \
        -DUNITTEST=%{unittest} \
        -DTIZEN_WAYLAND_BACKEND=%{tizen_wayland_backend}

VERBOSE=1 make %{?jobs:-j%jobs} \
2>&1 | sed \
-e 's%^.*: error: .*$%\x1b[37;41m&\x1b[m%' \
-e 's%^.*: warning: .*$%\x1b[30;43m&\x1b[m%'
export LD_LIBRARY_PATH=/emul/ia32-linux/lib:/emul/ia32-linux/usr/lib:$LD_LIBRARY_PATH
export CTEST_OUTPUT_ON_FAILURE=1
make test
%endif

%install
rm -rf %{buildroot}
%if "%{profile}" == "tv"
mkdir -p %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts
install -p -m 500 org.tizen.screen-reader.sh %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts/org.tizen.screen-reader.sh
%endif

# For build optimization for mobile/wearable
# In the unified build, this should be always true
%if "%{?profile}"!="mobile" && "%{?profile}"!="wearable"
_screen_reader_builddir=$(pwd)
cd build_no_tapi
%make_install
cd "$_screen_reader_builddir"
mv %{buildroot}%{AppDir}/bin/screen-reader %{buildroot}%{AppDir}/bin/screen-reader.no_tapi
%endif

# For build optimization for TV
# In the unified build, this should be always true
%if "%{profile}" != "tv"
%make_install
%endif

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest org.tizen.screen-reader.manifest
# For build optimization for TV
# In the unified build, this should be always true
%if "%{profile}" != "tv"
%{AppDir}/bin/screen-reader
%endif
%{AppDir}/res/sounds/*
%{AppDir}/res/locale/*/LC_MESSAGES/*
%{DataDir}/packages/%{name}.xml
%if "%{profile}" == "tv"
%{_datadir}/upgrade/vd_scripts/additional_scripts/org.tizen.screen-reader.sh
%endif

# For build optimization for mobile/wearable
# In the unified build, this should be always true
%if "%{?profile}"!="mobile" && "%{?profile}"!="wearable"
%post extension-no-tapi
ln -sf screen-reader.no_tapi %{AppDir}/bin/screen-reader
%preun extension-no-tapi
echo "You need to reinstall %{name} after uninstalling this if you are not uninstalling %{name} as well."
%files extension-no-tapi
%{AppDir}/bin/screen-reader.no_tapi
%endif

%if %{unittest}
%files unittests
%{AppDir}/include/*
%{AppDir}/lib/*
%{AppDir}/bin/test*

%post unittests
/sbin/ldconfig
%endif

