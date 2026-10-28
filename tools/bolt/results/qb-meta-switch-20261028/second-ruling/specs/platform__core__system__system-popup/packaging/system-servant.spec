%bcond_with wayland

Name:       system-servant
Summary:    Servant application for System FW
Version:    0.2.2
Release:    1
Group:      System/Utilities
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source1001:    org.tizen.powerkey-syspopup.manifest
Source1002:    org.tizen.overheat-syspopup.manifest
Source1015:    org.tizen.crash-syspopup.manifest
Source2001:    org.tizen.system-syspopup.manifest
Source2003:    org.tizen.system-signal-sender.manifest
BuildRequires:  pkgconfig(dali2-core)
BuildRequires:  pkgconfig(dali2-adaptor)
BuildRequires:  pkgconfig(dali2-adaptor-integration)
BuildRequires:  pkgconfig(dali2-ui-foundation)
BuildRequires:  pkgconfig(dali2-ui-components)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(appsvc)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(syspopup-caller)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(notification)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(deviced)
BuildRequires:  pkgconfig(feedback)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(capi-media-wav-player)
BuildRequires:  pkgconfig(capi-appfw-application)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(capi-media-recorder)
BuildRequires:  pkgconfig(capi-system-info)
Requires:	system-servant-compat = %{version}-%{release}
Recommends:     system-servant-profile_common = %{version}-%{release}

BuildRequires:  cmake
BuildRequires:  gettext-devel

%description
System applications such as app-launcher
and service file for dbus activation

%package profile_common
Summary:	System-servant configured for common profile
Provides:	system-servant-compat = %{version}-%{release}
Requires:	org.tizen.powerkey-syspopup.common
Requires:	org.tizen.system-syspopup.common
%description profile_common
System-popup (system-servant) configured for common profile.

%package -n org.tizen.crash-syspopup
Summary:    System popup application (crash system popup)
Group:      System/Utilities
Requires:   %{name} = %{version}-%{release}

%description -n org.tizen.crash-syspopup
to inform user crash information. It is activated
when crash event is happend

%package -n org.tizen.powerkey-syspopup.common
Summary:    Powerkey-popup application
Group:      System/Utilities
Requires:   %{name} = %{version}-%{release}

%description -n org.tizen.powerkey-syspopup.common
to inform user powerkey information. It is activated
when user power key event is happened

%package -n org.tizen.overheat-syspopup
Summary:    Overheat-popup application
Group:      System/Utilities
Requires:   %{name} = %{version}-%{release}

%description -n org.tizen.overheat-syspopup
to inform user overheat information. It is activated
when overheat event is happened

%package -n org.tizen.system-signal-sender
Summary:    System FW signal sender
Group:      System/Utilities
Requires:   %{name} = %{version}-%{release}

%description -n org.tizen.system-signal-sender
to inform user system FW signal sender. It is activated
when system event is happend

%package -n org.tizen.system-syspopup.common
Summary:    System popup application
Group:      System/Utilities
Requires:   %{name} = %{version}-%{release}

%description -n org.tizen.system-syspopup.common
to inform user system information. It is activated
when system event is happend

%prep
%setup -q

%build
chmod 0644 %{SOURCE1}
cp %{SOURCE1} .

chmod 0644 %{SOURCE1001}
cp %{SOURCE1001} .

chmod 0644 %{SOURCE1002}
cp %{SOURCE1002} .

chmod 0644 %{SOURCE1015}
cp %{SOURCE1015} .

chmod 0644 %{SOURCE2001}
cp %{SOURCE2001} .

chmod 0644 %{SOURCE2003}
cp %{SOURCE2003} .

%define DPMS none
%if %{with wayland}
%define DPMS wayland
%endif


# BUILD COMMON
mkdir -p build_common
cd build_common
%cmake .. \
		-DCMAKE_INSTALL_PREFIX=%{_prefix} \
		-DPKGNAME=%{name} \
		-DPROFILE=common \
		-DFORMFACTOR=rectangle \
		-DDPMS=%{DPMS} \
		-DTZ_SYS_RO_APP=%{TZ_SYS_RO_APP} \
		-DTZ_SYS_RO_PACKAGES=%{TZ_SYS_RO_PACKAGES} \
		-DTZ_SYS_SMACK=%{TZ_SYS_SMACK} \
		-DTZ_SYS_SHARE=%{TZ_SYS_SHARE} \
		-DTZ_SYS_RO_SHARE=%{TZ_SYS_RO_SHARE} \
		-DTZ_SYS_RO_APP=%{TZ_SYS_RO_APP} \
		-DNOTIFICATION_SERVICE=on

make %{?jobs:-j%jobs}
rm -rf %{buildroot}
%make_install
cd ..

