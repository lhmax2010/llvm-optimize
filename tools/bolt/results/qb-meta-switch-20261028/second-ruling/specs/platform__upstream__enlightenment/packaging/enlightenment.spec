%define USE_GCOV 0

Name:           enlightenment
Version:        0.20.0
Release:        tz11_4.4.2
License:        BSD-2-Clause and MIT
Summary:        The Enlightenment wayland display server
Url:            http://www.enlightenment.org/
Group:          Graphics/EFL
Source0:        enlightenment-%{version}.tar.bz2
Source1002:     enlightenment.vip.conf

%define TIZEN_REL_VERSION 1

# for the new view_client development
%define new_view_client false

BuildRequires:  meson
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(wayland-server)
%if 0%{?enable_pixmap_lifetime_probe}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(xdg-shell-unstable-v6-client)
BuildRequires:  pkgconfig(wayland-tbm-client)
%endif
BuildRequires:  pkgconfig(xdg-shell-server)
BuildRequires:  pkgconfig(xdg-shell-unstable-v6-server)
BuildRequires:  pkgconfig(scaler-server)
BuildRequires:  pkgconfig(screenshooter-server)
BuildRequires:  pkgconfig(screenshooter-client)
BuildRequires:  pkgconfig(tizen-extension-server)
BuildRequires:  pkgconfig(tizen-launch-server)
BuildRequires:  pkgconfig(wayland-tbm-server)
BuildRequires:  pkgconfig(tizen-remote-surface-server)
BuildRequires:  pkgconfig(tizen-surface-server)
BuildRequires:  pkgconfig(tizen-dpms-server)
BuildRequires:  pkgconfig(libtdm)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  pkgconfig(tzsh-server)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-creds-pid)
BuildRequires:  pkgconfig(libsmack)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(presentation-time-server)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(linux-explicit-synchronization-unstable-v1-server)
BuildRequires:  pkgconfig(tizen-hwc-server)
BuildRequires:  pkgconfig(wtz-foreign-server)
BuildRequires:  pkgconfig(wtz-shell-server)
BuildRequires:  pkgconfig(wtz-video-shell-server)
BuildRequires:  pkgconfig(wtz-test-server)
BuildRequires:  pkgconfig(pointer-constraints-unstable-v1-server)
BuildRequires:  pkgconfig(relative-pointer-unstable-v1-server)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(single-pixel-buffer-v1-server)
BuildRequires:  pkgconfig(pointer-warp-v1-server)
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(cursor-shape-v1-server)
BuildRequires:  pkgconfig(tizen-core)
Requires:       libwayland-extension-server

# for gtest/gmock
BuildRequires:  pkgconfig(gmock)

BuildRequires:  pkgconfig(libds)
BuildRequires:  pkgconfig(libds-xdg-shell-v6)
BuildRequires:  pkgconfig(libds-tizen) >= 0.1.5

%description
Enlightenment is a window manager.

%package devel
Summary:        Development components for the enlightenment package
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       pkgconfig(tizen-extension-server)

%description devel
Development files for enlightenment

%if ! 0%{?disable_tests}
%package tests
Summary: enlightenment tests package
Group: System/Libraries

%description tests
Tests binary for internal API in enlightenment

%package integ-tests
Summary: enlightenment integration tests package
Group: System/Libraries
Requires: enlightenment-tests

%description integ-tests
Integration tests binary for enlightenment with xkbcommon dependency
%endif

%package isu
Summary: ISU package for enlightenment
Group:   Graphics/EFL

%description isu
Configuration files to generate the ISU (Individual Service Upgrade) package

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="$CFLAGS -Wall -Werror -Wno-unused-value -Wno-stringop-overflow -Wno-stringop-truncation -Wno-error=deprecated-declarations"
%{?_toolchain:
%if %{toolchain_is clang}
CFLAGS=$(echo "$CFLAGS" | sed 's/-Wno-stringop-overflow//')
CFLAGS=$(echo "$CFLAGS" | sed 's/-Wno-stringop-truncation//')
CFLAGS="$CFLAGS -Wno-unused-function -Wno-typedef-redefinition -Wno-error=implicit-enum-enum-cast -Wno-error=incompatible-pointer-types-discards-qualifiers"
%endif
}

