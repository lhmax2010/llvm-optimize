Name:           capi-system-resource-monitor
Summary:        A Resource Monitor library in Tizen Native API
Version:        0.0.1
Release:        0
Group:          System/API
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
Source1001:     capi-system-resource-monitor.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(libpass-resource-monitor)
BuildRequires:  pkgconfig(libsyscommon)

%description
A Resource Monitor library in Tizen Native API

%package devel
Summary:  A Resource Monitor library in Tizen Native API (Development)
Group:    System / Kernel
Requires: %{name} = %{version}-%{release}

%description devel
A Resource Monitor library in Tizen Native API (Development)

%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage files
Group: Development/System

%description gcov
Collection of files related to line coverage using gcov.
%endif

%package tools
Summary:  A Resource Monitor library in Tizen Native API (Tool)
Group:    System / Kernel
Requires: %{name} = %{version}-%{release}

%description tools
A Resource Monitor library in Tizen Native API (Tool)

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
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \

make %{?jobs:-j%jobs}

%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%install
%make_install

%if 0%{?gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj/%{name}
install -m 0644 gcov-obj/* %{buildroot}%{_datadir}/gcov/obj/%{name}
%endif

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libcapi-system-resource-monitor.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/system/resource-monitor.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-system-resource-monitor.so

%files tools
%manifest %{name}.manifest
%{_prefix}/bin/system-resource-monitor

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
