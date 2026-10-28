Name:       tizen-core-wl
Summary:    Tizen core wayland library
Version:    0.2.3
Release:    0
Group:      Graphics System / Display Server
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(tizen-core) >= 0.4.2
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(wtz-screen-client)
BuildRequires:  pkgconfig(wtz-shell-client)
BuildRequires:  pkgconfig(wtz-blur-client)
BuildRequires:  pkgconfig(pointer-warp-v1-client)

BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gles20)
BuildRequires:  pkgconfig(wayland-egl-tizen)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-resource)
BuildRequires:  pkgconfig(wayland-tbm-client)
BuildRequires:  pkgconfig(tizen-launch-client)
BuildRequires:  pkgconfig(tizen-remote-surface-client)
BuildRequires:  pkgconfig(tizen-policy-ext-client)
BuildRequires:  pkgconfig(relative-pointer-unstable-v1-client)
BuildRequires:  pkgconfig(pointer-constraints-unstable-v1-client)
BuildRequires:  pkgconfig(wtz-blur-client)
BuildRequires:  pkgconfig(wtz-foreign-client)
BuildRequires:  pkgconfig(wtz-video-shell-client)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  wayland-protocols

Requires:       libwayland-extension-client
Requires:       libwayland-egl-tizen
Requires:       tizen-core >= 0.4.2

%description
Tizen core wayland library package.

%package devel
Summary:  Tizen core wayland library (Development)
Group:    Graphics System/Display Management

%description devel
Tizen core wayland library (Development) package.

# for samples
%if "%{disable_samples}" != "1"
%package samples
Summary:  Tizen core wayland samples package
Group:    Graphics System/Display Management

%description samples
Tizen core wayland samples package.
%endif

%package unittests
Summary:  Tizen core wayland unittest package
Group:    Graphics System/Display Management

%description unittests
Tizen core wayland unittests package.

%prep
%setup -q

%build
%if "%{disable_samples}" != "1"
%meson -Ddisable_samples=False
%else
%meson -Ddisable_samples=True
%endif
%meson_build

%install
%meson_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%attr(0644,root,root) %{_libdir}/libtizen-core-wl.so.*
%license LICENSE

%files devel
%{_includedir}/tizen-core-wl/*.h
%{_libdir}/pkgconfig/tizen-core-wl.pc
%{_libdir}/libtizen-core-wl.so

# for samples
%if "%{disable_samples}" != "1"
%files samples
%attr(-,root,root) %{_bindir}/sample-tcore-wl
%attr(-,root,root) %{_bindir}/sample-gl-simple-egl
%attr(-,root,root) %{_bindir}/sample-tcore-wl-blur
%attr(-,root,root) %{_bindir}/sample-tcore-wl-screen
%attr(-,root,root) %{_bindir}/sample-tcore-wl-data
%attr(-,root,root) %{_bindir}/sample-tcore-lock
%attr(-,root,root) %{_bindir}/sample-tcore-wl-screenshot
%attr(-,root,root) %{_bindir}/sample-tcore-gesture
%attr(-,root,root) %{_bindir}/sample-tcore-inputgen
%attr(-,root,root) %{_bindir}/sample-tcore-surface-drag
%attr(-,root,root) %{_bindir}/sample-tcore-thread
%attr(-,root,root) %{_bindir}/sample-tcore-wl-layout
%attr(-,root,root) %{_bindir}/sample-tcore-cursor-shape
%endif

%files unittests
%attr(-,root,root) %{_bindir}/tizen_core_wl_unittests
%attr(-,root,root) %{_bindir}/tizen_core_wl_integtests
