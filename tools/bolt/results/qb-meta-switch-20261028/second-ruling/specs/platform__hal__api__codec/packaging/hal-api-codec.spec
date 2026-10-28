%define module_name codec
%define name        hal-api-%{module_name}
%define res_path    /testcase/res/codec
%define enable_test 1

### main package #########
Name:       %{name}
Summary:    %{name} interface
Version:    1.10.2
Release:    0
Group:      Development/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}-manifest.xml
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(hal-api-common)
BuildRequires: tidl
BuildRequires: pkgconfig(rpc-port)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-package-manager)
%if "%{enable_test}" == "1"
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(libtbm)
%endif

%description
%{name} interface package for product vendor developer


### devel package #########
%package    devel
Summary:    %{name} interface
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
%{name} interface development package for product vendor developer


%if "%{enable_test}" == "1"
### test package #########
%package haltests
Summary: tests for %{name}

%description haltests
Haltests for %{name}
%endif


### build and install #########
%prep
%setup -q

mkdir -p ./src/generated
(cd src/generated && tidlc -p -l C -i ../../include/hal_codec_ipc_1.tidl -o hal_codec_proxy_1)

mkdir -p ./src/service_plugin/generated
(cd src/service_plugin/generated && tidlc -s -l C -i ../../../include/hal_codec_ipc_1.tidl -o hal_codec_stub_1)

%if "%{enable_test}" == "1"
export CXXFLAGS="$CXXFLAGS -D_LARGEFILE64_SOURCE -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\" -DTEST_FILES_PATH=\\\"%{_datadir}%{res_path}\\\""
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
	-DCMAKE_C_COMPILER=%__cc \
	-DCMAKE_CXX_COMPILER=%__cxx \
%if "%{enable_test}" == "1"
	-DENABLE_TESTS=YES\
	-DTESTCASE_RES_DIR=%{_datadir}%{res_path}\
%endif
	-DFULLVER=%{version}\
	-DMAJORVER=${MAJORVER}\
	-DCMAKE_INSTALL_PREFIX=%{_prefix}\
	-DCMAKE_LIBDIR_PREFIX=%{_libdir}

%build
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/hal
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/hal/
%if "%{enable_test}" == "1"
install -d -m 755 %{buildroot}%{_datadir}%{res_path}
install -m 644 tests/res/* %{buildroot}%{_datadir}%{res_path}
%endif
%make_install

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

%postun
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset


%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/hal/*.so.*
%{_libdir}/hal/libhal-backend-service-codec.so
%{_sysconfdir}/hal/%{name}-manifest.xml


%files devel
%defattr(-,root,root,-)
%{_includedir}/hal/*.h
%{_libdir}/hal/libhal-api-*.so
%{_libdir}/pkgconfig/*.pc

%if "%{enable_test}" == "1"
%files haltests
%manifest %{name}-haltests.manifest
%{_bindir}/hal/*
%{_datadir}%{res_path}/*
%endif

