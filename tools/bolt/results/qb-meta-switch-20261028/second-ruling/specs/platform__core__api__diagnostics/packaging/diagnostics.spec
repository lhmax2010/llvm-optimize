Name:       diagnostics
Version:    1.2.0
Release:    1
License:    Apache-2.0
Summary:    Tizen Diagnostics API
Group:      Diagnostics
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  cmocka
BuildRequires:  cmocka-devel
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(dumpsys)
BuildRequires:  pkgconfig(dumpsys-system)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(aul)
BuildRequires:  glib2-devel
%if 0%{?gcov:1}
BuildRequires:  lcov
BuildRequires:  zip
%else
%define gcov 0
%endif

Requires: dumpsys
Requires(post):  /sbin/ldconfig
Requires(postun):  /sbin/ldconfig

%description
Tizen Diagnostics API

%package devel
Summary:  Tizen Diagnostics API (Development)
Group:    Development/System
Requires: %{name} = %{version}-%{release}

%description devel
Tizen Diagnostics API (Development)

%package -n     libbugreport
Summary:        libbugreport provides API to communicate with bugreport-service
%description -n libbugreport

%package -n     libbugreport-devel
Summary:        package provides headers needed to develop programs using bugreport-service
%description -n libbugreport-devel

%prep
%setup -q

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DMAJORVER=${MAJORVER} -DFULLVER=%{version} -DENABLE_COVERAGE=%{gcov}
make %{?jobs:-j%jobs}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest packaging/%{name}.manifest
%{_libdir}/libdiagnostics.so.*
%license LICENSE.APLv2

%files devel
%{_includedir}/diagnostics.h
%{_libdir}/libdiagnostics.so
%{_libdir}/pkgconfig/diagnostics.pc

%files -n libbugreport
%license LICENSE.APLv2
%manifest packaging/%{name}.manifest
%{_libdir}/libbugreport.so.*

%files -n libbugreport-devel
%license LICENSE.APLv2
%manifest packaging/%{name}.manifest
%{_includedir}/libbugreport.h
%{_libdir}/libbugreport.so
%{_libdir}/pkgconfig/bugreport.pc