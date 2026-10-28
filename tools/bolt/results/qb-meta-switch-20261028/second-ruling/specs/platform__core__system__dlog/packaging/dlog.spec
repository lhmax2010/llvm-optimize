%define keepstatic yes
Name:       dlog
Summary:    Logging service
Version:    11.0.0
Release:    1
Group:      System/Libraries
License:    Apache-2.0, MIT, GPL-2.0
Source0:    %{name}-%{version}.tar.gz
Source101:  packaging/dlog.manifest
Source501:  packaging/01-dlog.rules

# NOTE: hardcoded instead of a build dependency on libudev.
#       Needed to prevent a cyclic build dependency in case
#       dlog is used in a package dependent on libsystemd,
#       since libudev is a part of it
%define _udevrulesdir %{_prefix}/lib/udev/rules.d

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: compiler-rt
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(libtzplatform-config)
%if 0%{?lowmem_notification:1}
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(gio-2.0)
%endif
%if 0%{?gcov:1}
BuildRequires: lcov
BuildRequires: zip
%endif

Requires:      %{name}-config-persistent-logs
Obsoletes:     %{name}-common < 6.5.3

%description
Shared files between libdlog and service

%package -n libdlog
Summary:    dlog library APIs
License:    MIT
Group:      Development/Libraries
Requires(pre): coreutils
Requires(post): coreutils
Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/chsmack
Requires(postun): /sbin/ldconfig
Requires: %{name} = %{version}-%{release}
Requires: %{name}-logger = %{version}-%{release}
Obsoletes: libdlogutil < 6.5.3
Obsoletes: libdlog-redirect-stdout < 6.5.3
%description -n libdlog
* libdlog - client API
* libdlogutil - log retrieval library
* libdlog_redirect_stdout - client library for attaching stdout/stderr

%package -n libdlog-devel
Summary:    Logging service dlog API
License:    MIT
Group:      Development/Libraries
Requires:   libdlog = %{version}-%{release}
Requires:   pkgconfig(capi-base-common)
Obsoletes:  libdlogutil-devel < 6.5.3
Obsoletes:  libdlog-redirect-stdout-devel < 6.5.3
%description -n libdlog-devel

%package -n libdlog-devel-static
Summary:    Logging service dlog API static build
License:    MIT
Group:      Development/Libraries
Requires:   libdlog = %{version}-%{release}
Requires:   pkgconfig(capi-base-common)
Obsoletes:  libdlogutil-devel < 6.5.3
Obsoletes:  libdlog-redirect-stdout-devel < 6.5.3
%description -n libdlog-devel-static

%package    logger
Summary:    Logger service
License:    Apache-2.0
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%if 0%{?lowmem_notification:1}
Requires:   pkgconf(gio-2.0)
%endif
%description logger

%package -n dlogutil
Summary:    print log data to the screen
Group:      Development/Libraries
%description -n dlogutil

%package    config-backend-zero-copy
License:    Apache-2.0
Summary:    Force usage of zero-copy dlog backend
Group:      Base/Startup
%description config-backend-zero-copy
Provides dlog config to enable zero-copy backend and tunes libdlog
performance while sacrificing some of dlog features (static and
dynamic filtering)

%package config-syslog
License:    Apache-2.0
Summary:    Logger: syslog-source logging via dlog
Group:      Base/Startup
Provides:   tizen-log-syslog
%description config-syslog
Systemd unit for syslog socket configation to use with dlog

%package config-persistent-logs
Summary: enable persistent storage of logs
%description config-persistent-logs
Enable persistent logs in dlog (stored in /var/log/dlog/)

%package config-qos
Summary: enable quality of service module
%description config-qos
Enables Quality of Service module in dlog

%package doc
Summary: dlog documentation
BuildRequires: doxygen
%description doc
Documentation for dlog

%package tests
Summary: dlog integration tests
Requires: lib%{name} = %{version}-%{release}
Requires(post): /usr/bin/chsmack
%description tests
Integration tests for dlog.

%if 0%{?gcov:1}
%package gcov
Summary:  gcov files for libdlog
Group:    Development/Libraries
%description gcov
This package contains gcov code coverage/profiling files for libdlog.
%endif

%package unittests
Summary: Coverage tests

%description unittests
Not actually unit tests, named that way just to conform to specification

%isu_package

%prep
%setup -q

%build
# TODO: Respect the defaults, and have all custom flags in one place
CFLAGS="-Wno-gnu-variable-sized-type-not-at-end -g"
TEST_CFLAGS="-Wno-gnu-variable-sized-type-not-at-end -Wno-logical-op-parentheses"

%if 0%{?gcov:1}
export CAPI_GCOV_CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CAPI_GCOV_CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export CAPI_GCOV_LDFLAGS="$LDFLAGS -lgcov"
TEST_CFLAGS+=" -ftest-coverage"
%endif

%if 0%{?asan:1}
export CFLAGS+=" -DASAN_BUILD=True"
export CXXFLAGS+=" -DASAN_BUILD=True"
TEST_CFLAGS+=" -DASAN_BUILD=True"
%endif

