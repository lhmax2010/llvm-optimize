%define on_off() %{expand:%%{?with_%{1}:ON}%%{!?with_%{1}:OFF}}


%if "%{?profile}" == "tv"
%undefine _with_tests
%else
%if "%{_arch}" == "aarch64"
%define _with_tests on
%endif
%endif

%bcond_with tests

%define libisu_version 0.0.2
%define liblscm_version 0.0.1
%define integration_tests_dir /usr/libexec/isu/
%define unit_tests_dir /usr/libexec/isu/
Summary: Individual Service Upgrade support
Name:    isu
Version: 9.0.6
Release: 1
Source0: %{name}-%{version}.tar.gz
License: MIT and Apache-2.0 and LGPL-2.1
Requires:       isu-plugin-parser = %{version}-%{release}
Requires:       isu-tools = %{version}-%{release}
BuildRequires:  cmake
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(dlogutil)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(mount)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  systemd-devel
BuildRequires:  cmocka-devel cmocka
BuildRequires:  pkgmgr-client-devel
%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%else
%define gcov 0
%endif

%{?_toolchain:
%if %{toolchain_is clang}
%ifarch aarch64
BuildRequires:  compiler-rt
%endif
%endif
}

%description
Individual Service Upgrade is Tizen mechanism used to allow extending
(replacing) system services found on read-only root file system via
specially prepared packages from read-writeable medium.
.
ISU uses systemd.generator(7) mechanism to install systemd services
from extension packages and modified bubblewrap to run service in
partially sandboxed environment.

%package -n     libisu
Summary:        ISU API library
%description -n libisu
Provies ISU API library

%package -n     ablc
Summary:        ablc
%description -n ablc
Provies ISU ablc binary

%package -n     libisu-devel
Summary:        Package provides headers needed to develop programs using ISU API
%description -n libisu-devel

%package -n     isu-plugin-parser
Summary:        Package provides package manager parser plugin to install ISU packages.
%description -n isu-plugin-parser

%package        tools
Summary:        Package provides tools to generate ISU packages
%description    tools

%if %{with tests}
%package        tests
Summary:        Package provides tools to test ISU
%description    tests
%endif

%package -n     liblscm
Summary:        Package provides a library to build custom ld.so.cache file
%description -n liblscm

%package -n     liblscm-devel
Summary:        Package provides a headers needed to develop programs using liblscm
Requires:       liblscm
%description -n liblscm-devel

%package -n     lscm
Summary:        Package provides a tool to build custom ld.so.cache file
Requires:       liblscm
%description -n lscm

%prep
%setup -q

%build
cp packaging/isu.manifest .

%cmake . \
       -DCMAKE_INSTALL_PREFIX=%{_prefix} \
       -DLIBISU_VERSION=%{libisu_version} \
       -DLIBLSCM_VERSION=%{liblscm_version} \
       -DCHECK_ISU_FEATURE=OFF \
       -DISU_INTEGRATION_TESTS_DIR=%{integration_tests_dir} \
       -DISU_UNIT_TESTS_DIR=%{unit_tests_dir} \
       -DENABLE_TESTS=%{on_off tests} \
       -DENABLE_COVERAGE=%{gcov}
make %{?_smp_mflags}
%if %{with tests}
echo "%{_arch}"
make ctest
%endif

%install
rm -rf %{buildroot}
%make_install

mkdir -p %{buildroot}/usr/libexec
mkdir -p %{buildroot}/usr/lib/systemd/system-generators
mkdir -p %{buildroot}/usr/lib/systemd/user-generators
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
mkdir -p %{buildroot}/etc/isu
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{integration_tests_dir}
install -m755 src/systemd_generator/isu-generator %{buildroot}/usr/libexec/
ln -s ../../../libexec/isu-generator %{buildroot}/usr/lib/systemd/system-generators/isu-system-generator
ln -s ../../../libexec/isu-generator %{buildroot}/usr/lib/systemd/user-generators/isu-user-generator
install -m644 -D src/helpers/service-common.inc %{buildroot}/etc/isu/service-common.inc
install -m644 -D src/helpers/user-service-common.inc %{buildroot}/etc/isu/user-service-common.inc
install -m644 config/isu.conf %{buildroot}/usr/lib/tmpfiles.d/isu.conf
install -m644 config/upgrade.cfg %{buildroot}/etc/isu/upgrade.cfg
install -m755 src/upgrade/701.isu.sh %{buildroot}/usr/share/upgrade/scripts/701.isu.sh
%if %{with tests}
install -m755 tests/integration/isu-integration-tests.sh %{buildroot}/%{integration_tests_dir}/isu-integration-tests.sh
install -m755 tests/integration/test_isu_package/isu-integration-tests.rpk %{buildroot}/%{integration_tests_dir}/isu-integration-tests.rpk
%endif

%install_service delayed.target.wants isud.service ablc.service
%install_service delayed.target.wants ablc.service

%files
%manifest isu.manifest
%license LICENSE.MIT LICENSE.APLv2
/usr/libexec/isu-generator
/usr/lib/systemd/user-generators/isu-user-generator
/usr/lib/systemd/system-generators/isu-system-generator
/usr/lib/tmpfiles.d/isu.conf
/etc/isu/service-common.inc
/etc/isu/user-service-common.inc
/etc/isu/upgrade.cfg
%{_bindir}/isu
%{_bindir}/isud
%{_bindir}/ablc
%{_bindir}/.boot_status
%attr(-,root,root) /etc/dbus-1/system.d/isud.conf
%attr(-,root,root) %{_unitdir}/isud.service
%attr(-,root,root) %{_unitdir}/ablc.service
%attr(-,root,root) %{_datadir}/dbus-1/system-services/org.tizen.system.isu.service
%{_unitdir}/delayed.target.wants/isud.service
%{_unitdir}/delayed.target.wants/ablc.service
/usr/share/upgrade/scripts/701.isu.sh

%files tools
%manifest isu.manifest
%license LICENSE.MIT
%{_bindir}/isu_pkgs_maker.py
%{_bindir}/isu_pkgs_maker_py2.py

%files -n libisu
%manifest isu.manifest
%license LICENSE.APLv2
%{_libdir}/libisu.so.*

%files -n libisu-devel
%manifest isu.manifest
%license LICENSE.APLv2
%{_libdir}/libisu.so
%{_includedir}/libisu.h
%{_includedir}/libisu-internal.h
%{_libdir}/pkgconfig/libisu.pc

%files -n isu-plugin-parser
%manifest isu.manifest
%license LICENSE.MIT
/etc/package-manager/parserlib/libisu-parser.so*
/usr/share/parser-plugins/isu-parser.info

%files -n lscm
%manifest isu.manifest
%license LICENSE.LGPL2.1
%{_bindir}/ld_so_cache_maker

%files -n liblscm
%manifest isu.manifest
%license LICENSE.LGPL2.1
%{_libdir}/liblscm.so.*

%files -n liblscm-devel
%manifest isu.manifest
%license LICENSE.MIT
%{_libdir}/liblscm.so
%{_libdir}/pkgconfig/liblscm.pc
%{_includedir}/lscm.h

%if %{with tests}
%files tests
%{integration_tests_dir}/isu-integration-tests.sh
%{integration_tests_dir}/isu-integration-tests.rpk
%{unit_tests_dir}/test_libisu
%{unit_tests_dir}/test_libisu_internal
%endif
