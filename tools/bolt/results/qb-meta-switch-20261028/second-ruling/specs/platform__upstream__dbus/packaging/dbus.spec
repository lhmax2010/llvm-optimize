%bcond_with coverage

%if 0%{?dev_wos:1} || 0%{?uid_app_sandboxing:1}
%define tizen_uid_security yes
%else
%define tizen_uid_security no
%endif

# Do not create provides from extension .so files because the main package
# should anchor any reverse-dependencies
%global __provides_exclude_from ^(.*\\.extension-kdbus)$

Name:           dbus
Url:            http://dbus.freedesktop.org/
Summary:        D-Bus Message Bus System
License:        AFL-2.1 or GPL-2.0+, LGPL-2.1+, MIT, BSD-3-Clause
Group:          Base/IPC
# COMMON1-BEGIN

%define with_systemd 1

BuildRequires:  autoconf-archive
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  expat-devel
BuildRequires:  libcap-ng-devel
%if %{with_systemd}
BuildRequires:  pkgconfig(libsystemd)
%endif
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-client-async)
BuildRequires:  pkgconfig(libdbuspolicy1)
BuildRequires:  pkgconfig(cynara-creds-pid) >= 0.23.0
%if "%{tizen_uid_security}" == "yes"
BuildRequires:  pkgconfig(cynara-uid)
%endif
Version:        1.12.20
Release:        3
Source0:        http://dbus.freedesktop.org/releases/dbus/dbus-%{version}.tar.gz
Source3:        dbus_at_console.ck
Source4:        baselibs.conf
Source7:        dbus.sh
Source1001:     dbus.manifest
Source1002:     dbus.vip.conf
# COMMON1-END
Requires:       security-config
Requires(pre):  /usr/bin/getent
Requires(pre):  /usr/sbin/useradd
Requires(pre):  /usr/sbin/groupadd
Provides:       dbus-1

%description
D-Bus is a message bus system, a simple way for applications to talk to
one another. D-Bus supplies both a system daemon and a
per-user-login-session daemon. Also, the message bus is built on top of
a general one-to-one message passing framework, which can be used by
any two apps to communicate directly (without going through the message
bus daemon).
.
This package provides dbus-daemon.

%package devel
Summary:    Developer package for D-Bus
License:    AFL-2.1 or GPL-2.0+
Group:      Development/Libraries
Requires:   dbus-libs = %{version}

%description devel
D-Bus is a message bus system, a simple way for applications to talk to
one another.
.
This package provides development libraries.

%package libs
Summary:    Library package for D-Bus
License:    AFL-2.1 or GPL-2.0+
Group:      System/Libraries

%description libs
D-Bus is a message bus system, a simple way for applications to talk to
one another.
.
This package provides shared libraries.

%package tests
Summary:    Package with binaries and data for dbus tests
License:    AFL-2.1 or GPL-2.0+, MIT

%description tests
This package contains installable tests. Tests are compatible with 'dbus-integration-tests' framework.

%if %{with coverage}
%package coverage
Summary:    Special version of dbus library for getting coverage analysis

%description coverage
Special version of dbus library for getting coverage analysis. *.gcda coverage files
are generated on each use of library in directory set by GCOV_PREFIX and GCOV_PREFIX_STRIP.
Use the library by modifying LD_LIBRARY_PATH.
This package is intended for debug/test use only.

%package coverage-objects
Summary:    Generated object files and gcov notes for coverage analysis

%description coverage-objects
We need to keep objects and gcno files to analyze coverage.
This package is intended for debug/test use only.
%endif

%package -n dbus-libs-extension-kdbus
Summary:	Extension for dbus to support KDBUS in Tizen
License:    AFL-2.1 or GPL-2.0+
Requires:	dbus = %{version}-%{release}

%description -n dbus-libs-extension-kdbus
This modifies dbus to support KDBUS in Tizen.

%prep
# COMMON2-BEGIN
%setup -n dbus-%{version} -q

%build
cp %{SOURCE1001} .
# We use -fpie/-pie for the whole build; this is the recommended way to harden
# the build upstream, see discussion in fdo#46570
export CFLAGS="${RPM_OPT_FLAGS} -fno-strict-aliasing -fPIC -fpie"
%ifarch %{arm}
export CFLAGS=${CFLAGS/-Wa,-mimplicit-it=thumb/}" -marm"
%endif
export LDFLAGS="-pie"
export CXXFLAGS="${RPM_OPT_FLAGS} -fno-strict-aliasing"
export CFLAGS="$CFLAGS -fstack-protector"
export CXXFLAGS="$CXXFLAGS -fstack-protector"
export V=1

