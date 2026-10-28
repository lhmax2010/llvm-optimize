Name:           pen-wave
Summary:        PenWave Rendering Engine
%define ver_str 1.4.0
Version:        %{ver_str}
Release:        2
Group:          DALI/NUI
License:        Apache-2.0
Source0:        %{name}.tar.gz
Source1001:     %{name}.manifest

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires:  pkgconfig
BuildRequires:  cmake

%description
Description: PenWave Engine

%{!?TZ_SYS_RO_SHARE: %global TZ_SYS_RO_SHARE /usr/share}
%global _libshare /usr/share/libpen-wave/

%package devel
Summary:  PenWave Engine(Development)
Requires: %{name} = %{version}-%{release}

%description devel
%devel_desc

####
#  Preparation
####
%prep
%setup -q -n %{name}
cp %{SOURCE1001} .

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} \
      -DINSTALL_PREFIX=%{_libdir} \
      -DINSTALL_RES_PREFIX=%{_libshare} \
      -DINSTALL_INC_PREFIX=%{_includedir} \
      -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE

####
#  Build
####
%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
make %{?jobs:-j%jobs}

####
#  Installation
####
%install
rm -rf %{buildroot}

%make_install

####
#  Post Install
####
%post
/sbin/ldconfig
exit 0

####
#  Post Uninstall
####
%postun
/sbin/ldconfig
exit 0

####
#  Files in Binary Packages
####
%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/*
%{_libshare}/target/*.conf
%{_libshare}/images/textures/*.png
%{_libshare}/fonts/*.ttf

%files devel
%manifest %{name}.manifest
%{_includedir}/renderer_ext_api.h
%{_includedir}/renderer_ext_types.h
%{_libdir}/*
