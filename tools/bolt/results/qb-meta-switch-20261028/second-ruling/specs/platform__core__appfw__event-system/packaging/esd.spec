Name:       esd
Summary:    Event system daemon
Version:    1.1.7
Release:    1
Group:      Application Framework/Service
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    esd.service
Source1001: %{name}.manifest
Source1002: %{name}.loader
BuildRequires: cmake
BuildRequires: pkgconfig(capi-system-resource)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(rpc-port)
BuildRequires: pkgconfig(bundle)
BuildRequires: pkgconfig(tizen-core)
BuildRequires: pkgconfig(united-service)

%if 0%{?gcov:1}
BuildRequires:  lcov
%endif

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Recommends: esd-mod-group
Recommends: esd-mod-cion

%description
Event System Daemon

%package devel
Summary:    Event system daemon (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Event system Daemon (devel)

#################################################
# unittests
#################################################
%package -n %{name}-unittests
Summary:    GTest for API
Group:      Application Framework/Testing
Requires:   %{name}

%description -n %{name}-unittests
GTest for API

%define _modname esd
%define _moddir %{_datadir}/united-service/%{_modname}

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake \
  -DMOD_DIR=%{_moddir} \
  -DFULLVER=%{version} \
  -DMAJORVER=${MAJORVER} \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  %if 0%{?asan} != 1
    -DASAN_ENABLED=FALSE
  %else
    -DASAN_ENABLED=TRUE
  %endif

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_unitdir}/basic.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/esd.service
ln -sf ../esd.service %{buildroot}%{_unitdir}/basic.target.wants/esd.service

mkdir -p %{buildroot}%{_moddir}
install -m 0644 %SOURCE1002 %{buildroot}%{_moddir}/esd.loader

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_bindir}/esd
%{_libdir}/libesd.so.*
%{_unitdir}/esd.service
%{_unitdir}/basic.target.wants/esd.service
%{_moddir}/mod/libevent-system-daemon.so
%{_moddir}/conf/event-system-daemon.service
%{_moddir}/esd.loader
%license LICENSE

%files devel
%{_includedir}/esd/*.hh
%{_libdir}/libesd.so
%{_libdir}/pkgconfig/*pc
