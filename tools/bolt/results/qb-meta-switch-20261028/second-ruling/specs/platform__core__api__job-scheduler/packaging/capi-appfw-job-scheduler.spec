Name:       capi-appfw-job-scheduler
Summary:    Job Scheduler library
Version:    0.1.14
Release:    0
Group:      System/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:     capi-appfw-job-scheduler.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(context-job-scheduler-client)
BuildRequires:  pkgconfig(context-common-client)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-appfw-service-application)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-client)

Recommends: amd-mod-job-scheduler

%description
Job Scheduler library in Tizen C API

%package devel
Summary:  Job Scheduler library in Tizen C API (Development)
Group:    System/API
Requires: %{name} = %{version}

%description devel
An Application library in SLP C API (Development) package.

%if 0%{?gcov:1}
%package gcov
Summary:  Job Scheduler library(gcov)
Group:    System/API

%description gcov
gcov objects of a job scheduler library
%endif

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	.

%__make %{?jobs:-j%jobs}

%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/libcapi-appfw-job-scheduler.so.*
%license LICENSE

%files devel
%manifest %{name}.manifest
%{_includedir}/appfw/*.h
%{_libdir}/pkgconfig/capi-appfw-job-scheduler.pc
%{_libdir}/libcapi-appfw-job-scheduler.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
