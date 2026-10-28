Name:       capi-media-wav-player
Summary:    A wav player library in Tizen C API
Version:    0.9.2
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-media-wav-player.manifest
BuildRequires:  meson
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(mm-workloop)
Requires:       %{name}-tools = %{version}-%{release}

# tests build option
%description
A wav player library in Tizen C API.

%package tools
Summary:  A wav player test tools in Tizen C API
Group:    Development/Tools
Requires: %{name} = %{version}-%{release}

%description tools
Test tools for wav player library in Tizen C API.

%package devel
Summary:  A wav player library in Tizen C API (Development)
Group:    Development/Multimedia
Requires: %{name} = %{version}-%{release}

%description devel
Development files for wav player library in Tizen C API.

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage files
Group: Development/Multimedia

%description gcov
Collection of files related to line coverage using gcov.
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
CFLAGS="$CFLAGS -DUSE_DLOG"
CXXFLAGS="$CXXFLAGS -DUSE_DLOG"
export CFLAGS CXXFLAGS
%if 0%{?gcov:1}
CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
LDFLAGS="$LDFLAGS -lgcov"
export CFLAGS CXXFLAGS LDFLAGS
%endif

%{meson} \
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

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-media-wav-player.so.*

%files tools
%manifest %{name}.manifest
%{_bindir}/wav_player_*

%files devel
%manifest %{name}.manifest
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-wav-player.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
