Name:           pipewire-modules-tizen
Summary:        PipeWire Tizen Modules
Version:        0.9.28
Release:        0
License:        MIT
Group:          Multimedia/Audio
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.manifest
BuildRequires:  pkgconfig(libpipewire-0.3) >= 1.6.0
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(hal-api-audio)
BuildRequires:  libmm-sound-devel >= 0.21.2
Requires:       libmm-sound >= 0.21.2
%if "%{tizen_profile_name}" == "tv"
BuildRequires:  pkgconfig(vconf)
%endif
BuildRequires:  pkgconfig(libpipewire-tizen-privilege)
BuildRequires:  pkgconfig(libpipewire-tizen-hal-utils)
BuildRequires:  meson >= 0.59.0

# Disable Tizen gcc-force-options (-Werror -Wshadow -Wmissing-field-initializers)
# which conflicts with third-party code (stb_vorbis) and SPA header macros.
%global gcc_warning_disable 1

%description
PipeWire Tizen Modules is a collection of Tizen-specific PipeWire modules.

%package tools
Summary: Target screening utilities for the Tizen PipeWire daemon
Requires: %{name} = %{version}-%{release}

%description tools
pw-stream-matrix drives channel/quantum stream matrices and tizen-service-cli
sends tizen-service (volume, ducking, wav-player, device) and keytone requests
without the client CAPI stack. Used for regression screening on targets
without TCT.

%prep
%setup -q

%build
# Size/dead-code trim: minsize gives -Os; add per-function/data sections so the
# linker can gc unreferenced code, and drop unused DT_NEEDED with --as-needed.
export CFLAGS="${CFLAGS} -ffunction-sections -fdata-sections"
export CXXFLAGS="${CXXFLAGS} -ffunction-sections -fdata-sections"
export LDFLAGS="${LDFLAGS} -Wl,--gc-sections -Wl,--as-needed"

%meson \
    --buildtype=minsize \
    -Dtizen=true \
    -Dtizen-hal=bypass \
    -Dhal-libdir=%{_hal_libdir} \
    -Dtizen-privilege=true \
    -Dtools=true \
%if "%{tizen_profile_name}" == "tv"
    -Dvolume-db=vconf \
%endif
    %{nil}
%meson_build

%install
%meson_install

# Copy manifest file to build directory
install -m 0644 %SOURCE1 .

%post
mkdir -p /opt/data/media-config
chown multimedia_fw:multimedia_fw /opt/data/media-config || :
chmod 775 /opt/data/media-config || :

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/pipewire-0.3/*.so*
%{_libdir}/spa-0.2/tizen/*

%files tools
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/pw-stream-matrix
%{_bindir}/tizen-service-cli
%{_bindir}/pw-record-permission-probe
