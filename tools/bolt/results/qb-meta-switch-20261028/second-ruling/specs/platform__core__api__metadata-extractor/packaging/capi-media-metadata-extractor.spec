Name:       capi-media-metadata-extractor
Summary:    A media metadata extractor library in Tizen Native API
Version:    0.2.21
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-media-metadata-extractor.manifest
Requires:   libmm-fileinfo >= 1.1.11
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
# pkgconfig(mm-fileinfo) is provided without a usable version; the floor
# for mm_file_plugin_ref() and the _simple() memory parsers goes on the package
BuildRequires:  libmm-fileinfo-devel >= 1.1.11
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(glib-2.0)

%description
A media metadata extractor library in Tizen Native API.

%package devel
Summary:  A media metadata extractor library in Tizen Native API (Development)
Group:    Multimedia/Development
Requires: %{name} = %{version}-%{release}

%description devel
A media metadata extractor library in Tizen Native API. (Development files included)

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Metadata Extractor library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a metadata extractor library in Tizen native API
%endif

%prep
%setup -q
cp %{SOURCE1001} .


%build
export CFLAGS="$CFLAGS -Wextra -Wshadow -Wwrite-strings -Wswitch-default"
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
%manifest %{name}.manifest
%{_libdir}/libcapi-media-metadata-extractor.so
%license LICENSE.APLv2.0

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/capi-media-metadata-extractor.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
