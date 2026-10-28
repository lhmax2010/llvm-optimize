%bcond_with wayland
Name:       e-mod-tizen-wl-textinput
Summary:    The Enlightenment WM Wayland Text Input Module for Tizen
Version:    0.11.33
Release:    1
Group:      Graphics & UI Framework/Other
License:    BSD-2-Clause
Source0:    %{name}-%{version}.tar.bz2
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(text-server)
BuildRequires: pkgconfig(input-method-server)
BuildRequires: pkgconfig(enlightenment)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtest)
BuildRequires: gcc-c++
BuildRequires: meson
BuildRequires: ninja
%if !%{with wayland}
ExclusiveArch:
%endif

%description
The Enlightenment WM Wayland Text Input Module for Tizen

%prep
%setup -q -n %{name}-%{version}

%build
CFLAGS="$CFLAGS -fvisibility=hidden -Werror"
CXXFLAGS="$CXXFLAGS -fvisibility=hidden -fvisibility-inlines-hidden -Werror"

meson setup build \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  -Dtests=true
ninja -C build %{?_smp_mflags}

%check
meson test -C build --no-rebuild -v

%install
DESTDIR=%{buildroot} ninja -C build install

%files
%defattr(-,root,root,-)
%{_libdir}/enlightenment/modules/e-mod-tizen-wl-textinput
%license COPYING

%define _unpackaged_files_terminate_build 0
