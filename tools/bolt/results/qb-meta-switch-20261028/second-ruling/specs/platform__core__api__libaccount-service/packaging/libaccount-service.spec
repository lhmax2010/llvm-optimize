Name:       libaccount-service
Summary:    Account DB library
Version:    0.4.26
Release:    1
Group:      Social & Content/API
License:    Apache-2.0
Source0:    libaccount-service-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(vconf)
BuildRequires:	pkgconfig(glib-2.0) >= 2.26
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(account-common)
BuildRequires:  pkgconfig(db-util)
BuildRequires:  pkgconfig(pkgmgr-installer)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Account DB libraryXB-Public-Package: no

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
%description devel
Development files for %{name}

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Account library (gcov)
Group:      Service Framework/Testing
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

#export   CFLAGS+=" -Wextra -Wcast-align -Wcast-qual -Wshadow -Wwrite-strings -Wswitch-default"
#export CXXFLAGS+=" -Wextra -Wcast-align -Wcast-qual -Wshadow -Wwrite-strings -Wswitch-default -Wnon-virtual-dtor -Wno-c++0x-compat"
#export   CFLAGS+=" -Wno-unused-parameter -Wno-empty-body"
#export CXXFLAGS+=" -Wno-unused-parameter -Wno-empty-body"

#export   CFLAGS+=" -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow -fno-common"
#export CXXFLAGS+=" -fno-omit-frame-pointer -fno-optimize-sibling-calls -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow"

export CFLAGS="${CFLAGS} -fPIC -fvisibility=hidden"
#cmake . -DCMAKE_INSTALL_PREFIX=/usr
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIBDIR=%{_libdir} \
	-DBINDIR=%{_bindir} \
	-DINCLUDEDIR=%{_includedir}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

rm -rf %{buildroot}%{_libdir}/accounts-svc

%post
/sbin/ldconfig
/usr/bin/sqlite3

%postun -p /sbin/ldconfig

%files
%manifest libaccount-service.manifest
%defattr(-,root,root,-)
%license LICENSE.APLv2
%{_libdir}/*.so.*

%files devel
%manifest libaccount-service.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_libdir}/pkgconfig/accounts-svc.pc
%{_includedir}/*.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