mkdir -p profile_common
mkdir -p profile_common/%{_bindir}
mkdir -p profile_common/%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin
mkdir -p profile_common/%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/shared/res
mkdir -p profile_common/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res
mkdir -p profile_common/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin
mv %{buildroot}/%{_bindir}/sysapp-launcher profile_common/%{_bindir}/sysapp-launcher.common
mv %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin/powerkey-popup profile_common/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin/powerkey-popup.common
mv %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/core_power_off.png profile_common/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res
mv %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/core_restart.png profile_common/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res
mv %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin/system-syspopup profile_common/%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin/system-syspopup.common

%install
cd build_common
%make_install
cd ..

#for common profile
install -m 0755 profile_common/%{_bindir}/* %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/
install -m 0755 profile_common/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin/powerkey-popup.common %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin/powerkey-popup.common
install -m 0755 profile_common/%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin/system-syspopup.common %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin/system-syspopup.common
install -m 0644 profile_common/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/core_power_off.png %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/core_power_off.png
install -m 0644 profile_common/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/core_restart.png %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/core_restart.png

# This is not used. (common has its own postfixed version)
rm -f %{buildroot}%{_bindir}/sysapp-launcher
rm -f %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin/powerkey-popup
rm -f %{buildroot}/%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin/system-syspopup

%check
cd build_common
./tests/system-popup-tests
cd ..




%post profile_common
# This does not support proper uninstall. To uninstall profile_common with
# correct system-servant kept, you need to reinstall system-servant after
# uninstalling profile_common
mv /%{_bindir}/sysapp-launcher.common /%{_bindir}/sysapp-launcher
mv /%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin/system-syspopup.common /%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin/system-syspopup

%post -n org.tizen.powerkey-syspopup.common
mv /%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin/powerkey-popup.common /%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin/powerkey-popup



%files
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_unitdir}/system-popup.service
%{_datadir}/dbus-1/system-services/org.tizen.system.popup.service
%config %{_sysconfdir}/dbus-1/system.d/launcher.conf

#po files to support multi-languages
%lang(ar) %{_datadir}/locale/ar/LC_MESSAGES/system-servant.mo
%lang(az) %{_datadir}/locale/az/LC_MESSAGES/system-servant.mo
%lang(bg) %{_datadir}/locale/bg/LC_MESSAGES/system-servant.mo
%lang(bn) %{_datadir}/locale/bn/LC_MESSAGES/system-servant.mo
%lang(ca) %{_datadir}/locale/ca/LC_MESSAGES/system-servant.mo
%lang(cs) %{_datadir}/locale/cs/LC_MESSAGES/system-servant.mo
%lang(da) %{_datadir}/locale/da/LC_MESSAGES/system-servant.mo
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/system-servant.mo
%lang(el_GR) %{_datadir}/locale/el_GR/LC_MESSAGES/system-servant.mo
%lang(en_PH) %{_datadir}/locale/en_PH/LC_MESSAGES/system-servant.mo
%lang(en) %{_datadir}/locale/en/LC_MESSAGES/system-servant.mo
%lang(en_US) %{_datadir}/locale/en_US/LC_MESSAGES/system-servant.mo
%lang(es_ES) %{_datadir}/locale/es_ES/LC_MESSAGES/system-servant.mo
%lang(es_US) %{_datadir}/locale/es_US/LC_MESSAGES/system-servant.mo
%lang(et) %{_datadir}/locale/et/LC_MESSAGES/system-servant.mo
%lang(eu) %{_datadir}/locale/eu/LC_MESSAGES/system-servant.mo
%lang(fa) %{_datadir}/locale/fa/LC_MESSAGES/system-servant.mo
%lang(fi) %{_datadir}/locale/fi/LC_MESSAGES/system-servant.mo
%lang(fr_CA) %{_datadir}/locale/fr_CA/LC_MESSAGES/system-servant.mo
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/system-servant.mo
%lang(ga) %{_datadir}/locale/ga/LC_MESSAGES/system-servant.mo
%lang(gl) %{_datadir}/locale/gl/LC_MESSAGES/system-servant.mo
%lang(gu) %{_datadir}/locale/gu/LC_MESSAGES/system-servant.mo
%lang(he) %{_datadir}/locale/he/LC_MESSAGES/system-servant.mo
%lang(hi) %{_datadir}/locale/hi/LC_MESSAGES/system-servant.mo
%lang(hr) %{_datadir}/locale/hr/LC_MESSAGES/system-servant.mo
%lang(hu) %{_datadir}/locale/hu/LC_MESSAGES/system-servant.mo
%lang(hy) %{_datadir}/locale/hy/LC_MESSAGES/system-servant.mo
%lang(is) %{_datadir}/locale/is/LC_MESSAGES/system-servant.mo
%lang(it_IT) %{_datadir}/locale/it_IT/LC_MESSAGES/system-servant.mo
%lang(ja_JP) %{_datadir}/locale/ja_JP/LC_MESSAGES/system-servant.mo
%lang(ka) %{_datadir}/locale/ka/LC_MESSAGES/system-servant.mo
%lang(kk) %{_datadir}/locale/kk/LC_MESSAGES/system-servant.mo
%lang(kn) %{_datadir}/locale/kn/LC_MESSAGES/system-servant.mo
%lang(ko_KR) %{_datadir}/locale/ko_KR/LC_MESSAGES/system-servant.mo
%lang(lt) %{_datadir}/locale/lt/LC_MESSAGES/system-servant.mo
%lang(lv) %{_datadir}/locale/lv/LC_MESSAGES/system-servant.mo
%lang(mk) %{_datadir}/locale/mk/LC_MESSAGES/system-servant.mo
%lang(ml) %{_datadir}/locale/ml/LC_MESSAGES/system-servant.mo
%lang(nb) %{_datadir}/locale/nb/LC_MESSAGES/system-servant.mo
%lang(nl) %{_datadir}/locale/nl/LC_MESSAGES/system-servant.mo
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/system-servant.mo
%lang(pt_BR) %{_datadir}/locale/pt_BR/LC_MESSAGES/system-servant.mo
%lang(pt_PT) %{_datadir}/locale/pt_PT/LC_MESSAGES/system-servant.mo
%lang(ro) %{_datadir}/locale/ro/LC_MESSAGES/system-servant.mo
%lang(ru_RU) %{_datadir}/locale/ru_RU/LC_MESSAGES/system-servant.mo
%lang(si) %{_datadir}/locale/si/LC_MESSAGES/system-servant.mo
%lang(sk) %{_datadir}/locale/sk/LC_MESSAGES/system-servant.mo
%lang(sl) %{_datadir}/locale/sl/LC_MESSAGES/system-servant.mo
%lang(sr) %{_datadir}/locale/sr/LC_MESSAGES/system-servant.mo
%lang(sv) %{_datadir}/locale/sv/LC_MESSAGES/system-servant.mo
%lang(ta) %{_datadir}/locale/ta/LC_MESSAGES/system-servant.mo
%lang(te) %{_datadir}/locale/te/LC_MESSAGES/system-servant.mo
%lang(th) %{_datadir}/locale/th/LC_MESSAGES/system-servant.mo
%lang(tr_TR) %{_datadir}/locale/tr_TR/LC_MESSAGES/system-servant.mo
%lang(uk) %{_datadir}/locale/uk/LC_MESSAGES/system-servant.mo
%lang(ur) %{_datadir}/locale/ur/LC_MESSAGES/system-servant.mo
%lang(uz) %{_datadir}/locale/uz/LC_MESSAGES/system-servant.mo
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/system-servant.mo
%lang(zh_HK) %{_datadir}/locale/zh_HK/LC_MESSAGES/system-servant.mo
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/system-servant.mo

%files profile_common
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{_bindir}/sysapp-launcher.common
%{_bindir}/system-cooperator
%{_datadir}/system-apps/res/icons/batt_full_icon.png
%{_datadir}/system-apps/res/icons/batt_full_indicator.png
%{_datadir}/system-apps/res/icons/noti_cooling_down.png
%{_datadir}/system-apps/res/icons/datausage_warning.png
%{_datadir}/system-apps/res/icons/led_torch.png
%{_datadir}/system-apps/res/icons/usb_icon.png

%files -n org.tizen.crash-syspopup
%manifest org.tizen.crash-syspopup.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{TZ_SYS_RO_APP}/org.tizen.crash-syspopup/bin/crash-popup
%{TZ_SYS_RO_SHARE}/packages/org.tizen.crash-syspopup.xml



%files -n org.tizen.system-syspopup.common
%manifest org.tizen.system-syspopup.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{TZ_SYS_RO_APP}/org.tizen.system-syspopup/bin/system-syspopup.common
%{TZ_SYS_RO_SHARE}/packages/org.tizen.system-syspopup.xml

%files -n org.tizen.powerkey-syspopup.common
%manifest org.tizen.powerkey-syspopup.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/bin/powerkey-popup.common
%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/core_power_off.png
%{TZ_SYS_RO_APP}/org.tizen.powerkey-syspopup/res/core_restart.png
%{TZ_SYS_RO_SHARE}/packages/org.tizen.powerkey-syspopup.xml



%files -n org.tizen.overheat-syspopup
%manifest org.tizen.overheat-syspopup.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{TZ_SYS_RO_APP}/org.tizen.overheat-syspopup/bin/overheat-popup
%{TZ_SYS_RO_SHARE}/packages/org.tizen.overheat-syspopup.xml

%files -n org.tizen.system-signal-sender
%manifest org.tizen.system-signal-sender.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{TZ_SYS_RO_APP}/org.tizen.system-signal-sender/bin/system-signal-sender
%{TZ_SYS_RO_SHARE}/packages/org.tizen.system-signal-sender.xml
