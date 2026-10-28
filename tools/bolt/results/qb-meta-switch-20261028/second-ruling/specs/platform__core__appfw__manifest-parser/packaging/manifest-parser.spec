Name:           manifest-parser
Summary:        Manifest parser
Version:        1.9.3
Release:        1
Group:          Application Framework/Package Management
License:        Apache-2.0 and BSD-3-Clause
Source0:        %{name}-%{version}.tar.gz
Source100:      %{name}.manifest

BuildRequires:  cmake
BuildRequires:  gtest-devel
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libxml-2.0)

Requires: ca-certificates-tizen

%description
This is a meta package that installs manifest parser.

%package devel
Summary:    Manifest parser development files
Group:      Application Framework/Package Management
Requires:   %{name} = %{version}
Provides:   manifest-parser-devel

%description devel
This package contains necessaary files for manifest-parser development

%package tests
Summary: Unit tests for manifest-parser
Requires: %{name} = %{version}

%description tests
Unit tests for al modules of manifest-parser

%package examples
Summary: Examples for manifest-parser
Requires: %{name} = %{version}

%description examples
Examples of manifest-parser usage

%prep
%setup -q
cp %{SOURCE100} .

%build
export CFLAGS="$(echo $CFLAGS | sed 's/-Wl,--as-needed//g')"
export CXXFLAGS="$(echo $CXXFLAGS | sed 's/-Wl,--as-needed//g')"
export FFLAGS="$(echo $FFLAGS | sed 's/-Wl,--as-needed//g')"
# BUILD_PARSER macro is defined so we can build two separate projects
# with cmake, which are on one repository. Later this macro
# is used in CMakeLists.txt files to distinguish, which project
# is currently being build.
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_BUILD_TYPE=%{?build_type:%build_type} \
         -DTIZEN_VERSION=%{tizen_version} \
         -DFULLVER=%{version} -DMAJORVER=${MAJORVER}

make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%{_datarootdir}/manifest-parser/languages-only.txt
%{_libdir}/libmanifest-parser.so.*
%{_libdir}/libmanifest-parser-utils.so.*
%{_libdir}/libdelta-manifest-handlers.so*
%license LICENSE LICENSE-xwalk

%files devel
%manifest %{name}.manifest
%{_libdir}/pkgconfig/*.pc
%{_includedir}/manifest_parser/*.h
%{_includedir}/manifest_parser/utils/*.h
%{_includedir}/delta/*.h
%{_libdir}/libmanifest-parser.so
%{_libdir}/libmanifest-parser-utils.so

%files tests
%manifest %{name}.manifest
%{_bindir}/manifest-parser-ut/*
%{_datadir}/manifest-parser-ut/*

%files examples
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/manifest-parser/*
%{_datadir}/manifest-parser/*
%license LICENSE LICENSE-xwalk

%changelog
* Tue Sep 01 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.5-1
- dependency removal; CSPHandler included in WidgetConfigParser;
- new TPK handler added

* Wed Aug 26 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.4-1
- String keys cleanup.

* Thu Aug 20 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.3-1
- TPK handlers added

* Tue Aug 18 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.2-1
- ConfigParsing and StartFile validation separation;
- AlwaysValidate removed, version checking improved

* Fri Aug 14 2015 Pawel Sikorski <p.sikorski@samsung.com> 1.1-1
-  Initial rpm changelog; AccountParser added to WGT parser; TPK parser initial patch
