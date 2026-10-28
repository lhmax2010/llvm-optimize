Name:       capi-content-media-content
Summary:    A Media content library in Tizen Native API
Version:    0.6.21
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-content-media-content.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libmedia-service)
BuildRequires:  pkgconfig(libmedia-utils)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(sqlite3)

%description
A Media content library in Tizen Native API.

%package devel
Summary:  A Media content library in Tizen Native API (Development)
Group:    Multimedia/Development
Requires: %{name} = %{version}-%{release}

%description devel
A Media content library in Tizen Native API. (Development file included)
%devel_desc

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Media Content library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a media content library in Tizen native API
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if "%{tizen_profile_name}" == "tv"
 -DTIZEN_PRODUCT_TV=YES \
%else
 -DTIZEN_PRODUCT_TV=NO \
%endif

%__make %{?jobs:-j%jobs}

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
%{_libdir}/libcapi-content-media-content.so.*
#License
%license LICENSE.APLv2.0

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files devel
%manifest %{name}.manifest
%{_includedir}/media-content/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-content-media-content.so
