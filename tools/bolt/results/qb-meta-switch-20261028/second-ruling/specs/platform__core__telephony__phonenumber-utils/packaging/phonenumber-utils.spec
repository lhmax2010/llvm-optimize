Name:       phonenumber-utils
Summary:    Phone Number Utilities
Version:    0.2.11
Release:    0
Group:      Telephony/Utilities
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.service
Source1001: %{name}.manifest
Source1002: %{name}-test.manifest
Source2001: %{name}.conf.in
BuildRequires: cmake
BuildRequires: gettext-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-system-settings)
BuildRequires: pkgconfig(tapi)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(db-util)
BuildRequires: security-config
BuildRequires: libphonenumber-devel
BuildRequires: pkgconfig(libsystemd)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

%define _unitdir /usr/lib/systemd/system
%define _dbus_name org.tizen.PhonenumberUtils.dbus

%description
Phone Number Utilities(location, formatted number, normalized number)

%package devel
Summary:    Phone Number Utilities (devel)
Group:      Telephony/Development
Requires:   %{name} = %{version}-%{release}

%description devel
Phone Number Utilities development kit

%package test
Summary:    Phone Number Utilities tester
Group:      Telephony/Utilities
Requires:   %{name} = %{version}

%description test
Tizen Phone Number Utilities tester

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    Phone Number Utilities (gcov)
Group:      Service Framework/Testing
%description gcov
gcov objects for coverage test
%endif

%prep
%setup -q
chmod g-w %_sourcedir/*
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

export LDFLAGS+=" -Wl,--copy-dt-needed-entries"
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} \
	-DFULLVER=%{version} \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
        -DPHND_LIB_DIR=%{_libdir} \
	-DPHND_SYS_DB=%{TZ_SYS_GLOBALUSER_DB} \
	-DCMAKE_CXX_STANDARD=17 \
	-DDBUS_INTERFACE=%{_dbus_name}


%install
rm -rf %{buildroot}

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

mkdir -p %{buildroot}/%{_sysconfdir}/dbus-1/system.d
sed -i 's/@DBUS_INTERFACE@/%{_dbus_name}/g' %SOURCE2001
install -m 0644 %SOURCE2001 %{buildroot}%{_sysconfdir}/dbus-1/system.d/%{name}.conf

%post
/sbin/ldconfig
systemctl daemon-reload
if [ $1 == 1 ]; then
    systemctl restart %{name}.service
fi


%postun
/sbin/ldconfig
if [ $1 == 0 ]; then
    systemctl stop %{name}.service
fi
systemctl daemon-reload


%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{_unitdir}/%{name}.service
%{_bindir}/%{name}-daemon
%{_datadir}/dbus-1/system-services/%{_dbus_name}.service
%{_libdir}/lib%{name}.so.*
%{_libdir}/lib%{name}-geocoding.so
%license LICENSE.APLv2
%config %{_sysconfdir}/dbus-1/system.d/%{name}.conf


%files devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/*.h


%files test
%defattr(-,root,root,-)
%manifest %{name}-test.manifest
%{_bindir}/%{name}-test
%license LICENSE.APLv2

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
