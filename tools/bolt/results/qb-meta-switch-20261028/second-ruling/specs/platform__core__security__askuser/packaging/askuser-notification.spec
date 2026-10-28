%{!?build_type:%global build_type RELEASE}

%if !%{defined with_systemd_daemon}
%define with_systemd_daemon 1
%endif

Name:       askuser-notification
Summary:    User daemon which shows popup with privilege request
Version:    0.8.8
Release:    1
Group:      Security/Access Control
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:    default.manifest
Source1002:    libaskuser-notification-common.manifest
BuildRequires: cmake
BuildRequires: libwayland-egl
BuildRequires: gettext-tools
%if %{with_systemd_daemon}
BuildRequires: pkgconfig(libsystemd)
%endif
BuildRequires: pkgconfig(cynara-plugin) >= 0.26.0
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-socket)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(security-privilege-manager) >= 1.4.1
BuildRequires: pkgconfig(security-manager) >= 2.6.0
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(dlog)
BuildRequires: boost-devel
%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%endif

%description
Provides daemon allowing user to grant or deny access to given privilege
for a client application, and a plugin for supporting custom
Cynara policy type "Ask user".

%package -n libaskuser-notification-common
Summary:    Askuser common library

%description -n libaskuser-notification-common
Askuser common library with common functionalities

%package devel
Requires: capi-privacy-privilege-manager
Summary: Askuser notification protocol library development files

%description devel
Askuser notification protocol library development files

%package test
Summary: Tools for testing privacy-privilege-manager C API
Requires(post): security-config

%description test
Provides tests for checking the API provided by capi-privacy-privilege-manager

%package unit-tests
Summary:    Askuser unit test binaries
Group:      Security/Development
Requires(post): security-config

%description unit-tests
Internal test for Askuser implementation.

%package -n capi-privacy-privilege-manager
Summary: Privacy Privilege Manager in TIZEN C API
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Obsoletes: askuser-notification-client
Obsoletes: askuser-notification-client-debuginfo

%description -n capi-privacy-privilege-manager
This CAPI allows an application to check if it has a given privilege.
Additionally, for privacy privileges, it provides an ability to determine
their statuses by displaying an appropriate pop-up dialog box. A user
can make a decision whether to give a privilege to an application or not.

%package -n privacy-privilege-admin
Summary: Privacy Privilege Admin C API
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n privacy-privilege-admin
This API administers privacy policies on the device. It can disable or
re-enable all privileges mapped to a given privacy for every application of
a user, and set, reset or check the privacy policy of an individual
application. It also allows querying the current privacy status.

%package -n privacy-privilege-admin-cmd
Summary: Command line tool for the Privacy Privilege Admin C API
Requires: privacy-privilege-admin = %{version}-%{release}

%description -n privacy-privilege-admin-cmd
Provides privacy-privilege-admin-cmd, a command line tool exposing the API
provided by privacy-privilege-admin.

%if "%{build_type}" == "COVERAGE"

%package coverage
Summary:    Askuser code coverage data
Group:      Security/Testing
Requires:   askuser-notification-unit-tests = %{version}-%{release}
Requires:   askuser-notification-debugsource = %{version}-%{release}
Requires:   lcov
Requires:   gcc

%description coverage
Askuser code coverage data

%endif

%global ppm_tester_dir %{?TZ_SYS_DATA:%TZ_SYS_DATA}%{!?TZ_SYS_DATA:/opt/data}/%{name}
%global ppm_tester_pkgid org.tizen.askuser-tester
%global ppm_tester_tpk %{ppm_tester_pkgid}-1.0.0.tpk

%prep
%setup -q

%build
export CXXFLAGS="$CXXFLAGS -Wno-implicit-fallthrough"
export CXXFLAGS="$CXXFLAGS -Werror=shadow"
export LDFLAGS="$LDFLAGS -Wl,--rpath=%{_libdir}"

%global coverage_dir %{_datadir}/askuser-notification-coverage

