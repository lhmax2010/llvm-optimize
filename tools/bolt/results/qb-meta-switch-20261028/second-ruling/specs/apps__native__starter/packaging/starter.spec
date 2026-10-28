%bcond_with wayland
%define __usrdir /usr/lib/systemd/user

Name:		starter
Summary:	This is a core application
Version:	0.5.54
Release:	1
Group:		Applications/Core Applications
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}_common.service
Source2:	%{name}.path

BuildRequires:  cmake
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(capi-system-media-key)
BuildRequires:  pkgconfig(db-util)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(syspopup-caller)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-system-system-settings)
BuildRequires:	pkgconfig(pkgmgr-info)
BuildRequires:	pkgconfig(tizen-core-wl)
BuildRequires:  gettext
BuildRequires:  gettext-tools
Requires(post): /usr/bin/vconftool
Requires:	%{name}-compat = %{version}-%{release}
Recommends:	%{name}-profile_common = %{version}-%{release}

%if !%{with wayland}
BuildRequires:  pkgconfig(utilX)
%endif

%description
This is for managing life-cycle of core applications.

%package profile_common
Summary:	Starter binary for common profile
Provides:	%{name}-compat = %{version}-%{release}
Provides:	%{name}-profile_tv = %{version}-%{release}
Provides:	%{name}-profile_ivi = %{version}-%{release}
%description profile_common
Starter has different build options and source codes for each profile.
This is for common/tv/ivi.

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

%ifarch %{arm}
export CFLAGS="$CFLAGS -DTIZEN_ARCH_ARM"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ARCH_ARM"
%else
# TODO: x86/64 != EMULATOR. Please fix it with consulting from SDK (changseok oh)
export CFLAGS="$CFLAGS -DTIZEN_ARCH_EMULATOR"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ARHC_EMULATOR"
%endif

%ifarch aarch64
export CFLAGS="$CFLAGS -DTIZEN_ARCH_ARM64"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ARCH_ARM64"
%endif
%if %{with wayland}
export WAYLAND_SUPPORT=On
export X11_SUPPORT=Off
export CFLAGS+=" -DEFL_BETA_API_SUPPORT"
%else
export WAYLAND_SUPPORT=Off
export X11_SUPPORT=On
%endif

export CFLAGS_COMMON="$CFLAGS"
export CXXFLAGS_COMMON="$CXXFLAGS"

# common
export CFLAGS="$CFLAGS_COMMON -DTIZEN_PROFILE_COMMON"
export CXXFLAGS="$CXXFLAGS_COMMON -DTIZEN_PROFILE_COMMON"
mkdir -p build_common
pushd build_common
cmake .. -DTIZEN_PROFILE_NAME=COMMON -DCMAKE_INSTALL_PREFIX=%{_prefix} -DWAYLAND_SUPPORT=${WAYLAND_SUPPORT} -DX11_SUPPORT=${X11_SUPPORT}
make
popd

%install
pushd build_common
%make_install
popd

mkdir -p %{buildroot}%{__usrdir}/default.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{__usrdir}/starter.service.common
# .common is to be renamed by %post script.
install -m 0644 %SOURCE2 %{buildroot}%{__usrdir}/starter.path
ln -s ../starter.path %{buildroot}%{__usrdir}/default.target.wants/starter.path

%find_lang %{name}

%post
sync

%post profile_common
mv %{__usrdir}/starter.service.common %{__usrdir}/starter.service
%preun profile_common
mv %{__usrdir}/starter.service %{__usrdir}/starter.service.common


%files -f %{name}.lang
%manifest starter.manifest
%defattr(-,root,root,-)
%license LICENSE

%files profile_common
%{_bindir}/starter
%{__usrdir}/starter.path
%{__usrdir}/default.target.wants/starter.path
%{__usrdir}/starter.service.common
%manifest starter.manifest
