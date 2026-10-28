Name:           capi-media-audio-io
Summary:        An Audio Input & Audio Output library in Tizen Native API
Version:        0.9.6
Release:        0
Group:          Multimedia/API
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
Source1001:     capi-media-audio-io.manifest
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libaudio-effect)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(mm-audio-conf)
BuildRequires:  pkgconfig(mm-workloop)
BuildRequires:  pkgconfig(mm-msgbox)

%description
An Audio Input & Audio Output library in Tizen Native API

%package devel
Summary:  An Audio Input & Audio Output library in Tizen Native API (Development)
Group:    Multimedia/Development
Requires: %{name} = %{version}-%{release}

%description devel
An Audio Input & Audio Output library in Tizen Native API (DEV)

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage files
Group: Development/Multimedia

%description gcov
Collection of files related to line coverage using gcov.
%endif

%package tool
Summary:  An Audio Input & Audio Output library in Tizen Native API (Tool)
Group:    Multimedia/Development
Requires: %{name} = %{version}-%{release}

%description tool
An Audio Input & Audio Output library in Tizen Native API (Tool)

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%{meson} \
%if "%{tizen_profile_name}" == "tv"
    -Dproduct_tv=true \
%endif
    -Dversion=%{version}
%{meson_build}

%install
%{meson_install}

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
%license LICENSE
%{_libdir}/libcapi-media-audio-io.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/media/audio_io.h
%if "%{tizen_profile_name}" == "tv"
%exclude %{_includedir}/media/audio_io_internal.h
%else
%{_includedir}/media/audio_io_internal.h
%endif
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-audio-io.so

%files tool
%manifest %{name}.manifest
%{_prefix}/bin/*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
