Name: iotivity
Version: 1.2.1
Release: 0
Summary: Samsung IoT Connectivity
Group: Network & Connectivity / IoT Connectivity
License: Apache-2.0
URL: https://www.iotivity.org/
Source0: http://mirrors.kernel.org/%{name}/%{version}/%{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-test.manifest

%if 0%{?tizen:1}
%define TARGET_OS tizen
%else
%define TARGET_OS linux
%endif

%if "%{tizen}" == "2.3"
%define TARGET_TRANSPORT IP
%endif

%if "%{profile}" == "ivi"
%define TARGET_TRANSPORT IP
%endif

%if "%{TARGET_OS}" == "linux"
%define TARGET_TRANSPORT IP
%endif

%define JOB %{?_smp_mflags} --stack-size=512

# default is RELEASE mode.
# If DEBUG mode is needed, please use tizen_build_devel_mode
%define RELEASE True
# For Example
%if %{RELEASE} == "True"
%define build_mode release
%define log_level INFO
%else
%define build_mode debug
%endif

%ifarch armv7l armv7hl armv7nhl armv7tnhl armv7thl
%define TARGET_ARCH "armeabi-v7a"
%endif
%ifarch armv7l
BuildRequires: python-accel-armv7l-cross-arm
%endif
%ifarch armv7hl
BuildRequires: python-accel-armv7hl-cross-arm
%endif
%ifarch aarch64
%define TARGET_ARCH "arm64"
BuildRequires: python-accel-aarch64-cross-aarch64
%endif
%ifarch riscv64
%define TARGET_ARCH "riscv64"
%endif
%ifarch x86_64
%define TARGET_ARCH "x86_64"
%endif
%ifarch %{ix86}
%define TARGET_ARCH "x86"
%endif

%define ex_install_dir %{buildroot}%{_bindir}
%define ex_lib_dir %{buildroot}%{_libdir}
%define ex_include_dir %{buildroot}%{_includedir}

%if 0%{?tizen_version_major} < 3
%if ! 0%{?license:0}
%define license %doc
%endif

%if ! 0%{?manifest:0}
%define manifest %doc
%endif
%endif

# Default values to be eventually overiden BEFORE or as gbs params:
%{!?ES_TARGET_ENROLLEE: %define ES_TARGET_ENROLLEE tizen}
%{!?LOGGING: %define LOGGING 1}
%{!?RD_MODE: %define RD_MODE CLIENT}
%{!?RELEASE: %define RELEASE 1}
%{!?ROUTING: %define ROUTING EP}
%{!?SECURED: %define SECURED 1}
%{!?TARGET_ARCH: %define TARGET_ARCH %{_arch}}
%{!?TARGET_OS: %define TARGET_OS tizen}
%{!?TARGET_TRANSPORT: %define TARGET_TRANSPORT IP,BLE}
%{!?VERBOSE: %define VERBOSE 1}
%{!?WITH_CLOUD: %define WITH_CLOUD 1}
%{!?WITH_MQ: %define WITH_MQ OFF}
%{!?WITH_PROXY: %define WITH_PROXY 0}
%{!?WITH_TCP: %define WITH_TCP 1}
%{!?DISABLE_TCP_SERVER: %define DISABLE_TCP_SERVER 1}
%{!?RD_MODE: %define RD_MODE CLIENT}
%{!?BLE_CUSTOM_ADV: %define BLE_CUSTOM_ADV False}
%{!?BLE_DIVISION: %define BLE_DIVISION VD}
%{!?DISABLE_BLE_SERVER: %define DISABLE_BLE_SERVER 0}
%{!?MULTIPLE_OWNER: %define MULTIPLE_OWNER 1}
%{!?BLE_TIZEN_55: %define BLE_TIZEN_55 True}
%{!?ENABLE_DUP: %define ENABLE_DUP True}
%{!?WITH_PROCESS_EVENT: %define WITH_PROCESS_EVENT 0}

