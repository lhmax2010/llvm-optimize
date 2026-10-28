Name:        inference-engine-interface
Summary:     Interface of inference engines
Version:     0.5.2
Release:     0
Group:       Multimedia/Framework
License:     Apache-2.0
Source0:     %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(python)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: gtest-devel

%description
Interface of inference engines

%package devel
Summary:    Interface of inference engines
Group:      Multimedia/Framework
Requires:   %{name} = %{version}-%{release}

%description devel
Interface of inference engines (Dev)


%package common
Summary:    Common interface of inference engines
Group:      Multimedia/Framework

%description common
Common interface of inference engines

%package common-devel
Summary:    Common interface of inference engines
Group:      Multimedia/Framework
Requires:   inference-engine-interface-common

%description common-devel
Common interface of inference engines (Dev)

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

mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/opt/usr/images/
%make_install

install -m 755 test/bin/inference_engine_profiler %{buildroot}%{_bindir}
install -m 755 test/bin/inference_engine_tc %{buildroot}%{_bindir}
install -m 755 start_profiler.sh %{buildroot}%{_bindir}
install -m 666 test/res/*.bin %{buildroot}/opt/usr/images
install -m 755 tools/bin/inference_engine_cltuner %{buildroot}%{_bindir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files common
%manifest inference-engine-interface-common.manifest
%license LICENSE.APLv2
%{_libdir}/libinference-engine-interface-common.so.*

%files common-devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/*common.pc
%{_libdir}/lib*-common.so
%{_bindir}/inference_engine_profiler
%{_bindir}/inference_engine_tc
%{_bindir}/start_profiler.sh
%{_bindir}/inference_engine_cltuner
/opt/usr/images/*.bin
