Name:           libds-tizen
Version:        0.1.20
Release:        0
Summary:        Wayland Compositor Library for Tizen
License:        MIT
URL:            http://www.tizen.org/
Source:         %name-%version.tar.xz
Source1001:     %name.manifest

BuildRequires:  meson
BuildRequires:  pkgconfig(libds)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(tizen-extension-server)
BuildRequires:  pkgconfig(tizen-extension-client)
BuildRequires:  pkgconfig(tizen-launch-server)
BuildRequires:  pkgconfig(tizen-launch-client)
BuildRequires:  pkgconfig(text-server)
BuildRequires:  pkgconfig(text-client)
BuildRequires:  pkgconfig(input-method-server)
BuildRequires:  pkgconfig(input-method-client)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(xkbcommon)

BuildRequires:  pkgconfig(libtdm)
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(wayland-tbm-server)
BuildRequires:  pkgconfig(wayland-tbm-client)
BuildRequires:  pkgconfig(tizen-dpms-server)
BuildRequires:  pkgconfig(tizen-dpms-client)
BuildRequires:  pkgconfig(tizen-surface-server)
BuildRequires:  pkgconfig(tizen-surface-client)
BuildRequires:  pkgconfig(tizen-hwc-server)
BuildRequires:  pkgconfig(tizen-hwc-client)
BuildRequires:  pkgconfig(tizen-remote-surface-server)
BuildRequires:  pkgconfig(tizen-remote-surface-client)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-pid)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(scaler-server)
BuildRequires:  pkgconfig(scaler-client)
BuildRequires:  pkgconfig(xdg-shell-unstable-v6-server)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(wtz-blender-server)
BuildRequires:  pkgconfig(wtz-blur-server)
BuildRequires:  pkgconfig(wtz-shell-server)
BuildRequires:  pkgconfig(wtz-shell-client)
BuildRequires:  pkgconfig(wtz-screen-server)
BuildRequires:  pkgconfig(wtz-screen-client)
BuildRequires:  pkgconfig(linux-explicit-synchronization-unstable-v1-server)
BuildRequires:  pkgconfig(thorvg)
BuildRequires:  pkgconfig(egl)

%description
Wayland Compositor Library for Tizen

## libds-tizen (main library: all features are included in libds-tizen.so)
%package devel
Summary:    Wayland Compositor Library for Tizen
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development package of Wayland Compositor Library for Tizen

## libds-tizen-allocator-tbm (separate: pluggable allocator)
%package allocator-tbm
Summary: Allocator Library with TBM
Group:   Development/Libraries

%description allocator-tbm
Allocator Library with TBM

%package allocator-tbm-devel
Summary: TBM Allocator Development package
Group:   Development/Libraries
Requires:   %{name}-allocator-tbm = %{version}-%{release}
Requires:   %{name}-devel = %{version}-%{release}

%description allocator-tbm-devel
TBM Allocator Development package

## libds-tizen-backend-tdm (separate: pluggable ds backend)
%package backend-tdm
Summary: TDM Backend Library for libds-tizen
Group:   Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-allocator-tbm = %{version}-%{release}

%description backend-tdm
TDM Backend Library for libds-tizen

%package backend-tdm-devel
Summary: TDM Backend Development package
Group:   Development/Libraries
Requires:   %{name}-backend-tdm = %{version}-%{release}
Requires:   %{name}-devel = %{version}-%{release}

%description backend-tdm-devel
TDM Backend Development package

%prep
%setup -q
cp %{SOURCE1001} .

%build
meson setup \
    --prefix /usr \
    --libdir %{_libdir} \
    --bindir %{_bindir} \
    builddir \
    -Dkeylayout_dir="%{TZ_SYS_RO_SHARE}/X11/xkb/tizen_key_layout.txt"
ninja -C builddir all

%install
export DESTDIR=%{buildroot}
ninja -C builddir install

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libds-tizen.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_includedir}/libds-tizen/*.h
%dir %{_includedir}/libds-tizen/allocator
%dir %{_includedir}/libds-tizen/backend
%dir %{_includedir}/libds-tizen/types
%{_includedir}/libds-tizen/types/*
%{_libdir}/pkgconfig/libds-tizen.pc
%{_libdir}/libds-tizen.so
%{_bindir}/libds-tizen-*-tests
%exclude %{_bindir}/libds-tizen-allocator-tbm-tests
%{_bindir}/video-punch-client
%{_bindir}/ds-simple-dpms
%{_bindir}/input-generator

%files allocator-tbm
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libds-tizen-allocator-tbm.so.*

%files allocator-tbm-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_includedir}/libds-tizen/allocator/tbm.h
%{_libdir}/pkgconfig/libds-tizen-allocator-tbm.pc
%{_libdir}/libds-tizen-allocator-tbm.so
%{_bindir}/libds-tizen-allocator-tbm-tests

%files backend-tdm
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libds-tizen-backend-tdm.so.*

%files backend-tdm-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
%{_includedir}/libds-tizen/backend/tdm.h
%{_includedir}/libds-tizen/backend/tdm_output_hwc.h
%{_libdir}/pkgconfig/libds-tizen-backend-tdm.pc
%{_libdir}/libds-tizen-backend-tdm.so
%{_bindir}/tdm-backend
%{_bindir}/tinyds-tdm
%{_bindir}/tinyds-tdm2
%{_bindir}/tinyds-render-test
%{_bindir}/launch_anim.svg
%{_bindir}/launch_anim.json
%{_bindir}/sparkles.json
%{_bindir}/ds-simple-tbm
