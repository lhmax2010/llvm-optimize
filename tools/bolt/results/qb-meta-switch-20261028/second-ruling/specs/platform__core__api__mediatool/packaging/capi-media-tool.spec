Name:       capi-media-tool
Summary:    A Core API media tool library in Tizen Native API
Version:    1.2.4
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libtbm)
%if "%{gtests}" == "1"
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(gmock)
%endif

%description
A Core API media tool library in Tizen Native API


%package devel
Summary:  A Core API media tool library in Tizen Native API (Development)
Group:    Multimedia/API
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(libtbm)

%description devel


%package tools
Summary:  A Core API media tool library in Tizen Native API (Tools)
Requires: %{name} = %{version}-%{release}

%description tools


%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Media Tool library in Tizen Native API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a media tool library in Tizen native API
%endif


%prep
%setup -q


%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif
export CFLAGS="$CFLAGS -DPATH_LIBDIR=\\\"%{_libdir}\\\""

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
SO_FULLVER=0.2.0
SO_MAJORVER=`echo ${SO_FULLVER} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . \
%if "%{gtests}" == "1"
	-DMEDIA_TOOL_GTESTS_BUILD=On \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DSO_FULLVER=${SO_FULLVER} \
	-DSO_MAJORVER=${SO_MAJORVER}

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


%post
/sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%manifest capi-media-tool.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-media-tool.so.*


%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-tool.so


%files tools
%manifest %{name}-tools.manifest
%license LICENSE.APLv2
%{_bindir}/*


%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

