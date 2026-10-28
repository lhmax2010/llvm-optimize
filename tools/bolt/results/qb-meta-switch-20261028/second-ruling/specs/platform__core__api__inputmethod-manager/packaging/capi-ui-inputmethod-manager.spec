Name:       capi-ui-inputmethod-manager
Summary:    Input Method Manager Library
Version:    0.10.1
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(isf)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(gmock)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Input Method Manager Library

%package devel
Summary:  Input Method Manager Library (Development)
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Input Method Manager Library (Development)

%if 0%{?gcov:1}
%package gcov
Summary:  Input Method Manager (gcov)
Group:    Graphics & UI Framework/Input
%description gcov
Input Method gcov objects
%endif

%package unittests
Summary:    inputmethod manager tests
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description unittests
GTest for inputmethod manager

%prep
%setup -q


%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -fPIC -fvisibility=hidden -Werror"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE -fPIC -fvisibility=hidden -Werror"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE -fPIC -fvisibility=hidden"

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

rm -rf CMakeFiles
rm -rf CMakeCache.txt
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=/usr -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DLIB_INSTALL_DIR:PATH=%{_libdir}

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

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
	echo "setup start"
}

test_main() {
	echo "test_main start"
	/usr/bin/capi-ui-inputmethod-manager_unittest
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
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}

%check
%if 0%{?gcov:1}
ctest -V --output-on-failure %{?_smp_mflags}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o %{name}.info
genhtml %{name}.info -o %{name}.out
zip -r %{name}.zip %{name}.out %{name}.info
install -m 0644 %{name}.zip %{buildroot}%{_datadir}/gcov/
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest capi-ui-inputmethod-manager.manifest
%{_libdir}/libcapi-ui-inputmethod-manager.so.*
%license LICENSE

%files devel
%{_includedir}/inputmethod_manager*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-ui-inputmethod-manager.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%files unittests
%{_bindir}/*
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
