Name:       capi-system-system-settings
Summary:    A System Settings library in Tizen Native API
Version:    0.0.5
Release:    0

Group:      System/System Info
License:    Apache-2.0
URL : https://git.tizen.org/cgit/platform/core/api/system-settings
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(alarm-service)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(gmock)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  capi-system-info-test
BuildRequires:  default-fonts-sdk
%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
System setting api for get,set configuration

%package util-lib
Summary: Utility library for %{name}
Group: System/System Info
Requires: %{name} = %{version}

%description util-lib
The %{name}-utils pacakge contains an utility library for handling font and image

%package devel
Summary:  A System Settings library in Tizen Native API (Development)
Group:    System/System Info
Requires: %{name} = %{version}
Requires:  pkgconfig(capi-base-common)

%description devel
System setting api for get,set configuration

%package unittests
Summary: Test Programs for %{name}
Group: System/Testing

%description unittests
The %{name}-unittests pacakge contains programs for checking the %{name}.

%if 0%{?gcov:1}
%package gcov
Summary:  A System Settings library in Tizen Native API
Group:    System/Testing

%description gcov
System Settings library gcov objects
%endif

%define tizen_profile_name mobile
%define sys_setting_test_dir  %{_bindir}/sys-settings

%prep
%setup -q
cp %{SOURCE1001} ./%{name}.manifest

%build
%if "%{?tizen_profile_name}" == "wearable"
export CFLAGS="$CFLAGS -DTIZEN_WEARABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_WEARABLE"
export FFLAGS="$FFLAGS -DTIZEN_WEARABLE"
%else
export CFLAGS="$CFLAGS -DTIZEN_MOBILE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_MOBILE"
export FFLAGS="$FFLAGS -DTIZEN_MOBILE"
%endif

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version} \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DTZ_SYS_DATA=%{TZ_SYS_DATA} \
	-DTZ_SYS_ETC=%{TZ_SYS_ETC} \
	-DTZ_SYS_RO_SHARE=%{TZ_SYS_RO_SHARE} \
	-DTZ_SYS_SHARE=%{TZ_SYS_SHARE} \
	-DSYSCONF_DIR=%{_sysconfdir} \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
	-DTEST_INSTALL_DIR:PATH=%{sys_setting_test_dir} \
	-DSST_RES_DIR=%{TZ_SYS_GLOBALUSER_DATA}/settings \
	-DSTDOUT_LOG=%{?stdlog:1}%{!?stdlog:0} \
%if 0%{?thread_number}
	-DN_THREADS=%{thread_number}
%else
	-DN_THREADS=1
%endif

make %{?_smp_mflags}

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
	if [ -d "conf_example" ]; then
		rm -rf ./conf_example
		rm -rf ./tests
	fi
	ln -s /usr/bin/sys-settings/tests ./tests
	ln -s /usr/bin/sys-settings/conf_example ./conf_example
}

test_main() {
	echo "test_main start"
	/usr/bin/sys-settings/sst-unit-test
	/usr/bin/sys-settings/sst-unit-test-err-interface
	/usr/bin/sys-settings/sst-unit-test-err-font
}

teardown() {
	echo "teardown start"
	rm -rf ./tests
	rm -rf ./conf_example
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
#bash tests/scripts/vconf_golden_master.sh
%if 0%{?gcov:1}
LD_LIBRARY_PATH=.:tests:libutil tests/sst-unit-test-err-interface
LD_LIBRARY_PATH=.:tests:libutil tests/sst-unit-test
LD_LIBRARY_PATH=.:tests:libutil tests/sst-unit-test-err-font
lcov -c --ignore-errors mismatch,graph,unused,inconsistent --no-external -b $PWD -d $PWD -o %{name}.info
genhtml  %{name}.info  -o out --legend --show-details
%else
LD_LIBRARY_PATH=.:tests:libutil tests/sst-unit-test-err-interface
LD_LIBRARY_PATH=.:tests:libutil tests/sst-unit-test
LD_LIBRARY_PATH=.:tests:libutil tests/sst-unit-test-err-font
%endif

%post -p /sbin/ldconfig
%post util-lib -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun util-lib -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/lib*settings.so.*
%license LICENSE.APLv2

%files util-lib
%manifest %{name}.manifest
%{_libdir}/lib*settings-util.so
%license LICENSE.APLv2

%files devel
%manifest %{name}.manifest
%{_libdir}/lib*settings.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/system/*.h

%files unittests
%manifest %{name}.manifest
%{sys_setting_test_dir}/*
%{_libdir}/libsys-settings-mock.so
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%license LICENSE.APLv2

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
