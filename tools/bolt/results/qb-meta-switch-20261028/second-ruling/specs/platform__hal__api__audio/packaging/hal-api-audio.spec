Name:       hal-api-audio
Summary:    TIZEN Audio HAL
Version:    2.0.5
Release:    0
Group:      System/Libraries
License:    Apache-2.0
URL:        http://tizen.org
Source0:    hal-api-audio-%{version}.tar.gz
Source1:    %{name}-manifest.xml
BuildRequires: cmake
BuildRequires: pkgconfig(hal-api-common)
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(gmock)

%description
TIZEN Audio HAL

%package    devel
Summary:    %{name} interface
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
%{name} interface development package for product vendor developer

%package    haltests
Summary:    gtest for audio HAL APIs
Group:      Development/Tools
Version:    %{version}

%description    haltests
haltests for audio HAL APIs.

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DCMAKE_LIBDIR_PREFIX=%{_libdir}

make %{?jobs:-j%jobs}

%install
install -d -m 755 %{buildroot}%{_datadir}/testcase/res/audio/
install -m 644 testcase/*.raw %{buildroot}%{_datadir}/testcase/res/audio/
mkdir -p %{buildroot}%{_sysconfdir}/hal
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/hal/

%make_install

%post
/sbin/ldconfig
%{_bindir}/hal-compatibility-checker --reset

%postun
/sbin/ldconfig
%{_bindir}/hal-compatibility-checker --reset

%files
%defattr(-,root,root,-)
%manifest hal-api-audio.manifest
%defattr(-,root,root,-)
%{_libdir}/hal/*.so*
%license LICENSE.APLv2
%{_sysconfdir}/hal/%{name}-manifest.xml

%files devel
%defattr(-,root,root,-)
%{_includedir}/hal/*.h
%{_libdir}/pkgconfig/*.pc

%files haltests
%defattr(-,root,root,-)
%manifest %{name}-haltests.manifest
%{_bindir}/hal/audio-haltests
%{_datadir}/testcase/res/audio/*

