Name:       calendar-service
Summary:    DB library for calendar
Version:    0.1.185
Release:    1
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}d.service
Source2:    org.tizen.CalendarService.dbus.service
Source5:    %{name}d.service.tv
Source1001: %{name}.manifest
Source1002: %{name}.conf.in
Source2001: ALARM.a%{name}.service
BuildRequires: cmake
BuildRequires: python3-setuptools
BuildRequires: pkgconfig(db-util)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkgconfig(alarm-service)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-appfw-application)
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(capi-system-info)

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# TV profile does not have contacts-service2.
# if wearable, ivi, common, mobile ||"undefined"
%if "%{?profile}" != "tv"
BuildRequires: pkgconfig(accounts-svc)
BuildRequires: pkgconfig(contacts-service2)
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Provides: %{name}-compat = %{version}-%{release}

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%description
Calendar Service for using Calendar DB

%package profile_tv
Summary:	for TV
Provides:	%{name}-compat = %{version}-%{release}
Conflicts:	%{name}
%description profile_tv
for TV


%package -n lib%{name}
Summary:	client library
%if "%{?profile}" != "tv"
Requires:	%{name}-compat = %{version}-%{release}
Recommends: %{name} = %{version}-%{release}
%else
Requires:	%{name}-profile_tv = %{version}-%{release}
%endif
%description -n lib%{name}
client library for calendar



%define _dbus_interface org.tizen.CalendarService.dbus

%package devel
Summary:    DB library for calendar
Group:      Development/Libraries
Requires:   lib%{name} = %{version}-%{release}

%description devel
Calendar Service for using Calendar DB(development Kit)

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Calendar Service (gcov)
Group:      Service Framework/Testing
%description gcov
gcov objects for coverage test
%endif

%prep
%setup -q
chmod g-w %_sourcedir/*
cp %SOURCE1001 .

# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# TV profile does not have contacts-service2.
# if wearable, ivi, common, mobile ||"undefined"
%if "%{?profile}" != "tv"
%define _tizen_profile_tv 0
%else
%define _tizen_profile_tv 1
%endif

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
CXXFLAGS="$CXXFLAGS -DU_USING_ICU_NAMESPACE=1"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version} -DBIN_INSTALL_DIR:PATH=%{_bindir} \
		-DDBUS_INTERFACE=%{_dbus_interface} -DTIZEN_PROFILE_TV=%{_tizen_profile_tv}

make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

mkdir -p %{buildroot}%{_unitdir_user}/default.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir_user}
install -m 0644 %SOURCE5 %{buildroot}%{_unitdir_user}

mkdir -p %{buildroot}%{_datadir}/dbus-1/services
install -m 0644 %SOURCE2 %{buildroot}%{_datadir}/dbus-1/services

mkdir -p %{buildroot}/%{_sysconfdir}/dbus-1/session.d
sed -i 's/@DBUS_INTERFACE@/%{_dbus_interface}/g' %SOURCE1002
install -m 0644 %SOURCE1002 %{buildroot}%{_sysconfdir}/dbus-1/session.d/%{name}.conf

# alarm dbus service file
mkdir -p %{buildroot}%{_datadir}/dbus-1/services
install -m 0644 %SOURCE2001 %{buildroot}%{_datadir}/dbus-1/services


%post -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name} -p /sbin/ldconfig

%post profile_tv
mv %{_unitdir_user}/calendar-serviced.service.tv %{_unitdir_user}/calendar-serviced.service

%preun profile_tv
mv %{_unitdir_user}/calendar-serviced.service %{_unitdir_user}/calendar-serviced.service.tv


%files
%{_unitdir_user}/%{name}d.service
# This is for backward-compatibility. This does not deteriorate 4.0 Configurability
# TV profile does not have contacts-service2.
# if wearable, ivi, common, mobile ||"undefined"
%if "%{?profile}" != "tv"
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/calendar-serviced
%{_datadir}/dbus-1/services/%{_dbus_interface}.service
%config %{_sysconfdir}/dbus-1/session.d/%{name}.conf
%{_datadir}/dbus-1/services/ALARM.acalendar-service.service
%license LICENSE.APLv2
%endif


%files profile_tv
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/calendar-serviced-tv
%{_unitdir_user}/%{name}d.service.tv
%{_datadir}/dbus-1/services/%{_dbus_interface}.service
%config %{_sysconfdir}/dbus-1/session.d/%{name}.conf
%{_datadir}/dbus-1/services/ALARM.acalendar-service.service
%license LICENSE.APLv2

%files -n lib%{name}
%manifest %{name}.manifest
%{_libdir}/lib%{name}2.so.*
%license LICENSE.APLv2

%files devel
%defattr(-,root,root,-)
%{_includedir}/calendar-service2/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/calendar-service2.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
