Name: trust-anchor
Version: 2.1.2
Release: 0
License: Apache-2.0
Source0: file://%{name}-%{version}.tar.gz
Summary: Trust Anchor API
Group: Security/Certificate Management
BuildRequires: gcc
BuildRequires: cmake
BuildRequires: coreutils
BuildRequires: pkgconfig(klay)
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: ca-certificates
BuildRequires: ca-certificates-devel
Requires: security-config
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%global lib_name         tanchor
%global runtime_lib_name %{lib_name}-runtime
%global user_name        security_fw
%global group_name       security_fw
%global smack_label      System
%global pkg_smack_label  System::Shared

%global tanchor_base     %{TZ_SYS_DATA}/%{lib_name}
%global tanchor_pkg      %{tanchor_base}/pkg
%global tanchor_bundle   %{tanchor_base}/ca-bundle.pem
%global tanchor_sysca    %{tanchor_base}/.sysca
%global tanchor_pkgcerts %{tanchor_base}/.pkgcerts
%global tanchor_test     %{tanchor_base}/test
%global tanchor_example  %{tanchor_base}/example

%description
The package provides trust-anchor which the application can assign
SSL root certificates for its HTTPS communication.

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/lib%{lib_name}.so.2
%{_libdir}/lib%{lib_name}.so.%{version}
%dir %attr(-, %{user_name}, %{group_name}) %{tanchor_base}
%dir %attr(-, %{user_name}, %{group_name}) %{tanchor_pkg}
%attr(-, %{user_name}, %{group_name}) %{tanchor_bundle}
%attr(-, %{user_name}, %{group_name}) %{tanchor_pkgcerts}
%attr(444 %{user_name}, %{group_name}) %{tanchor_sysca}

%prep
%setup -q

%build
%{!?build_type:%define build_type "RELEASE"}

%if %{build_type} == "DEBUG" || %{build_type} == "PROFILING" || %{build_type} == "CCOV"
	CFLAGS="$CFLAGS -Wp,-U_FORTIFY_SOURCE"
	CXXFLAGS="$CXXFLAGS -Wp,-U_FORTIFY_SOURCE"
%endif

%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%cmake . -DCMAKE_BUILD_TYPE=%{build_type} \
		 -DLIB_NAME=%{lib_name} \
		 -DRUNTIME_LIB_NAME=%{runtime_lib_name} \
		 -DLIB_VERSION=%{version} \
		 -DUSER_NAME=%{user_name} \
		 -DGROUP_NAME=%{group_name} \
		 -DSMACK_LABEL=%{smack_label} \
		 -DPKG_SMACK_LABEL=%{pkg_smack_label} \
		 -DTANCHOR_BASE=%{tanchor_base} \
		 -DTANCHOR_PKG=%{tanchor_pkg} \
		 -DTANCHOR_BUNDLE=%{tanchor_bundle} \
		 -DTANCHOR_SYSCA=%{tanchor_sysca} \
		 -DTANCHOR_PKG_CERTS=%{tanchor_pkgcerts} \
		 -DTANCHOR_TEST=%{tanchor_test} \
		 -DTANCHOR_EXAMPLE=%{tanchor_example} \
		 -DTZ_SYS_CA_CERTS=%{TZ_SYS_CA_CERTS} \
		 -DTZ_SYS_CA_BUNDLE=%{TZ_SYS_CA_BUNDLE} \
		 -DTZ_SYS_RO_CA_CERTS=%{TZ_SYS_RO_CA_CERTS} \
		 -DTZ_SYS_RO_CA_BUNDLE=%{TZ_SYS_RO_CA_BUNDLE} \
		 -DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}%{tanchor_pkg}

touch %{buildroot}%{tanchor_bundle}
touch %{buildroot}%{tanchor_sysca}
touch %{buildroot}%{tanchor_pkgcerts}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

## Runtime Package ###############################################################
%package runtime
Summary: Trust Anchor Runtime API
Group:   Certificate Management
Requires: %{name} = %{version}-%{release}

%description runtime
The package provides runtime APIs of trust-anchor for launchpad

%files runtime
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/lib%{runtime_lib_name}.so.2
%{_libdir}/lib%{runtime_lib_name}.so.%{version}

## Devel Package ###############################################################
%package devel
Summary: Trust Anchor API (development files)
Group:   Security/Development
Requires: %{name} = %{version}-%{release}

%description devel
The package provides Trust Anchor API development files.

%files devel
%{_includedir}/%{lib_name}/error.h
%{_includedir}/%{lib_name}/trust-anchor.h
%{_includedir}/%{lib_name}/trust-anchor.hxx
%{_libdir}/lib%{lib_name}.so
%{_libdir}/lib%{runtime_lib_name}.so
%{_libdir}/pkgconfig/%{lib_name}.pc
%{_libdir}/pkgconfig/%{runtime_lib_name}.pc

## Test Package ##############################################################
%package -n trust-anchor-test
Summary: Trust Anchor API test
Group: Security/Development
BuildRequires: pkgconfig(libcurl)

%description -n trust-anchor-test
Testcases for trust anchor library

%files -n trust-anchor-test
%{_bindir}/%{lib_name}-test-installer
%{_bindir}/%{lib_name}-test-launcher
%{_bindir}/%{lib_name}-test-clauncher
%{_bindir}/%{lib_name}-test-internal
%{_bindir}/%{lib_name}-test-ssl
%{_bindir}/%{lib_name}-test-init.sh
%attr(-, %{user_name}, %{group_name}) %{tanchor_test}
%attr(-, %{user_name}, %{group_name}) %{tanchor_test}/certs

## Example Package ############################################################
%package -n trust-anchor-example
Summary: Trust Anchor API example
Group: Security/Other

%description -n trust-anchor-example
Examples for trust anchor library

%files -n trust-anchor-example
%{tanchor_example}/installer.c
%{tanchor_example}/launcher.c
