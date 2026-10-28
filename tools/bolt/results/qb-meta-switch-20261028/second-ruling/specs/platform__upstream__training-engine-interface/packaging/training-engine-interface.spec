Name:        training-engine-interface
Summary:     Common interface for training engines
Version:     0.3.2
Release:     0
Group:       Multimedia/Framework
License:     Apache-2.0
Source0:     %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: gtest-devel
BuildRequires: pkgconfig(inference-engine-interface-common)

%description
Common interface for training engines

%package common
Summary:    Provide common interface library files for training engine excution
Group:      Multimedia/Framework

%description common
Common interface library files for training engine excution

%package common-devel
Summary:    Provide header and library files for backend development of training engine
Group:      Multimedia/Framework
Requires:   training-engine-interface-common

%description common-devel
Header and library files for backend development of training engine

%package tools
Summary:	Provide test binaries for testing training engine backends
Group:		Multimedia/Framework
Requires:	training-engine-interface-common

%description tools
Summary: Test binaries for testing training engine backends

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

export CFLAGS+=" -DPATH_LIBDIR=\\\"%{_libdir}\\\" -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS+=" -DPATH_LIBDIR=\\\"%{_libdir}\\\" -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake . -DFULLVER=%{version} -DMAJORVER=${MAJORVER} -DTZ_SYS_BIN=%TZ_SYS_BIN \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/usr/share/capi-media-vision/bin
%make_install

install -m 755 test/bin/training_engine_tc %{buildroot}%{_bindir}
install -m 755 test/bin/training_engine_simpleshot %{buildroot}%{_bindir}
install -m 444 test/res/*.dat %{buildroot}/usr/share/capi-media-vision/bin

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files common
%manifest training-engine-interface-common.manifest
%license LICENSE.APLv2
%{_libdir}/libtraining-engine-interface-common.so.*

%files common-devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*common.pc
%{_libdir}/lib*-common.so

%files tools
%{_bindir}/training_engine_tc
%{_bindir}/training_engine_simpleshot
/usr/share/capi-media-vision/bin/*.dat
