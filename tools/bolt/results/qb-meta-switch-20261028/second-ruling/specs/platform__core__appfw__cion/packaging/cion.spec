Name:       cion
Summary:    Tizen Companion Framework
Version:    1.2.28
Release:    1
Group:      Application Framework/Communication
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    esd-cion.socket
Source1001: %{name}.manifest
Source1002: cion-mqtt-plugin.manifest

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: cion-mqtt-plugin

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(capi-system-system-settings)
BuildRequires: pkgconfig(cynara-creds-self)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(parcel)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(tizen-shared-queue)
BuildRequires: pkgconfig(uuid)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(vine)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(tizen-database)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(libesd)
BuildRequires: pkgconfig(rpc-port)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-package-manager)

BuildRequires: tidl

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Tizen Companion Library

%package devel
Summary:  Companion library (Development)
Group:    Application Framework/Communication
Requires: %{name} = %{version}-%{release}

%description devel
Companion library (Development) package.

%package -n esd-mod-cion
Summary:    ESD module for cion
Group:      Application Framework/Service

%description -n esd-mod-cion
This module is for cion

%define _moddir %{_datadir}/esd

#################################################
# unittests
#################################################
%package unittests
Summary:    GTest for Companion library
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for Companion library

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Companion library (gcov)
Group:      Application Framework/Testing

%description gcov
Companion library gcov objects
%endif

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
tidlc -p -l C++ -i ./tidl/cion.tidl -o cion_proxy
mv cion_proxy.* ./cion/common/util/
tidlc -s -l C++ -i ./tidl/cion.tidl -o cion_stub
mv cion_stub.* ./modules/cion/

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake  -DFULLVER=%{version} \
        -DMAJORVER=${MAJORVER} \
        -DBINDIR=%{_appbindir} \
        -DLOCALEDIR=%{_localedir} \
        -DMANIFESTDIR=%{_manifestdir} \
        -DRESDIR=%{_resdir} \
        -DSHAREDRESDIR=%{_shareddir}/res \
        -DESD_MODULES_DIR=%{_moddir} \
        .

%__make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/esd-cion.socket
ln -sf ../esd-cion.socket %{buildroot}%{_unitdir}/sockets.target.wants/esd-cion.socket

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

#TODO: enable check section
#%check
#ctest --output-on-failure %{?_smp_mflags}
export LD_LIBRARY_PATH=../cion
ctest -V
%if 0%{?gcov:1}
lcov -c --exclude="unittests" --ignore-errors mismatch,graph,unused,inconsistent --no-external -q -d . -o cion.info
genhtml --ignore-errors inconsistent cion.info -o cion.out
zip -r cion.zip cion.out
install -m 0644 cion.zip %{buildroot}%{_datadir}/gcov/obj/
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/cion_unittests
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

%preun

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post unittests
%if 0%{?gcov:1}
%{_bindir}/cion_unittests
%endif

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libcion.so.*

%files devel
%{_includedir}/cion/*
%{_libdir}/libcion.so
%{_libdir}/pkgconfig/cion.pc

#################################################
# mqtt-plugin
#################################################
%package mqtt-plugin
Summary: Library for developing the mqtt-plugin
Group: Applications/Application Utility
License: Apache-2.0

%description mqtt-plugin
Provide APIs to develop the mqtt-plugin.

%post mqtt-plugin
/sbin/ldconfig

%postun mqtt-plugin -p /sbin/ldconfig

%files mqtt-plugin
%manifest cion-mqtt-plugin.manifest
%defattr(-,root,root,-)
%{_libdir}/libcion-mqtt-plugin.so.*
%license LICENSE

%package mqtt-plugin-devel
Summary: mqtt-plugin development library (dev)
Group: Development/Libraries
Requires: cion-mqtt-plugin

%description mqtt-plugin-devel
Header & package configuration files to support development of the mqtt-plugin.

%files mqtt-plugin-devel
%{_includedir}/cion-mqtt-plugin/*
%{_libdir}/libcion-mqtt-plugin.so
%{_libdir}/pkgconfig/cion-mqtt-plugin.pc

%files -n esd-mod-cion
%manifest %{name}.manifest
%license LICENSE
%{_moddir}/mod/libesd-mod-cion.so
%{_unitdir}/esd-cion.socket
%{_unitdir}/sockets.target.wants/esd-cion.socket

#################################################
# unittests
#################################################
%files unittests
%{_bindir}/cion_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# cion-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
