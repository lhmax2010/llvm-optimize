Name:        vision-source
Summary:     vision source
Version:     1.0.0
Release:     0
Group:       Multimedia/Framework
License:     Apache-2.0
Source0:     %{name}-%{version}.tar.gz
BuildRequires: cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(iniparser)
BuildRequires: pkgconfig(capi-media-tool)

%description
Vision source

%package devel
Summary:    Interface of vision source
Group:      Multimedia/Framework
Requires:   %{name} = %{version}-%{release}

%description devel
Interface of vision source (Dev)

%prep
%setup -q

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

%cmake -DHAL_SYSCONFDIR=%{_hal_sysconfdir}/multimedia .
make %{?jobs:-j%jobs}

%install

%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/*.so
%license LICENSE.APLv2
%config %{_sysconfdir}/vision_source.ini

%files devel
%{_includedir}/media/*.h
%license LICENSE.APLv2
%{_libdir}/pkgconfig/*.pc
