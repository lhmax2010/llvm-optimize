Name:       mmsvc-recorder
Summary:    A Recorder module for muse server
Version:    1.0.1
Release:    0
Group:      Multimedia/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(mm-camcorder)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(mmsvc-camera)
BuildRequires:  pkgconfig(legacy-camera)
BuildRequires:  pkgconfig(mm-common)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(muse-server)
%if "%{gtests}" == "1"
BuildRequires:  pkgconfig(gmock)
%endif

%description
A Recorder module for muse servier and native recorder API.


%package devel
Summary:  A Recorder module for muse server (Development)
Requires: %{name} = %{version}-%{release}

%description devel
Development related files of a recorder module for muse server.


%prep
%setup -q


%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . \
%if "%{gtests}" == "1"
	-DENABLE_GTESTS=On\
%else
	-DENABLE_GTESTS=Off\
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix}\
	-DFULLVER=%{version}\
	-DMAJORVER=${MAJORVER}\
	-DLIBDIR=%{_libdir}
make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
%make_install


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%manifest mmsvc-recorder.manifest
%license LICENSE.APLv2
%{_libdir}/liblegacy-recorder.so
%{_libdir}/libmuse-recorder.so
%if "%{gtests}" == "1"
%{_bindir}/gtests-*
%endif

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*.pc
