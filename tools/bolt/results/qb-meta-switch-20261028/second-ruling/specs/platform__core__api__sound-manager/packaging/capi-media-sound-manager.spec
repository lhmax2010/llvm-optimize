Name:       capi-media-sound-manager
Summary:    Sound Manager library
Version:    0.9.9
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Patch0:     0001-Apply-TV-product-patch.patch
BuildRequires:  meson
BuildRequires:  pkgconfig(dlog)
BuildRequires:  libmm-sound-devel
BuildRequires:  pkgconfig(capi-base-common)

# tests build option: default off; build the test suite (incl. sound_manager_leak_test)
# with `gbs build --define "build_test 1"`. Default stays 0 so normal/product builds
# don't compile/install test binaries or pull in the 'check' BuildRequires.
%{!?build_test: %define build_test 1}

%if %{build_test}
BuildRequires:  pkgconfig(check)
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A Sound Manager library in Tizen C API

%if %{build_test}
%package tools
Summary:  Sound Manager library (Tools)
Group:    Multimedia/Tools
Requires: %{name} = %{version}-%{release}

%description tools
A Sound Manager library in Tizen C API (Tools)
%endif

%package devel
Summary:  Sound Manager library (Development)
Group:    Multimedia/Development
Requires: %{name} = %{version}-%{release}

%description devel
A Sound Manager library in Tizen C API (DEV)

%devel_desc

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

%if "%{tizen_profile_name}" == "tv"
echo "tizen_product_tv"
cp %{PATCH0} .
patch -p1 < %{PATCH0}
%endif

%build
%if "%{tizen_profile_name}" == "tv"
export CFLAGS="${CFLAGS} -DTIZEN_FEATURE_TV_PROD"
%endif

export CFLAGS="${CFLAGS} -DUSE_DLOG"
export CXXFLAGS="${CXXFLAGS} -DUSE_DLOG"
%if 0%{?gcov:1}
export CFLAGS="${CFLAGS} -fprofile-arcs -ftest-coverage"
export CXXFLAGS="${CXXFLAGS} -fprofile-arcs -ftest-coverage"
export LDFLAGS="${LDFLAGS} -lgcov"
%endif

%{meson} \
            -Dversion=%{version} \
%if %{build_test}
            -Dbuild_test=true \
%else
            -Dbuild_test=false \
%endif
            %{nil}

%{meson_build}

%install
%{meson_install}

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -not -regex ".*\(internal\).*$" -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/libcapi-media-sound-manager.so*
%license LICENSE

%if %{build_test}
%files tools
%manifest %{name}.manifest
%{_bindir}/sound_manager_*
%endif

%files devel
%manifest %{name}.manifest
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-sound-manager.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
