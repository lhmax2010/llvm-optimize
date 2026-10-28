%define _usrdir /usr
%define _ugdir  %{_usrdir}/apps/ug-setting-mobileap-efl

Name:		ug-setting-mobileap-efl
Summary:	Tethering UI Gadget Library
Version:	1.0.162
Release:	1
Group:		App/Network
License:	Flora-1.1
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	pkgconfig(evas)
BuildRequires:	pkgconfig(elementary)
BuildRequires:	pkgconfig(ui-gadget-1)
BuildRequires:	pkgconfig(capi-network-wifi-manager)
BuildRequires:	pkgconfig(capi-network-tethering)
BuildRequires:	pkgconfig(capi-network-connection)
BuildRequires:	pkgconfig(notification)
BuildRequires:	pkgconfig(aul)
BuildRequires:	pkgconfig(bundle)
BuildRequires:	pkgconfig(efl-extension)
BuildRequires:	cmake
BuildRequires:	edje-bin
BuildRequires:	gettext-tools
Requires(post):	/usr/bin/vconftool

%description
Tethering UI Gadget Library

%prep
%setup -q

%build
cmake -DCMAKE_INSTALL_PREFIX="%{_ugdir}"  \
%if "%{?_with_emulator}" == "1"
	-DTIZEN_FEATURE_EMULATOR=1 \
%endif
	.

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install

%post

%files
%manifest ug-setting-mobileap-efl.manifest
%defattr(-,root,root,-)
/usr/ug/res/locale/*/LC_MESSAGES/ug-setting-mobileap-efl*
/usr/ug/res/images/ug-setting-mobileap-efl/*.png
%{_ugdir}/res/edje/ug-setting-mobileap-efl/*.edj
%{_ugdir}/res/help/ug-setting-mobileap-efl/help_setting_tethering.xml
%{_ugdir}/lib/ug/libug-setting-mobileap-efl.so
/usr/share/packages/ug-setting-mobileap-efl.xml
/usr/apps/ug-setting-mobileap-efl/shared/res/tables/ug-setting-mobileap-efl_ChangeableColorInfo.xml
/usr/apps/ug-setting-mobileap-efl/shared/res/tables/ug-setting-mobileap-efl_fontInfoTable.xml
%license LICENSE
