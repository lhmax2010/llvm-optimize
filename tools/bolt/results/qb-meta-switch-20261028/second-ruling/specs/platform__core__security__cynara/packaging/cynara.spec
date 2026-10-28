Name:       cynara
Summary:    Cynara service with client libraries
Version:    0.27.0
Release:    1
Group:      Security/Application Privilege
License:    Apache-2.0 or MIT
Source0:    %{name}-%{version}.tar.gz
Source1000:    %{name}-rpmlintrc
Source1001:    cynara.manifest
Source1002:    cynara-tests.manifest
Requires:      default-ac-domains
Requires:      libcynara-commons = %{version}
BuildRequires: cmake
BuildRequires: zip
BuildRequires: pkgconfig(capi-system-resource)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(cynara-commons)
%{?systemd_requires}

# alternatives: DLOG, JOURNAL, NONE, (otherwise SYSLOG is used)
%if !%{defined log_type}
%define log_type "DLOG"
%endif

%if !%{defined build_type}
%define build_type RELEASE
%endif

%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%global coverage_dir %{_datadir}/cynara-coverage
%endif

%description
Cynara service and tests (cynara-tests)

%package -n cynara-tests
Summary:    Cynara - cynara test binaries
BuildRequires: pkgconfig(cynara-commons)
BuildRequires: pkgconfig(gmock)
Requires:      libcynara-commons = %{version}

%description -n cynara-tests
Cynara serivce tests

%prep
%setup -q -n cynara-%{version}
cp -a %{SOURCE1001} .
cp -a %{SOURCE1002} .

%build
export CXXFLAGS+=" -Wl,-z,relro,-z,now"

%if %{?build_type} == "DEBUG"|| %{?build_type} == "COVERAGE"
export CXXFLAGS+=" -Wp,-U_FORTIFY_SOURCE"
%endif

export LDFLAGS+=" -Wl,--rpath=%{_libdir}"

%cmake . \
        -DBUILD_TESTS=OFF \
        -DBUILD_WITH_SYSTEMD_DAEMON=ON \
        -DLOG_TYPE=%{log_type} \
        -DCMAKE_BUILD_TYPE=%{?build_type} \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DLIB_DIR:PATH=%{_libdir} \
        -DBIN_DIR:PATH=%{_bindir} \
        -DSBIN_DIR:PATH=%{_sbindir} \
        -DSYS_CONFIG_DIR:PATH=%{_sysconfdir} \
        -DINCLUDE_DIR:PATH=%{_includedir} \
        -DLOCAL_STATE_DIR:PATH=%{_localstatedir} \
        -DDATA_ROOT_DIR:PATH=%{_datadir} \
        -DSYSTEMD_UNIT_DIR:PATH=%{_unitdir} \
        -DSOCKET_DIR:PATH=/run/%{name} \
%if "%{?dev_wos}" != "1"
        -DSMACK_ENABLED="ON" \
%endif
%if "%{?dev_wos}" == "1" || "%{?uid_app_sandboxing}" == "1"
        -DUID_SANDBOXING_ENABLED="ON" \
%endif
%if "%{build_type}" == "COVERAGE"
        -DCOVERAGE_DIR=%{coverage_dir} \
%endif
        -DMONITORING=ON
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
mkdir -p %{buildroot}%{_datadir}/cynara/db
ln -s ../cynara.socket %{buildroot}%{_unitdir}/sockets.target.wants/cynara.socket
ln -s ../cynara-admin.socket %{buildroot}%{_unitdir}/sockets.target.wants/cynara-admin.socket
ln -s ../cynara-agent.socket %{buildroot}%{_unitdir}/sockets.target.wants/cynara-agent.socket
ln -s ../cynara-monitor-get.socket %{buildroot}%{_unitdir}/sockets.target.wants/cynara-monitor-get.socket
ln -s ../cynara.service %{buildroot}%{_unitdir}/multi-user.target.wants/cynara.service

%post
### Add file capabilities if needed
### setcap/getcap binary are useful. To use them you must install libcap and libcap-tools packages
### In such case uncomment Requires with those packages

systemctl daemon-reload
systemctl restart %{name}.service

%preun
if [ $1 = 0 ]; then
    # unistall
    systemctl stop cynara.service
fi

%files
%manifest cynara.manifest
%license LICENSE LICENSE.MIT
%attr(755,root,root) %{_bindir}/cynara
%attr(-,root,root) %{_unitdir}/cynara.service
%attr(-,root,root) %{_unitdir}/multi-user.target.wants/cynara.service
%attr(-,root,root) %{_unitdir}/cynara.target
%attr(-,root,root) %{_unitdir}/sockets.target.wants/cynara.socket
%attr(-,root,root) %{_unitdir}/cynara.socket
%attr(-,root,root) %{_unitdir}/sockets.target.wants/cynara-admin.socket
%attr(-,root,root) %{_unitdir}/cynara-admin.socket
%attr(-,root,root) %{_unitdir}/sockets.target.wants/cynara-agent.socket
%attr(-,root,root) %{_unitdir}/cynara-agent.socket
%attr(-,root,root) %{_unitdir}/sockets.target.wants/cynara-monitor-get.socket
%attr(-,root,root) %{_unitdir}/cynara-monitor-get.socket
%attr(755,root,root) %{_datadir}/cynara/
%dir %attr(755,cynara,cynara) %{_libdir}/%{name}/plugin/service

%files -n cynara-tests
%manifest cynara-tests.manifest
%attr(755,root,root) %{_bindir}/cynara-tests

%if "%{build_type}" == "COVERAGE"
%package -n cynara-coverage
Summary:    Cynara code coverage data
Group:      Security/Testing
Requires:   cynara-tests = %{version}
Requires:   cynara-debugsource = %{version}
Requires:   lcov
Requires:   gcc

%description -n cynara-coverage
Cynara code coverage data

%files -n cynara-coverage
%manifest cynara-tests.manifest
%{_bindir}/cynara-coverage.sh
%coverage_dir

%endif

