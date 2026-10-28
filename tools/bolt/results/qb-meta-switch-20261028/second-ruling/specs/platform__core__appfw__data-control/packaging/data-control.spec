Name:       data-control
Summary:    Data Control library
Version:    0.4.33
Release:    1
Group:      Application Framework/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(appsvc)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

# runtime requires
Requires(post): /sbin/ldconfig
Requires(post): coreutils
Requires(postun): /sbin/ldconfig

Provides:   capi-data-control

%description
Data Control library

%package devel
Summary:  Data Control library (Development)
Group:    Application Framework/Development
Requires: %{name} = %{version}-%{release}

%description devel
Data Control library (DEV)

#################################################
# data-control-unittests
#################################################
%package -n data-control-unittests
Summary:    GTest for Data Control API
Group:      Development/Libraries
Requires:   %{name}

%description -n data-control-unittests
GTest for data-control API

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:  Data Control API(gcov)
Group:    Application Framework/Libraries

%description gcov
gcov objects of a data control library
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

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER}

# Call make instruction with smp support
%__make %{?jobs:-j%jobs}

%check
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o data_control.info
genhtml data_control.info -o data_control.out
zip -r data_control.zip data_control.out
install -m 0644 data_control.zip %{buildroot}%{_datadir}/gcov/obj/data_control.zip
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

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
}

test_main() {
    echo "test_main start"
    /usr/bin/data_control_unittests
}

teardown() {
    echo "teardown start"
}

main() {
    setup
    test_main
    teardown
}

main "\$*"
EOF

mkdir -p %{buildroot}%{_bindir}/tizen-unittests/%{name}
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%{_libdir}/lib%{name}.so.*
%{_libdir}/libcapi-data-control.so.*
%config %{_sysconfdir}/dbus-1/session.d/data-control.conf

%manifest %{name}.manifest
%license LICENSE.APLv2

%files devel
%{_includedir}/appfw/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib%{name}.so

#################################################
# data-control-unittests
#################################################
%files -n data-control-unittests
%{_bindir}/data_control_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# data-control-gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
