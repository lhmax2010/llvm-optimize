Name:       voice-control
Summary:    Voice control client library and daemon
Version:    1.101.4
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-devel.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires:  gawk
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(buxton2)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-audio-io)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(db-util)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  pkgconfig(bundle)

BuildRequires:  cmake
BuildRequires:  tidl

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Voice Control client library and daemon


%package devel
Summary:    Voice control header files for VC development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%description devel
Voice control header files for VC development.


%package widget-devel
Summary:    Voice control widget header files for VC development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%description widget-devel
Voice control widget header files for VC development.


%package manager-devel
Summary:    Voice control manager header files for VC development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%description manager-devel
Voice control manager header files for VC development.


%package setting-devel
Summary:    Voice control setting header files for VC development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%description setting-devel
Voice control setting header files for VC development.


%package engine-devel
Summary:    Voice control engine header files for VC development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%description engine-devel
Voice control engine header files for VC development.

%if 0%{?gcov:1}
%package gcov
Summary:	Voice control (gcov)
Group:		Graphics & UI Framework/Voice Framework
%description gcov
Voice control gcov objects
%endif

%package unittests
Summary:    Voice control tests
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description unittests
GTest for Voice Control


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} %{SOURCE1002} .

tidlc -p -l C -i tidl/vc.tidl -o vc_proxy -n
tidlc -s -l C -i tidl/vc.tidl -o vcd_stub -n

tidlc -p -l C -i tidl/vc_setting.tidl -o vc_setting_proxy -n
tidlc -s -l C -i tidl/vc_setting.tidl -o vcd_setting_stub -n

tidlc -p -l C -i tidl/vc_mgr.tidl -o vc_mgr_proxy -n
tidlc -s -l C -i tidl/vc_mgr.tidl -o vcd_mgr_stub -n
tidlc -s -l C -i tidl/vcd_mgr.tidl -o vc_mgr_stub -n
tidlc -p -l C -i tidl/vcd_mgr.tidl -o vcd_mgr_proxy -n

tidlc -p -l C -i tidl/vc_widget.tidl -o vc_widget_proxy -n
tidlc -s -l C -i tidl/vc_widget.tidl -o vcd_widget_stub -n
tidlc -s -l C -i tidl/vcd_widget.tidl -o vc_widget_stub -n
tidlc -p -l C -i tidl/vcd_widget.tidl -o vcd_widget_proxy -n

mv vc_* client
mv vcd_* server

%build
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

%if "%{tizen_profile_name}" == "tv"
export CFLAGS="$CFLAGS -DTV_PRODUCT"
cmake . -DCMAKE_INSTALL_PREFIX=/usr -DLIBDIR=%{_libdir} -DBINDIR=%{_bindir} -DINCLUDEDIR=%{_includedir} \
        -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE -D_TV_PRODUCT=TRUE -DTZ_SYS_BIN=%TZ_SYS_BIN -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP
%else
cmake . -DCMAKE_INSTALL_PREFIX=/usr -DLIBDIR=%{_libdir} -DBINDIR=%{_bindir} -DINCLUDEDIR=%{_includedir} \
        -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE -DTZ_SYS_BIN=%TZ_SYS_BIN -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP
make %{?jobs:-j%jobs}
%endif

%install
rm -rf %{buildroot}

%if "%{tizen_profile_name}" == "tv"
mkdir -p %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts
install -p -m 500 script/migration/voice-control.sh %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts/voice-control.sh
%endif

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find ./server/ -name '*.gcno' -exec rm {} \;
find ./audio-manager/ -name '*.gcno' -exec rm {} \;
find ./testsuite/ -name '*.gcno' -exec rm {} \;
find ./engine-parser/ -name '*.gcno' -exec rm {} \;
find . -name '*_cmd_db.c.gcno' -exec rm {} \;
find . -name '*_config_*.gcno' -exec rm {} \;
find . -name '*_parser.c.gcno' -exec rm {} \;
find . -name 'vc_setting*.gcno' -exec rm {} \;
find . -name 'vc_widget*.gcno' -exec rm {} \;
find . -name '*tidl*.gcno' -exec rm {} \;
find . -name '*proxy*.gcno' -exec rm {} \;
find . -name '*stub*.gcno' -exec rm {} \;
find . -name 'vc_command_util*.gcno' -exec rm {} \;
find . -name 'VoiceControl*.gcno' -exec rm {} \;
find . -name '*_data*.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
    touch /opt/share/askuser_disable
    mount -o remount,rw /
    tpk-backend --preload -y org.tizen.vc-unittests
}