BuildRequires:  expat-devel
BuildRequires:  python3, libcurl-devel
BuildRequires:  scons
BuildRequires:  boost-devel
BuildRequires:  boost-thread
BuildRequires:  boost-system
BuildRequires:  boost-filesystem
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(sqlite3)
%if "%{TARGET_OS}" == "tizen"
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-network-connection)
BuildRequires:  pkgconfig(capi-network-bluetooth) >= 0.1.52
%else
%if 0%{?fedora:1}
BuildRequires:  sqlite-devel
BuildRequires:  gettext-devel
%endif
%endif
Requires(postun): /sbin/ldconfig
Requires(post): /sbin/ldconfig

%description
An open source reference implementation of the OIC standard specifications
IoTivity Base Libraries are included.


%package service
Summary: Development files for %{name}
Group: Network & Connectivity/Service
Requires: %{name} = %{version}-%{release}

%description service
The %{name}-service package contains service libraries files for
developing applications that use %{name}-service.

%package test
Summary: Development files for %{name}
Group: Network & Connectivity/Testing
Requires: %{name} = %{version}-%{release}

%description test
The %{name}-test package contains example files to show
how the iotivity works using %{name}-test

%package devel
Summary: Development files for %{name}
Group: Network & Connectivity/Development
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
chmod g-w %_sourcedir/*

cp LICENSE.md LICENSE

cp %{SOURCE1001} .
%if 0%{?tizen_version_major} < 3
cp %{SOURCE1002} .
%else
cp %{SOURCE1001} ./%{name}-test.manifest
%endif

%build
CFLAGS="${CFLAGS:-%optflags} -Wno-implicit-function-declaration -Wno-incompatible-pointer-types" ; export CFLAGS ;
scons %{JOB} --prefix=%{_prefix} \
    ES_TARGET_ENROLLEE=%{ES_TARGET_ENROLLEE} \
    LIB_INSTALL_DIR=%{_libdir} \
    LOGGING=%{LOGGING} \
    RD_MODE=%{RD_MODE} \
    RELEASE=%{RELEASE} \
    ROUTING=%{ROUTING} \
    SECURED=%{SECURED} \
    TARGET_ARCH=%{TARGET_ARCH} \
    TARGET_OS=%{TARGET_OS} \
    TARGET_TRANSPORT=%{TARGET_TRANSPORT} \
    VERBOSE=%{VERBOSE} \
    WITH_CLOUD=%{WITH_CLOUD} \
    WITH_MQ=%{WITH_MQ} \
    WITH_PROXY=%{WITH_PROXY} \
    WITH_TCP=%{WITH_TCP} \
    DISABLE_TCP_SERVER=%{DISABLE_TCP_SERVER} \
    RD_MODE=%{RD_MODE} \
    BLE_CUSTOM_ADV=%{BLE_CUSTOM_ADV} \
    BLE_DIVISION=%{BLE_DIVISION} \
    BLE_TIZEN_55=%{BLE_TIZEN_55} \
    ENABLE_DUP=%{ENABLE_DUP} \
    DISABLE_BLE_SERVER=%{DISABLE_BLE_SERVER} \
    MULTIPLE_OWNER=%{MULTIPLE_OWNER} \
    LOG_LEVEL=%{log_level} \
    WITH_PROCESS_EVENT=%{WITH_PROCESS_EVENT} \
    #eol

%install
%if 0%{?tizen_version_major} < 3
mkdir -p %{buildroot}/%{_datadir}/license
cp LICENSE %{buildroot}/%{_datadir}/license/%{name}
%endif

mkdir -p %{ex_install_dir}
mkdir -p %{ex_include_dir}
mkdir -p %{ex_lib_dir}/pkgconfig
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/examples/OICMiddle/OICMiddle %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/devicediscoveryclient %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/devicediscoveryserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/fridgeclient %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/fridgeserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/garageclient %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/garageserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/groupclient %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/groupserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/lightserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/presenceclient %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/presenceserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/roomclient %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/roomserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/simpleclient %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/simpleclientHQ %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/simpleclientserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/simpleserver %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/simpleserverHQ %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/threadingsample %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/oic_svr_db_server.dat %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/examples/oic_svr_db_client.dat %{ex_install_dir}
#cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/libcoap.a %{buildroot}%{_libdir}
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/lib*.a  %{buildroot}%{_libdir}

# Install so files
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/lib*.so  %{buildroot}%{_libdir}
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/src/lib*.so  %{buildroot}%{_libdir}
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/csdk/lib*.so  %{buildroot}%{_libdir}
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/oc_logger/lib*.so  %{buildroot}%{_libdir}
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/service/easy-setup/mediator/richsdk/lib*.so  %{buildroot}%{_libdir}

# Install pc file
cp ./*.pc %{buildroot}%{_libdir}/pkgconfig

%if 0%{?WITH_PROXY} == 1
mkdir -p %{ex_install_dir}/proxy-sample
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/service/coap-http-proxy/samples/proxy_main %{ex_install_dir}/proxy-sample/
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/service/coap-http-proxy/samples/proxy_client %{ex_install_dir}/proxy-sample/
%endif

%if 0%{?SECURED} == 1
mkdir -p %{ex_install_dir}/provisioning
mkdir -p %{ex_install_dir}/provision-sample
mkdir -p %{ex_include_dir}/mbedtls

cp -R ./extlibs/mbedtls/mbedtls/include/mbedtls/ %{buildroot}%{_includedir}
cp ./resource/csdk/security/include/*.h %{buildroot}%{_includedir}
cp ./resource/csdk/connectivity/api/*.h %{buildroot}%{_includedir}/
cp ./resource/csdk/security/include/internal/*.h %{buildroot}%{_includedir}/
cp ./resource/csdk/security/provisioning/include/oxm/*.h %{buildroot}%{_includedir}
cp ./resource/csdk/security/provisioning/include/internal/*.h %{buildroot}%{_includedir}
cp ./resource/csdk/security/provisioning/include/*.h %{buildroot}%{_includedir}
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/csdk/security/provisioning/sample/sampleserver_justworks %{ex_install_dir}/provision-sample/
cp ./resource/csdk/security/provisioning/sample/oic_svr_db_server_justworks.dat %{ex_install_dir}/provision-sample/
cp out/%{TARGET_OS}/%{TARGET_ARCH}/%{build_mode}/resource/csdk/security/provisioning/sample/sampleserver_randompin %{ex_install_dir}/provision-sample/
cp ./resource/csdk/security/provisioning/sample/oic_svr_db_server_randompin.dat %{ex_install_dir}/provision-sample/

%endif


mkdir -p %{ex_include_dir}/service/resource-encapsulation
mkdir -p %{ex_include_dir}/service/notification
mkdir -p %{ex_include_dir}/service/easy-setup
mkdir -p %{ex_include_dir}/resource/targets
mkdir -p %{ex_include_dir}/c_common

# Install missed header files
cp service/resource-encapsulation/include/*.h %{buildroot}%{_includedir}/service/resource-encapsulation
cp service/notification/include/*.h %{buildroot}%{_includedir}/service/notification
cp service/notification/cpp-wrapper/common/*.h %{buildroot}%{_includedir}/service/notification
cp service/notification/cpp-wrapper/provider/inc/*.h %{buildroot}%{_includedir}/service/notification
cp service/notification/cpp-wrapper/consumer/inc/*.h %{buildroot}%{_includedir}/service/notification
cp service/easy-setup/inc/*.h %{buildroot}%{_includedir}/service/easy-setup
cp service/easy-setup/mediator/richsdk/inc/* %{buildroot}%{_includedir}/service/easy-setup
cp service/easy-setup/enrollee/inc/*.h %{buildroot}%{_includedir}/service/easy-setup
cp resource/oc_logger/include/targets/*.h %{buildroot}%{_includedir}/resource/targets
cp resource/include/* %{buildroot}%{_includedir}/resource
cp resource/c_common/platform_features.h %{buildroot}%{_includedir}/c_common
cp resource/c_common/iotivity_config.h %{buildroot}%{_includedir}/c_common
cp resource/csdk/resource-directory/include/*.h %{buildroot}%{_includedir}/resource
cp resource/csdk/stack/include/*.h %{buildroot}%{_includedir}/resource
cp resource/oc_logger/include/*.h %{buildroot}%{_includedir}/resource
cp resource/oc_logger/include/*.hpp %{buildroot}%{_includedir}/resource

cp resource/c_common/*.h %{buildroot}%{_includedir}/c_common
cp resource/c_common/ocrandom/include/*.h %{buildroot}%{_includedir}/c_common
cp resource/c_common/oic_string/include/*.h %{buildroot}%{_includedir}/c_common
cp resource/c_common/oic_malloc/include/*.h %{buildroot}%{_includedir}/c_common
cp resource/c_common/ocevent/include/*.h %{buildroot}%{_includedir}/c_common
cp resource/c_common/octhread/include/*.h %{buildroot}%{_includedir}/c_common
cp resource/csdk/stack/include/*.h %{buildroot}%{_includedir}/c_common
cp resource/csdk/logger/include/*.h %{buildroot}%{_includedir}/c_common

cp service/easy-setup/inc/*.h %{buildroot}%{_includedir}
cp service/easy-setup/enrollee/inc/*.h %{buildroot}%{_includedir}
cp service/easy-setup/mediator/richsdk/inc/*.h %{buildroot}%{_includedir}
cp service/easy-setup/enrollee/inc/samsung/*.h %{buildroot}%{_includedir}

install -d %{buildroot}%{_includedir}/iotivity
ln -fs ../resource %{buildroot}%{_includedir}/iotivity/
ln -fs ../service %{buildroot}%{_includedir}/iotivity/
ln -fs ../c_common %{buildroot}%{_includedir}/iotivity/

rm -rfv out %{buildroot}/out %{buildroot}/${HOME} ||:


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%if 0%{?tizen_version_major} < 3
%{_datadir}/license/%{name}
%else
%license LICENSE
%endif
%{_libdir}/liboc.so
%{_libdir}/liboc_logger.so
%{_libdir}/liboc_logger_core.so
%{_libdir}/liboctbstack.so
%{_libdir}/libconnectivity_abstraction.so
%if 0%{?SECURED} == 1
%{_libdir}/libmbedtls.so
%{_libdir}/libocpmapi.so
%{_libdir}/libocprovision.so
%endif

%files service
%manifest %{name}.manifest
%defattr(-,root,root,-)
%if 0%{?tizen_version_major} < 3
%{_datadir}/license/%{name}
%else
%license LICENSE
%endif
#%{_libdir}/libBMISensorBundle.so
#%{_libdir}/libDISensorBundle.so
#%{_libdir}/libHueBundle.so
%{_libdir}/librcs_client.so
%{_libdir}/librcs_common.so
#%{_libdir}/librcs_container.so
%{_libdir}/librcs_server.so
%{_libdir}/libresource_directory.so
%{_libdir}/libESEnrolleeSDK.so
%{_libdir}/libESMediatorRich.so
%{_libdir}/libnotification*.so
%if 0%{?WITH_PROXY} == 1
%{_libdir}/libcoap_http_proxy.so
%endif
%if "%{TARGET_OS}" == "linux"
%{_libdir}/libnotification*.so
%endif

%files test
%manifest %{name}-test.manifest
%defattr(-,root,root,-)
%if 0%{?tizen_version_major} < 3
%{_datadir}/license/%{name}
%else
%license LICENSE
%endif
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%if 0%{?tizen_version_major} < 3
%{_datadir}/license/%{name}
%else
%license LICENSE
%endif
%if 0%{?SECURED} == 1
%endif
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*
