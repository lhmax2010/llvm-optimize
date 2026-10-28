# BUILD_TCORE_ENABLE: 0 (default) = ECORE, 1 = TCORE, for Tizen 11 only.
# Example: gbs build ... --define "BUILD_TCORE_ENABLE 1"
# Resolve the backend here for both dependencies and build options.
%{!?BUILD_TCORE_ENABLE:%global BUILD_TCORE_ENABLE 0}
%global tizen_wayland_backend ECORE
%if 0%{?tizen_version_major} == 11
%if "%{BUILD_TCORE_ENABLE}" != "0" && "%{BUILD_TCORE_ENABLE}" != "1"
%{error:BUILD_TCORE_ENABLE must be 0 or 1}
%endif
%if "%{BUILD_TCORE_ENABLE}" == "1"
%global tizen_wayland_backend TCORE
%endif
%endif

Name:       capi-system-media-key
Summary:    A System Information library in SLP C API
Version:    0.2.15
Release:    6
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-system-media-key.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(tizen-dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
%if "%{tizen_wayland_backend}" == "TCORE"
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)
%else
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(ecore-input)
BuildRequires:  pkgconfig(evas)
BuildRequires:  pkgconfig(ecore-wl2)
%endif

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
%{summary}.

%package devel
Summary:  A Media Key library in SLP C API (Development)
Group:    System/API
Requires: %{name} = %{version}

%description devel
%devel_desc

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%if 0%{?gcov:1}
%package gcov
Summary:  A media key library(gcov)
Group:    System/API

%description gcov
gcov objects of an media key library
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
export CXXFLAGS="$CXXFLAGS -DEFL_BETA_API_SUPPORT "
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DFULLVER=%{version} -DLIB_INSTALL_DIR=%{_libdir} \
	-DMAJORVER=${MAJORVER} \
	-DTIZEN_WAYLAND_BACKEND=%{tizen_wayland_backend} \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	.

make %{?jobs:-j%jobs}

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/media-key-unittests
}

teardown() {
    echo "teardown start"
}

main() {
    setup
    test_main
    teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/

%check
(cd tests/media-key_unittests && LD_LIBRARY_PATH=../../src ctest -V)
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o media_key.info
genhtml media_key.info -o media_key.out
zip -r media_key.zip media_key.out
install -m 0644 media_key.zip %{buildroot}%{_datadir}/gcov/obj/
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libcapi-system-media-key.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/system/media_key.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-system-media-key.so

%files unittests
%{_bindir}/media-key-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
