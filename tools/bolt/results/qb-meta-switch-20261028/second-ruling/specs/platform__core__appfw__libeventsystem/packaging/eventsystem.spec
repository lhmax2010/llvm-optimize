Name:       eventsystem
Summary:    Event system library
Version:    0.1.60
Release:    1
Group:      Application Framework/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    esd-group.socket
BuildRequires:  cmake
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(libesd)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(parcel)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(pkgmgr-parser)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  pkgconfig(security-manager)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(vconf)

%define _moddir %{_datadir}/esd

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Recommends: esd

%description
Event System Library

%package devel
Summary:    Event system library (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Event system library (devel)

#################################################
# eventsystem-unittests
#################################################
%package -n %{name}-unittests
Summary:    GTest for EventySystem API
Group:      Application Framework/Testing
Requires:   %{name}

%description -n %{name}-unittests
GTest for EventSystem API

%package -n esd-mod-group
Summary:    ESD module for app events
Group:      Application Framework/Service

%description -n esd-mod-group
This module is for app events


#################################################
# eventsystem-benchmark
#################################################
%package -n %{name}-benchmark
Summary:    Benchmark for EventySystem API
Group:      Application Framework/Testing
Requires:   %{name}

%description -n %{name}-benchmark
Benchmark for EventySystem API


#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:  Event System API(gcov)
Group:    Application Framework/Testing

%description gcov
gcov objects of a eventsystem
%endif

%prep
%setup -q

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . -DFULLVER=%{version} \
  -DMAJORVER=${MAJORVER} \
  -DESD_MODULES_DIR=%{_moddir} \
  %if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE
  %else
    -DASAN_ENABLED=TRUE
  %endif
make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH="../../src:../../modules/group"
ctest -V

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o ${name}.info
lcov -r ${name}.info "/unit_tests/*" -o ${name}.info
genhtml ${name}.info -o out --legend --show-details
%endif

%install
rm -rf %{buildroot}

%make_install
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/esd-group.socket
ln -sf ../esd-group.socket %{buildroot}%{_unitdir}/sockets.target.wants/esd-group.socket

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
    /usr/bin/eventsystem-unittests
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


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%posttrans
rm -rf %{_moddir}/mod/libesd-mod-dbus-event.so

%files
%manifest eventsystem.manifest
%defattr(-,root,root,-)
%{_libdir}/libeventsystem.so.*
%{_sysconfdir}/package-manager/parserlib/metadata/libeventsystem-plugin.so
%{_datarootdir}/parser-plugins/eventsystem-plugin.info
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/*.h
%{_libdir}/libeventsystem.so
%{_libdir}/pkgconfig/eventsystem.pc

#################################################
# eventsystem-unittests
#################################################
%files -n %{name}-unittests
%{_bindir}/%{name}-unittests
%{_bindir}/%{name}-integtests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# eventsystem-benchmark
#################################################
%files -n %{name}-benchmark
%{_bindir}/%{name}-benchmark

#################################################
# eventsystem-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files -n esd-mod-group
%manifest %{name}.manifest
%{_unitdir}/esd-group.socket
%license LICENSE
%{_moddir}/mod/libesd-mod-group.so
%{_unitdir}/sockets.target.wants/esd-group.socket

