Name:       tizen-watcher
Summary:    Tizen Watcher
Version:    1.0.17
Release:    1
Group:      Application Framework/Application Launcher
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}d.service
Source1003: %{name}d.socket
BuildRequires:  cmake
BuildRequires:  tidl
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-libopener)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-parser)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(gtest)

%if 0%{?with_examples:1}
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-appfw-app-control)
%endif

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Tizen Watcher library and daemon provides functions to trigger actions.

%package devel
Summary:  Tizen Watcher Library (Development)
Requires: %{name} = %{version}

%description devel
Tizen Watcher library provides functions to trigger actions.

%if 0%{?with_examples:1}
%package -n tizen-watcher-example
Summary:  Tizen Watcher example
Requires: %{name} = %{version}

%description -n tizen-watcher-example
Tizen Watcher Example Package
%endif

%if 0%{?gcov:1}
%package gcov
Summary:  Tizen Watcher (gcov)

%description gcov
Tizen Watcher gcov objects
%endif

%define logdir /var/log/appfw/tizen-watcher

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .
/bin/bash ./tidl/prebuild.sh

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
%if 0%{?asan:1}
export CXXFLAGS+=" -Wno-maybe-uninitialized"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_VERBOSE_MAKEFILE:BOOL=%{?verbose_make:ON}%{!?verbose_make:OFF} \
         -DUNITDIR=%{_unitdir} \
         -DFULLVER=%{version} \
         -DMAJORVER=${MAJORVER} \
         -DLOGDIR=%{logdir} \
         -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
         -DWITH_EXAMPLES=%{?with_examples:ON}%{!?with_examples:OFF} \
         %if 0%{?asan} != 1
          -DASAN_ENABLED=FALSE
         %else
          -DASAN_ENABLED=TRUE
         %endif

%__make %{?_smp_mflags}

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 755 -d %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1002} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1003} %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_unitdir}/sysinit.target.wants
ln -sf ../%{name}d.service %{buildroot}%{_unitdir}/sysinit.target.wants/%{name}d.service

mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
ln -sf ../%{name}d.socket %{buildroot}%{_unitdir}/sockets.target.wants/%{name}d.socket

mkdir -p %{buildroot}%{logdir}

%check
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors graph,mismatch,unused,inconsistent --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o %{name}.out --legend --show-details
zip -r %{name}.zip %{name}.out
mkdir -p %{buildroot}%{_datadir}/gcov/
install -m 0644 %{name}.zip %{buildroot}%{_datadir}/gcov/
%endif

%post
# setgid: logs recreated by rotation must inherit the collector's group.
chmod 2755 %{logdir}
chsmack -t -a User::Home %{logdir}
chown -R app_fw:priv_platform %{logdir}
touch %{logdir}/tizen-watcherd.log
chown app_fw:priv_platform %{logdir}/tizen-watcherd.log
chsmack -a User::Home %{logdir}/tizen-watcherd.log

touch %{logdir}/plugin-loader.log
chown app_fw:priv_platform %{logdir}/plugin-loader.log
chsmack -a User::Home %{logdir}/plugin-loader.log

touch %{logdir}/fault-report.log
chown app_fw:priv_platform %{logdir}/fault-report.log
# Not world readable: the report carries module load addresses and build ids.
chmod 0640 %{logdir}/fault-report.log
chsmack -a User::Home %{logdir}/fault-report.log

/sbin/ldconfig
if [ $1 -eq 2 ]; then
  systemctl daemon-reload
fi
systemctl restart %{name}d.service
systemctl restart %{name}d.socket

%preun
if [ $1 -eq 0 ]; then
  systemctl stop %{name}d
fi

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  systemctl daemon-reload
fi

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/%{name}d
%{_bindir}/%{name}-util
%{_unitdir}/%{name}d.service
%{_unitdir}/sysinit.target.wants/%{name}d.service
%{_unitdir}/%{name}d.socket
%{_unitdir}/sockets.target.wants/%{name}d.socket
%{_libdir}/lib%{name}.so.*
%{_sysconfdir}/package-manager/parserlib/metadata/libtizen-watcher-plugin.so
%{_datarootdir}/parser-plugins/tizen-watcher-plugin.info
%attr(2775,app_fw,system_share) %{logdir}

%files devel
%manifest %{name}.manifest
%{_libdir}/lib%{name}.so
%{_includedir}/tizen-watcher/*.h
%{_libdir}/pkgconfig/%{name}.pc

%if 0%{?with_examples:1}
# Signing
%define tizen_sign_base %{_prefix}/apps/org.tizen.watcher-example:%{_prefix}/apps/org.tizen.watcher-systemd-example:%{_prefix}/apps/org.tizen.watcher-tpk-example
%define tizen_sign 1
%define tizen_author_sign 1
%define tizen_dist_sign 1
%define tizen_sign_level platform

%files -n tizen-watcher-example
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_prefix}/apps/org.tizen.watcher-example/*
%{_datadir}/packages/org.tizen.watcher-example.xml
%{_prefix}/apps/org.tizen.watcher-systemd-example/*
%{_datadir}/packages/org.tizen.watcher-systemd-example.xml
%{_prefix}/apps/org.tizen.watcher-tpk-example/*
%{_datadir}/packages/org.tizen.watcher-tpk-example.xml
%endif

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
