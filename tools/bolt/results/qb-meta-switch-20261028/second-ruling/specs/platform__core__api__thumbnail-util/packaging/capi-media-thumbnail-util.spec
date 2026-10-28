Name:       capi-media-thumbnail-util
Summary:    A media thumbnail util library in Tizen Native API
Version:    0.2.3
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(media-thumbnail)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A media thumbnail util library in Tizen Native API.

%package devel
Summary:  A media thumbnail util library in Tizen Native API (Development)
Group:    Multimedia/Development
Requires: %{name} = %{version}-%{release}

%description devel
A media thumbnail util library in Tizen Native API. (Development files included)

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Thumbnail Util library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a thumbnail util in Tizen native API
%endif

%prep
%setup -q


%build
export CFLAGS="$CFLAGS -Wextra -Wno-array-bounds"
export CFLAGS="$CFLAGS -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow"
export CFLAGS="$CFLAGS -Wwrite-strings -Wswitch-default"
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
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
%manifest capi-media-thumbnail-util.manifest
%{_libdir}/libcapi-media-thumbnail-util.so.*
# Unversioned name stays in the runtime package: releases before 0.2.2 had
# SONAME libcapi-media-thumbnail-util.so, so binaries linked against them
# (TCT, apps built with older rootstraps) resolve this name at load time.
%{_libdir}/libcapi-media-thumbnail-util.so
%license LICENSE.APLv2.0

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/capi-media-thumbnail-util.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