%cmake . \
        -DCMAKE_BUILD_TYPE=%{?build_type} \
        -DBUILD_WITH_SYSTEMD_DAEMON=%{?with_systemd_daemon} \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DPPM_TESTER_DIR=%{ppm_tester_dir} \
        -DPPM_TESTER_TPK=%{ppm_tester_tpk} \
        -DCOVERAGE_DIR=%{coverage_dir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/
%make_install

%if %{with_systemd_daemon}
mkdir -p %{buildroot}/%{_unitdir}/sockets.target.wants
ln -s ../askuser-notification-stream.socket %{buildroot}/%{_unitdir}/sockets.target.wants/askuser-notification-stream.socket
%endif

cp -a %{SOURCE1001} %{SOURCE1002} %{buildroot}%{_datadir}/

%post
%if %{with_systemd_daemon}
systemctl daemon-reload
%endif

systemctl restart cynara.service
if [ $1 = 2 ]; then
    # update - workaround for ditry user-session service restart, only for platform development case
    echo "WARNING: askuser-notification updated; to ensure system stability & proper operation, reboot your device"
fi

%preun

%postun
systemctl restart cynara.service

%post -n libaskuser-notification-common -p /sbin/ldconfig

%postun -n libaskuser-notification-common -p /sbin/ldconfig

%post -n capi-privacy-privilege-manager -p /sbin/ldconfig

%postun -n capi-privacy-privilege-manager -p /sbin/ldconfig

%post -n privacy-privilege-admin -p /sbin/ldconfig

%postun -n privacy-privilege-admin -p /sbin/ldconfig

%post test
/usr/share/security-config/configure_askuser.sh ENABLE
if [ $1 = 1 ]; then
	# install the ppm tester C# app
	pkgcmd -i -t tpk -p %{ppm_tester_dir}/%{ppm_tester_tpk}
fi

if [ $1 = 2 ]; then
	# reinstall the ppm tester C# app
	pkgcmd -u -n %{ppm_tester_pkgid}
	pkgcmd -i -t tpk -p %{ppm_tester_dir}/%{ppm_tester_tpk}
fi

%postun test
if [ $1 = 0 ]; then
	# uninstall the ppm tester C# app
	pkgcmd -u -n %{ppm_tester_pkgid}
fi

%post unit-tests
# unit tests require askable policy levels (see SmFixture.cpp)
/usr/share/security-config/configure_askuser.sh ENABLE

%files -n %{name}
%manifest %{_datadir}/default.manifest
%license LICENSE
%attr(755,root,root) /usr/bin/askuser-notification
%if %{with_systemd_daemon}
%{_unitdir}/askuser-notification.service
%{_unitdir}/askuser-notification-stream.socket
%{_unitdir}/sockets.target.wants
%endif
%{_libdir}/cynara/plugin/service/*.so
%{_libdir}/cynara/plugin/client/*.so

%files -n libaskuser-notification-common
%manifest %{_datadir}/libaskuser-notification-common.manifest
%license LICENSE
%{_libdir}/libaskuser-notification-common-core.so.*
%{_libdir}/libaskuser-notification-common.so.*
%{_libdir}/libaskuser-notification.so.*

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/privacy-privilege-manager/*.h
%{_includedir}/privacy-privilege-admin/*.h
%{_libdir}/*.so

%files test
%manifest %{_datadir}/default.manifest
%license LICENSE
%attr(755,root,root) %{_bindir}/askuser-notification-test
%attr(755,root,root) %{_bindir}/capi-privacy-privilege-manager-test
%{ppm_tester_dir}/%{ppm_tester_tpk}

%files unit-tests
%manifest %{_datadir}/default.manifest
%license LICENSE
%attr(755,root,root) %{_bindir}/askuser-notification-unit-tests

%files -n capi-privacy-privilege-manager
%manifest %{_datadir}/default.manifest
%license LICENSE
%attr(644,-,-) %{_libdir}/libcapi-privacy-privilege-manager.so.*

%files -n privacy-privilege-admin
%manifest %{_datadir}/default.manifest
%license LICENSE
%attr(644,-,-) %{_libdir}/libprivacy-privilege-admin.so.*

%files -n privacy-privilege-admin-cmd
%manifest %{_datadir}/default.manifest
%license LICENSE
%attr(755,root,root) %{_bindir}/privacy-privilege-admin-cmd

%if "%{build_type}" == "COVERAGE"

%files coverage
%manifest %{_datadir}/default.manifest
%license LICENSE
%{_bindir}/askuser-notification-coverage.sh
%coverage_dir

%endif
