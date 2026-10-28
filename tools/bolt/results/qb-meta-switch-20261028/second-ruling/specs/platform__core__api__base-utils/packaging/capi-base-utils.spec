Name:       capi-base-utils
Summary:    Base Utils
Version:    3.1.5
Release:    2
Group:      Base
License:    Apache-2.0 and ICU
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)

BuildRequires:  gtest-devel
%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
The base utils library for internationalization and localization

%package devel
License:    Apache-2.0 and ICU
Summary:    The Base Utils Library (Development)
Group:      Base
Requires:   %{name} = %{version}-%{release}

%description devel
The base utils library for internationalization and localization (Development)

%package -n i18ninfo
License:    Apache-2.0
Summary:    The Base Utils Tool
Group:      Base
Requires:	capi-base-utils

%description -n i18ninfo
The base utils library test tool

# gcov
%if 0%{?gcov:1}
%package gcov
Summary:    %{name} gcov data

%description gcov
Base utils gcov objects
%endif

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
%endif

%cmake -DPKG_NAME=%{name} -DPKG_VERSION=%{version} \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DSTDOUT_LOG=%{?stdlog:1}%{!?stdlog:0}

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
	pushd %{_bindir}/tizen-unittests/capi-base-utils
	/usr/bin/tct-base-utils-core
	popd
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
mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}/tests/res
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/
install -m 0755 ./tests/res/* %{buildroot}%{_bindir}/tizen-unittests/%{name}/tests/res

%check
%if 0%{?gcov:1}
tests/tct-base-utils-core
lcov -c --ignore-errors mismatch --ignore-errors graph  --ignore-errors inconsistent --no-external -b . -d . --exclude "$PWD/tests/include/*" -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest capi-base-utils.manifest
%{_libdir}/libbase-utils-i18n.so*
%license LICENSE LICENSE.ICU

%files devel
%defattr(-,root,root,-)
%{_includedir}/base/utils_i18n*.h
%{_libdir}/pkgconfig/*.pc

%files -n i18ninfo
%defattr(-,root,root,-)
%{_bindir}/i18ninfo

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%{_bindir}/tct-base-utils-core
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%{_bindir}/tizen-unittests/%{name}/tests/res/*
