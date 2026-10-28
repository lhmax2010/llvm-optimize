Name: bluetooth-share
Summary: Bluetooth file share Agent
Version: 0.10.0
Release: 1
Group: Network & Connectivity/Bluetooth
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: 500.%{name}_upgrade.sh
BuildRequires: cmake
BuildRequires: gettext-tools
BuildRequires: pkgconfig(appcore-efl)
BuildRequires: pkgconfig(appsvc)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(bluetooth-api)
BuildRequires: pkgconfig(calendar-service2)
BuildRequires: pkgconfig(capi-content-media-content)
BuildRequires: pkgconfig(contacts-service2)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-dbus)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(db-util)
BuildRequires: pkgconfig(deviced)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(ecore)
BuildRequires: pkgconfig(eventsystem)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(notification)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(storage)
BuildRequires: pkgconfig(storage)
BuildRequires: pkgconfig(syspopup-caller)
BuildRequires: pkgconfig(vconf)
Requires(post): smack
#Requires(post): coreutils
%if 0%{?gcov:1}
BuildRequires: gtest-devel
BuildRequires: lcov
BuildRequires: tar
%endif

%description
Bluetooth File Share Agent

%package -n libbluetooth-share
Summary:    Bluetooth share library
Group:      Network & Connectivity/Bluetooth
Requires:   %{name} = %{version}-%{release}

%description -n libbluetooth-share
Bluetooth share library

%package -n libbluetooth-share-devel
Summary:    Development package for libbluetooth-share
Group:      Network & Connectivity/Development
Requires:   %{name} = %{version}-%{release}

%description -n libbluetooth-share-devel
Development package for libbluetooth-share

%global upgrade_data_path /usr/share/upgrade/data

%prep
%setup -q
cp %{SOURCE1001} %{SOURCE1002} ./

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS+=" -Wno-error=implicit-enum-enum-cast"
%endif
}

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version} \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DSYSTEMD_DIR:PATH=%{_unitdir} \
	-DDATA_DIR:PATH=%{TZ_SYS_DATA} \
	-DENABLE_CONTACTS_SVC=1 \
	-DENABLE_CALENDAR_SVC=1 \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}
make %{?_smp_mflags}

%install
%make_install
%if 0%{?gcov:1}
find .. -name '*.gcno' -printf '%%P\n' | tar cf %{name}-gcov.tar -C .. -T -
install -d -m 755 %{buildroot}%{_datadir}/gcov/obj
tar xf %{name}-gcov.tar -C %{buildroot}%{_datadir}/gcov/obj
%endif

mkdir -p %{buildroot}%{upgrade_data_path}
mkdir -p %{buildroot}%{TZ_SYS_UPGRADE_SCRIPTS}
install -D -m 0755 init_db.sh %{buildroot}%{upgrade_data_path}
install -D -m 0755 %{SOURCE1002} %{buildroot}%{TZ_SYS_UPGRADE_SCRIPTS}

%check
%if 0%{?gcov:1}
LD_LIBRARY_PATH=lib LD_PRELOAD=tests/libbt-share-mock.so tests/bt-share-gtest
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post
%{TZ_SYS_DATA}/%{name}/init_db.sh

%post -n libbluetooth-share -p /sbin/ldconfig

%postun -n libbluetooth-share -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%attr(755, network_fw, network_fw)%{TZ_SYS_DATA}/%{name}
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-start.service
%{TZ_SYS_UPGRADE_SCRIPTS}/500.%{name}_upgrade.sh
%{TZ_SYS_DATA}/%{name}/init_db.sh
%{upgrade_data_path}/init_db.sh
#%{_datadir}/dbus-1/system-services/org.bluetooth.share.service
%license LICENSE.APLv2
%exclude %{_bindir}/bt-share-gtest
%exclude %{_datadir}/gcov/*

%files -n libbluetooth-share
%manifest %{name}.manifest
%{_libdir}/*.so.*
%license LICENSE.APLv2

%files -n libbluetooth-share-devel
%{_includedir}/%{name}-api/%{name}-api.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-api.pc
