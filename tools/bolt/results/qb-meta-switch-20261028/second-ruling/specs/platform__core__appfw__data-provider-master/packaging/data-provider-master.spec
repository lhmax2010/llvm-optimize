%bcond_with wayland

Name: data-provider-master
Summary: Master service provider for notification
Version: 1.11.3
Release: 1
Group: Applications/Core Applications
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
# Source1: data-provider-master.service
Source2: esd-dpm.socket
Source1001: %{name}.manifest
BuildRequires: cmake, gettext-tools, smack, coreutils
BuildRequires: tidl
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(db-util)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(pkgmgr)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(notification-ex)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(alarm-service)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(security-manager)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(tizen-core)
BuildRequires: pkgconfig(united-service)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(rpc-port)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

Requires: notification-ex
Requires(post): dbus
%description

#################################################
# data-provider-master-unittests
#################################################
%package -n %{name}-unittests
Summary:    GTest for Data Provider Master API
Group:      Application Framework/Testing
Requires:   %{name}

%description -n %{name}-unittests
GTest for data-provider-master API

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:  Data Provider Master API(gcov)
Group:    Application Framework/Testing

%description gcov
gcov objects of a data provider master
%endif

%define _modname esd
%define _moddir %{_datadir}/united-service/%{_modname}

%prep
%setup -q
cp %{SOURCE1001} .
/bin/bash ./tidl/prebuild.sh

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%ifarch %ix86
export TARGET=emulator
%else
export TARGET=device
%endif

%cmake . \
    -DMOD_DIR=%{_moddir} \
	-DNAME=%{name} \
	-DTARGET=${TARGET} \
	-DMAJORVER=${MAJORVER} \
	-DFULLVER=%{version} \
	-DCMAKE_EXPORT_COMPILE_COMMANDS=ON

CFLAGS="${CFLAGS} -Wall -Winline -Werror" LDFLAGS="${LDFLAGS}" make %{?jobs:-j%jobs}

%check
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
# install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/data-provider-master.service

install -m 0644 org.tizen.data_provider_service.busname %{buildroot}%{_unitdir}/org.tizen.data_provider_service.busname

mkdir -p %{buildroot}%{_unitdir}/busnames.target.wants
ln -s ../org.tizen.data_provider_service.busname %{buildroot}%{_unitdir}/busnames.target.wants/org.tizen.data_provider_service.busname

mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/esd-dpm.socket
ln -sf ../esd-dpm.socket %{buildroot}%{_unitdir}/sockets.target.wants/esd-dpm.socket

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
    /usr/bin/data-provider-master-unittests
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

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license LICENSE
# %attr(0755,root,root) %{_bindir}/data-provider-master
# %attr(0644,root,root) %{_unitdir}/data-provider-master.service
%attr(0644,root,root) %{_datadir}/dbus-1/system-services/org.tizen.data_provider_service.service
%attr(0644,root,root) %{_unitdir}/org.tizen.data_provider_service.busname
%{_unitdir}/busnames.target.wants/org.tizen.data_provider_service.busname
%config %{_sysconfdir}/dbus-1/system.d/data-provider-master.conf
%{_moddir}/mod/libdata-provider-master.so
%{_moddir}/conf/data-provider-master.service
#%defattr(-,owner,users,-)
%{_unitdir}/esd-dpm.socket
%{_unitdir}/sockets.target.wants/esd-dpm.socket

#################################################
# data-provider-master-unittests
#################################################
%files -n %{name}-unittests
%{_bindir}/%{name}-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# data-provider-master-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

# End of a file
