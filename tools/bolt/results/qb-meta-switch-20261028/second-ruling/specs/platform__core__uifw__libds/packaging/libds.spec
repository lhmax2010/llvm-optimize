# One GBS build emits two runtimes and shared development/xdg-shell packages.

Name:           libds
Version:        0.1.31
Release:        0
Summary:        Wayland Compositor Library
Conflicts:      libds-pixman
License:        MIT
URL:            http://www.tizen.org/
Source:         %{name}-%{version}.tar.xz
Source1001:     libds.manifest

BuildRequires:  meson
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(gmock)
# TBM is a core platform buffer dependency in both renderer variants.
BuildRequires:  pkgconfig(libtbm)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gles20)
BuildRequires:  pkgconfig(gbm)

%description
Wayland Compositor Library

%package devel
Summary:    Common development files for either libds runtime
Requires:   %{name} = %{version}-%{release}
# Prefer the default runtime when GBS expands pkgconfig(libds) BuildRequires.
Recommends: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development package of Wayland Compositor Library

%package xdg-shell-v6
Summary: Wayland Compositor Library for xdg-shell-v6
Recommends: %{name}%{?_isa} = %{version}-%{release}

%description xdg-shell-v6
Wayland Compositor Library for xdg-shell-v6

%package xdg-shell-v6-devel
Summary: Wayland Compositor Development package for xdg-shell-v6
Requires: %{name}-xdg-shell-v6 = %{version}-%{release}
Recommends: %{name}%{?_isa} = %{version}-%{release}

%description xdg-shell-v6-devel
Wayland Compositor Development package for xdg-shell-v6

%package pixman
Summary:    Wayland Compositor Library with the pixman renderer only
# Avoid matching our own compatibility Provide during upgrades/reinstalls.
Conflicts:  libds%{?_isa}
Provides:   libds = %{version}-%{release}
RemovePathPostfixes: .pixman

%description pixman
Software-only Wayland Compositor Library, without EGL, GLES or GBM.

%package tests
Summary:    Common tests for either libds runtime
Requires:   %{name} = %{version}-%{release}
Recommends: %{name}%{?_isa} = %{version}-%{release}

%description tests
Common test executables for either runtime, without GPU library dependencies.
GLES-specific tests are skipped when the loaded libds does not support GLES.

%prep
%setup -q
cp %{SOURCE1001} libds.manifest

%build
# GPU SDKs are installed by GBS up front, but are never probed or used by
# the first build. Explicit renderer sets prevent accidental autodetection.
meson setup --prefix /usr --libdir %{_libdir} --bindir %{_bindir} \
    -Dtests=true -Drenderers=pixman build-pixman
ninja -C build-pixman all
meson setup --prefix /usr --libdir %{_libdir} --bindir %{_bindir} \
    -Dtests=true -Drenderers=gles,pixman build-gles
ninja -C build-gles all

%install
# Preserve both variants until RPM creates all payloads. Only temporary
# on-disk names have .pixman; RemovePathPostfixes restores installed names.
DESTDIR="$PWD/stage-gles" ninja -C build-gles install
python3 packaging/stage-renderer-rpm.py --root "$PWD/stage-gles" \
    --buildroot %{buildroot} --libdir %{_libdir} --tests --output-prefix normal
DESTDIR="$PWD/stage-pixman" ninja -C build-pixman install
python3 packaging/stage-renderer-rpm.py --root "$PWD/stage-pixman" \
    --buildroot %{buildroot} --libdir %{_libdir} --suffix .pixman \
    --common --output-prefix pixman

%check
export XDG_RUNTIME_DIR="$PWD/test-runtime"
mkdir -p "$XDG_RUNTIME_DIR"
chmod 0700 "$XDG_RUNTIME_DIR"
# Software rendering, backend selection and ABI contracts need no GPU.
LIBDS_TEST_EXPECT_BACKENDS=4 ./build-pixman/tests/libds-tests --gtest_filter=-RendererTest.*
./build-pixman/tests/libds-profile-thread-id-tests
./build-pixman/tests/libds-profile-phase-tests
# Keep real EGL/TBM device suites installed for target validation.
LIBDS_TEST_EXPECT_BACKENDS=6 ./build-gles/tests/libds-tests --gtest_filter=-RendererTest.*:ClipMaskTest.*:ProfileRenderTest.*
./build-gles/tests/libds-profile-gpu-tests
./build-gles/tests/libds-profile-thread-id-tests
./build-gles/tests/libds-profile-phase-tests

# Run the exact shared test binaries against the alternative runtime as well.
export LD_LIBRARY_PATH="$PWD/build-pixman/src"
LIBDS_TEST_EXPECT_BACKENDS=4 ./build-gles/tests/libds-tests --gtest_filter=-RendererTest.*
./build-gles/tests/libds-profile-gpu-tests
./build-gles/tests/libds-profile-thread-id-tests
./build-gles/tests/libds-profile-phase-tests

%files  -f normal-runtime.files
%manifest libds.manifest
%defattr(-,root,root,-)
%license LICENSE

%files devel -f pixman-devel.files
%manifest libds.manifest
%defattr(-,root,root,-)
%license LICENSE

%files xdg-shell-v6 -f pixman-xdg.files
%manifest libds.manifest
%defattr(-,root,root,-)
%license LICENSE

%files xdg-shell-v6-devel -f pixman-xdg-devel.files
%manifest libds.manifest
%defattr(-,root,root,-)
%license LICENSE


%files pixman -f pixman-runtime.files
%manifest libds.manifest
%defattr(-,root,root,-)
%license LICENSE

%files tests -f normal-tests.files
%manifest libds.manifest
%defattr(-,root,root,-)
%license LICENSE
