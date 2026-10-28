%define keepstatic 1
Name:    klay
Version: 0.0.2
Release: 0
License: Apache-2.0
Source0: file://%{name}-%{version}.tar.gz
Source1: %name.manifest
Summary: Tizen Klay library
Group:   Development/Libraries
BuildRequires: gcc
BuildRequires: cmake
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(libtzplatform-config)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
The klay package provides a library which can be used for many servers
and clients.

%files
%manifest %name.manifest
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libklay.so.%{version}
%{_libdir}/libklay.so.0

%prep
%setup -q
cp %SOURCE1 .

%build
%{!?build_type:%define build_type "RELEASE"}

%if %{build_type} == "DEBUG" || %{build_type} == "PROFILING" || %{build_type} == "CCOV"
	CFLAGS="$CFLAGS -Wp,-U_FORTIFY_SOURCE"
	CXXFLAGS="$CXXFLAGS -Wp,-U_FORTIFY_SOURCE"
%endif

%cmake . -DVERSION=%{version} \
         -DCMAKE_BUILD_TYPE=%{build_type} \
         -DTEST_DATA_INSTALL_DIR=%{TZ_SYS_DATA}/klay-test \

make %{?jobs:-j%jobs}

%install
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

## Devel Package ##############################################################
%package devel
Summary: Tizen Klay development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(glib-2.0)

%description devel
The klay-devel package provides libraries and header files necessary for
developing with the Klay library.

%files devel
%manifest %name.manifest
%defattr(644,root,root,755)
%{_libdir}/libklay.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_includedir}/klay

## Test Package ##############################################################
%package test
Summary: Klay test
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description test
Testcases for klay library.

%files test
%manifest %name.manifest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/klay-test
%attr(755,root,root) %{TZ_SYS_DATA}/klay-test/test-proc.sh
