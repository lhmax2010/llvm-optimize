Name:       capi-ui-sticker
Summary:    Sticker client library and daemon
Version:    1.3.6
Release:    1
Group:      Graphics & UI Framework/Input
License:    Apache-2.0 and MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    capi-ui-sticker.service
Source2:    org.tizen.sticker.server.service
Source3:    capi-ui-sticker.conf
BuildRequires:  cmake, coreutils
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-appfw-package-manager)
BuildRequires:  pkgconfig(capi-appfw-event)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(gmock)

%if 0%{?sec_product_feature_profile_wearable}
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(capi-appfw-preference)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  pkgconfig(sap-client-stub-api)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-media-thumbnail-util)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  hash-signer

Requires(post): signing-client
Requires:       org.tizen.sticker-receiver
%endif

Requires:       security-config
Requires(post): /sbin/ldconfig
Requires(post): dbus
Requires(postun): /sbin/ldconfig

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Sticker client library and daemon

%package devel
Summary:    Sticker client library and daemon (Development)
Group:      Graphics & UI Framework/Input
Requires:   %{name} = %{version}-%{release}

%if 0%{?sec_product_feature_profile_wearable}
%define _companion_app_name org.tizen.sticker-receiver

%package -n %{_companion_app_name}
Summary:    Sticker companion service
Group:      Graphics & UI Framework/Input
Requires:   %{name} = %{version}-%{release}
%endif


%description devel
Sticker client library and daemon (Development)

%if 0%{?sec_product_feature_profile_wearable}
%description -n %{_companion_app_name}
Sticker companion service
%endif

%if 0%{?gcov:1}
%package gcov
Summary:  Sticker client library and daemon (gcov)
Group:      Graphics & UI Framework/Input
%description gcov
Sticker client library and daemon (gcov)
%endif

%package unittests
Summary:    Sticker tests
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description unittests
GTest for sticker

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE2} .

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden -Werror"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE -fvisibility=hidden"

%cmake . \
%if 0%{?sec_product_feature_profile_wearable}
        -DCOMPANION_MODE=true \
%endif
         -DCMAKE_INSTALL_PREFIX=/usr -DLIBDIR=%{_libdir} -DBINDIR=%{_bindir} -DINCLUDEDIR=%{_includedir} \
         -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE -DTZ_SYS_BIN=%TZ_SYS_BIN -DTZ_USER_SHARE=%TZ_USER_SHARE \
         -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES

make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find ./server/ -name '*.gcno' -exec rm {} \;
find ./tests/ -name '*.gcno' -not -path "*/client/*" -exec rm {} \;
find . -name '*_dbus*.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
	echo "setup start"
}

test_main() {
	echo "test_main start"
	/usr/bin/capi-ui-sticker-unittest
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

mkdir -p %{buildroot}/%{TZ_SYS_ETC}/dump.d/module.d
cp -af dump/sticker_log_dump.sh %{buildroot}/%{TZ_SYS_ETC}/dump.d/module.d

mkdir -p %{buildroot}%{_prefix}/lib/systemd/system
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/capi-ui-sticker.service

mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services
install -m 0644 %SOURCE2 %{buildroot}%{_datadir}/dbus-1/system-services/org.tizen.sticker.server.service

mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
install -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/dbus-1/system.d/capi-ui-sticker.conf

%if 0%{?sec_product_feature_profile_wearable}
%define tizen_sign 1
%define tizen_sign_base %{TZ_SYS_RO_APP}/%{_companion_app_name}
%define tizen_sign_level public
%define tizen_author_sign 1
%define tizen_dist_sign 1
%endif

%check
%if 0%{?gcov:1}
%if 0%{?run_unittest:1}
ctest --output-on-failure %{?_smp_mflags}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o capi-ui-sticker.info
genhtml capi-ui-sticker.info -o capi-ui-sticker.out
zip -r capi-ui-sticker.zip capi-ui-sticker.out capi-ui-sticker.info
install -m 0644 capi-ui-sticker.zip %{buildroot}%{_datadir}/gcov
%endif
%endif

%post
/sbin/ldconfig

mkdir -p -m 0775 /opt/share/sticker-data
chown -R ui_fw:ui_fw /opt/share/sticker-data
chsmack -t /opt/share/sticker-data
chsmack -a "User::App::Shared" /opt/share/sticker-data

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE COPYING.MIT
%{_libdir}/lib*.so
%attr(0755,ui_fw,ui_fw) %{_bindir}/sticker-server
%attr(0644,root,root) %{_unitdir}/capi-ui-sticker.service
%attr(0644,root,root) %{_datadir}/dbus-1/system-services/org.tizen.sticker.server.service
%config %{_sysconfdir}/dbus-1/system.d/capi-ui-sticker.conf
%{TZ_SYS_RO_SHARE}/parser-plugins/capi-ui-sticker.info
%{TZ_SYS_RO_ETC}/package-manager/parserlib/category/libcapi-ui-sticker-parser.so*
%{TZ_SYS_RO_ETC}/package-manager/parserlib/metadata/libcapi-ui-sticker-parser.so*
%{TZ_SYS_ETC}/dump.d/module.d/*

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/capi-ui-sticker-consumer.pc
%{_libdir}/pkgconfig/capi-ui-sticker-provider.pc
%{_includedir}/sticker_error.h
%{_includedir}/sticker_data.h
%{_includedir}/sticker_consumer.h
%{_includedir}/sticker_provider.h

%if 0%{?sec_product_feature_profile_wearable}
%post -n %{_companion_app_name}
/usr/bin/signing-client/hash-signer-client.sh -a -d -p platform %{TZ_SYS_RO_APP}/%{_companion_app_name}

%files -n %{_companion_app_name}
%manifest receiver/%{_companion_app_name}.manifest
%license LICENSE
%{TZ_SYS_RO_PACKAGES}/%{_companion_app_name}.xml
%{TZ_SYS_RO_APP}/%{_companion_app_name}/*
%endif

%files unittests
%license LICENSE
%{_bindir}/capi-ui-sticker-unittest
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
