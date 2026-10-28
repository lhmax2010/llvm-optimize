%{!?build_type:%global build_type RELEASE}

Name:    cert-svc
Summary: Certification service
Version: 3.0.0
Release: 0
Group:   Security/Certificate Management
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: coreutils
BuildRequires: findutils
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(klay)
BuildRequires: openssl3
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(libpcrecpp)
BuildRequires: pkgconfig(xmlsec1)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(key-manager)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: ca-certificates
BuildRequires: ca-certificates-devel
BuildRequires: ca-certificates-tizen-devel
BuildRequires: boost-devel

%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%endif

Requires: ca-certificates
Requires: ca-certificates-tizen
Requires: security-config
# to prevent auto require lower version of libc including examples/resource/player/bin/player
# https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering?rd=PackagingDrafts/AutoProvidesAndRequiresFiltering
%global __requires_exclude_from examples/


%global user_name security_fw
%global group_name security_fw
%global smack_domain_name System
%global coverage_dir    %{_datadir}/cert-svc-coverage

%global bin_dir                 %{?TZ_SYS_BIN:%TZ_SYS_BIN}%{!?TZ_SYS_BIN:%_bindir}
%global lib_dir                 %{?TZ_SYS_LIB:%TZ_SYS_LIB}%{!?TZ_SYS_LIB:%_libdir}
%global etc_dir                 %{?TZ_SYS_ETC:%TZ_SYS_ETC}%{!?TZ_SYS_ETC:/opt/etc}
%global rw_data_dir             %{?TZ_SYS_SHARE:%TZ_SYS_SHARE}%{!?TZ_SYS_SHARE:/opt/share}
%global ro_data_dir             %{?TZ_SYS_RO_SHARE:%TZ_SYS_RO_SHARE}%{!?TZ_SYS_RO_SHARE:%_datadir}
%global rw_app_dir              %{?TZ_SYS_RW_APP:%TZ_SYS_RW_APP}%{!?TZ_SYS_RW_APP:/opt/usr/apps}

%global cert_svc_ro_path        %ro_data_dir/cert-svc
%global cert_svc_examples       %cert_svc_ro_path/examples
%global cert_svc_tests          %rw_app_dir/cert-svc-tests

%description
Certification service

%package devel
Summary:    Certification service (development files)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Certification service (development files)

%package test
Summary:  Certification service (tests)
Group:    Security/Testing
Requires: ca-certificates-tizen
Requires: %{name} = %{version}-%{release}
Requires: %{name}-test-binaries = %{version}-%{release}

%description test
Certification service (tests)

%package test-binaries
Summary:  Certification service (test binaries)
Group:    Security/Testing
AutoReq:  no
Requires: %{name}-test = %{version}-%{release}

%description test-binaries
Certification service (test binaries)

%if "%{build_type}" == "COVERAGE"
%package coverage
Summary:    Certification service code coverage data
Group:      Security/Testing
Requires:   cert-svc-test = %{version}-%{release}
Requires:   cert-svc-debugsource = %{version}-%{release}
Requires:   lcov
Requires:   gcc

%description coverage
Certification service code coverage data
%endif

%prep
%setup -q

%build
%if 0%{?tizen_build_devel_mode}
export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"
%endif

%ifarch %{ix86}
export CFLAGS="$CFLAGS -DTIZEN_EMULATOR_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_EMULATOR_MODE"
export FFLAGS="$FFLAGS -DTIZEN_EMULATOR_MODE"
%endif

# gcc v9 and new Tizen toolchain adds Wall and this code pretty much always checks string & buffer lenghts

%{!?_toolchain:
export CFLAGS="$CFLAGS -Wno-stringop-truncation -Wno-stringop-overflow"
export CXXFLAGS="$CXXFLAGS -Wno-stringop-truncation -Wno-stringop-overflow"
}

%{?_toolchain:
%if %{toolchain_is gcc}
export CFLAGS="$CFLAGS -Wno-stringop-truncation -Wno-stringop-overflow"
export CXXFLAGS="$CXXFLAGS -Wno-stringop-truncation -Wno-stringop-overflow"
%endif
}


%cmake . -DVERSION=%version \
         -DINCLUDEDIR=%_includedir \
         -DUSER_NAME=%user_name \
         -DGROUP_NAME=%group_name \
         -DSMACK_DOMAIN_NAME=%smack_domain_name \
         -DRO_DATA_DIR=%ro_data_dir \
         -DBIN_DIR=%bin_dir \
         -DLIB_DIR=%lib_dir \
         -DTZ_SYS_CA_CERTS=%TZ_SYS_CA_CERTS \
         -DCERT_SVC_RO_PATH=%cert_svc_ro_path \
         -DCERT_SVC_TESTS=%cert_svc_tests \
         -DCERT_SVC_EXAMPLES=%cert_svc_examples \
         -DCOVERAGE_DIR=%{coverage_dir} \
         -DCMAKE_BUILD_TYPE=%build_type \
         -DSYSTEMD_UNIT_DIR=%_unitdir

make %{?_smp_mflags}

%install
%make_install


%files
%manifest %name.manifest
%license LICENSE
%_libdir/libcert-svc-vcore.so.*
%attr(-, %{user_name}, %{group_name}) %cert_svc_ro_path/schema.xsd

%files devel
%manifest %name.manifest
%_includedir/*
%_libdir/pkgconfig/*
%_libdir/libcert-svc-vcore.so

%files test
%manifest %name.manifest
%bin_dir/cert-svc-test*
%dir %cert_svc_tests
%cert_svc_tests/certs
%cert_svc_tests/unit_test_data
%_libdir/libcert-svc-validator-plugin.so

%bin_dir/cert-svc-example*
%cert_svc_examples

%bin_dir/cert-svc-unit-tests

%files test-binaries
%manifest %name.manifest
%cert_svc_tests/apps

%if "%{build_type}" == "COVERAGE"
%files coverage
%manifest %{name}.manifest
%license LICENSE
%{bin_dir}/cert-svc-coverage.sh
%coverage_dir
%endif