# Create kdbus extension first (dbus)
%reconfigure						\
    --disable-static 					\
    --with-pic						\
    --with-dbus-user=dbus 				\
    --libexecdir=%{_libdir}/%{name}			\
    --libdir=%{_libdir}					\
    --enable-inotify					\
    --disable-doxygen-docs				\
    --disable-xml-docs					\
%if %{with_systemd}
    --enable-systemd					\
%endif
    --enable-kdbus-transport				\
    --enable-libdbuspolicy                      	\
    --with-console-auth-dir=/var/run/dbus/at_console/	\
    --with-system-socket=/run/dbus/system_bus_socket	\
    --with-systemdsystemunitdir=%{_unitdir}		\
    --with-systemduserunitdir=%{_unitdir_user}		\
    --enable-user-session				\
    --enable-cynara					\
    --enable-tizen-uid-security=%{tizen_uid_security}	\
    --enable-modular-tests				\
    --enable-installed-tests

make %{?_smp_mflags}

mkdir -p extension-kdbus
pushd dbus/.libs/
# rm if symlink. mv if regular file.
for FILE in libdbus-*.so*; do test -h "$FILE" && rm "$FILE" || mv "$FILE" ../../extension-kdbus/ ; done
popd

%{__make} clean

# Support for generating separate packages with libraries generating coverage files
# WARNING: if coverage build is enabled, incremental builds will not work correctly.
#          Use the option only to generate dbus-coverage packages.
%if %{with coverage}
%reconfigure						\
    --disable-static 					\
    --with-pic						\
    --with-dbus-user=dbus				\
    --libexecdir=%{_libdir}/%{name}			\
    --libdir=%{_libdir}					\
    --enable-inotify					\
    --disable-doxygen-docs				\
    --disable-xml-docs					\
%if %{with_systemd}
    --enable-systemd					\
%endif
    --enable-kdbus-transport				\
    --enable-libdbuspolicy				\
    --with-console-auth-dir=/var/run/dbus/at_console/	\
    --with-system-socket=/run/dbus/system_bus_socket	\
    --with-systemdsystemunitdir=%{_unitdir}		\
    --with-systemduserunitdir=%{_unitdir_user}		\
    --enable-user-session				\
    --enable-cynara					\
    --enable-tizen-uid-security=%{tizen_uid_security}	\
    --enable-modular-tests				\
    --enable-installed-tests				\
    --enable-compiler-coverage

make %{?_smp_mflags}
mkdir coverage
cp dbus/.libs/libdbus-1.so.3 coverage
mkdir coverage-objects
find dbus -name '*.o' -exec cp '{}' coverage-objects ';'
find dbus -name '*.gcno' -exec cp '{}' coverage-objects ';'

%endif

%reconfigure						\
    --disable-static					\
    --with-pic						\
    --with-dbus-user=dbus				\
    --libexecdir=%{_libdir}/%{name}			\
    --libdir=%{_libdir}					\
    --enable-inotify					\
    --disable-doxygen-docs				\
    --disable-xml-docs					\
%if %{with_systemd}
    --enable-systemd					\
%endif
    --with-console-auth-dir=/var/run/dbus/at_console/	\
    --with-system-socket=/run/dbus/system_bus_socket	\
    --with-systemdsystemunitdir=%{_unitdir}		\
    --with-systemduserunitdir=%{_unitdir_user}		\
    --enable-user-session				\
    --enable-cynara					\
    --enable-tizen-uid-security=%{tizen_uid_security}	\
    --enable-modular-tests				\
    --enable-installed-tests

make %{?_smp_mflags}

%install
# COMMON2-END
make DESTDIR=%{buildroot} install

# kdbus extension
pushd extension-kdbus
for FILE in *; do mv "$FILE" "%{buildroot}%{_libdir}/$FILE.extension-kdbus"; done
popd

