Name:       capi-context
Summary:    Tizen Context Framework Native API
Version:    1.0.6
Release:    1
Group:      Service Framework/Context
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(jsoncpp)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(pkgmgr-info)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: pkgconfig(cynara-creds-self)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(context-app-history-client)
BuildRequires: pkgconfig(context-job-scheduler-client)

# Backward compatibility
Provides: context

%description
Tizen Context Framework Native API

%if "%{gcov}" == "0"
%global gcov 0
%else
%{?gcov: %global gcov 1}
%{!?gcov: %global gcov 0}
%endif

%prep
%setup -q

%build
%if %{gcov}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

export CXXFLAGS+=" -Wall -Wextra -Wcast-align -Wshadow -Wwrite-strings -Wswitch-default -Wno-unused-parameter"
export CXXFLAGS+=" -Wformat=2 -Wno-empty-body -fomit-frame-pointer -fno-optimize-sibling-calls"
export CXXFLAGS+=" -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow"
export CXXFLAGS+=" -Wnon-virtual-dtor -std=c++0x"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version}
make %{?_smp_mflags}

%install
%make_install

%if %{gcov}
# 컴파일시 gcno 파일이 생성됨 해당 파일을 gcov.rpm 에 추가할수 있게 복사
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

# Backward compatibility
ln -s %{name}.pc %{buildroot}/%{_libdir}/pkgconfig/context.pc
ln -s lib%{name}.so.%{version} %{buildroot}/%{_libdir}/libcontext.so.0

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest packaging/%{name}.manifest
%{_libdir}/*.so.*
%license LICENSE

%package devel
Summary:    Tizen Context Framework Native API (Development)
Group:      System/API
Requires:	%{name} = %{version}-%{release}

%description devel
Tizen Context Framework Native API (Development)

%files devel
%{_includedir}/context-service/*.h
%{_includedir}/context-service/wearable/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%package test
Summary:    Tizen Context Framework Testsuite
Group:      Service Framework/Context

%description test
Tizen Context Framework Testsuite

%files test
%manifest testsuite/capi-context-test.manifest
%{_bindir}/context-test
%license LICENSE

%if %{gcov}
%package gcov
Summary:    Tizen Context Framework Native API (gcov)
Group:      Service Framework/Testing

%description gcov
gcov objects for coverage test

%files gcov
%{_datadir}/gcov/obj/*
%endif
