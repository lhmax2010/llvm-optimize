%if "%{?tizen_profile_name}" == "tv"
%define WITH_VD 1
%else
%define WITH_VD 0
%endif

# update manager
%define dbus_conf_directory %{_sysconfdir}/dbus-1/system.d
%define dbus_conf_file update-manager.conf
%define service_file update-manager.service

Name:           update-control
Version:        1.0.6
Release:        0
License:        Apache-2.0
Summary:        Update Control API
Group:          System/API
Source0:        %{name}-%{version}.tar.gz
Source1:    	%{dbus_conf_file}
Source2:    	%{service_file}

Source1001:     %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-system-device)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(hal-api-device)
BuildRequires:  pkgconfig(pkgmgr-info)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-update-control)
BuildRequires:  libtar-devel
BuildRequires:  python3-setuptools
%if "%{?WITH_VD}" == "0"
BuildRequires:  glibc-devel-static
BuildRequires:  glib2-devel-static
BuildRequires:  capi-system-info-devel-static
BuildRequires:  capi-base-common-devel-static
BuildRequires:  libdlog-devel-static
%endif

%description
An Update Control library in Tizen C API

%package devel
Summary:  A Update Control library in Core API (Development)
Group:    Development/System
Requires: %{name} = %{version}-%{release}

%description devel

%package daemon
Summary:  Tizen Update Manager Daemon
Group:    Development/System
Requires: %{name} = %{version}-%{release}

%description daemon

%package plugin
Summary:  A Update Control plugin library
Group:    Development/System
Requires: %{name} = %{version}-%{release}

%description plugin

%prep
%setup -q
cp %{SOURCE1001} .

%build
%if 0%{?asan} || 0%{?ubsan} || 0%{?hwasan}
export BUILD_WITH_ASAN=1
%else
export BUILD_WITH_ASAN=0
%endif
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export CXXFLAGS+=" -fprofile-arcs -ftest-coverage"
export FFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if 0%{?asan:1}
export CFLAGS+=" -Wno-stringop-truncation"
%endif

%cmake . -DMAJORVER=${MAJORVER} \
	 -DFULLVER=%{version} \
	 -DDEBUG_MODE=on \
	 -DBINARY_PATH=%{_bindir} \
	 -DGCOV=%{?gcov:1}%{!?gcov:0} \
%if "%{?WITH_VD}" == "1"
	 -DSTATIC_LINKING=0
%else
	 -DSTATIC_LINKING=1
%endif

%__make %{?jobs:-j%jobs}

%install
%make_install

# update manager
mkdir -p %{buildroot}/%{dbus_conf_directory}
install -m 0644 %{SOURCE1} %{buildroot}/%{dbus_conf_directory}/%{dbus_conf_file}

mkdir -p %{buildroot}/%{_unitdir}
install -m 0644 %{SOURCE2} %{buildroot}/%{_unitdir}/%{service_file}
mkdir -p %{buildroot}/%{_unitdir}/multi-user.target.wants
ln -s ../%{service_file} %{buildroot}/%{_unitdir}/multi-user.target.wants/%{service_file}

%post
/sbin/ldconfig
chsmack -a 'System::Tools' %{_bindir}/osu

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/libupdate-control.so.*
%{_bindir}/osu

%files daemon
%{_bindir}/update-manager
%{_bindir}/delta-verifier
%{dbus_conf_directory}/%{dbus_conf_file}
%{_unitdir}/%{service_file}
%{_unitdir}/multi-user.target.wants/%{service_file}

%files devel
%manifest %{name}.manifest
%{_includedir}/system/update_control.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libupdate-control.so
