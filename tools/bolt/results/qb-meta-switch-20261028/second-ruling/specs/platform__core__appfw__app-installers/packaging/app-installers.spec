Name:           app-installers
Summary:        Application installers
Version:        1.37.12
Release:        1
Group:          Application Framework/Package Management
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
Source1000:     app-installers.manifest
Source1001:     app-installers-tests.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-parser)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(security-manager)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(minizip)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(cert-svc-vcore)
BuildRequires:  pkgconfig(manifest-parser-utils)
BuildRequires:  pkgconfig(delta-manifest-handlers)
BuildRequires:  pkgconfig(security-privilege-manager)
BuildRequires:  pkgconfig(tpk-manifest-handlers)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(app2sd)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(vconf-internal-keys)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(ttrace)
BuildRequires:  pkgconfig(tanchor)
BuildRequires:  pkgconfig(libsmack)
BuildRequires:  pkgconfig(libsessiond)
BuildRequires:  pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

Requires: ca-certificates-tizen
Requires: libtzplatform-config
Requires: xdelta3
Requires(post): /usr/bin/chsmack

%define unpackdir /opt/usr/share/package-unpacked
%define rwsignaturedir /opt/share/signatures
%define rosignaturedir /usr/share/signatures
%define logdir /var/log/appfw/app-installers

%description
This is a meta package that installs the common application
installers of Tizen.

%package devel
Summary:    App-installers development files
Group:      Application Framework/Package Management
Requires:   %{name} = %{version}

%description devel
This package contains header files of app-installers common library

%package tests
Summary: Smoke tests for app-installers
Requires: %{name} = %{version}

%description tests
Smoke tests for all modules of app-installers and common utils for smoke test

%if 0%{?gcov:1}
%package gcov
Summary:    App-installers (gcov)
Group:      Application Framework/Testing

%description gcov
App-installers gcov objects
%endif

%prep
%setup -q

cp %{SOURCE1000} .
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type} \
         -DCMAKE_VERBOSE_MAKEFILE:BOOL=%{?verbose_make:ON}%{!?verbose_make:OFF} \
         -DTIZEN_FULL_VERSION=%{tizen_full_version} \
         -DUNITDIR=%{_unitdir} \
         -DUNITDIR_USER=%{_unitdir_user} \
         -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
         -DUNPACKDIR=%{unpackdir} \
         -DLOGDIR=%{logdir} \
         -DTIZEN_FEATURE_SMACK_DISABLE:BOOL=%{?dev_wos:ON}%{!?dev_wos:OFF} \
         %if 0%{?asan} != 1
           -DASAN_ENABLED=FALSE
         %else
           -DASAN_ENABLED=TRUE
         %endif

make %{?_smp_mflags}

%check
export LD_LIBRARY_PATH=../../src/common/
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
lcov -r %{name}.info  "/unit_tests/*" -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

mkdir -p %{buildroot}%{unpackdir}
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
ln -sf ../package-recovery.service %{buildroot}%{_unitdir}/multi-user.target.wants/package-recovery.service
mkdir -p %{buildroot}%{rosignaturedir}
mkdir -p %{buildroot}%{rwsignaturedir}
mkdir -p %{buildroot}%{logdir}

%post
chsmack -a System %{unpackdir}
chsmack -t -a User::Home %{logdir}
chown -R app_fw:priv_platform %{logdir}
chmod 755 %{logdir}
touch %{logdir}/installation-history.log
chown app_fw:priv_platform %{logdir}/installation-history.log
chsmack -a User::Home %{logdir}/installation-history.log

%postun

%files
%defattr(-,root,root)
%{_datarootdir}/parser-plugins/plugins_list.txt
%manifest app-installers.manifest
%{_libdir}/libapp-installers.so.*
%{_bindir}/pkgdir-tool
%{_prefix}/share/dbus-1/system-services/org.tizen.pkgdir_tool.service
%{_sysconfdir}/dbus-1/system.d/org.tizen.pkgdir_tool.conf
%{_unitdir}/pkgdir-tool.service
%{_bindir}/pkg_initdb
%attr(0755,root,root) %{_sysconfdir}/gumd/useradd.d/10_package-manager-add.post
%attr(0755,root,root) %{_sysconfdir}/gumd/userdel.d/11_package-manager-del.post
%attr(2775,app_fw,system_share) %{logdir}
%{_bindir}/pkg_recovery
%{_unitdir}/package-recovery.service
%{_unitdir}/multi-user.target.wants/package-recovery.service
%{unpackdir}
%license LICENSE
%{rosignaturedir}
%{rwsignaturedir}

%files devel
%{_includedir}/app-installers/common/*.h
%{_includedir}/app-installers/common/*/*.h
%{_includedir}/app-installers/common/*/*/*.h
%{_libdir}/pkgconfig/app-installers.pc
%{_libdir}/libapp-installers.so

%files tests
%manifest app-installers-tests.manifest
%{_bindir}/app-installers-ut/*
%{_datadir}/app-installers-ut/*
%{_libdir}/libtest-assessor-lib.so*
%{_libdir}/libsmoke-utils.so*
%{_includedir}/app-installers/smoke_tests/common/smoke_utils.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%changelog
* Tue Sep 01 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.8-1
- manifest-parser alignement; icons fixes; boost namespace cleanup
- package directories update (security policy, tmp and cache dirs)
- apps killing during update/deinstallation

* Thu Aug 27 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.7-1
- fixes: privileges list length, manifest generation, icon for tpk
- RequestMode introduction

* Fri Aug 21 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.6-1
- Icons generation fix;
- Privilege translation for backward compatilibity

* Fri Aug 21 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.5-1
- [Bug] Fix installation/deinstallation mode with smack

* Thu Aug 20 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.4-1
- WebApp encryption alignement to the libwebappenc API change
- TPK recovery, update; WGT RDS fixup; icon fixes;
- Smoke tests updated

* Tue Aug 18 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.3-1
- TPK installer exposed and TPK smoke tests added; smoke tests cleanup;
- preserving icons extensions in backup; fix deinstallation rollback
- SMACK label changed

* Fri Aug 14 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.2-1
- Account info added to manifest.xml during installation; Smoke tests added; TPK update detection

* Fri Aug 14 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.1-1
- Initial rpm changelog; Recovery (WGT) mode added, warngings cleanup; undo() can return ERROR