cp %{SOURCE101} .

%autogen
%configure \
%if 0%{?lowmem_notification:1}
--enable-lowmem-notification
%endif

make %{?jobs:-j%jobs} CFLAGS+='-D__DLOG_VERSION=\"%{version}\" -D__DLOG_RELEASE=\"%{release}\"'

# autoconf adds a bunch of flags, including -O2.
# Clear those so that test coverage can be measured properly
CFLAGS="$TEST_CFLAGS"
make check CFLAGS+='-D__DLOG_VERSION=\"%{version}\" -D__DLOG_RELEASE=\"%{release}\"'

make dox

%if 0%{?gcov:1}
%check -n libdlog
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d ./src -o dlog.info
genhtml dlog.info -o dlog.out
zip -r dlog.zip dlog.out dlog.info
install -m 0644 dlog.zip %{buildroot}%{_datadir}/gcov/
%endif

%install
rm -rf %{buildroot}

%make_install
mkdir -p %{buildroot}/usr/bin/

mkdir -p %{buildroot}/usr/share/doc/dlog
cp -r documentation/* %{buildroot}/usr/share/doc/dlog

mkdir -p %{buildroot}%{_unitdir}/basic.target.wants/
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants/
mkdir -p %{buildroot}%{_unitdir}/paths.target.wants/
ln -s ../dlog_logger.service %{buildroot}%{_unitdir}/basic.target.wants/dlog_logger.service
ln -s ../dlog_dev-log.socket %{buildroot}%{_unitdir}/sockets.target.wants/dlog_dev-log.socket
ln -s ../dlog_cleanup.path %{buildroot}%{_unitdir}/paths.target.wants/dlog_cleanup.path

mkdir -p %{buildroot}%{_udevrulesdir}
install -m 0644 %SOURCE501 %{buildroot}%{_udevrulesdir}/01-dlog.rules

mkdir -p %{buildroot}/var/log/dlog

mkdir -p %{buildroot}/var/lib/dlog-tests
mkdir -p %{buildroot}/usr/share/dlog-filters.conf.test
mkdir -p %{buildroot}/var/lib/dlog-unittests
mkdir -p %{buildroot}/usr/share/dlog-filters.conf.unittest

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%files -n dlogutil
%manifest dlog.manifest
%license LICENSE.APACHE2.0 LICENSE.MIT
%attr(750,log,log) %{_bindir}/dlogutil
%attr(755,log,log) %{_bindir}/dlogsend
%attr(750,log,log) %{_bindir}/dlog_cleanup
%attr(750,log,log) %{_bindir}/dlogmetrics
%attr(755,log,log) %{_bindir}/dlog_redirect_stdout
%{_unitdir}/dlog_cleanup.service
%{_unitdir}/dlog_cleanup.path
%{_unitdir}/paths.target.wants/dlog_cleanup.path
%attr(750,log,log) %{_bindir}/dlogctl

%post -n dlogutil
chsmack %{_bindir}/dlogctl -a "System::Tools"

%post -n libdlog -p /sbin/ldconfig

%post
chsmack -a System /var/log/dlog
# set timestamp to beginning of the unix epoch to make rotation work even if we are run on system with no/broken rtc
touch -m -t 197001010000.01 /var/log/dlog/critical.a
touch -m -t 197001010000.00 /var/log/dlog/critical.b
chmod 660 /var/log/dlog/critical*
chown log:log /var/log/dlog/critical*
chsmack -e 'System' %{_libexecdir}/dlog-log-critical

%files
%manifest dlog.manifest
%license LICENSE.APACHE2.0
%{_sysconfdir}/dlog.conf
%{_sysconfdir}/dlog.conf.d/20-pipe.conf
%{_sysconfdir}/dlog.conf.d/25-logger.conf
# not in a separate package for debugging convenience
%{_sysconfdir}/dlog.conf.d/86-disable-dlog.conf_inactive
%attr(755,log,log) /var/log/dlog
%attr(2551,log,log) %{_libexecdir}/dlog-log-critical
/usr/lib/tmpfiles.d/dlog-run.conf
%{_udevrulesdir}/01-dlog.rules

%files -n libdlog
%manifest dlog.manifest
%license LICENSE.MIT
%{_libdir}/libdlog.so.0
%{_libdir}/libdlog.so.0.0.0
%{_libdir}/libdlogutil.so.*
%{_libdir}/libdlog_redirect_stdout.so.*

%files -n libdlog-devel
%manifest dlog.manifest
%license LICENSE.MIT
%{_includedir}/dlog/dlog.h
%{_includedir}/dlog/dlog-internal.h
%{_includedir}/dlog/dlogutil.h
%{_includedir}/dlog/dlog-redirect-stdout.h
%{_libdir}/libdlog.so
%{_libdir}/libdlogutil.so
%{_libdir}/libdlog_redirect_stdout.so
%{_libdir}/pkgconfig/dlog.pc
%{_libdir}/pkgconfig/dlogutil.pc
%{_libdir}/pkgconfig/dlog-redirect-stdout.pc

%files -n libdlog-devel-static
%manifest dlog.manifest
%license LICENSE.MIT
%{_libdir}/libdlog.a
%{_libdir}/libdlog_redirect_stdout.a
%{_libdir}/libdlogutil.a

%files unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
%{_bindir}/tizen-unittests/%{name}/test_capi_coverage
%{_bindir}/tizen-unittests/%{name}/test_libdlogutil_cov
%{_datadir}/dlog-coverage.conf
%dir %attr(755,log,log) /var/lib/dlog-unittests
%dir %attr(755,log,log) /usr/share/dlog-filters.conf.unittest

%files logger
%manifest dlog.manifest
%license LICENSE.APACHE2.0
%attr(750,log,log) %{_bindir}/dlog_logger
%{_unitdir}/basic.target.wants/dlog_logger.service
%{_unitdir}/dlog_logger.service
/usr/lib/systemd/system-generators/dlog-unit-generator

%files config-backend-zero-copy
%manifest dlog.manifest
%license LICENSE.APACHE2.0 LICENSE.MIT
/usr/lib/modules/modules-load.d/tizen-modules-dlog-zero-copy.conf
%{_sysconfdir}/dlog.conf.d/30-zero-copy.conf

%files config-syslog
%manifest dlog.manifest
%license LICENSE.APACHE2.0 LICENSE.MIT
%{_unitdir}/sockets.target.wants/dlog_dev-log.socket
%{_unitdir}/dlog_dev-log.socket

%files config-persistent-logs
%{_sysconfdir}/dlog.conf.d/10-persistent-logs.conf

%files config-qos
%{_sysconfdir}/dlog.conf.d/15-qos.conf

%files doc
%manifest dlog.manifest
%license LICENSE.APACHE2.0 LICENSE.MIT
/usr/share/doc/dlog

%files tests
%manifest dlog.manifest
%license LICENSE.APACHE2.0 LICENSE.MIT
%{_bindir}/dlog_test
%{_bindir}/dlog_test_header
%{_bindir}/dlog_test_daemon_early_quit
%{_bindir}/dlog_test_backend_autodetection
%{_bindir}/dlog_test_tid_filtering_secure_logging
%{_bindir}/dlog_test_stdout_redirect
%{_bindir}/dlog_test_logger_buffering_logging
%{_bindir}/dlog_cpu
/usr/share/doc/dlog/README.testsuite
%{_libexecdir}/libdlog/perf_libdlog
%{_libexecdir}/libdlog/dlog_stdout_benchmark
%{_libexecdir}/libdlog/dlog_compression_benchmark
%{_libexecdir}/libdlog/test_libdlog
%{_libexecdir}/libdlog/test_libdlogutil
%{_libexecdir}/libdlog/test_verifytime
%{_libexecdir}/libdlog/test_libredirect
%{_libexecdir}/libdlog/test_libredirect_multi
%{_libexecdir}/libdlog/test_filters
%{_libexecdir}/libdlog/test_config_redirect
%{_datadir}/dlog-pipe.conf.test
%{_datadir}/dlog-logger.conf.test
%{_datadir}/dlog-zero-copy.conf.test
%{_datadir}/dlog-logger.conf.alias
%{_datadir}/dlog-pipe.conf.cpu
%{_datadir}/dlog-logger.conf.cpu
%{_datadir}/dlog-pipe.conf.qos
%{_datadir}/dlog-logger.conf.qos
%{_datadir}/dlog-pipe.conf.plog
%{_datadir}/dlog-logger.conf.plog
%{_datadir}/dlog-pipe.conf.autodetect
%{_datadir}/dlog-logger.conf.autodetect
%{_datadir}/dlog-logger.conf.stdout_enable.1
%{_datadir}/dlog-logger.conf.stdout_enable.2
%{_datadir}/dlog-logger.conf.stdout_enable.3
%{_datadir}/dlog-pipe.conf.stdout_enable.1
%{_datadir}/dlog-pipe.conf.stdout_enable.2
%{_datadir}/dlog-pipe.conf.stdout_enable.3
%{_datadir}/dlog-zero-copy.conf.stdout_enable.1
%{_datadir}/dlog-zero-copy.conf.stdout_enable.2
%{_datadir}/dlog-zero-copy.conf.stdout_enable.3
%{_datadir}/dlog-logger.conf.compress
%{_datadir}/dlog-pipe.conf.compress
%{_sysconfdir}/dlog.conf.d/99-dlog-logger.disable-platform-logging-for-testsuite.conf
%dir %attr(755,log,log) /var/lib/dlog-tests
%dir %attr(755,log,log) /usr/share/dlog-filters.conf.test

%post tests
chsmack -a System /var/lib/dlog-tests
echo "Warning! Installation of dlog-tests will break platform logging."
echo "This is done intentionally, to make logger and zero-copy backend testing possible."
echo "To restore normal behavior, please uninstall dlog-tests package."
echo ""
echo "For more information please read the /usr/share/doc/dlog/README.testsuite file"
echo ""
echo "A reboot is required to properly configure logger and zero-copy backend for testing."

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
