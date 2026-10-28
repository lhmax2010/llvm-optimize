%define USE_GCOV 0

Name: e-tizen-unittests
Version: 0.6.31
Release: 1
Summary: The test case runner for enlightenment
URL: http://www.enlightenment.org
Group: Graphics & UI Framework/Other
Source0: %{name}-%{version}.tar.gz
License: BSD-2-Clause
BuildRequires: pkgconfig(enlightenment)
BuildRequires: pkgconfig(libtbm)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(eldbus)
BuildRequires: pkgconfig(capi-ui-efl-util)
BuildRequires: pkgconfig(ecore-wl2)
BuildRequires: gettext
BuildRequires: pkgconfig(tizen-extension-client)
BuildRequires: pkgconfig(tizen-launch-client)
BuildRequires: pkgconfig(tzsh-screensaver-manager-service)
BuildRequires: pkgconfig(tzsh-screensaver-service)
BuildRequires: pkgconfig(tzsh-quickpanel-service)
BuildRequires: pkgconfig(tzsh-quickpanel)
BuildRequires: gtest-devel
BuildRequires: pkgconfig(edje)
BuildRequires: edje-tools
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(pixman-1)
BuildRequires: pkgconfig(aul)
BuildRequires: pkgconfig(capi-appfw-app-control)
BuildRequires: cmake
BuildRequires: hash-signer
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(ecore)
BuildRequires: pkgconfig(efl-extension)

%description
This package is a test case runner for enlightenment.

%prep
%setup -q

%build
export GC_SECTIONS_FLAGS="-fdata-sections -ffunction-sections -Wl,--gc-sections"
export CXXFLAGS+=" -Wall -Werror -g -fPIC -rdynamic ${GC_SECTIONS_FLAGS} -DEFL_BETA_API_SUPPORT "
export LDFLAGS+=" -Wl,--hash-style=both -Wl,--as-needed -Wl,--rpath=/usr/lib"
%if "%{USE_GCOV}" == "1"
export CXXFLAGS+=" -DTIZEN_TEST_GCOV "
%endif
%if "%{tizen_profile_name}" == "tv"
export CXXFLAGS+=" -DDISABLE_GESTURE_TESTS -Wno-error=shadow -Wno-error=missing-field-initializers "
%endif

%autogen
%configure --prefix=/usr
make %{?_smp_mflags}

%define _pkg_dir /usr/apps/org.tizen.input-test
%define _sys_packages_dir /usr/share/packages

cd input-test && \
  cmake -S . -B build \
    -DTZ_SYS_RO_PACKAGES=%{TZ_SYS_RO_PACKAGES} && \
  cmake --build build --parallel

%install
rm -rf %{buildroot}
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/
%__mkdir_p %{buildroot}%{_pkg_dir}/bin
%__mkdir_p %{buildroot}%{_sys_packages_dir}
%__cp -afr data/img/launchimg_splash.png  %{buildroot}/usr/share/e_tizen_unittests/data/
%__cp -afr data/test.txt  %{buildroot}/usr/share/e_tizen_unittests/data/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestBaseOperation/
%__cp -afr data/img/mobile/etTestBaseOperation/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestBaseOperation/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestBaseMulti/
%__cp -afr data/img/mobile/etTestBaseMulti/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestBaseMulti/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestEffect/
%__cp -afr data/img/mobile/etTestEffect/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestEffect/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestNotification/
%__cp -afr data/img/mobile/etTestNotification/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestNotification/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestRotation/
%__cp -afr data/img/mobile/etTestRotation/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestRotation/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestSplash/
%__cp -afr data/img/mobile/etTestSplash/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestSplash/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestTransientFor/
%__cp -afr data/img/mobile/etTestTransientFor/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestTransientFor/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestTzshScreenSaver/
%__cp -afr data/img/mobile/etTestTzshScreenSaver/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestTzshScreenSaver/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestInput/
%__cp -afr data/img/mobile/etTestInput/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestInput/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestFocus/
%__cp -afr data/img/mobile/etTestFocus/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestFocus/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestAuxHint/
%__cp -afr data/img/mobile/etTestAuxHint/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestAuxHint/
%__mkdir_p %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestIconicState/
%__cp -afr data/img/mobile/etTestIconicState/*.png  %{buildroot}/usr/share/e_tizen_unittests/data/mobile/etTestIconicState/

install -D -m 755 input-test/build/input-test \
  %{buildroot}%{_pkg_dir}/bin/input-test
install -D -m 644 org.tizen.input-test.xml \
  %{buildroot}%{_sys_packages_dir}/

# install
make install DESTDIR=%{buildroot}

%define tizen_sign 1
%define tizen_sign_base %{_pkg_dir}
%define tizen_sign_level platform
%define tizen_author_sign 1
%define tizen_dist_sign 1

%post
/sbin/ldconfig

touch /opt/share/askuser_disable
mount -o remount,rw /
tpk-backend --preload -y org.tizen.input-test

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%attr(550,root,root) %{_bindir}/e_tizen_unittests
%license COPYING
%{_datadir}/e_tizen_unittests/data/
%{_pkg_dir}/bin/input-test
%{_sys_packages_dir}/org.tizen.input-test.xml
%{_pkg_dir}/author-signature.xml
%{_pkg_dir}/signature1.xml
