Name:       tts
Summary:    Text To Speech client library and daemon
Version:    1.100.10
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
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(buxton2)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-audio-io)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(ecore)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libgum)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pkgmgr)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(pkgmgr-installer)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(gmock)
BuildRequires:  pkgconfig(rpc-port)

BuildRequires:  cmake
BuildRequires:  tidl

%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%endif

%description
Text To Speech client library and daemon.


%package devel
Summary:    Text To Speech header files for TTS development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%package setting-devel
Summary:    Text To Speech setting header files for TTS development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%package engine-devel
Summary:    Text To Speech engine header files for TTS development
Group:      libdevel
Requires:   %{name} = %{version}-%{release}

%description devel
Text To Speech header files for TTS development.

%description setting-devel
Text To Speech setting header files for TTS development.

%description engine-devel
Text To Speech engine header files for TTS development.

%if 0%{?gcov:1}
%package gcov
Summary:	Text To Speech (gcov)
Group:		Graphics & UI Framework/Voice Framework
%description gcov
Text To Speech gcov objects
%endif

%package unittests
Summary:    TTS tests
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description unittests
GTest for TTS


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} %{SOURCE1002} .

tidlc -p -l C -i tidl/tts.tidl -o tts_proxy
tidlc -s -l C -i tidl/tts.tidl -o ttsd_stub

mv tts_proxy* client
mv ttsd_stub* server

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

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} -DBINDIR=%{_bindir} -DINCLUDEDIR=%{_includedir} \
        -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE -DTZ_SYS_BIN=%TZ_SYS_BIN \
        -DTZ_SYS_RO_PACKAGES=%TZ_SYS_RO_PACKAGES -DTZ_SYS_RO_APP=%TZ_SYS_RO_APP

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%if "%{tizen_profile_name}" == "tv"
mkdir -p %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts
install -p -m 500 script/migration/tts.sh %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts/tts.sh
%else
mkdir -p %{buildroot}%{_datadir}/upgrade/scripts
install -p -m 755 script/public_migration/500.tts.sh %{buildroot}%{_datadir}/upgrade/scripts/500.tts.sh
%endif

%if "%{tizen_profile_name}" == "tv"
mv -f org.tizen.voice.ttsserver.tv.service org.tizen.voice.ttsserver.service
mv -f org.tizen.voice.ttsnotiserver.tv.service org.tizen.voice.ttsnotiserver.service
mv -f org.tizen.voice.ttssrserver.tv.service org.tizen.voice.ttssrserver.service
mv -f org.tizen.voice.ttsinterruptserver.tv.service org.tizen.voice.ttsinterruptserver.service
%endif

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find ./test/ -name '*.gcno' -exec rm {} \;
find ./server/ -name '*.gcno' -exec rm {} \;
find ./tests/ -name '*.gcno' -exec rm {} \;
find ./engine-parser/ -name '*.gcno' -exec rm {} \;
find . -name '*_config*.gcno' -exec rm {} \;
find . -name '*_tidl*.gcno' -exec rm {} \;
find . -name '*_dbus*.gcno' -exec rm {} \;
find . -name '*_proxy*.gcno' -exec rm {} \;
find . -name '*_setting*.gcno' -exec rm {} \;
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

cat << EOF > run-unittest.sh
#!/bin/sh
setup() {
    echo "setup start"
    touch /opt/share/askuser_disable
    mount -o remount,rw /
    tpk-backend --preload -y org.tizen.tts-unittests
}

test_main() {
    echo "test_main start"
    launch_app org.tizen.tts-unittests __AUL_SDK__ UNIT_TEST __LAUNCH_APP_MODE__ SYNC
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
%if "%{_ctest_enable}" == "true"
ctest -V --output-on-failure %{?_smp_mflags}
%if 0%{?gcov:1}
lcov -c --ignore-errors mismatch,graph,unused --no-external -q -d . -o gcov.info
genhtml gcov.info
%endif
%endif

%post
/sbin/ldconfig

mkdir -p %{_libdir}/voice

mkdir -p %{TZ_SYS_RO_SHARE}/voice/test

mkdir -p -m 0775 %{TZ_SYS_DATA}/.voice
chsmack -t %{TZ_SYS_DATA}/.voice
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice
mkdir -p %{TZ_SYS_DATA}/.voice/tts/engine-info
mkdir -p -m 0775 %{TZ_SYS_DATA}/.voice/tts/personal-info
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/tts
chsmack -t %{TZ_SYS_DATA}/.voice/tts/engine-info
chsmack -t %{TZ_SYS_DATA}/.voice/tts/personal-info
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/tts/engine-info
chsmack -a "User::App::Shared" %{TZ_SYS_DATA}/.voice/tts/personal-info
chown -R ui_fw:users %{TZ_SYS_DATA}/.voice

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{TZ_SYS_RO_SHARE}/voice/tts/1.0/tts-config.xml
%{TZ_SYS_RO_SHARE}/dbus-1/system-services/org.tizen.voice.ttsserver.service
%{TZ_SYS_RO_SHARE}/dbus-1/system-services/org.tizen.voice.ttsnotiserver.service
%{TZ_SYS_RO_SHARE}/dbus-1/system-services/org.tizen.voice.ttssrserver.service
%{TZ_SYS_RO_SHARE}/dbus-1/system-services/org.tizen.voice.ttsinterruptserver.service
#%{TZ_SYS_RO_SHARE}/voice/test/tts-test
%{_bindir}/tts_getengine
%{TZ_SYS_RO_ETC}/package-manager/parserlib/metadata/libtts-engine-parser.so*
#%{TZ_SYS_RO_ETC}/package-manager/parserlib/metadata/libtts-engine-language-pack-parser.so*
/etc/dbus-1/system.d/tts-server.conf
%if "%{tizen_profile_name}" == "tv"
%{_datadir}/upgrade/vd_scripts/additional_scripts/tts.sh
%else
%{_datadir}/upgrade/scripts/500.tts.sh
%endif

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/tts.pc
%{_includedir}/tts.h
%{_includedir}/tts_internal.h

%files setting-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/tts-setting.pc
%{_includedir}/tts_setting.h

%files engine-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/tts-engine.pc
%{_includedir}/ttse.h
%{_includedir}/ttse_internal.h

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

%files unittests
%manifest tests/org.tizen.tts-unittests.manifest
%defattr(-,root,root,-)
%{TZ_SYS_RO_PACKAGES}/org.tizen.tts-unittests.xml
%{TZ_SYS_RO_APP}/org.tizen.tts-unittests/res/test_pcm.dat
%{TZ_SYS_RO_APP}/org.tizen.tts-unittests/bin/tts-unittests
%{_bindir}/tizen-unittests/%{name}/run-unittest.sh
