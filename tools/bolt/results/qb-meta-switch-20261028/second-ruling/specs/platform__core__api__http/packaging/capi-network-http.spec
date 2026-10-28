Name:		capi-network-http
Summary:	Http Framework
Version:	0.0.39
Release:	0
Group:		System/Network
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(capi-base-common)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(capi-network-connection)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(cynara-client)
BuildRequires:	pkgconfig(cynara-creds-self)
BuildRequires:	pkgconfig(gmock)
BuildRequires:	cmake
%if 0%{?gcov:1}
BuildRequires: lcov
BuildRequires: tar
%endif
Requires(post):		/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
Http framework library for CAPI

%package devel
Summary:	Development package for Http framework library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%description devel
Development package for Http framework library

%package tool
Summary:	Test Application for Http framework library
Group:		Network & Connectivity/Utilities
Requires:	%{name} = %{version}

%description tool
Test Application for Http framework library

%if 0%{?gcov:1}
%package gcov
Summary:  HTTP library(gcov)
Group:    Network/Testing
%description gcov
gcov objects for coverage test
%endif

%prep
%setup -q

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

%cmake -DBUILD_GTESTS=%{?gcov:1}%{!?gcov:0} -DLIB_INSTALL_DIR=%{_libdir} \
	-DUSE_LOCALHOST_SERVER=%{?gproxy:0}%{!?gproxy:1} \
	.

make %{?_smp_mflags}

%install
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' ! -path '*/tools/*' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%check
%if 0%{?gcov:1}
%if 0%{?gproxy:1}
env all_proxy=%{gproxy} tests/http-gtest # http://[proxy addr]:[port]
%else
tests/http-gtest
%endif
%endif

%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -b . -d . -o %{name}.info
genhtml %{name}.info -o out --legend --show-details
%endif

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest capi-network-http.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/network/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%license LICENSE

%files tool
%manifest capi-network-http.manifest
%{_bindir}/http_test
%license LICENSE


%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
