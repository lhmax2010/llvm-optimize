Name:       resource-information
Summary:    Resource Information
Version:    0.1
Release:    3
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: expat-devel
BuildRequires: expat
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(glib-2.0)

%if ( "%{vdut}" == "=c" || "%{vdut}" == "=u" )
BuildRequires:  pkgconfig(gtest_gmock)
%endif

%define _pkgconfigdir %{_libdir}/pkgconfig
%define _packagedir %{_libdir}/%{name}
%define _pkgdir %TZ_SYS_RW_APP/%{name}
%define _includedir %{_libdir}/%{name}
%define _bindir %{TZ_SYS_BIN}

%description
This package provides information of hardware devices of Tizen

%package devel
Summary: resource_information header files, static libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files and static libraries
for resource-information.

%package validator
Summary: resource_information file validator
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description validator
This package provides binary for checking validity of resource-information file

%if 0%{?vd_gcov:1}
%package gcov
Summary: gcov enabled package
Group: gcov package

%description gcov
This package is gcov package for coverage measurement.
%endif

%prep

%setup -q

%if ( "%{vdut}" == "=c" || "%{vdut}" == "=u" )
%define _vd_unit_test -DVD_UNIT_TEST=1
%package ut
Summary: Unit testing package with gtest
%description ut
Description: Unit testing package with gtest
%files ut
%defattr(-,root,root,-)
%{_pkgdir}-ut/*
%endif

%build
export CFLAGS="$CFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS="$CXXFLAGS -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

%ifarch armv7l
%else
echo EMULATOR
export CFLAGS="$CFLAGS -DBUILD_EMULATOR"
export CXXFLAGS="$CXXFLAGS -DBUILD_EMULATOR"
%endif

export CFLAGS="$CFLAGS %{?__vd_cflags}"
export CXXFLAGS="$CXXFLAGS %{?__vd_cxxflags}"

%if 0%{?vd_gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . \
    %{?_vd_unit_test:%_vd_unit_test} \
    -DCMAKE_INSTALL_PREFIX=%{_packagedir} \
    -DPACKAGE_NAME=%{name} \
    -DBINDIR=%{_bindir} \
    -DINCLUDEDIR=%{_includedir} \
    -DPKGCONFIG_INSTALL_DIR=%{_pkgconfigdir} \
    -DVERSION=%{version} \
    -DMAJORVERSION=${MAJORVER} \
    -DLIBDIR=%{_libdir} \
    -DTZ_SYS_RW_APP=%{TZ_SYS_RW_APP} \
    -DVD_CFG_LICENSING=%{_vd_cfg_licensing}

%if ("%{vdut}" == "=c")
%define _covfile %{name}-ut.cov
export COVFILE=~/%{_covfile}
cov01 -1
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%if 0%{?vd_gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj
find . \( -name '*.gcno' -o -name '*.cpp' -o -name '*.c' -o -name '*.h' \) ! -path "./ut/*" ! -path "./test/*" ! -path "*/CompilerIdCXX/*" ! -path "*/CompilerIdC/*" -exec cp --parents -r '{}' %{buildroot}%{_datadir}/gcov/obj ';'
%endif

%clean
%if ("%{vdut}" == "=c")
mv ~/%{_covfile} ~/rpmbuild/RPMS/armv7l/
echo %{_covfile} > ~/rpmbuild/RPMS/armv7l/covfile.txt
%endif
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%manifest resource-information.manifest
%license LICENSE.APLv2

%files devel
%defattr(-,root,root,-)
%{_pkgconfigdir}/resource-information.pc
%{_includedir}/*.h
%{_libdir}/*.so

%files validator
%defattr(-,root,root,-)
#%{TZ_SYS_BIN}/ri_info_validator

%if 0%{?vd_gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif

%post

%postun
