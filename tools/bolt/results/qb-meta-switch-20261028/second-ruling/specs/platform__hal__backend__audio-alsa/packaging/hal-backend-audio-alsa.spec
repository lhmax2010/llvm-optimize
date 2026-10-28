Name:       hal-backend-audio-alsa
Summary:    TIZEN Audio HAL using ALSA
Version:    0.0.7
Release:    0
Group:      System/Libraries
License:    Apache-2.0
URL:        http://tizen.org
Source0:    %{name}-%{version}.tar.gz
BuildRequires: pkgconfig(hal-rootstrap)
#BuildRequires: pkgconfig(tinyalsa)
Provides: libhal-backend-audio.so

%description
TIZEN Audio HAL using ALSA

%prep
%setup -q -n %{name}-%{version}

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE -DSYSCONFDIR=\\\"%{_hal_sysconfdir}\\\""
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

export USE_TINYALSA="0"

%autogen
./configure --libdir=%{_hal_libdir}

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
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_hal_libdir}/libhal-backend-audio.so
%{_hal_licensedir}/%{name}/*