mkdir -p %{buildroot}/usr/sbin
install -d %{buildroot}/%{_localstatedir}/run/dbus
mkdir -p %{buildroot}/%{_libdir}/pkgconfig
mkdir -p %{buildroot}/lib/dbus-1/system-services
mkdir -p %{buildroot}/%{_datadir}/dbus-1/system-services
mkdir -p %{buildroot}/%{_datadir}/dbus-1/interfaces
#
chmod a-x AUTHORS CONTRIBUTING.md NEWS README doc/*.txt doc/file-boilerplate.c doc/TODO
#
install -d %{buildroot}%{_sysconfdir}/ConsoleKit/run-session.d
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/ConsoleKit/run-session.d

rm -rf %{buildroot}/%{_libdir}/*.la
rm -rf %{buildroot}/%{_bindir}/dbus-launch

# install script for login shells (/etc/profile.d)
install -d %{buildroot}%{_sysconfdir}/profile.d
install -m 0644 %{SOURCE7} %{buildroot}%{_sysconfdir}/profile.d/dbus.sh

mkdir -p %{buildroot}/%{_sysconfdir}/resourced/vip-process.d
cp %{SOURCE1002} %{buildroot}/%{_sysconfdir}/resourced/vip-process.d/dbus.conf

# docs
rm -rf %{buildroot}%{_datadir}/doc

# build test binaries and copy test data
%define relative_dbus_tests_base_dir %{_libdir}/dbus-tests
%define dbus_tests_base_dir %{buildroot}%{relative_dbus_tests_base_dir}
%define dbus_installed_tests_dir %{_libdir}/dbus/installed-tests/dbus
mkdir -p %{dbus_tests_base_dir}/test-suites/dbus-tests/

mkdir -p %{dbus_tests_base_dir}/runner/
%__cc %{_builddir}/%{name}-%{version}/test-runner.c -g -o %{dbus_tests_base_dir}/runner/dbus-tests
rm -fr %{buildroot}/usr/share/installed-tests/dbus
# The tests are installed in standard directory for dbus tests.
# However, we need to have the tests also available for dbus-integration-tests package.
# Thus, we link selected tests to our dbus-integration-tests directory
for f in manual-dir-iter manual-tcp test-corrupt test-dbus-daemon \
		 test-dbus-daemon-eavesdrop test-fdpass test-loopback test-marshal \
		 test-monitor test-printf test-refs test-relay test-sd-activation \
		 test-shell test-syntax test-syslog test-uid-permissions
do ln -s %{dbus_installed_tests_dir}/$f %{dbus_tests_base_dir}/test-suites/dbus-tests/$f; done

%if "%{tizen_uid_security}" == "yes"
sed -i -e 's,ListenStream=.*,ListenStream=/run/dbus_session_bus,' %{buildroot}%{_unitdir_user}/dbus.socket
sed -i -e 's,TIZEN_UID_SECURITY=0,TIZEN_UID_SECURITY=1,' %{buildroot}/etc/profile.d/dbus.sh
mkdir -p %{buildroot}%{_unitdir}/user@.service.d
printf "[Service]\nEnvironment=\nEnvironment=DBUS_SESSION_BUS_ADDRESS=kernel:path=/sys/fs/kdbus/%i-user/bus;unix:path=/run/dbus_session_bus\n" > %{buildroot}%{_unitdir}/user@.service.d/dbus_session_busaddr.conf
%endif

%if %{with coverage}
%define relative_cov_lib_dir %{relative_dbus_tests_base_dir}/coverage-libs
%define cov_lib_dir %{buildroot}%{relative_cov_lib_dir}
mkdir -p %{cov_lib_dir}
mkdir -p %{cov_lib_dir}/objects
install -m 0755 coverage/* %{cov_lib_dir}
install -m 0644 coverage-objects/* %{cov_lib_dir}/objects
%endif

%pre
# Add the "dbus" user and group
getent group  dbus > /dev/null || /usr/sbin/groupadd -r -g 81 dbus 2> /dev/null || :
getent passwd dbus > /dev/null || /usr/sbin/useradd -c 'System message bus' -u 81 -g 81 \
                                   -s /sbin/nologin -r -d '/' dbus 2> /dev/null || :

%post
# Set the smack label of executable binary tools
chsmack %{_bindir}/dbus-cleanup-sockets -a "System::Tools"
chsmack %{_bindir}/dbus-daemon -a "System::Tools"
chsmack %{_bindir}/dbus-monitor -a "System::Tools" -e "System"
chsmack %{_bindir}/dbus-run-session -a "System::Tools"
chsmack %{_bindir}/dbus-send -a "System::Tools"
chsmack %{_bindir}/dbus-uuidgen -a "System::Tools"
chsmack %{_bindir}/dbus-test-tool -a "System::Tools"
chsmack %{_bindir}/dbus-update-activation-environment -a "System::Tools"

%post -n dbus-libs-extension-kdbus
rm %{_sysconfdir}/resourced/vip-process.d/dbus.conf
pushd %{_libdir}
for FILE in libdbus*.so.*.extension-kdbus; do mv "$FILE" "${FILE%.extension-kdbus}"; done
popd

%files -n dbus-libs-extension-kdbus
%manifest %{name}.manifest
%license LICENSE.AFL-2.1_or_GPL-2.0+
%{_libdir}/libdbus*.so.*.extension-kdbus

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.AFL-2.1_or_GPL-2.0+ LICENSE.BSD-3-Clause LICENSE.LGPL-2.1+ LICENSE.MIT
%defattr(-, root, root)
%dir /lib/dbus-1
%dir /lib/dbus-1/system-services
%config(noreplace) %{_sysconfdir}/dbus-1/session.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.conf
%config(noreplace) %{_datadir}/dbus-1/session.conf
%config(noreplace) %{_datadir}/dbus-1/system.conf
%{_sysconfdir}/ConsoleKit
%{_bindir}/dbus-cleanup-sockets
%{_bindir}/dbus-daemon
%{_bindir}/dbus-monitor
%{_bindir}/dbus-run-session
%{_bindir}/dbus-send
%{_bindir}/dbus-uuidgen
%{_bindir}/dbus-test-tool
%{_bindir}/dbus-update-activation-environment
# See doc/system-activation.txt in source tarball for the rationale
# behind these permissions
%attr(4750,root,dbus) %verify(not mode) %{_libdir}/dbus/dbus-daemon-launch-helper
%dir %{_unitdir}
%{_unitdir}/dbus.socket
%{_unitdir}/dbus.service
%dir %{_unitdir}/sockets.target.wants
%{_unitdir}/sockets.target.wants/dbus.socket
%dir %{_unitdir_user}
%{_unitdir_user}/dbus.socket
%{_unitdir_user}/dbus.service
%dir %{_unitdir_user}/sockets.target.wants
%{_unitdir_user}/sockets.target.wants/dbus.socket
%dir %{_sysconfdir}/dbus-1
%dir %{_datadir}/dbus-1/session.d
%dir %{_datadir}/dbus-1/system.d
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/interfaces
%dir %{_datadir}/dbus-1/services
%dir %{_datadir}/dbus-1/system-services
%{_sysconfdir}/profile.d/dbus.sh
%{_prefix}/lib/sysusers.d/dbus.conf
%{_prefix}/lib/tmpfiles.d/dbus.conf
%{_sysconfdir}/resourced/vip-process.d/dbus.conf
%if "%{tizen_uid_security}" == "yes"
%{_unitdir}/user@.service.d/dbus_session_busaddr.conf
%endif

%files libs
%manifest %{name}.manifest
%license LICENSE.AFL-2.1_or_GPL-2.0+
%exclude %{_libdir}/libdbus*.so.*.extension-kdbus
%defattr(-, root, root)
%{_libdir}/libdbus-1.so.*

%files devel
%manifest %{name}.manifest
%license LICENSE.AFL-2.1_or_GPL-2.0+
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libdbus-1.so
%{_libdir}/dbus-1.0/include
%{_libdir}/pkgconfig/dbus-1.pc
%dir %{_libdir}/dbus-1.0
%{_libdir}/cmake/DBus1/DBus1Config.cmake
%{_libdir}/cmake/DBus1/DBus1ConfigVersion.cmake
%{_datadir}/xml/dbus-1/busconfig.dtd
%{_datadir}/xml/dbus-1/introspect.dtd

%files tests
%manifest %{name}.manifest
%license LICENSE.AFL-2.1_or_GPL-2.0+ LICENSE.MIT
%defattr(-,root,root)
%{_libdir}/dbus-tests/test-suites/dbus-tests
%{_libdir}/dbus-tests/runner/dbus-tests
%{_libdir}/dbus/installed-tests

%if %{with coverage}
%files coverage
%{relative_cov_lib_dir}/*
%files coverage-objects
%{relative_cov_lib_dir}/objects/*
%endif

%changelog
