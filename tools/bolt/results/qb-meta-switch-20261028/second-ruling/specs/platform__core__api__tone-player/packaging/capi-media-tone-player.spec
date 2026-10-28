Name:       capi-media-tone-player
Summary:    A tone player library in Tizen C API
Version:    0.2.13
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-media-tone-player.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(mm-sound)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(gio-2.0)

%description
A tone player library in Tizen C API.


%package devel
Summary:  A tone player library in Tizen C API (Development)
Group:    Development/Multimedia
Requires: %{name} = %{version}-%{release}

%description devel
%devel_desc

%package tools
Summary:  Tone player test tools
Group:    Development/Tools
Requires: %{name} = %{version}-%{release}

%description tools
Test tools for tone player library.

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
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER}


make %{?jobs:-j%jobs}

%install
%make_install

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
%license LICENSE
%{_libdir}/libcapi-media-tone-player.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-tone-player.so

%files tools
%manifest %{name}.manifest
%{_bindir}/tone_player_test

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
