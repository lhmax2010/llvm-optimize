Name:       contacts-service
Summary:    Contacts Service
Version:    0.13.79
Release:    0
Group:      Social & Content/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.service
Source2:    %{name}.socket
Source3:    %{name}-mobile.service
Source1001: %{name}.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(db-util)
BuildRequires: pkgconfig(vconf)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(tapi)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-media-image-util)
BuildRequires: pkgconfig(pims-ipc)
BuildRequires: pkgconfig(accounts-svc)
BuildRequires: pkgconfig(libexif)
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(cynara-client)
BuildRequires: pkgconfig(cynara-session)
BuildRequires: pkgconfig(cynara-creds-socket)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(icu-uc)
BuildRequires: pkgconfig(phonenumber-utils)
BuildRequires: pkgconfig(libsystemd)
%if 0%{?gcov:1}
BuildRequires: lcov
%endif
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Contacts Service Library

%package -n lib%{name}
Summary:	New Contacts service library
Requires:	%{name} = %{version}-%{release}
%description -n lib%{name}
New Contact Serivce Client Library

%package devel
Summary:  Contacts Service(devel)
Group:    Social & Content/Development
Requires: lib%{name} = %{version}-%{release}
%description devel
New Contacts Service Library (devel) files

%package test
Summary:  Contacts Service(test)
Group:    Social & Content/Testing
Requires: lib%{name} = %{version}-%{release}
%description test
New Contacts Service Test Program

#################################################
# gcov
#################################################
%if 0%{?gcov:1}
%package gcov
Summary:    COntacts library (gcov)
Group:      Service Framework/Testing
%description gcov
gcov objects for coverage test
%endif

%prep
%setup -q
chmod g-w %_sourcedir/*
cp %{SOURCE1001} ./%{name}.manifest
cp %{SOURCE1001} ./%{name}-test.manifest

%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_VERBOSE_MAKEFILE=OFF \
	-DMAJORVER=${MAJORVER} -DFULLVER=%{version} \
	-DBIN_INSTALL_DIR:PATH=%{_bindir} \
	-DTZ_SYS_ETC=%TZ_SYS_ETC \
	-DENABLE_LOG_FEATURE:BOOL=ON \
	-DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}

%__make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%make_install

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

mkdir -p %{buildroot}%{_unitdir_user}/delayed.target.wants
install -m 0644 %SOURCE3 %{buildroot}%{_unitdir_user}/contacts-service.service.mobile
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir_user}/contacts-service.service
ln -s ../contacts-service.service %{buildroot}%{_unitdir_user}/delayed.target.wants/contacts-service.service

mkdir -p %{buildroot}%{_unitdir_user}/sockets.target.wants
install -m 0644 %SOURCE2 %{buildroot}%{_unitdir_user}/contacts-service.socket
ln -s ../contacts-service.socket %{buildroot}%{_unitdir_user}/sockets.target.wants/contacts-service.socket

%post
_PROFILE=`grep "TZ_BUILD_PROFILE" "/etc/tizen-build.conf" | awk -F '=' '{print $2}'`
if [ "$_PROFILE" != "mobile" ]
then
	rm %{_unitdir_user}/contacts-service.service.mobile
else
	mv %{_unitdir_user}/contacts-service.service.mobile %{_unitdir_user}/contacts-service.service
fi

%post test
chsmack -e "User" /usr/bin/contacts-service-test

%post -n lib%{name} -p /sbin/ldconfig


%postun -n lib%{name} -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/contacts-service-ipcd*
%{_unitdir_user}/contacts-service.service
%{_unitdir_user}/contacts-service.service.mobile
%{_unitdir_user}/delayed.target.wants/contacts-service.service
%{_unitdir_user}/sockets.target.wants/contacts-service.socket
%{_unitdir_user}/contacts-service.socket
%license LICENSE.APLv2

%files -n lib%{name}
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libcontacts-service2.so.*
%license LICENSE.APLv2

%files devel
%defattr(-,root,root,-)
%{_libdir}/libcontacts-service2.so
%{_libdir}/pkgconfig/contacts-service2.pc
%{_includedir}/contacts-svc/contacts.h
%{_includedir}/contacts-svc/contacts_*.h
%license LICENSE.APLv2

%files test
%manifest %{name}-test.manifest
%defattr(-,root,root,-)
%{_bindir}/contacts-service-test
%license LICENSE.APLv2

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
