Name:       capi-media-image-util
Summary:    A Image Utility library in Tizen Native API
Version:    0.4.7
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-media-image-util.manifest
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(mmutil-common)
BuildRequires:  pkgconfig(mmutil-jpeg)
BuildRequires:  pkgconfig(mmutil-imgp)
BuildRequires:  pkgconfig(mmutil-gif)
BuildRequires:  pkgconfig(mmutil-magick)
BuildRequires:  pkgconfig(mmutil-anim)
BuildRequires:  pkgconfig(mmutil-heif)
BuildRequires:  pkgconfig(mmutil-jxl)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  cmake

%description
A Image Utility library in Tizen Native API package

%package devel
Summary:    A Image Utility library in Tizen Native API (Development)
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description devel
A Image Utility library in Tizen Native API (Development) package

%package tool
Summary:    Image Utility tools
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description tool
Image Utility Library - Tools.

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Image Utility library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a image utility library in Tizen native API
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="${CFLAGS} -Wextra -Wno-array-bounds -D_FORTIFY_SOURCE=2"
export CFLAGS="${CFLAGS} -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow"
export CFLAGS="${CFLAGS} -Wwrite-strings -Wswitch-default"
export CFLAGS="${CFLAGS} -DGIF_ENCODER_V2"
export CFLAGS="${CFLAGS} -DPATH_LIBDIR=\\\"%{_libdir}\\\""
%if 0%{?gcov:1}
export CFLAGS="${CFLAGS} -fprofile-arcs -ftest-coverage"
export CXXFLAGS="${CXXFLAGS} -fprofile-arcs -ftest-coverage"
export FFLAGS="${FFLAGS} -fprofile-arcs -ftest-coverage"
export LDFLAGS="${LDFLAGS} -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \

%__make %{?jobs:-j%jobs}

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
%manifest %{name}.manifest
%license LICENSE.APLv2.0
%{_libdir}/lib*.so.*

%files devel
%manifest %{name}.manifest
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/media/*.h

%files tool
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
