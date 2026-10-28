Name: capi-telephony
Version: 0.3.0
Release: 1
Summary: Telephony Core API

Group: Telephony/API
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(tapi)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(openssl3)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(cynara-creds-self)
BuildRequires: pkgconfig(gmock)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Telephony public API library

%package devel
Summary: Telephony Core API
Group: Telephony/Development
Requires: %{name} = %{version}
Requires: pkgconfig

%description devel
Telephony public API library (development library)

%package unittests
Summary: Test Programs for %{name}
Group: Telephony/Testing

%description unittests
The %{name}-unittests pacakge contains programs for checking quality the %{name}.

%define tel_header_dir %{_includedir}/telephony

%prep
%setup -q
cp %{SOURCE1001} ./%{name}.manifest

%build

%{?asan:
export CFLAGS+=" -Wno-format-truncation "
}

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version} \
	-DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DHEADER_DIR:PATH=%{tel_header_dir} \
	-DTEST_INSTALL_DIR:PATH=%{_bindir}/%{name} \
	-DSTDOUT_LOG=%{?stdlog:1}%{!?stdlog:0}
make %{?_smp_mflags}

%install
%make_install

%check
tests/tel-gtest

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/lib%{name}.so.*
%license LICENSE.APLv2

%files devel
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc
%{tel_header_dir}/telephony*.h

%files unittests
%manifest %{name}.manifest
%{_bindir}/telephony-test
%{_bindir}/%{name}/*gtest*
%license LICENSE.APLv2
