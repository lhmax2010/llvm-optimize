Name:       capi-media-controller
Summary:    A media controller library in Tizen Native API
Version:    1.0.20
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    mediacontroller.service
Source2:    mediacontroller.socket
Source3:    mediacontroller2.service
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(cynara-creds-socket)
BuildRequires:  pkgconfig(cynara-uid)
BuildRequires:  pkgconfig(capi-appfw-app-control)
BuildRequires:  pkgconfig(vconf)

# socket activation enable(1), disable(0)
%if ("%{tizen_profile_name}" == "tv")
%define product_tv 1
%if ("%{_vd_cfg_product_type}" == "AUDIO")
%define on_demand 1
%else
%if ("%{sec_buildconf_optimized_memory}" == "1")
%define on_demand 1
%else
%define on_demand 0
%endif
%endif
%else
%define product_tv 0
%define on_demand 1
%endif

%description
This package provides a media controller library in Tizen Native API

%package -n mediacontroller
Summary:    A media controller service for media controller library
Group:      Multimedia/Service

%description -n mediacontroller
This packeage provides media controller service for media controller library

%package devel
Summary:    A media controller library in Tizen Native API (Development)
Group:      Multimedia/Development
Requires:   %{name} = %{version}-%{release}

%description devel
This package provides a media controller library in Tizen Native API(Development files included)
%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Media Controller library in Tizen C API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a media controller library in Tizen native API
%endif
%prep
%setup -q

%build
export CFLAGS="$CFLAGS -Wextra -Wno-array-bounds -Wno-cast-function-type"
export CFLAGS="$CFLAGS -Wno-ignored-qualifiers -Wno-unused-parameter -Wshadow"
export CFLAGS="$CFLAGS -Wwrite-strings -Wswitch-default"
export CFLAGS="$CFLAGS -DGST_EXT_TIME_ANALYSIS -include stdint.h"
%if 0%{?gcov:1}
export CFLAGS="$CFLAGS -fprofile-arcs -ftest-coverage"
export CXXFLAGS="$CXXFLAGS -fprofile-arcs -ftest-coverage"
export FFLAGS="$FFLAGS -fprofile-arcs -ftest-coverage"
export LDFLAGS="$LDFLAGS -lgcov"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
SO_FULLVER=0.3.2
SO_MAJORVER=`echo ${SO_FULLVER} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DSO_FULLVER=${SO_FULLVER} -DSO_MAJORVER=${SO_MAJORVER} \
%if %{on_demand}
 -DON_DEMAND_SOCKET_ACTIVATION=YES \
%else
 -DON_DEMAND_SOCKET_ACTIVATION=NO \
%endif

%__make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

# Daemon & socket activation
mkdir -p %{buildroot}%{_unitdir}
%if %{on_demand}
mkdir -p %{buildroot}%{_unitdir}/sockets.target.wants
%else
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
%endif

# change
%if %{on_demand}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/mediacontroller.service
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/mediacontroller.socket
ln -s ../mediacontroller.socket %{buildroot}%{_unitdir}/sockets.target.wants/mediacontroller.socket
mkdir -p %{buildroot}/etc/gumd/useradd.d
cp -rf %{_builddir}/%{name}-%{version}/30_media-controller-add.post %{buildroot}/etc/gumd/useradd.d/30_media-controller-add.post
%else
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/mediacontroller.service
ln -s ../mediacontroller.service %{buildroot}%{_unitdir}/multi-user.target.wants/mediacontroller.service
%endif

%if 0%{?product_tv}
# os update
mkdir -p %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts
install -p -m 500 packaging/capi-media-controller.sh %{buildroot}%{_datadir}/upgrade/vd_scripts/additional_scripts/capi-media-controller.sh
%endif

%if 0%{?gcov:1}
builddir=$(basename $PWD)
gcno_obj_dir=%{buildroot}%{_datadir}/gcov/obj/%{name}/"$builddir"
mkdir -p "$gcno_obj_dir"
find . -name '*.gcno' -exec cp --parents '{}' "$gcno_obj_dir" ';'
%endif

%post

%postun

%post -n mediacontroller
%if %{on_demand}
chmod 755 /etc/gumd/useradd.d/30_media-controller-add.post
%endif
%postun -n mediacontroller

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*.so.*
%license LICENSE.APLv2.0

%files -n mediacontroller
%manifest media-controller-service.manifest
%defattr(-,root,root,-)
%{_bindir}/mediacontroller
%{_unitdir}/mediacontroller.service
%if %{on_demand}
%{_unitdir}/mediacontroller.socket
%{_unitdir}/sockets.target.wants/mediacontroller.socket
/etc/gumd/useradd.d/30_media-controller-add.post
%else
%{_unitdir}/multi-user.target.wants/mediacontroller.service
%endif
%if 0%{?product_tv}
%{_datadir}/upgrade/vd_scripts/additional_scripts/capi-media-controller.sh
%endif
%license LICENSE.APLv2.0

%files devel
%{_libdir}/*.so
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/capi-media-controller.pc

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif
