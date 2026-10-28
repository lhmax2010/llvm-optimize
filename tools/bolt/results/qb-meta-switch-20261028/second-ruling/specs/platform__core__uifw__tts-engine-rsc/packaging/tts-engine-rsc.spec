Name:       tts-engine-rsc
Summary:    Text To Speech default engine resource
Version:    0.0.2
Release:    1
Group:      Graphics & UI Framework/Voice Framework
License:    Flora-1.1
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires: cmake
BuildRequires: pkgconfig(libtzplatform-config)

%description
Description: Text To Speech default engine resource

####
#  Preparation
####
%prep
%setup -q
cp %{SOURCE1001} .

%define APP_PREFIX	%{TZ_SYS_RO_APP}/%{name}
export LD_LIBRARY_PATH=%{APP_PREFIX}/lib


cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} \
      -DCMAKE_INSTALL_PREFIX=/usr \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=1 \
      -DTZ_SYS_RO_SHARE=%TZ_SYS_RO_SHARE \
      -DAPP_INSTALL_PREFIX=%{APP_PREFIX}

####
#  Build
####
%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
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
%defattr(-,root,root,-)
%manifest %{name}.manifest
%{TZ_SYS_RO_SHARE}/voice/tts/smt_vdata/
