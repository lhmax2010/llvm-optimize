%global _support_weblog 0

Name:       push
Summary:    Push services and client library
Version:    0.7.6
Release:    1
Group:      Application Framework/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    pushd.service
Source2:    pushd.asan.conf
Source3:    500.push_upgrade.sh
Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/sqlite3
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(libtzplatform-config)

%if %{_support_weblog}
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(json-glib-1.0)
%endif


%description
Push services and client library.

%package -n libpush
Summary:    Push service client library
Group:      Application Framework/Libraries
Requires:   %{name}-bin = %{version}-%{release}

%description -n libpush
Push service client library

%package -n libpush-devel
Summary:    Push service client library (DEV)
Group:      Development/Libraries
Requires:   libpush = %{version}-%{release}
Requires:   capi-appfw-application-devel

%description -n libpush-devel
Push service client library (DEV)

%package bin
Summary:    Push service daemon
Group:      Application Framework/Service

%description bin
Push service daemon

%package tool
Summary:    Push service tool
Group:      Development/Tools
Requires:   libpush = %{version}-%{release}
Requires:   %{name}-bin = %{version}-%{release}

%description tool
Push service tool


%prep
%setup -q

%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/pushd.service
%install_service multi-user.target.wants pushd.service
%if "%{asan}" == "1"
mkdir -p %{buildroot}%{_unitdir}/pushd.service.d
install -m 644 %SOURCE2 %{buildroot}%{_unitdir}/pushd.service.d/pushd.asan.conf
%endif
mkdir -p %{buildroot}%{TZ_SYS_UPGRADE_SCRIPTS}
install -m 755 %{SOURCE3} %{buildroot}%{TZ_SYS_UPGRADE_SCRIPTS}

mkdir -p %{buildroot}%{_includedir}
cp -a include/push-service.h %{buildroot}%{_includedir}
cp -a include/push.h %{buildroot}%{_includedir}
%if %{_support_weblog}
	include/pushlog.h %{buildroot}%{_includedir}
%endif

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a push.pc %{buildroot}%{_libdir}/pkgconfig/
mkdir -p %{buildroot}%{_bindir}


mkdir -p %{buildroot}/usr/share/push


%ifarch armv7l

pushd armv7l/lib/
for FILE in libpush.so*; do cp -a "$FILE" "%{buildroot}%{_libdir}/$FILE"; done
popd
pushd armv7l/bin/
for FILE in push*; do cp -a "$FILE" "%{buildroot}%{_bindir}/$FILE"; done
popd
pushd armv7l/share/push/
for FILE in *.cer; do cp -a "$FILE" "%{buildroot}/usr/share/push/$FILE"; done
popd
%if %{_support_weblog}
	armv7l/bin/pushlog_tool
%endif
%endif


%ifarch armv7hl

pushd armv7hl/lib/
for FILE in libpush.so*; do cp -a "$FILE" "%{buildroot}%{_libdir}/$FILE"; done
popd
pushd armv7hl/bin/
for FILE in push*; do cp -a "$FILE" "%{buildroot}%{_bindir}/$FILE"; done
popd
pushd armv7hl/share/push/
for FILE in *.cer; do cp -a "$FILE" "%{buildroot}/usr/share/push/$FILE"; done
popd
%if %{_support_weblog}
	armv7hl/bin/pushlog_tool
%endif
%endif


%ifarch aarch64

pushd aarch64/lib64/
for FILE in libpush.so*; do cp -a "$FILE" "%{buildroot}%{_libdir}/$FILE"; done
popd
pushd aarch64/bin/
for FILE in push*; do cp -a "$FILE" "%{buildroot}%{_bindir}/$FILE"; done
popd
pushd aarch64/share/push/
for FILE in *.cer; do cp -a "$FILE" "%{buildroot}/usr/share/push/$FILE"; done
popd
%if %{_support_weblog}
	aarch64/bin/pushlog_tool
%endif
%endif


%ifarch riscv64

