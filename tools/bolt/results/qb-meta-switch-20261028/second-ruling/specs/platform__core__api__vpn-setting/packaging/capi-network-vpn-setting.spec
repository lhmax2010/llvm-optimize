%define ipsec_test yes

Name:       capi-network-vpn-setting
Summary:    Default VPN Library
Version:    0.1.5
Release:    1
Group:      System/Network
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: 	capi-network-vpn-setting.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(libtzplatform-config)

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%if 0%{?gcov:1}
BuildRequires: lcov
%endif

%if "%{ipsec_test}" == "yes"
BuildRequires:  openssl3

%global rw_app_dir %{?TZ_SYS_RW_APP:%TZ_SYS_RW_APP}%{!?TZ_SYS_RW_APP:/opt/usr/apps}
%global cert_examples %rw_app_dir/vpn-cert-examples
%define etc_dir     %{?TZ_SYS_ETC:%TZ_SYS_ETC}%{!?TZ_SYS_ETC:/opt/etc}
%define ro_etc_dir  %{?TZ_SYS_RO_ETC:%TZ_SYS_RO_ETC}%{!?TZ_SYS_RO_ETC:%_sysconfdir}
%global ca_certs_dir %{?TZ_SYS_CA_CERTS:%TZ_SYS_CA_CERTS}%{!?TZ_SYS_CA_CERTS:%etc_dir/ssl/certs}

%global host_cert_examples %etc_dir/vpn-cert-examples
%endif

%description
Library code for CAPI's to interact with the Default VPN functionality on TIZEN platform.

%package devel
Summary:  Default VPN Development Package
Group:    System/Network
Requires: %{name} = %{version}-%{release}

%description devel
Development Library for Default VPN functionality on TIZEN platform.

%package test
Summary:    Default VPN Test Package
Requires:   %{name} = %{version}

%description test
Test cases for Default VPN Functionality on TIZEN platform.

%if "%{ipsec_test}" == "yes"
%package host-cert
Summary:    Certification for host
AutoReqProv: no

%description host-cert
Certification and private key for strongswan responder
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
%if "%{ipsec_test}" == "yes"
        -DIPSEC_TEST=1 \
        -DCERT_EXAMPLES=%cert_examples \
        -DHOST_CERT_EXAMPLES=%host_cert_examples \
        -DCA_CERTS_DIR=%ca_certs_dir \
%endif
%if 0%{?gtests:1}
	-DBUILD_GTESTS=%{?gtests:1}%{!?gtests:0} \
%endif
%if 0%{?gcov:1}
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0} \
%endif
        -DFULLVER=%{version} \
        -DMAJORVER=${MAJORVER}

make %{?_smp_mflags}

%install
%make_install

%if "%{ipsec_test}" == "yes"
mkdir -p %buildroot%cert_examples
mkdir -p %buildroot%host_cert_examples
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%attr(644,-,-) %{_libdir}/libcapi-network-vpn-setting.so.*
%license LICENSE.APLv2
%if 0%{?gtests:1}
%attr(500, network_fw, network_fw) %{_bindir}/gtest*
%endif

%files devel
%manifest %{name}.manifest
#%{_includedir}/network/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-network-vpn-setting.so

%files test
%manifest %{name}.manifest
%{_bindir}/vpn_setting_test
%if "%{ipsec_test}" == "yes"
%{cert_examples}/*

%files host-cert
%{host_cert_examples}/*
%endif

