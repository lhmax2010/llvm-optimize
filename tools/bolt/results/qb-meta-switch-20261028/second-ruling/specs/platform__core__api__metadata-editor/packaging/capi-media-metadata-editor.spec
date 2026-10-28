Name:       capi-media-metadata-editor
Summary:    A metadata editor library in Tizen Native API
Version:    0.2.8
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  pkgconfig(glib-2.0)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A media metadata editor library in Tizen Native API.

%package devel
Summary:  A metadata editor library in Tizen Native API (Development)
Group:    Multimedia/Development
Requires: %{name} = %{version}-%{release}

%description devel
A media metadata editor library in Tizen Native API. (Development files included)

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Metadata Editor library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a metadata editor library in Tizen native API
%endif

%prep
%setup -q

%build
export CFLAGS+=" -Wextra -Wno-array-bounds"
export CFLAGS+=" -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow"
export CFLAGS+=" -Wwrite-strings -Wswitch-default"
CXXFLAGS=${CXXFLAGS/-fgnu89-inline/}
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
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
%manifest capi-media-metadata-editor.manifest
%{_libdir}/libcapi-media-metadata-editor.so
%license LICENSE.APLv2.0

%files devel
%{_includedir}/metadata-editor/*.h
%{_libdir}/pkgconfig/capi-media-metadata-editor.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
