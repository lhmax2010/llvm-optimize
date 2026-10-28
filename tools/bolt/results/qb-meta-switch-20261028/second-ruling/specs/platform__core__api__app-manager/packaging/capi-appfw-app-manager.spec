Name:       capi-appfw-app-manager
Summary:    Application Manager API
Version:    0.18.0
Release:    1
Group:      Application Framework/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(gmock)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
The Application Manager API provides functions to get information about running applications.

%package devel
Summary:  Application Manager API (Development)
Group:    Application Framework/Libraries
Requires: %{name} = %{version}

%description devel
The Application Manager API provides functions to get information about running applications. (DEV)

%package unittests
Summary:    GTest for app-manager API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for app-manager API

%if 0%{?gcov:1}
%package gcov
Summary:  Application Manager API(gcov)
Group:    Application Framework/API

%description gcov
gcov objects for an application manager library
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
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
%if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE
%else
    -DASAN_ENABLED=TRUE
%endif
%__make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH="../../src"
ctest --verbose %{?_smp_mflags}
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o app-manager.info
genhtml app-manager.info -o app-manager.out
zip -r app-manager.zip app-manager.out
install -m 0644 app-manager.zip %{buildroot}%{_datadir}/gcov/
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
GCOV_PATH="/tmp/home/abuild/rpmbuild/BUILD"
PAKCAGE="%{name}-%{version}"

set_perm() {
    ## Sets the permission for applications
    /usr/bin/find /tmp/home/ -print | /usr/bin/xargs -n1 /usr/bin/chsmack -a "System::Run" &> /dev/null
    /usr/bin/find /tmp/home/ -print | /usr/bin/xargs -n1 /usr/bin/chsmack -a "System::Run" -t &> /dev/null
    /usr/bin/chmod -R 777 /tmp/home/
}

setup() {
    echo "setup start"
    /usr/bin/mkdir -p "${GCOV_PATH}/${PACKAGE}"
    set_perm
}

test_main() {
    echo "test_main start"
    export "GCOV_PREFIX=/tmp"
    /usr/bin/app-manager_unittests
}

teardown() {
    echo "teardown start"
    set_perm
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
%{_libdir}/libcapi-appfw-app-manager.so.*
%{_bindir}/appmgr_tool
%manifest %{name}.manifest
%license LICENSE

%files devel
%{_includedir}/appfw/*.h
%{_libdir}/libcapi-appfw-app-manager.so
%{_libdir}/pkgconfig/*.pc

%files unittests
%{_bindir}/app-manager_unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
