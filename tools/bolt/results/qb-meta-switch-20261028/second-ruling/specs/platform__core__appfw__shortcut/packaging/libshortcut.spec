Name: libshortcut
Summary: Shortcut add feature supporting library
Version: 0.10.5
Release: 0
Group: Applications/Core Applications
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source2: esd-shortcut.socket

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake, gettext-tools, coreutils
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(db-util)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(gmock)
BuildRequires: pkgconfig(capi-appfw-app-common)
BuildRequires: pkgconfig(capi-appfw-app-manager)
BuildRequires: pkgconfig(capi-appfw-package-manager)
BuildRequires: pkgconfig(rpc-port)
BuildRequires: pkgconfig(parcel)
BuildRequires: pkgconfig(libesd)
BuildRequires: pkgconfig(tizen-database)

BuildRequires: tidl

%define _moddir %{_datadir}/esd

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
[Shortcut] AddToHome feature supporting library for menu/home screen developers.

%package devel
Summary:    AddToHome feature supporting library development files
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
[Shortcut] AddToHome feature supporting library for menu/home screen developers(dev).

#################################################
# shortcut_unittests
#################################################
%package unittests
Summary:    GTest for shortcut API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for shortcut API

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:  Shortcut API(gcov)
Group:    System/API

%description gcov
gcov objects of an Shortcut library
%endif

%prep
%setup -q
cp %{SOURCE1001} .
tidlc -p -l C++ -i ./tidl/shortcut.tidl -o shortcut_proxy
mv shortcut_proxy.* ./lib/src/
tidlc -s -l C++ -i ./tidl/shortcut.tidl -o shortcut_stub
mv shortcut_stub.* ./modules/shortcut/

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
	-DSYSCONFDIR=%{_sysconfdir} \
	-DDB_PATH=%{TZ_SYS_DB}/.shortcut_service.db \
	-DESD_MODULES_DIR=%{_moddir} \
	-DMAJORVER=${MAJORVER} \
	-DFULLVER=%{version} \
	%if 0%{?asan} != 1
		-DASAN_ENABLED=FALSE
	%else
		-DASAN_ENABLED=TRUE
	%endif

make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH=./lib
ctest -V
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o shortcut.info
lcov -r shortcut.info "_proxy*" -o shortcut.info
lcov -r shortcut.info "_stub*" -o shortcut.info
lcov -r shortcut.info "/unit_tests/*" -o shortcut.info
lcov -r shortcut.info "/mock/*" -o shortcut.info
genhtml shortcut.info -o shortcut.out
zip -r shortcut.zip shortcut.out
install -m 0644 shortcut.zip %{buildroot}%{_datadir}/gcov/shortcut.zip
%endif

%install
rm -rf %{buildroot}

%make_install
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
install -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/esd-shortcut.socket
ln -sf ../esd-shortcut.socket %{buildroot}%{_unitdir}/sockets.target.wants/esd-shortcut.socket

mkdir -p %{buildroot}%{TZ_SYS_DB}

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
    /usr/bin/shortcut_unittests
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

%post
/sbin/ldconfig

if [ ! -d %{TZ_SYS_DB} ]
then
	mkdir %{TZ_SYS_DB}
fi

%postun -n %{name} -p /sbin/ldconfig

%files -n libshortcut
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libshortcut.so.*
%{_sysconfdir}/package-manager/parserlib/*
%{_moddir}/mod/libesd-mod-shortcut.so
%{_unitdir}/esd-shortcut.socket
%{_datarootdir}/parser-plugins/shortcut.info
%{_unitdir}/sockets.target.wants/esd-shortcut.socket

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/shortcut/shortcut.h
%{_includedir}/shortcut/shortcut_manager.h
%{_includedir}/shortcut/shortcut_error.h
%{_libdir}/pkgconfig/shortcut.pc
%{_libdir}/libshortcut.so

#################################################
# shortcut_unittests
#################################################
%files unittests
%{_bindir}/shortcut_unittests
%{_bindir}/shortcut_integtests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