pushd riscv64/lib64/
for FILE in libpush.so*; do cp -a "$FILE" "%{buildroot}%{_libdir}/$FILE"; done
popd
pushd riscv64/bin/
for FILE in push*; do cp -a "$FILE" "%{buildroot}%{_bindir}/$FILE"; done
popd
pushd riscv64/share/push/
for FILE in *.cer; do cp -a "$FILE" "%{buildroot}/usr/share/push/$FILE"; done
popd
%if %{_support_weblog}
	riscv64/bin/pushlog_tool
%endif
%endif


%ifarch %{ix86}

pushd x86/lib/
for FILE in libpush.so*; do cp -a "$FILE" "%{buildroot}%{_libdir}/$FILE"; done
popd
pushd x86/bin/
for FILE in push*; do cp -a "$FILE" "%{buildroot}%{_bindir}/$FILE"; done
popd
pushd x86/share/push/
for FILE in *.cer; do cp -a "$FILE" "%{buildroot}/usr/share/push/$FILE"; done
popd
%if %{_support_weblog}
	x86/bin/pushlog_tool
%endif
%endif


%ifarch x86_64

pushd x86_64/lib64/
for FILE in libpush.so*; do cp -a "$FILE" "%{buildroot}%{_libdir}/$FILE"; done
popd
pushd x86_64/bin/
for FILE in push*; do cp -a "$FILE" "%{buildroot}%{_bindir}/$FILE"; done
popd
pushd x86_64/share/push/
for FILE in *.cer; do cp -a "$FILE" "%{buildroot}/usr/share/push/$FILE"; done
popd
%if %{_support_weblog}
	x86_64/bin/pushlog_tool
%endif
%endif


%post bin
mkdir -p %{TZ_SYS_DB}
sqlite3 %{TZ_SYS_DB}/.push.db "PRAGMA journal_mode = PERSIST; create table a(a); drop table a;" > /dev/null
chown service_fw:service_fw %{TZ_SYS_DB}/.push.db
chown service_fw:service_fw %{TZ_SYS_DB}/.push.db-journal
chmod 600 %{TZ_SYS_DB}/.push.db
chmod 600 %{TZ_SYS_DB}/.push.db-journal
chsmack -a "System" %{TZ_SYS_DB}/.push.db
chsmack -a "System" %{TZ_SYS_DB}/.push.db-journal

%post -n libpush
/sbin/ldconfig

%postun -n libpush -p /sbin/ldconfig

%files -n libpush
%manifest libpush.manifest
%license LICENSE
%attr(755,root,root) %{_libdir}/libpush.so.*

%files -n libpush-devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libpush.so

%files bin
%manifest push-bin.manifest
%{_bindir}/pushd
%attr(644,service_fw,service_fw) /usr/share/push/*.cer
%license LICENSE
%attr(755,-,-) %{TZ_SYS_UPGRADE_SCRIPTS}/500.push_upgrade.sh

%{_unitdir}/pushd.service
%{_unitdir}/multi-user.target.wants/pushd.service
%if "%{asan}" == "1"
%{_unitdir}/pushd.service.d/pushd.asan.conf
%endif

%files tool
%manifest push-tool.manifest
%{_bindir}/push_tool

%if %{_support_weblog}
	%{_bindir}/pushlog_tool
%endif



%changelog
* Sat Nov 3 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.26
- Prevent bug fixed(out-of bounds read, dead code,..)
* Mon Oct 22 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.25
- bundle null check added & protobuf null check added
* Wed Sep 19 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.24
- when pkg is uninstalled, db process is added
* Fri Sep 7 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.23
- emul check logic is changed(using capi-system-info)
* Tue Sep 4 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.22
- decoding of message with space character which is urlencoded to "+"
* Wed Aug 29 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.21
- package uninstalled event added
* Fri Aug 17 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.20
- debug msg added & some internal function name changed
* Wed Aug 8 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.19
- push noti default action is silent, and old key is deleted
* Wed Aug 8 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.18
- tapi imei api is changed for new tapi
* Tue Aug 7 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.17
- emulator check func is added
* Wed Jul 25 2012 Jooseok Park <jooseok.park@samsung.com> - 0.2.16
- OSP Push noti support(alertMessage,..)

