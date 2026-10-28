Name:           syspopup
Summary:        Syspopup package
Version:        0.3.12
Release:        0
Group:          System/Libraries
License:        Apache-2.0
Source0:        syspopup-%{version}.tar.gz
Source1001:     %{name}.manifest
Source1002:     %{name}-devel.manifest
Source1003:     %{name}-caller.manifest
Source1004:     %{name}-caller-devel.manifest
Source1005:     %{name}-tcore.manifest
Source1006:     %{name}-tcore-devel.manifest

BuildRequires:  cmake
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(ecore-wl2)
BuildRequires:  pkgconfig(capi-ui-efl-util)
BuildRequires:  pkgconfig(evas)
BuildRequires:  pkgconfig(elementary)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(capi-system-info)
%if "%{?dev_wos}" != "1"
BuildRequires: pkgconfig(libsmack)
%endif
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-core-wl)

Requires(posttrans): /usr/bin/rm

%define upgrade_script_path /usr/share/upgrade/scripts

%description
syspopup package for popup

%package devel
Summary:    Syspopup development package
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
syspopup development package popup

%package caller
Summary:          Syspopup-caller package
Group:            System/Libraries
Requires:         %{name} = %{version}-%{release}
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description caller
syspopup-caller package for popup

%package caller-devel
Summary:    Syspopup-caller development package
Group:      System/Development
Requires:   %{name} = %{version}-%{release}

%description caller-devel
syspopup-caller development package for popup

%package tcore
Summary:          Syspopup-tcore package
Group:            System/Libraries
Requires:         %{name} = %{version}-%{release}
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description tcore
syspopup-tcore package for tizen-core based popup

%package tcore-devel
Summary:    Syspopup-tcore development package
Group:      System/Development
Requires:   %{name}-tcore = %{version}-%{release}

%description tcore-devel
syspopup-tcore development package for tizen-core based popup

%package test
Summary:    Syspopup test tool package
Group:      System/Testing
Requires:   %{name} = %{version}-%{release}

%description test
syspopup test tool package

%prep
%setup -q
cp %{SOURCE1001} %{SOURCE1002} %{SOURCE1003} %{SOURCE1004} %{SOURCE1005} %{SOURCE1006} .

%build
export CFLAGS="$CFLAGS -DEFL_BETA_API_SUPPORT "
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake -DTZ_SYS_RO_PACKAGES=%{TZ_SYS_RO_PACKAGES} \
	-DTZ_SYS_RO_SHARE=%{TZ_SYS_RO_SHARE} \
	-DEXTRA_CFLAGS=-fPIC \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	-DSYSCONFDIR=%{_sysconfdir} \
	-DTIZEN_FEATURE_SMACK_DISABLE:BOOL=%{?dev_wos:ON}%{!?dev_wos:OFF} \
	-DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
	.

make %{?jobs:-j%jobs}

%install
%make_install
mkdir -p %{buildroot}%{_datadir}
touch %{buildroot}%{_datadir}/popup_noti_term

mkdir -p %{buildroot}%{upgrade_script_path}
cp -f scripts/502.syspopup_upgrade.sh %{buildroot}%{upgrade_script_path}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post caller -p /sbin/ldconfig

%postun caller -p /sbin/ldconfig

%post tcore -p /sbin/ldconfig

%postun tcore -p /sbin/ldconfig

%posttrans
if [ -e %{_sysconfdir}/config/model-config.xml ]; then
	PROFILE=`grep "feature\/profile" %{_sysconfdir}/config/model-config.xml`
	case "${PROFILE}" in
	*"mobile"*)
		rm -rf %{_datarootdir}/syspopup/default/wearable.xml
		rm -rf %{_datarootdir}/syspopup/default/tv.xml
		rm -rf %{_datarootdir}/syspopup/default/common.xml
		rm -rf %{_datarootdir}/syspopup/default/ivi.xml
		;;
	*"wearable"*)
		rm -rf %{_datarootdir}/syspopup/default/mobile.xml
		rm -rf %{_datarootdir}/syspopup/default/tv.xml
		rm -rf %{_datarootdir}/syspopup/default/common.xml
		rm -rf %{_datarootdir}/syspopup/default/ivi.xml
		;;
	*"tv"*)
		rm -rf %{_datarootdir}/syspopup/default/mobile.xml
		rm -rf %{_datarootdir}/syspopup/default/wearable.xml
		rm -rf %{_datarootdir}/syspopup/default/common.xml
		rm -rf %{_datarootdir}/syspopup/default/ivi.xml
		;;
	*"common"*)
		rm -rf %{_datarootdir}/syspopup/default/mobile.xml
		rm -rf %{_datarootdir}/syspopup/default/wearable.xml
		rm -rf %{_datarootdir}/syspopup/default/tv.xml
		rm -rf %{_datarootdir}/syspopup/default/ivi.xml
		;;
	*"ivi"*)
		rm -rf %{_datarootdir}/syspopup/default/mobile.xml
		rm -rf %{_datarootdir}/syspopup/default/wearable.xml
		rm -rf %{_datarootdir}/syspopup/default/tv.xml
		rm -rf %{_datarootdir}/syspopup/default/common.xml
		;;
	*)
		rm -rf %{_datarootdir}/syspopup/default/mobile.xml
		rm -rf %{_datarootdir}/syspopup/default/wearable.xml
		rm -rf %{_datarootdir}/syspopup/default/tv.xml
		rm -rf %{_datarootdir}/syspopup/default/common.xml
		rm -rf %{_datarootdir}/syspopup/default/ivi.xml
		;;
	esac
else
	rm -rf %{_datarootdir}/syspopup/default/mobile.xml
	rm -rf %{_datarootdir}/syspopup/default/wearable.xml
	rm -rf %{_datarootdir}/syspopup/default/tv.xml
	rm -rf %{_datarootdir}/syspopup/default/common.xml
	rm -rf %{_datarootdir}/syspopup/default/ivi.xml
fi

/usr/bin/sp_initdb

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/sp_initdb
%{_libdir}/libsyspopup.so.*
%{_datadir}/popup_noti_term
%license LICENSE
%{upgrade_script_path}/502.syspopup_upgrade.sh
%{_sysconfdir}/syspopup/preload/*
%{_prefix}/share/syspopup/*

%files devel
%manifest %{name}-devel.manifest
%defattr(-,root,root,-)
%{_includedir}/SLP_SYSPOPUP_PG.h
%{_includedir}/syspopup.h
%{_libdir}/libsyspopup.so
%{_libdir}/pkgconfig/syspopup.pc

%files caller
%manifest %{name}-caller.manifest
%defattr(-,root,root,-)
%{_libdir}/libsyspopup_caller.so.*
%license LICENSE

%files caller-devel
%manifest %{name}-caller-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/libsyspopup_caller.so
%{_includedir}/syspopup_caller.h
%{_libdir}/pkgconfig/syspopup-caller.pc

%files tcore
%manifest %{name}-tcore.manifest
%defattr(-,root,root,-)
%{_libdir}/libsyspopup-tcore.so.*
%license LICENSE

%files tcore-devel
%manifest %{name}-tcore-devel.manifest
%defattr(-,root,root,-)
%{_libdir}/libsyspopup-tcore.so
%{_includedir}/syspopup_tcore.h
%{_libdir}/pkgconfig/syspopup-tcore.pc

%files test
%manifest %{name}-caller.manifest
%{_bindir}/sp_test
