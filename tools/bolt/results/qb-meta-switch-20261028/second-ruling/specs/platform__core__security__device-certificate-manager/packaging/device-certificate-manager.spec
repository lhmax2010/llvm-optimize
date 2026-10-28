%{!?build_type:%global build_type RELEASE}

Name: device-certificate-manager
Summary: Device Certificate Manager daemon and libraries
Version: 3.0.1
Release: 0
Group: Security/Secure Storage
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: device-certificate-manager.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(protobuf-lite)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-creds-socket)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(hal-api-security)
BuildRequires: pkgconfig(openssl3)
BuildRequires: boost-devel
%if "%{build_type}" == "COVERAGE"
BuildRequires: lcov
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires: boost-system
%{?systemd_requires}

%global user_name		security_fw
%global group_name		security_fw
%global smack_domain_name	System
%global coverage_dir		%{_datadir}/device-certificate-manager-coverage

%description
Device Certificate Manager provides cryptography services for the Iotivity framework.

%package -n device-certificate-manager-devel
Summary:	Device Certificate Manager (development)
Group:		Security/Development
Requires:	device-certificate-manager = %{version}-%{release}

%description -n device-certificate-manager-devel
Device Certificate Manager development headers and libraries

%package -n device-certificate-manager-ext-devel
Summary:	Device Certificate Manager (development/extension API)
Group:		Security/Development
Requires:	device-certificate-manager = %{version}-%{release}

%description -n device-certificate-manager-ext-devel
Device Certificate Manager development headers and libraries only for extension of the API

%package -n device-certificate-manager-tests
Summary:	Internal tests for Device Certificate Manager
Group:		Security/Testing
License:	Apache-2.0 and BSL-1.0
BuildRequires: pkgconfig(security-manager)
BuildRequires: pkgconfig(openssl3)
Requires:	device-certificate-manager = %{version}-%{release}
Requires:	boost-test
Requires(post): /usr/bin/system-info-tool
Requires(postun): /usr/bin/system-info-tool

%description -n device-certificate-manager-tests
Internal tests for Device Certificate Manager

%if "%{build_type}" == "COVERAGE"

%package -n device-certificate-manager-coverage
Summary:	Device Certificate Manager code coverage data
Group:		Security/Testing
Requires:	device-certificate-manager-tests = %{version}-%{release}
Requires:	device-certificate-manager-debugsource = %{version}-%{release}
Requires:	lcov
Requires:	gcc

%description -n device-certificate-manager-coverage
Device Certificate Manager code coverage data

%endif

%prep
%setup -q
cp -a %{SOURCE1001} .

%build
%cmake . -DCMAKE_BUILD_TYPE=%{build_type} \
	-DSYSTEMD_UNIT_DIR=%{_unitdir} \
	-DUSER_NAME=%{user_name} \
	-DGROUP_NAME=%{group_name} \
	-DSMACK_DOMAIN_NAME=%{smack_domain_name} \
	-DCOVERAGE_DIR=%{coverage_dir}

make

%install
%make_install
%install_service sockets.target.wants device-certificate-manager.socket

%post
/sbin/ldconfig
systemctl daemon-reload
if [ $1 = 1 ]; then
	# installation
	systemctl start device-certificate-manager.socket device-certificate-manager.service
fi

if [ $1 = 2 ]; then
	# update
	systemctl stop device-certificate-manager.service device-certificate-manager.socket
	systemctl start device-certificate-manager.socket device-certificate-manager.service
fi

%preun
if [ $1 = 0 ]; then
	# unistall
	systemctl stop device-certificate-manager.service device-certificate-manager.socket
fi

%postun
/sbin/ldconfig
if [ $1 = 0 ]; then
	# unistall
	systemctl daemon-reload
fi

%post -n device-certificate-manager-tests

/usr/bin/system-info-tool -s tizen.org/feature/security.device_certificate bool 1

%postun -n device-certificate-manager-tests

if [ $1 = 0 ]; then
	/usr/bin/system-info-tool -s tizen.org/feature/security.device_certificate bool 0
fi

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/device-certificate-managerd
%{_libdir}/libdevice-certificate-manager.so.*
%{_libdir}/libdevice-certificate-manager-ext.so.*
%{_unitdir}/device-certificate-manager.service
%{_unitdir}/sockets.target.wants/device-certificate-manager.socket
%{_unitdir}/device-certificate-manager.socket

%files devel
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libdevice-certificate-manager.so
%{_includedir}/device-certificate-manager/device_certificate_manager.h
%{_libdir}/pkgconfig/device-certificate-manager.pc

%files ext-devel
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libdevice-certificate-manager-ext.so
%{_includedir}/device-certificate-manager/device_certificate_manager_ext.h
%{_includedir}/device-certificate-manager/device_certificate_manager_ext_types.h
%{_libdir}/pkgconfig/device-certificate-manager-ext.pc

%files tests
%manifest %{name}.manifest
%license LICENSE
%license LICENSE.BSL-1.0
%{_bindir}/device-certificate-manager-tests

%if "%{build_type}" == "COVERAGE"

%files coverage
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/device-certificate-manager-coverage.sh
%coverage_dir

%endif
