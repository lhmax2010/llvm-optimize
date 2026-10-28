Name:       stt
Summary:    Speech To Text client library and daemon
Version:    1.101.5
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Source1002: %{name}-devel.manifest
Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/buxton2ctl
Requires(postun): /sbin/ldconfig
Requires:  gawk
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:	pkgconfig(buxton2)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-audio-io)
BuildRequires:  pkgconfig(capi-media-wav-player)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-self)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(gmock)
%if "%{tizen_profile_name}" == "tv"
BuildRequires:  pkgconfig(capi-network-bluetooth)
BuildRequires:  pkgconfig(capi-network-bluetooth-tv)
BuildRequires:  pkgconfig(farfield-voice-api)
%endif

BuildRequires:  cmake

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Speech To Text client library and daemon.


%package devel
Summary:    Speech To Text header files for STT development
Group:      Graphics & UI Framework/Development
Requires:   %{name} = %{version}-%{release}

%package file-devel
Summary:    File To Text header files for STT FILE development
Group:      Graphics & UI Framework/Development
Requires:   %{name} = %{version}-%{release}

%package setting-devel
Summary:    Speech To Text setting header files for STT development
Group:      Graphics & UI Framework/Development
Requires:   %{name} = %{version}-%{release}

%package engine-devel
Summary:    Speech To Text engine header files for STT development
Group:      Graphics & UI Framework/Development
Requires:   %{name} = %{version}-%{release}

%package unittests
Summary:    STT tests
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description unittests
GTest for STT

%description devel
Speech To Text header files for STT development.

%description file-devel
File To Text header files for STT FILE development.

%description setting-devel
Speech To Text setting header files for STT development.

%description engine-devel
Speech To Text engine header files for STT development.

%if 0%{?gcov:1}
%package gcov
Summary:	Speech To Text (gcov)
Group:		Graphics & UI Framework/Voice Framework
%description gcov
Speech To Text gcov objects
%endif


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} %{SOURCE1002} .


%build
export CFLAGS="$CFLAGS -DTIZEN_ENGINEER_MODE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_ENGINEER_MODE"
export FFLAGS="$FFLAGS -DTIZEN_ENGINEER_MODE"

export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage -DTIZEN_TEST_GCOV"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif


%if "%{tizen_profile_name}" == "tv"
export CFLAGS="$CFLAGS -DTV_PRODUCT"
cmake . -DCMAKE_INSTALL_PREFIX=/usr -DLIBDIR=%{_libdir} -DBINDIR=%{_bindir} -DINCLUDEDIR=%{_includedir} \
        -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE -DTZ_SYS_BIN=%TZ_SYS_BIN -D_TV_PRODUCT=TRUE \
        -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP
%else
cmake . -DCMAKE_INSTALL_PREFIX=/usr -DLIBDIR=%{_libdir} -DBINDIR=%{_bindir} -DINCLUDEDIR=%{_includedir} \
        -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE -DTZ_SYS_BIN=%TZ_SYS_BIN \
        -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP
%endif

make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts
install -p -m 500 script/migration/stt.sh %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts/stt.sh

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find ./server/ -name '*.gcno' -exec rm {} \;
find ./engine-parser/ -name '*.gcno' -exec rm {} \;
find ./testsuite/ -name '*.gcno' -exec rm {} \;
find . -name '*_client.c.gcno' -exec rm {} \;
find . -name '*_dbus.c.gcno' -exec rm {} \;
find . -name 'stt_config*.gcno' -exec rm {} \;
find . -name '*_engine.c.gcno' -exec rm {} \;
find . -name 'sttd*.gcno' -exec rm {} \;
find . -name '*_file*.gcno' -exec rm {} \;
find . -name '*_network.c.gcno' -exec rm {} \;
find . -name '*_setting.c.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
    touch /opt/share/askuser_disable
    mount -o remount,rw /
    tpk-backend --preload -y org.tizen.stt-unittests
}

test_main() {
    echo "test_main start"
    launch_app org.tizen.stt-unittests __AUL_SDK__ UNIT_TEST __LAUNCH_APP_MODE__ SYNC
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

mkdir -p %{_libdir}/voice/

mkdir -p %{TZ_SYS_RO_SHARE}/voice/test

mkdir -p -m 0775 %{TZ_SYS_DATA}/.voice
chsmack -t %{TZ_SYS_DATA}/.voice
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice
mkdir -p -m 0775 %{TZ_SYS_DATA}/.voice/stt/1.0/engine-info
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/stt
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/stt/1.0
chsmack -t %{TZ_SYS_DATA}/.voice/stt/1.0/engine-info
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/stt/1.0/engine-info
if [ -d /opt/usr/home/owner/share/.voice/stt/1.0/engine-info ]; then
    cp -af /opt/usr/home/owner/share/.voice/stt/1.0/engine-info/. %{TZ_SYS_DATA}/.voice/stt/1.0/engine-info/ || true
fi
if [ -d /opt/usr/data/.voice/stt/1.0/engine-info ]; then
    cp -af /opt/usr/data/.voice/stt/1.0/engine-info/. %{TZ_SYS_DATA}/.voice/stt/1.0/engine-info/ || true
fi
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/stt/1.0/engine-info/*.xml 2>/dev/null || true
chown -R ui_fw:users %{TZ_SYS_DATA}/.voice

rm -f /etc/dbus-1/session.d/stt-server.conf
rm -f %{TZ_SYS_RO_SHARE}/dbus-1/services/org.tizen.voice.sttserver.service
rm -f %{TZ_SYS_RO_SHARE}/dbus-1/services/org.tizen.voice.sttservercustom.service

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_libdir}/lib*.so
/etc/dbus-1/system.d/stt-server.conf
%{TZ_SYS_RO_SHARE}/voice/stt/1.0/stt-config.xml
%{TZ_SYS_RO_SHARE}/dbus-1/system-services/org.tizen.voice.sttserver.service
%{TZ_SYS_RO_SHARE}/dbus-1/system-services/org.tizen.voice.sttservercustom.service
#%{TZ_SYS_RO_SHARE}/voice/test/stt-test
#%{TZ_SYS_BIN}/*
%{_bindir}/voice_getengine
%{TZ_SYS_RO_ETC}/package-manager/parserlib/metadata/libstt-engine-parser.so*
%{_datadir}/upgrade/vd_scripts/additional_scripts/stt.sh

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/stt.pc
%{_includedir}/stt.h
%{_includedir}/stt_internal.h

%files file-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/stt-file.pc
%{_includedir}/stt_file.h

%files setting-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/stt-setting.pc
%{_includedir}/stt_setting.h

%files engine-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/stt-engine.pc
%{_includedir}/stte.h
%{_includedir}/stte_internal.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%manifest testsuite/unittests/org.tizen.stt-unittests.manifest
%defattr(-,root,root,-)
%{TZ_SYS_RO_PACKAGES}/org.tizen.stt-unittests.xml
%{TZ_SYS_RO_APP}/org.tizen.stt-unittests/res/test_pcm.dat
%{TZ_SYS_RO_APP}/org.tizen.stt-unittests/res/ringtone.wav
%{TZ_SYS_RO_APP}/org.tizen.stt-unittests/bin/stt-unittests
%{TZ_SYS_RO_APP}/org.tizen.stt-unittests/bin/stt-itc
%{TZ_SYS_RO_APP}/org.tizen.stt-unittests/bin/libstt_mock.so*
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
