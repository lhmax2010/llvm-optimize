Name:       context-sensor-recorder
Summary:    Sensor recorder service server and client libraries
Version:    4.0.1
Release:    1
Group:      Service Framework/Context
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(sensor)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(context-common-server)
BuildRequires: pkgconfig(context-common-client)

Requires:   %{name}-dummy = %{version}-%{release}
Requires:   context-service

Provides:   %{name}-profile_mobile = %{version}-%{release}
Provides:   %{name}-profile_wearable = %{version}-%{release}

%global __provides_exclude ^.*-genuine\\.so.*$

%description
This package provides fully functional libraries of the sensor recorder service,
which is a part of the Tizen Contextual service framework.
The libraries replace the dummy libraries installed by %{name}-dummy.


%package dummy
Summary:    Sensor recorder service 'dummy' libraries

%description dummy
This package provides dummy libraries of the sensor recorder service,
which is a part of the Tizen Contextual service framework.
Installing %{name} replaces these dummy libraries with the actually functional libraries.


%package devel
Summary:    Headers of the sensor recorder service server and client libraries
Group:      Service Framework/Context
Requires:	%{name}-dummy = %{version}-%{release}

%description devel
This package provides headers of the sensor recorder service libraries,
which is a part of the Tizen Contextual service framework.


%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

export CXXFLAGS+=" -Wextra -Wcast-align -Wshadow -Wwrite-strings -Wswitch-default -Wno-unused-parameter"
export CXXFLAGS+=" -Wno-empty-body -fomit-frame-pointer -fno-optimize-sibling-calls"
export CXXFLAGS+=" -fno-strict-aliasing -fno-unroll-loops -fsigned-char -fstrict-overflow"
export CXXFLAGS+=" -Wnon-virtual-dtor -std=c++0x"

%cmake . -DCMAKE_VERBOSE_MAKEFILE=OFF -DMAJORVER=${MAJORVER} -DFULLVER=%{version}
make %{?_smp_mflags}

%install
%make_install


%post
pushd %{_libdir}
ln -sf lib%{name}-client-genuine.so.%{version} lib%{name}-client.so.%{version}
ln -sf lib%{name}-server-genuine.so.%{version} lib%{name}-server.so.%{version}
chsmack -a "_" lib%{name}-client.so.%{version}
chsmack -a "_" lib%{name}-server.so.%{version}
popd
/sbin/ldconfig

%preun
echo "You need to reinstall %{name}-dummy to keep using the APIs after uninstalling this."

%files
%manifest packaging/%{name}.manifest
%{_libdir}/lib%{name}-client-genuine.so.*
%{_libdir}/lib%{name}-server-genuine.so.*
%license LICENSE


%post dummy
/sbin/ldconfig

%files dummy
%manifest packaging/%{name}.manifest
%{_libdir}/lib%{name}-client.so.*
%{_libdir}/lib%{name}-server.so.*
%license LICENSE


%files devel
%{_includedir}/context-service/*.h
%{_includedir}/context-service/*/*.h
%{_libdir}/lib%{name}-client.so
%{_libdir}/lib%{name}-server.so
%{_libdir}/pkgconfig/*.pc
