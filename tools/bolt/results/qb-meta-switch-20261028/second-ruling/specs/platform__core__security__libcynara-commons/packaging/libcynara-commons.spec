Name:       libcynara-commons
Summary:    Cynara - cynara commons library
Version:    0.27.0
Release:    1
Group:      Security/Application Privilege
License:    Apache-2.0 or MIT
Source0:    cynara-%{version}.tar.gz
Source1000:    %{name}-rpmlintrc
Source1002:    libcynara-client.manifest
Source1003:    libcynara-admin.manifest
Source1004:    cynara-commons-tests.manifest
Source1005:    libcynara-agent.manifest
Source1006:    libcynara-commons.manifest
Source1012:    cynara-db-migration.manifest
Source1013:    cyad.manifest
Source1014:    cynara-db-chsgen.manifest
Source1015:    libcynara-monitor.manifest
Source1020:    libcynara-client-helpers.manifest
Requires:      default-ac-domains
Requires(pre): cynara-db-migration >= %{version}
%if "%{?dev_wos}" != "1"
Requires(post):   smack
BuildRequires: pkgconfig(libsmack)
%endif
Requires(postun): cynara-db-migration >= %{version}
BuildRequires: cmake
BuildRequires: zip
Obsoletes:     libcynara-storage

# alternatives: DLOG, JOURNAL, NONE, (otherwise SYSLOG is used)
# WARNING!
# when choosing JOURNAL, make sure not to introduce cyclic dependency
# check if systemd depends on libdbus-policy!
%if !%{defined log_type}
%define log_type "DLOG"
%endif


%if %{log_type} == "DLOG"
BuildRequires: pkgconfig(dlog)
%endif

%if %{log_type} == "JOURNAL"
BuildRequires: pkgconfig(libsystemd)
%endif

%if !%{defined build_type}
%define build_type RELEASE
%endif

%if %{?build_type} == "DEBUG"

BuildRequires: libdw-devel
BuildRequires: pkgconfig(libunwind)

%endif

%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%global coverage_dir %{_datadir}/cynara-commons-coverage
%endif

%global project_name cynara

# We need to simulate the provides old pre-merge libraries had and rpm derives
# the soname from ELF which might carry an ISA marker. We need to simulate that.
%if "%{__isa_bits}" == "64"
%global so_isa ()(64bit)
%else
%global so_isa %{nil}
%endif

%global compat_libs client-commons creds-commons creds-pid creds-self creds-socket session uid uid-creds

%package -n cynara-devel
Summary:    Cynara development files
Requires:   libcynara-admin = %{version}
Requires:   libcynara-agent = %{version}
Requires:   libcynara-client = %{version}
Requires:   libcynara-commons = %{version}
Requires:   libcynara-client-helpers = %{version}
Requires:   libcynara-monitor = %{version}
Obsoletes:  libcynara-admin-devel
Obsoletes:  libcynara-agent-devel
Obsoletes:  libcynara-client-async-devel
Obsoletes:  libcynara-client-commons-devel
Obsoletes:  libcynara-client-devel
Obsoletes:  libcynara-commons-devel
Obsoletes:  libcynara-creds-commons-devel
Obsoletes:  libcynara-creds-socket-devel
Obsoletes:  libcynara-plugin-devel
Obsoletes:  libcynara-session-devel
Obsoletes:  libcynara-storage-devel

%description -n cynara-devel
Cynara development files

%package -n cynara-commons-tests
Summary:    Cynara - cynara-commons test binaries
BuildRequires: pkgconfig(gmock)

%description -n cynara-commons-tests
Cynara-commons tests

%package -n libcynara-client
Summary:    Cynara - client libraries
Requires:   libcynara-client-helpers = %{version}
BuildRequires: pkgconfig(capi-system-resource)
Obsoletes:  libcynara-client-commons
Obsoletes:  libcynara-client-async

%description -n libcynara-client
Client libraries for checking policies: synchronous and asynchronous

%package -n libcynara-admin
Summary:    Cynara - admin client library
BuildRequires: pkgconfig(capi-system-resource)

%description -n libcynara-admin
admin client library for setting, listing and removing policies

%package -n libcynara-agent
Summary:    Cynara - agent client library

%description -n libcynara-agent
agent client library for communication with cynara service and plugins

%description -n libcynara-commons
cynara common library with common functionalities

%package -n libcynara-client-helpers
Summary:    Cynara - client common code and credentials, session and uid helpers
Requires:   libcynara-commons = %{version}
Provides:   libcynara-creds-commons = %{version}
Provides:   libcynara-creds-pid = %{version}
Provides:   libcynara-creds-self = %{version}
Provides:   libcynara-creds-socket = %{version}
Provides:   libcynara-session = %{version}
Provides:   libcynara-uid = %{version}
Provides:   libcynara-uid-creds = %{version}
Obsoletes:  libcynara-creds-commons
Obsoletes:  libcynara-creds-pid
Obsoletes:  libcynara-creds-self
Obsoletes:  libcynara-creds-socket
Obsoletes:  libcynara-session
Obsoletes:  libcynara-uid
Obsoletes:  libcynara-uid-creds
Provides:   libcynara-client-commons.so.0%{so_isa}
Provides:   libcynara-creds-commons.so.0%{so_isa}
Provides:   libcynara-creds-pid.so.0%{so_isa}
Provides:   libcynara-creds-self.so.0%{so_isa}
Provides:   libcynara-creds-socket.so.0%{so_isa}
Provides:   libcynara-session.so.0%{so_isa}
Provides:   libcynara-uid.so.0%{so_isa}
Provides:   libcynara-uid-creds.so.0%{so_isa}

%description -n libcynara-client-helpers
The cynara client common code and every credentials, session and uid helper
in one shared object.

%package -n cynara-db-migration
Summary:    Migration tools for Cynara's database
Requires:   findutils

%description -n cynara-db-migration
Migration tools for Cynara's database

%package -n cyad
Summary: Cynara's command-line tool
Requires:   libcynara-admin = %{version}
Requires:   libcynara-commons = %{version}

%description -n cyad
Command-line tool to manage Cynara's database

%package -n libcynara-monitor
Summary:    Cynara - monitor client library

%description -n libcynara-monitor
Monitor client library for obtaining check logs

%prep
%setup -q -n cynara-%{version}
cp -a %{SOURCE1002} .
cp -a %{SOURCE1003} .
cp -a %{SOURCE1004} .
cp -a %{SOURCE1005} .
cp -a %{SOURCE1006} .
cp -a %{SOURCE1012} .
cp -a %{SOURCE1013} .
cp -a %{SOURCE1014} .
cp -a %{SOURCE1015} .
cp -a %{SOURCE1020} .

%build
export CXXFLAGS+=" -Wl,-z,relro,-z,now"

%if %{?build_type} == "DEBUG" || %{?build_type} == "COVERAGE"
export CXXFLAGS+=" -Wp,-U_FORTIFY_SOURCE"
%endif

export LDFLAGS+=" -Wl,--rpath=%{_libdir}"

%cmake . \
        -DBUILD_TESTS=ON \
        -DBUILD_WITH_SYSTEMD_DAEMON=OFF \
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
        -DSOCKET_DIR:PATH=/run/%{project_name} \
%if "%{?dev_wos}" != "1"
        -DCYNARA_CLIENT_METHOD_DEFAULT=smack \
        -DCYNARA_USER_METHOD_DEFAULT=uid \
        -DDB_FILES_SMACK_LABEL="System" \
        -DSMACK_ENABLED="ON" \
%endif
%if "%{?dev_wos}" == "1" || "%{?uid_app_sandboxing}" == "1"
        -DCYNARA_CLIENT_METHOD_DEFAULT=context \
        -DCYNARA_USER_METHOD_DEFAULT=owner \
        -DUID_SANDBOXING_ENABLED="ON" \
%endif
%if "%{build_type}" == "COVERAGE"
        -DCOVERAGE_DIR=%{coverage_dir} \
%endif
        -DMONITORING=ON
make %{?jobs:-j%jobs}

%install
#rm -rf %{buildroot}
%make_install

%post -n libcynara-client -p /sbin/ldconfig

%postun -n libcynara-client -p /sbin/ldconfig

%post -n libcynara-admin -p /sbin/ldconfig

%postun -n libcynara-admin -p /sbin/ldconfig

%post -n libcynara-agent -p /sbin/ldconfig

%postun -n libcynara-agent -p /sbin/ldconfig

%pre -n libcynara-commons

if [ $1 -gt 1 ] ; then
    # upgrade
    %{_sbindir}/cynara-db-migration upgrade -f 0.0.0 -t %{version}
else
    # install
    %{_sbindir}/cynara-db-migration install -t %{version}
fi

%post -n libcynara-commons -p /sbin/ldconfig

%postun -n libcynara-commons

/sbin/ldconfig
if [ $1 = 0 ]; then
    %{_sbindir}/cynara-db-migration uninstall -f %{version}
    systemctl daemon-reload
fi

%post -n libcynara-client-helpers -p /sbin/ldconfig

%postun -n libcynara-client-helpers -p /sbin/ldconfig

%post -n libcynara-monitor -p /sbin/ldconfig

%postun -n libcynara-monitor -p /sbin/ldconfig

# posttrans used as a safest place to create the symlinks as ldconfig might
# remove some symlinks in intermediate state during updates (post/postun)
%posttrans -n libcynara-client-helpers
for lib in %{compat_libs}; do
    ln -sf libcynara-client-helpers.so.0 %{_libdir}/libcynara-${lib}.so.0
done
/sbin/ldconfig

%files -n cynara-devel
%license LICENSE LICENSE.MIT
%{_includedir}/cynara/*.h
%{_includedir}/cynara/attributes/*.h
%{_includedir}/cynara/config/*.h
%{_includedir}/cynara/containers/*.h
%{_includedir}/cynara/cpu-priority/*.h
%{_includedir}/cynara/error/*.h
%{_includedir}/cynara/exceptions/*.h
%{_includedir}/cynara/log/*.h
%{_includedir}/cynara/lock/*.h
%{_includedir}/cynara/no_smack/*.h
%{_includedir}/cynara/plugin/*.h
%{_includedir}/cynara/protocol/*.h
%{_includedir}/cynara/request/*.h
%{_includedir}/cynara/response/*.h
%{_includedir}/cynara/storage/*.h
%{_includedir}/cynara/types/*.h
%{_includedir}/cynara/utils/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files -n cynara-commons-tests
%manifest cynara-commons-tests.manifest
%attr(755,root,root) %{_bindir}/cynara-commons-tests
%attr(755,root,root) %{_bindir}/cynara-db-migration-tests
%attr(755,root,root) %{_bindir}/cynara-check-cmd
%attr(755,root,root) %{_datarootdir}/%{project_name}/tests

%files -n libcynara-client
%manifest libcynara-client.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-client.so.*
%{_libdir}/libcynara-client-async.so.*
%dir %attr(755,cynara,cynara) %{_libdir}/%{project_name}/plugin/client

%files -n libcynara-admin
%manifest libcynara-admin.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-admin.so.*

%files -n libcynara-agent
%manifest libcynara-agent.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-agent.so.*

%files -n libcynara-commons
%manifest libcynara-commons.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-commons.so.*
%{_libdir}/libcynara-storage.so.*
%dir %attr(700,cynara,cynara) %{_localstatedir}/cynara

%files -n libcynara-client-helpers
%manifest libcynara-client-helpers.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-client-helpers.so.*
%ghost %{_libdir}/libcynara-client-commons.so.0
%ghost %{_libdir}/libcynara-creds-commons.so.0
%ghost %{_libdir}/libcynara-creds-pid.so.0
%ghost %{_libdir}/libcynara-creds-self.so.0
%ghost %{_libdir}/libcynara-creds-socket.so.0
%ghost %{_libdir}/libcynara-session.so.0
%ghost %{_libdir}/libcynara-uid.so.0
%ghost %{_libdir}/libcynara-uid-creds.so.0
%{_sysconfdir}/%{project_name}/creds.conf

%files -n cynara-db-migration
%manifest cynara-db-migration.manifest
%manifest cynara-db-chsgen.manifest
%license LICENSE LICENSE.MIT
%attr(700,root,root) %{_sbindir}/cynara-db-migration
%attr(700,root,root) %{_sbindir}/cynara-db-chsgen

%files -n cyad
%manifest cyad.manifest
%license LICENSE LICENSE.MIT
%attr(700,root,root) %{_sbindir}/cyad

%files -n libcynara-monitor
%manifest libcynara-monitor.manifest
%license LICENSE LICENSE.MIT
%{_libdir}/libcynara-monitor.so.*

%if "%{build_type}" == "COVERAGE"
%package -n cynara-commons-coverage
Summary:    Cynara code coverage data
Group:      Security/Testing
Requires:   cynara-commons-tests = %{version}
Requires:   libcynara-commons-debugsource = %{version}
Requires:   lcov
Requires:   gcc

%description -n cynara-commons-coverage
Cynara code coverage data

%files -n cynara-commons-coverage
%manifest cynara-commons-tests.manifest
%{_bindir}/cynara-commons-coverage.sh
%coverage_dir

%endif
