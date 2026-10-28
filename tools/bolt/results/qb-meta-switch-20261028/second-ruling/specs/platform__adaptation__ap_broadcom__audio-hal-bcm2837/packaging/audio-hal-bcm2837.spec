Name:       audio-hal-bcm2837
Summary:    TIZEN Audio HAL for BCM2837
Version:    0.10.1
Release:    0
Group:      System/Libraries
License:    Apache-2.0
URL:        http://tizen.org
Source0:    audio-hal-bcm2837-%{version}.tar.gz
BuildRequires: pkgconfig(hal-rootstrap)
BuildRequires: cmake
Provides: libhal-backend-audio.so

# Define to use tinyalsa (0: use alsa-lib, 1: use tinyalsa)
%define use_tinyalsa 1

# Define to build test programs (0: disable, 1: enable)
%define build_test 1

%description
TIZEN Audio HAL for BCM2837

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\" -fPIC"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE -fPIC"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

%cmake -DCMAKE_INSTALL_PREFIX=/hal -DCMAKE_INSTALL_LIBDIR=%{_hal_libdir} -DUSE_TINYALSA=%{use_tinyalsa} -DBUILD_TEST=%{build_test}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install
mkdir -p %{buildroot}%{_hal_licensedir}/%{name}
cp LICENSE.Apache-2.0 %{buildroot}%{_hal_licensedir}/%{name}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%manifest audio-hal-bcm2837.manifest
%defattr(-,root,root,-)
%{_hal_libdir}/libhal-backend-audio.so
%{_hal_licensedir}/%{name}/*

%if %{build_test}
%package test
Summary:    Test programs for audio-hal-bcm2837
Group:      System/Libraries

%description test
Test programs for audio-hal-bcm2837

%files test
%defattr(-,root,root,-)
%{_hal_bindir}/*
%endif
