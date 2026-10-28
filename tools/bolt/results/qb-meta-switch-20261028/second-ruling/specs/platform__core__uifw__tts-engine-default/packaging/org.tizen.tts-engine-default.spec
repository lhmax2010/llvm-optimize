%define _optdir	/opt
%define _appdir	%{_optdir}/apps

Name:       org.tizen.tts-engine-default
Summary:    Text To Speech default engine library
Version:    1.100.1
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: cmake
BuildRequires: pkgconfig(libtzplatform-config)

# Exclude boost requires/provides
#%global _privatelibs libboost_iostreams.so.1.58.0|libboost_system.so.1.58.0|libboost_thread.so.1.58.0
#%global __provides_exclude %{_privatelibs}
#%global __requires_exclude %{_privatelibs}

%description
Description: Text To Speech default engine library

####
#  Preparation
####
%prep
%setup -q
cp %{SOURCE1001} .

cat LICENSE LICENSE.Apache > LICENSE.merge
cp LICENSE.merge LICENSE
rm LICENSE.merge

%define APP_PREFIX	%{TZ_SYS_RO_APP}/%{name}
export LD_LIBRARY_PATH=%{APP_PREFIX}/lib

%define MANIFESTDIR	%{TZ_SYS_RO_PACKAGES}

cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=1 \
      -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE \
	  -DAPP_INSTALL_PREFIX=%{APP_PREFIX} \
	  -DAPP_MANIFESTDIR=%{MANIFESTDIR}

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
%license LICENSE
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{APP_PREFIX}/bin/*
%{APP_PREFIX}/lib/*
#%{APP_PREFIX}/data/smt_vdata/*
%{MANIFESTDIR}/org.tizen.tts-engine-default.xml

