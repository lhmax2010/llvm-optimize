Name:       badge
Summary:    Badge library
Version:    0.5.7
Release:    1
Group:      Applications/Core Applications
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    esd-badge.socket
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(rpc-port)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(libesd)
BuildRequires: pkgconfig(tizen-database)

BuildRequires: tidl

%define _moddir %{_datadir}/esd

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

BuildRequires: cmake
Requires(post): /sbin/ldconfig
requires(postun): /sbin/ldconfig

%description
Client/Server library for updating badge information

%package devel
Summary:    Badge library (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Development files needed to build software that needs to system a system badge.

%package service-devel
Summary:    Badge library (service-devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description service-devel
Development files needed to build badge service

#################################################
# badge-unittests
#################################################
%package unittests
Summary:    GTest for badge API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for badge API

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:  Badge library (gcov)
Group:    System/API

%description gcov
gcov objects of a Badge library
%endif

%prep
%setup -q
tidlc -p -l C++ -i ./tidl/badge.tidl -o badge_proxy
mv badge_proxy.* ./src/
tidlc -s -l C++ -i ./tidl/badge.tidl -o badge_stub
mv badge_stub.* ./modules/badge/


%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export LDFLAGS="$LDFLAGS -Wl,--rpath=%{_prefix}/lib -Wl,--as-needed"
LDFLAGS="$LDFLAGS"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
	-DMAJORVER=${MAJORVER} \
  -DDB_PATH=%{TZ_SYS_DB}/.badge.db \
  -DESD_MODULES_DIR=%{_moddir} \
	-DFULLVER=%{version}
make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH=../../src
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o badge.info
lcov -r badge.info "_proxy*" -o badge.info
lcov -r badge.info "_stub*" -o badge.info
lcov -r badge.info "/unit_tests/*" -o badge.info
lcov -r badge.info "/mock/*" -o badge.info
genhtml badge.info -o badge.out
zip -r badge.zip badge.out
install -m 0644 badge.zip %{buildroot}%{_datadir}/gcov/badge.zip
%endif

%install

%make_install
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/esd-badge.socket
ln -sf ../esd-badge.socket %{buildroot}%{_unitdir}/sockets.target.wants/esd-badge.socket

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
    /usr/bin/badge_unittests
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

%post
/sbin/ldconfig

if [ ! -d %{TZ_SYS_DB} ]
then
	mkdir -p %{TZ_SYS_DB}
fi

%postun -p /sbin/ldconfig

%files
%manifest badge.manifest
%defattr(-,root,root,-)
%{_libdir}/libbadge.so.*
%license LICENSE
%{_includedir}/badge/badge.h
%{_includedir}/badge/badge_internal.h
%{_includedir}/badge/badge_setting.h
%{_includedir}/badge/badge_error.h
%{_moddir}/mod/libesd-mod-badge.so
%{_unitdir}/esd-badge.socket
%{_unitdir}/sockets.target.wants/esd-badge.socket

%files devel
%defattr(-,root,root,-)
%{_includedir}/badge/badge.h
%{_includedir}/badge/badge_internal.h
%{_includedir}/badge/badge_setting.h
%{_includedir}/badge/badge_error.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/libbadge.so

%files unittests
%{_bindir}/badge_unittests
%{_bindir}/badge_integtests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# badge-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
