Name:       multi-assistant
Summary:    Multi Assistant client library and daemon
Version:    0.3.22
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-devel.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires:  gawk
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-message-port)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  cmake

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Multi assistant client library and daemon


%package devel
Summary:    Multi assistant header files for MA development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%description devel
Multi assistant header files for MA development.


%package ui-devel
Summary:    Multi assistant manager header files for MA development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%description ui-devel
Multi assistant manager header files for MA development.

%package unittests
Summary:    multi assistant unittests
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description unittests
GTest for multi assistant

%if 0%{?gcov:1}
%package gcov
Summary:  Multi assistant (gcov)
Group:      Graphics & UI Framework/Voice Framework
%description gcov
Multi assistant gcov objects
%endif

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} %{SOURCE1002} .


%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

export CFLAGS+=" -Wno-stringop-overflow -Wno-format-overflow -Wno-format-truncation -Wno-stringop-truncation"
export CXXFLAGS+=" -Wno-stringop-overflow -Wno-format-overflow -Wno-format-truncation -Wno-stringop-truncation"

%cmake . -DCMAKE_INSTALL_PREFIX=/usr -DLIBDIR=%{_libdir} -DBINDIR=%{_bindir} -DINCLUDEDIR=%{_includedir} \
        -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE -DTZ_SYS_BIN=%TZ_SYS_BIN \
%if "%{?profile}" == "tv"
    -DUSE_TRUSTED_MESSAGE_PORT="1" \
%else
    -DUSE_TRUSTED_MESSAGE_PORT="0" \
%endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts
install -p -m 500 script/migration/multi-assistant.sh %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts/multi-assistant.sh

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
find $gcno_obj_dir -name 'ma_ui*' -delete
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
	echo "setup start"
}

test_main() {
	echo "test_main start"
	/usr/bin/multi-assistant-unittests
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

%check
%if 0%{?gcov:1}
ctest --output-on-failure %{?_smp_mflags}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o %{name}.info
genhtml %{name}.info -o %{name}.out
zip -r %{name}.zip %{name}.out %{name}.info
install -m 0644 %{name}.zip %{buildroot}%{_datadir}/gcov/
%endif

%post
/sbin/ldconfig

mkdir -p %{_libdir}/multiassistant/ma

%postun -p /sbin/ldconfig

%files
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libma.so
%{_libdir}/libma_ui.so
%{TZ_SYS_RO_SHARE}/multiassistant/ma/1.0/ma-config.xml
%{TZ_SYS_RO_SHARE}/dbus-1/services/org.tizen.multiassistant*
%{TZ_SYS_RO_SHARE}/parser-plugins/multi-assistant.info
%{TZ_SYS_RO_ETC}/package-manager/parserlib/metadata/libma_assistant_parser.so*
%{_datadir}/upgrade/vd_scripts/additional_scripts/multi-assistant.sh

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/multi-assistant.pc
%{_includedir}/multi_assistant.h
%{_includedir}/multi_assistant_ui.h
%{_includedir}/multi_assistant_common.h
%{_includedir}/multi_assistant_settings.h
%{_includedir}/multi_assistant_internal.h
%{_includedir}/multi_assistant_service.h

%files ui-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/multi-assistant-ui.pc
%{_includedir}/multi_assistant_ui.h
%{_includedir}/multi_assistant_common.h
%{_includedir}/multi_assistant_settings.h

%files unittests
%{_bindir}/multi-assistant-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/*
%endif