%if "%{tizen_profile_name}" != "tv"
CFLAGS="$CFLAGS -DUSE_E_APPINFO"
LDFLAGS="$LDFLAGS "
%endif
%if "%{USE_GCOV}" == "1"
CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV "
LDFLAGS="$LDFLAGS -lgcov "
%endif

%if 0%{?enable_pixmap_lifetime_probe}
pixmap_probe_option=true
%else
pixmap_probe_option=false
%endif

meson setup \
    builddir --reconfigure \
    --prefix /usr \
    --libdir %{_libdir} \
    --bindir %{_bindir} \
    %{?disable_tests:-Dtests=false}%{!?disable_tests:-Dtests=true} \
    -Dpixmap_lifetime_probe="$pixmap_probe_option"

%install
export DESTDIR=%{buildroot}
ninja -C builddir install
ln -sf %{_bindir}/enlightenment_info %{buildroot}%{_bindir}/winfo

mkdir -p %{buildroot}/%{_sysconfdir}/resourced/vip-process.d
cp %{SOURCE1002} %{buildroot}/%{_sysconfdir}/resourced/vip-process.d/enlightenment.conf

%if ! 0%{?disable_tests}
%check
%{buildroot}%{_bindir}/enlightenment-pixmap-lifetime-tests
%{buildroot}%{_bindir}/enlightenment-tests --gtest_filter=-EViewImageTest.Test_e_view_image_alpha_set_get:EViewImageTest.Test_e_vew_image_animated_frame_set_get:EViewImageTest.Test_e_view_image_animated_frame_count_get:EViewImageTest.Test_e_view_image_animated_frame_duration_get:EViewImageTest.Test_e_view_image_border_center_fill_set_get:EViewImageTest.Test_e_view_image_border_set_get:EViewImageTest.Test_e_view_image_colorspace_set_get:EViewImageTest.Test_e_view_image_fill_set_get:EViewImageTest.Test_e_view_image_filled_set_get:EViewImageTest.Test_e_view_image_load_size_set_get:EViewImageTest.Test_e_view_image_source_set_get:ServiceGestureLifecycle.*
%{buildroot}%{_bindir}/enlightenment-data-transfer-tests
%endif

%post
/usr/bin/chsmack %{_bindir}/enlightenment_info* -a "System::Tools"
/usr/bin/chsmack %{_bindir}/winfo* -a "System::Tools"

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING COPYING.MIT
%attr(550,root,root) %{_bindir}/enlightenment
%attr(550,root,root) %{_bindir}/enlightenment_info
%{_bindir}/winfo*
%{_libdir}/enlightenment/*
%{_datadir}/enlightenment/*
%{_sysconfdir}/resourced/vip-process.d/enlightenment.conf

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/enlightenment/*
%{_libdir}/pkgconfig/*.pc

%if ! 0%{?disable_tests}
%files tests
%defattr(-,root,root,-)
%attr(550,root,root) %{_bindir}/enlightenment-tests
%attr(550,root,root) %{_bindir}/enlightenment-data-transfer-tests

%files integ-tests
%defattr(-,root,root,-)
%attr(550,root,root) %{_bindir}/enlightenment-integ-tests
%attr(550,root,root) %{_bindir}/enlightenment-pixmap-lifetime-tests
%if 0%{?enable_pixmap_lifetime_probe}
%attr(550,root,root) %{_bindir}/enlightenment-pixmap-live-tests
%endif
%endif

%files isu
/etc/isu/enlightenment/isu.cfg
/etc/isu/enlightenment/system-services/display-manager.service
