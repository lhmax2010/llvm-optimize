Name:       capi-appfw-alarm
Summary:    An Alarm library in SLP C API
Version:    0.3.7
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-appfw-alarm.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(alarm-service)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(notification)
BuildRequires:  pkgconfig(tizen-dlog)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
An Alarm library in C API package.

%package devel
Summary:  An Alarm library in SLP C API (Development)
Group:    System/API
Requires: %{name} = %{version}

%description devel
An Alarm library in C API (Development) package.

#################################################
# capi-appfw-alarm-unittests
#################################################
%package unittests
Summary:    GTest for alarm API
Group:      System/API
Requires:   %{name}

%description unittests
GTest for alarm API

#################################################
# capi-appfw-alarm-gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:  An alarm library(gcov)
Group:    System/API

%description gcov
gcov objects of an alarm library
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
    %if 0%{?asan} != 1
      -DASAN_ENABLED=FALSE
    %else
      -DASAN_ENABLED=TRUE
    %endif
%check
export LD_LIBRARY_PATH="../../src"
ctest --verbose %{?_smp_mflags}
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o alarm.info --exclude "test/*"
genhtml alarm.info -o alarm.out
zip -r alarm.zip alarm.out alarm.info
install -m 0644 alarm.zip %{buildroot}%{_datadir}/gcov/obj/alarm.zip
%endif

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
GCOV_PATH="/tmp/home/abuild/rpmbuild/BUILD"
PACKAGE="%{name}-%{version}"

set_perm(){
    ## Sets the permission for applications
    /usr/bin/find /tmp/home/ -print | /usr/bin/xargs -n1 /usr/bin/chsmack -a "System::Run" &> /dev/null
    /usr/bin/find /tmp/home/ -print | /usr/bin/xargs -n1 /usr/bin/chsmack -a "System::Run" -t &> /dev/null
    /usr/bin/chmod -R 777 /tmp/home
}

setup(){
    echo "setup start"
    /usr/bin/mkdir -p "${GCOV_PATH}/${PACKAGE}"
    set_perm
}

test_main(){
    echo "test_main start"
    export "GCOV_PREFIX=/tmp"
    /usr/bin/alarm_unittests
}

main(){
    setup
    test_main
    teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-alarm.so.*

%license LICENSE

%files devel
%manifest %{name}.manifest
%{_includedir}/appfw/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-appfw-alarm.so


#################################################
# capi-appfw-alarm-unittests
#################################################
%files unittests
%{_bindir}/alarm_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# capi-appfw-alarm-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
