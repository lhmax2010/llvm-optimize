Name:		voice-control-elm
Summary:	voice-control-elm library
Version:	0.100.2
Release:	1
Group:		Graphics & UI Framework/Voice Framework
License:	Apache-2.0
URL:		N/A
Source0:	%{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-devel.manifest
BuildRequires:	cmake
BuildRequires:	edje-tools
BuildRequires:	pkgconfig(capi-base-common)
BuildRequires:	pkgconfig(capi-system-info)
BuildRequires:	pkgconfig(cynara-client)
BuildRequires:	pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(ecore)
BuildRequires:	pkgconfig(eina)
BuildRequires:	pkgconfig(edje)
BuildRequires:	pkgconfig(capi-ui-efl-util)
BuildRequires:	pkgconfig(elementary)
BuildRequires:	pkgconfig(evas)
BuildRequires:	pkgconfig(libtzplatform-config)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(voice-control-widget)
BuildRequires:	pkgconfig(vconf)
BuildRequires:	gettext-tools
BuildRequires:	pkgconfig(gmock)

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
voice-control-elm library that provides advanced Voice Driven Control over UI

%package devel
Summary:	voice-control-elm library development headers
Group:		Development/Libraries
Requires:	 %{name} = %{version}

%description devel
voice-control-elm library development headers

%if 0%{?gcov:1}
%package gcov
Summary:	voice-control-elm (gcov)
Group:		Graphics & UI Framework/Voice Framework
%description gcov
voice-control-elm gcov objects
%endif

%package unittests
Summary:    voice-control-elm tests
Group:      Development/Libraries
Requires:   %{name} = %{version}

%description unittests
voice-control-elm gtests

%prep
%setup -q
cp %{SOURCE1001} %{SOURCE1002} .

%build
export LDFLAGS+=" -Wl,--rpath=%{_libdir} -Wl,--hash-style=both -Wl,--as-needed"

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

rm -rf objdir
mkdir objdir

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%{?SRPOL_DEBUG:
(cd objdir && cmake .. -DVERSION=%{version} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIBDIR=%{_libdir} \
	-DINCLUDEDIR=%{_includedir} \
	-DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE \
	-DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES \
	-DTZ_SYS_RO_APP=%TZ_SYS_RO_APP \
	-DTZ_SYS_BIN=%TZ_SYS_BIN \
	-DCMAKE_BUILD_TYPE=Debug \
	-DMAJORVER=${MAJORVER} \
	-DSRPOL_DEBUG="1")
}
%{!?SRPOL_DEBUG:
(cd objdir && cmake .. -DVERSION=%{version} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIBDIR=%{_libdir} \
	-DINCLUDEDIR=%{_includedir} \
	-DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE \
	-DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES \
	-DTZ_SYS_RO_APP=%TZ_SYS_RO_APP \
	-DTZ_SYS_BIN=%TZ_SYS_BIN \
	-DCMAKE_BUILD_TYPE=Debug \
	-DMAJORVER=${MAJORVER} \
	-DSRPOL_DEBUG="0")
}
(cd objdir && make %{?jobs:-j%jobs})


%install
rm -rf %{buildroot}

(cd objdir &&
%make_install)

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find ./objdir/tests/ -name '*.gcno' -exec rm {} \;
find . -name 'vc_elm_*.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
    touch /opt/share/askuser_disable
    mount -o remount,rw /
    tpk-backend --preload -y org.tizen.vc-elm-unittests
}

test_main() {
    echo "test_main start"
    launch_app org.tizen.vc-elm-unittests __AUL_SDK__ UNIT_TEST __LAUNCH_APP_MODE__ SYNC
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
install -m 0755 run-unittest.sh %{buildroot}%{_bindir}/tizen-unittests/%{name}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

mkdir -p %{TZ_SYS_RO_SHARE}/voice

%files
%license LICENSE
%manifest %{name}.manifest
%attr(644,root,root)
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%{_datadir}/*
%{TZ_SYS_RO_SHARE}/locale/*
%{TZ_SYS_RO_SHARE}/voice/vc-elm/1.0/voice-control-elm-config.xml

%files devel
%manifest %{name}-devel.manifest
%{_libdir}/*.so
%{_includedir}/voice_control_elm.h
%{_includedir}/voice_control_elm_private.h
%{_libdir}/pkgconfig/%{name}.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%manifest tests/org.tizen.vc-elm-unittests.manifest
%defattr(-,root,root,-)
%{TZ_SYS_RO_PACKAGES}/org.tizen.vc-elm-unittests.xml
%{TZ_SYS_RO_APP}/org.tizen.vc-elm-unittests/bin/vc-elm-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
