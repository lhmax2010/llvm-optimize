Name:       tidl
Summary:    Tizen Interface Definition Language
Version:    3.1.6
Release:    1
Group:      Application Framework/Building
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-tests.manifest

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  gtest-devel
BuildRequires:  pkgconfig(glib-2.0)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Tizen Interface Definition Language

%package tests
Summary:    Unit tests for TIDL
Requires:   %{name} = %{version}

%description tests
Unit tests for TIDL

%package action-toolchain
Summary:    Tizen Action toolchain for TIDL
Requires:   %{name} = %{version}

%description action-toolchain
Tizen Action toolchain utilities for converting .action and .entity schemas
to TIDL and generating service stubs through tidlc.

%define _action_toolchain_datadir %{_datadir}/tizen-action-toolchain
%define _share_dir /opt/usr/share

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS="$CFLAGS -Wno-unused-const-variable -Wno-pessimizing-move -Wno-unused-private-field"
export CXXFLAGS="$CXXFLAGS -Wno-unused-const-variable -Wno-pessimizing-move -Wno-unused-private-field"
%endif
}
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
  %if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE
  %else
    -DASAN_ENABLED=TRUE
  %endif

%__make %{?_smp_mflags}

%check
ctest -V %{?_smp_mflags}
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%install
rm -rf %{buildroot}
%make_install

%preun

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%license LICENSE
%manifest %{name}.manifest
%{_bindir}/tidlc

%files tests
%manifest %{name}.manifest
%{_bindir}/tidl-unit-tests
%{_share_dir}/*

%files action-toolchain
%manifest %{name}.manifest
%{_bindir}/action2tidl
%{_bindir}/actionc
%{_action_toolchain_datadir}/*