test_main() {
    echo "test_main start"
    launch_app org.tizen.vc-unittests __AUL_SDK__ UNIT_TEST __LAUNCH_APP_MODE__ SYNC
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

%post
/sbin/ldconfig

mkdir -p %{_libdir}/voice/vc

mkdir -p -m 0775 %{TZ_SYS_DATA}/.voice
chsmack -t %{TZ_SYS_DATA}/.voice
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice
mkdir -p -m 0775 %{TZ_SYS_DATA}/.voice/vc
mkdir -p -m 0775 %{TZ_SYS_DATA}/.voice/vc/1.0
mkdir -p -m 0775 %{TZ_SYS_DATA}/.voice/vc/1.0/engine-info
# Force group-writable mode even when the directories already exist (upgrade case;
# 'mkdir -p' does not change the mode of an existing directory). The VC daemon runs
# as uid 5001 (group 'users') and must be able to create its command DB (.vc_info.db)
# directly under .voice/vc, so these directories have to be group-writable (0775).
chmod 0775 %{TZ_SYS_DATA}/.voice/vc %{TZ_SYS_DATA}/.voice/vc/1.0 %{TZ_SYS_DATA}/.voice/vc/1.0/engine-info
# The command DB (.vc_info.db) is created at run time directly under .voice/vc by
# whichever voice-control process runs first (engine or a client). Mark the
# directory SMACK-transmute so those files inherit the shared "User::App::Shared"
# label instead of the creator's per-package label; otherwise another package
# (e.g. a different engine or the ITC test app) is denied access to the DB.
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/vc
chsmack -t %{TZ_SYS_DATA}/.voice/vc
chsmack -t %{TZ_SYS_DATA}/.voice/vc/1.0
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/vc/1.0
chsmack -t %{TZ_SYS_DATA}/.voice/vc/1.0/engine-info
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/vc/1.0/engine-info
chown -R ui_fw:users %{TZ_SYS_DATA}/.voice

%postun -p /sbin/ldconfig

%files
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libvc.so
%{_libdir}/libvc_setting.so
%{_libdir}/libvc_widget.so
%{_libdir}/libvc_manager.so
%{_libdir}/libvc_engine.so
%{_bindir}/vc_getengine
%{TZ_SYS_RO_SHARE}/voice/vc/1.0/vc-config.xml
%{TZ_SYS_RO_SHARE}/voice/vc/1.0/dependency-audio-manager/libvc-audio-manager.so
%{TZ_SYS_RO_SHARE}/parser-plugins/voice-control.info
%{TZ_SYS_RO_ETC}/package-manager/parserlib/metadata/libvc-engine-parser.so*
%if "%{tizen_profile_name}" == "tv"
%{_datadir}/upgrade/vd_scripts/additional_scripts/voice-control.sh
%endif

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/voice-control.pc
%{_includedir}/voice_control.h
%{_includedir}/voice_control_internal.h
%{_includedir}/voice_control_authority.h
%{_includedir}/voice_control_command.h
%{_includedir}/voice_control_common.h
%{_includedir}/voice_control_key_defines.h
%{_includedir}/voice_control_command_expand.h

%files widget-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/voice-control-widget.pc
%{_includedir}/voice_control_widget.h
%{_includedir}/voice_control_command.h
%{_includedir}/voice_control_common.h
%{_includedir}/voice_control_key_defines.h
%{_includedir}/voice_control_command_expand.h
%{_includedir}/voice_control_internal.h

%files manager-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/voice-control-manager.pc
%{_includedir}/voice_control_manager.h
%{_includedir}/voice_control_manager_internal.h
%{_includedir}/voice_control_command.h
%{_includedir}/voice_control_common.h
%{_includedir}/voice_control_key_defines.h
%{_includedir}/voice_control_command_expand.h

%files setting-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/voice-control-setting.pc
%{_includedir}/voice_control_setting.h

%files engine-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/voice-control-engine.pc
%{_includedir}/vce.h
%{_includedir}/vce_internal.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%defattr(-,root,root,-)
%{TZ_SYS_RO_PACKAGES}/org.tizen.vc-unittests.xml
%{TZ_SYS_RO_APP}/org.tizen.vc-unittests/res/*
%{TZ_SYS_RO_APP}/org.tizen.vc-unittests/bin/vc-unittests
%{TZ_SYS_RO_APP}/org.tizen.vc-unittests/bin/vc-itctests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
