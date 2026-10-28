%define dbdir %{_localstatedir}/lib/%{name}
%define basedbdir %{_sysconfdir}/%{name}
%define upgrade_script_path /usr/share/upgrade/scripts

Name:           buxton2
Version:        1.9.15
Release:        0
License:        Apache-2.0
Summary:        A security-enabled configuration system
Group:          System/Configuration
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}.conf
Source2:        %{name}.service
Source3:        %{name}.socket
Source4:        %{name}.tmpfiles.conf
Source1001:     %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(cynara-client-async)
BuildRequires:  pkgconfig(cynara-creds-pid)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-uid)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(libsessiond)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(sqlite3)
Requires:       security-config
Requires(post): /usr/bin/getent
Requires(post): /usr/bin/chown
Requires(post): /usr/sbin/useradd
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/bin/chsmack
Requires(posttrans): /usr/bin/chsmack
Requires(posttrans): /usr/bin/chmod
Obsoletes:      buxton
Provides:       buxton

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Buxton is a security-enabled configuration management system. It
features a layered approach to configuration storage, with each
layer containing key-value pairs. Mandatory Access Control (MAC) is
implemented at the key-value level. Cynara is used as default for MAC.

Buxton provides a C library (libbuxton) for client applications to
use. Internally, buxton uses a daemon (buxtond) for processing
client requests and enforcing MAC. Also, a CLI (buxtonctl) is
provided for interactive use and for use in shell scripts.

%package devel
Summary: A security-enabled configuration system - development files
Requires: %{name} = %{version}

%description devel
Buxton is a security-enabled configuration management system. It
features a layered approach to configuration storage, with each
layer containing key-value pairs. Mandatory Access Control (MAC) is
implemented at the key-value level. Cynara is used as default for MAC.

Buxton provides a C library (libbuxton) for client applications to
use. Internally, buxton uses a daemon (buxtond) for processing
client requests and enforcing MAC. Also, a CLI (buxtonctl) is
provided for interactive use and for use in shell scripts.

This package provides development files for Buxton.


%package -n vconf-compat
Summary:       buxton wrapper for vconf APIs
Requires:      %{name} = %{version}
Requires:      /usr/bin/getopt
Obsoletes:     vconf-buxton
Obsoletes:     vconf
Obsoletes:     vconf-keys
Provides:      vconf-buxton
Provides:      vconf
Provides:      vconf-keys

%description -n vconf-compat
Buxton wrapper library for providing vconf APIs


%package -n vconf-compat-devel
Summary:       buxton wrapper for vconf APIs (devel)
Requires:      vconf-compat = %{version}
Requires:      vconf-internal-keys-devel
BuildRequires: pkgconfig(vconf-internal-keys)
Obsoletes:     vconf-buxton-devel
Obsoletes:     vconf-buxton-keys-devel
Obsoletes:     vconf-devel
Obsoletes:     vconf-keys-devel
Provides:      vconf-buxton-devel
Provides:      vconf-buxton-keys-devel
Provides:      vconf-devel
Provides:      vconf-keys-devel

%description -n vconf-compat-devel
Buxton wrapper library for providing vconf APIs (devel)

%if 0%{?gcov:1}
%package gcov
Summary:  buxton wrapper for vconf APIs (gcov)
Group:    Application Framework/API

%description gcov
gcov objects for a buxton2 library
%endif

%package unittests
Summary:    %{name} unittests binary

%description unittests
unittests binary

%prep
%setup -q
cp %{SOURCE1001} .

%build

# for Address space layout randomization
export CFLAGS="$CFLAGS -fPIE "
export LDFLAGS="$LDFLAGS -pie"

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

%cmake -DVERSION=%{version} \
	-DCONFPATH:PATH=%{_sysconfdir}/%{name}.conf \
	-DMODULE_DIR:PATH=%{_libdir}/%{name} \
	-DBASE_DB_DIR:PATH=%{basedbdir} \
	-DDB_DIR:PATH=%{_localstatedir}/lib/%{name} \
	-DTMPFS_DIR:PATH=/run/%{name} \
	-DSOCKPATH:PATH=/run/%{name}-0 \
	-DNDEBUG:BOOL=FALSE \
	-DDEBUG_LOG:BOOL=FALSE \
	.

