Name:        dfs-adaptation
Summary:     Adaptation of depth-from-stereo
Version:     1.0.10
Release:     1
Group:       Multimedia/Framework
License:     Apache-2.0
Source0:     %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(iniparser)

%description
Adaptaion of depth-from-stereo

%package devel
Summary:    Adaptaion of depth-from-stereo
Group:      Multimedia/Framework
Requires:   %{name} = %{version}-%{release}

%description devel
Adaptaion of depth-from-stereo (Dev)

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

%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%{_libdir}/libdfs-*.so.*

%files devel
%{_includedir}/media/*.h
%{_libdir}/pkgconfig/dfs*.pc
%{_libdir}/libdfs-*.so
