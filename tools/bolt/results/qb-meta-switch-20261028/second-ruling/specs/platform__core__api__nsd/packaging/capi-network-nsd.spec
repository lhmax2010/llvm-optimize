Name:       capi-network-nsd
Summary:    A Network Service Discovery libraries in Native API
Version:    0.2.8
Release:    1
Group:      System/Network
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:    capi-network-nsd.manifest
Source1002:    libnsd-dns-sd.manifest
Source1003:    libnsd-ssdp.manifest
Source1004:    nsd-tests.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dns_sd)
BuildRequires:  pkgconfig(gssdp-1.0)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:	pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(gmock)
%if 0%{?gcov:1}
BuildRequires:  tar
BuildRequires:	lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
NSD library in Tizen C API This package provides both SSDP and
DNS-SD Tizen C API

%package devel
Summary:  A NSD library in Native API (Development)
Requires:   libnsd-dns-sd = %{version}-%{release}
Requires:   libnsd-ssdp = %{version}-%{release}

%description devel
Netowrk Service Discovery library in Tizen C API development files

%package tests
Summary:    NSD - NSD test binaries

%description tests
NSD tests for both DNS-SD and SSDP Tizen C API

%package -n libnsd-dns-sd
Summary:    NSD - DNS-SD library in Tizen C API

%description -n libnsd-dns-sd
Network Service Discovery library for DNS-SD

%package -n libnsd-ssdp
Summary:    NSD - SSDP library in Tizen C API

%description -n libnsd-ssdp
Network Service Discovery library for SSDP

%if 0%{?gcov:1}
%package gcov
Summary:	NSD library (gcov)
Group:		Network/Testing

%description gcov
gcov objects for coverage test
%endif

%prep
%setup -q
chmod 644 %{SOURCE1001}
chmod 644 %{SOURCE1002}
chmod 644 %{SOURCE1003}
cp -a %{SOURCE1001} .
cp -a %{SOURCE1002} .
cp -a %{SOURCE1003} .
cp -a %{SOURCE1004} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
        -DCMAKE_BUILD_TYPE=%{?build_type} \
        -DCMAKE_VERBOSE_MAKEFILE=ON \
        -DLIB_DIR:PATH=%{_libdir} \
        -DBIN_DIR:PATH=%{_bindir} \
        -DINCLUDE_DIR:PATH=%{_includedir} \
        -DLOCAL_STATE_DIR:PATH=%{_localstatedir} \
        -DDATA_ROOT_DIR:PATH=%{_datadir} \
        -DFULLVER=%{version} \
        -DMAJORVER=${MAJORVER} \
        -DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}
make %{?_smp_mflags}

%install

%make_install
%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%check
tests/tct-nsd-core
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o nsd.info
genhtml nsd.info -o out --legend --show-details
%endif

%post -n libnsd-dns-sd -p /sbin/ldconfig

%postun -n libnsd-dns-sd -p /sbin/ldconfig

%post -n libnsd-ssdp -p /sbin/ldconfig

%postun -n libnsd-ssdp -p /sbin/ldconfig

%files
%manifest capi-network-nsd.manifest
%license LICENSE

%files devel
%{_includedir}/nsd/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files tests
%manifest nsd-tests.manifest
%attr(755,root,root) %{_bindir}/dns-sd-test
%attr(755,root,root) %{_bindir}/dns-sd-internal-test
%attr(755,root,root) %{_bindir}/ssdp-test
%attr(755,root,root) %{_bindir}/tct-nsd-core

%files -n libnsd-dns-sd
%manifest libnsd-dns-sd.manifest
%license LICENSE
%{_libdir}/libnsd-dns-sd.so.*

%files -n libnsd-ssdp
%manifest libnsd-ssdp.manifest
%license LICENSE
%{_libdir}/libnsd-ssdp.so.*

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%exclude %{_datadir}/gcov/obj/*/*/tests/*
%endif