%__make %{?_smp_mflags}

%install
%make_install

# create the database directory
install -m 700 -d %{buildroot}%{basedbdir}
install -m 700 -d %{buildroot}%{_localstatedir}/lib/%{name}

# install config file
install -m 755 -d %{buildroot}%{_sysconfdir}
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf

# install systemd unit files
install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.socket
install -m 755 -d %{buildroot}%{_tmpfilesdir}
install -m 644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/%{name}.conf

install -m 755 -d %{buildroot}%{_unitdir}/basic.target.wants
ln -sf ../%{name}.service %{buildroot}%{_unitdir}/basic.target.wants/

# enable socket activation
install -m 755 -d %{buildroot}%{_unitdir}/sockets.target.wants
ln -sf ../%{name}.socket %{buildroot}%{_unitdir}/sockets.target.wants/

mkdir -p %{buildroot}%{upgrade_script_path}
cp -f scripts/990.buxton2_upgrade.sh %{buildroot}%{upgrade_script_path}

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
    /usr/bin/buxton2-unit-test
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

%check
export LD_LIBRARY_PATH=../../vconf-compat:../../lib
ctest -V

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post
/sbin/ldconfig

# buxtond runs as user buxton of group buxton
# create it on need!
getent group buxton > /dev/null || groupadd -r -g 375 buxton 2> /dev/null
getent passwd buxton > /dev/null || useradd -c "buxton" -u 375 -g 375 \
		                            -s /sbin/nologin -r -d /var/lib/empty buxton 2> /dev/null

# The initial DBs will not have the correct labels and
# permissions when created in postinstall during image
# creation, so we set these file attributes here.
chown -R buxton:buxton "%{basedbdir}"
chsmack -a System "%{basedbdir}"
chsmack -t "%{basedbdir}"

chown -R buxton:buxton "%{dbdir}"
chsmack -a System "%{dbdir}"
chsmack -t "%{dbdir}"

%posttrans
chown -R buxton:buxton "%{basedbdir}"
chmod 0600 %{basedbdir}/*
chsmack -a System %{basedbdir}/*

chown -R buxton:buxton "%{dbdir}"
chmod 0600 %{dbdir}/*
chsmack -a System %{dbdir}/*

%postun -p /sbin/ldconfig

%post -n vconf-compat -p /sbin/ldconfig

%postun -n vconf-compat -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(0750,root,system_share) %{_bindir}/buxton2ctl
%{_sbindir}/buxton2d
%{_libdir}/%{name}/*.so
%{_libdir}/libbuxton2.so.*
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/sockets.target.wants/%{name}.socket
%{_unitdir}/basic.target.wants/%{name}.service
%attr(0700,buxton,buxton) %dir %{_localstatedir}/lib/%{name}
%attr(0700,buxton,buxton) %dir %{basedbdir}
%attr(0750,root,root) %{upgrade_script_path}/990.buxton2_upgrade.sh
%attr(0750,root,root) /opt/etc/dump.d/module.d/buxton_dump.sh

%files devel
%manifest %{name}.manifest
%{_includedir}/buxton2.h
%{_libdir}/libbuxton2.so
%{_libdir}/pkgconfig/buxton2.pc

%files -n vconf-compat
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%attr(0750,root,system_share) %{_bindir}/vconftool
%{_libdir}/libvconf.so.*

%files -n vconf-compat-devel
%manifest %{name}.manifest
%{_includedir}/vconf/vconf.h
%{_includedir}/vconf/vconf-keys.h
%{_libdir}/libvconf.so
%{_libdir}/pkgconfig/vconf.pc

%files unittests
%attr(0755,root,root) %{_bindir}/buxton2-unit-test
%attr(0755,root,root) %{_bindir}/tizen-unittests/%{name}/run-unittest.sh


%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
