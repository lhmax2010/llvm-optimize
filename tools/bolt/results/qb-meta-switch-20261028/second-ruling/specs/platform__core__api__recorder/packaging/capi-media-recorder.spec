Name:       capi-media-recorder
Summary:    A Recorder API
Version:    1.0.5
Release:    0
Group:      Multimedia/API
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-media-camera)
BuildRequires:  pkgconfig(mm-camcorder)
BuildRequires:  pkgconfig(mmsvc-camera)
BuildRequires:  pkgconfig(mmsvc-recorder)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(muse-client)
BuildRequires:  pkgconfig(capi-media-tool)
BuildRequires:  pkgconfig(capi-media-audio-io)
BuildRequires:  pkgconfig(capi-media-sound-manager)
BuildRequires:  pkgconfig(storage)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(tizen-core-wl)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
A Recorder library in Tizen Native API


%package devel
Summary:  A Recorder API (Development)
Requires: %{name} = %{version}-%{release}


%description devel
Development related files for a Recorder library in Tizen Native API.


%package test-headed
Summary:  A recorder API testsuite for headed target
Requires: %{name} = %{version}-%{release}

%description test-headed
Tizen Native recorder API testsuite for headed target.


%package test-headless
Summary:  A recorder API testsuite for headless target
Requires: %{name} = %{version}-%{release}

%description test-headless
Tizen Native recorder API testsuite for headless target.


%if 0%{?gcov:1}
%package gcov
Summary: Line Coverage of Recorder library in Tizen Native API
Group: Development/Multimedia

%description gcov
Collection of files related to Line Coverage. It is teseted as gcov for a recorder library in Tizen native API
%endif


%prep
%setup -q


%build
%if 0%{?gcov:1}
export CFLAGS+=" -fprofile-arcs -ftest-coverage"
export LDFLAGS+=" -lgcov"
%endif
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
SO_FULLVER=0.4.0
SO_MAJORVER=`echo ${SO_FULLVER} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DSO_FULLVER=${SO_FULLVER} -DSO_MAJORVER=${SO_MAJORVER}
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

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libcapi-media-recorder.so.*


%files devel
%{_includedir}/media/recorder.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libcapi-media-recorder.so


%files test-headed
%manifest %{name}-test-headed.manifest
%license LICENSE.APLv2
%{_bindir}/recorder_test_headed


%files test-headless
%manifest %{name}-test-headless.manifest
%license LICENSE.APLv2
%{_bindir}/recorder_test_headless


%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

