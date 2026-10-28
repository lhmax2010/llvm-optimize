%if "%{_with_da_profile}" == "1"
%define WITH_DA 1
%else
%define WITH_DA 0
%endif

Name:           libdbuspolicy
Summary:        Helper library for fine-grained userspace policy handling
License:        MIT
Group:          Base/IPC
Version:        1.2.0
Release:        0
Source:         %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest
Source2001:     libdbuspolicy-verify-data.target
Source2002:     libdbuspolicy-verify-data.service
BuildRequires:  boost-devel
BuildRequires:  libexpat-devel
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(openssl3)
BuildRequires:  pkgconfig(cynara-creds-self)
%if %{WITH_DA} == 0
BuildRequires:  linux-tizen-modules-headers
%endif
Requires:       %{name}-serializer

%package devel
License:        MIT and LGPL-2.1+
Summary:        Helper library for fine-grained userspace policy handling-development package
%if %{WITH_DA} == 0
# NB: The following is because we want libdbuspolicy-devel to provide the Tizen kernel headers directly.
# This way, installing this package provides a complete kdbus development environment.
Requires:       linux-tizen-modules-headers
%endif

%package serializer
Summary:        Tool to serialize dbus policy

%package assert-data-valid
Requires:       %{name}-serializer
Summary:        Systemd units to perform boot-time serialized data verification

%package tests
Summary:        Helper library for fine-grained userspace policy handling-development package
Requires:       %{name} = %{version}

%description
libdbuspolicy is a helper library for fine-grained userspace
policy handling (with SMACK support)

%description devel
libdbuspolicy is a helper library for fine-grained userspace
policy handling (with SMACK support). This package contains
development files.

%description serializer
dbuspolicy-serializer is a tool to serialize dbus policy

%description assert-data-valid
Perform boot-time serialized data verification, fail the boot if vierification fails
.
Note that installing this package actually replaces systemd default.target. Use with care.

%description tests
This package contains contains integration tests for libdbuspolicy.

%if 0%{?enable_doxygen:1}
%package doc
Summary:        Documentation for libdbuspolicy
BuildRequires:	doxygen

%description doc
Doxygen documentation for libdbuspolicy.
%endif

%define testsdirname %{name}-tests
%define runnername %{testsdirname}
%define dbustestsdir %{_libdir}/dbus-tests

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE2001} ./libdbuspolicy-verify-data.target
cp %{SOURCE2002} ./libdbuspolicy-verify-data.service

%if %{WITH_DA} == 0
# When building libdbuspolicy, the header files are configured to prioritize
# the src directory. As a result, it references the kdbus.h within the package
# instead of the kdbus.h located in linux-tizen-modules-headers.
# If linux-tizen-modules-headers can be used, remove the kdbus.h in the package.
rm -f src/linux/kdbus.h
%endif

%build
%reconfigure --libdir=%{_libdir}	--prefix=/usr --enable-tests \
%if 0%{?enable_doxygen:1}
--enable-doxygen
%endif
make configure
make %{?_smp_mflags}
make %{?_smp_mflags} all-tests
make %{?_smp_mflags} check

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
rm %{buildroot}%{_libdir}/libdbuspolicy1.la

%define testconfigsdir %{dbustestsdir}/configs/%{testsdirname}
%define btestconfigsdir %{buildroot}%{testconfigsdir}
mkdir -p %{btestconfigsdir}
libtool --mode=install install -m 0644 tests/default_allow/system.conf %{btestconfigsdir}

%define testconfigsystemddir %{testconfigsdir}/system.d
%define btestconfigsystemddir %{buildroot}%{testconfigsystemddir}
mkdir -p %{btestconfigsystemddir}
libtool --mode=install install -m 0644 tests/default_allow/system.d/ownerships.test.conf %{btestconfigsystemddir}
libtool --mode=install install -m 0644 tests/default_allow/system.d/signals.test.conf %{btestconfigsystemddir}
libtool --mode=install install -m 0644 tests/default_allow/system.d/methods.test.conf %{btestconfigsystemddir}
libtool --mode=install install -m 0644 tests/default_allow/system.d/cynara.test.conf %{btestconfigsystemddir}

%define testsuitedir %{dbustestsdir}/test-suites/%{testsdirname}
%define btestsuitedir %{buildroot}%{testsuitedir}
mkdir -p %{btestsuitedir}
libtool --mode=install install -m 0755 src/cynara_prepare.sh %{btestsuitedir}
libtool --mode=install install -m 0755 stest_* dbus_daemon %{btestsuitedir}

%define testrunnerdir %{dbustestsdir}/runner
%define btestrunnerdir %{buildroot}%{testrunnerdir}
mkdir -p %{btestrunnerdir}
libtool --mode=install install -m 0755 %{runnername} %{btestrunnerdir}

mkdir -p -m755 %{buildroot}%{_unitdir}
install -m644 libdbuspolicy-verify-data.target %{buildroot}/%{_unitdir}/
install -m644 libdbuspolicy-verify-data.service %{buildroot}/%{_unitdir}/

%if %{WITH_DA} == 1
mkdir -p -m755 %{buildroot}%{_includedir}/linux/
install -m644 src/linux/kdbus.h %{buildroot}%{_includedir}/linux/
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%posttrans assert-data-valid
rm -f %{_unitdir}/.%{name}.backup.default.target
mv %{_unitdir}/default.target %{_unitdir}/.%{name}.backup.default.target
ln -sf libdbuspolicy-verify-data.target %{_unitdir}/default.target

%preun assert-data-valid
rm -f %{_unitdir}/default.target
mv %{_unitdir}/.%{name}.backup.default.target %{_unitdir}/default.target

%files
%manifest %{name}.manifest
%license LICENSE.MIT
%defattr(-,root,root)
%{_libdir}/libdbuspolicy1.so.*

%files devel
%manifest %{name}.manifest
%license LICENSE.MIT LICENSE.LGPL2.1
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libdbuspolicy1.so

%files serializer
%manifest %{name}.manifest
%license LICENSE.MIT
%defattr(-,root,root)
%{_bindir}/dbuspolicy-serializer
%{_bindir}/dbuspolicy-printer
%{_bindir}/dbuspolicy-finder

%files assert-data-valid
%manifest %{name}.manifest
%license LICENSE.MIT
%{_unitdir}/libdbuspolicy-verify-data.target
%{_unitdir}/libdbuspolicy-verify-data.service
%{_bindir}/dbuspolicy-verifier

%if 0%{?enable_doxygen:1}
%files doc
%license LICENSE.MIT
%defattr(-,root,root)
%{_datadir}/doc/dbuspolicy/*
%endif
%changelog

%files tests
%license LICENSE.MIT
%defattr(-,root,root)
%{testrunnerdir}/%{runnername}
%{testsuitedir}/*
%{testconfigsdir}/*
