Name:           openal-soft
Version:        1.17.2
Release:        19
License:        LGPL-2.0+
Summary:        A cross-platform 3D audio API
URL:            http://connect.creativelabs.com/openal/
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source1001: 	openal-soft.manifest
BuildRequires:  cmake
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(capi-media-sound-manager)
BuildRequires: pkgconfig(alsa)

%description
OpenAL is a cross-platform 3D audio API appropriate for use with gaming
applications and many other types of audio applications.

%package devel
Summary:        openal-soft development package
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
Development package for OpenAL, a cross-platform 3D audio API
appropriate for use with gaming applications and many other types of
audio applications.

%prep
%setup -q
cp %{SOURCE1001} .

%build

export CFLAGS="$CFLAGS -D__TIZEN__ -DUSE_DLOG "
export TIZEN_BUILD=1

%cmake . -DALSOFT_REQUIRE_PULSEAUDIO=OFF -DALSOFT_BACKEND_PULSEAUDIO=OFF -DALSOFT_REQUIRE_ALSA=ON
make %{?_smp_mflags}

%install
%make_install


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/openal-info
%{_bindir}/altonegen
%{_libdir}/libopenal.so.*
/etc/openal/alsoft.conf
%exclude /usr/lib/debug/.build-id/*
%exclude %{_datadir}/openal/hrtf/*

%files devel
%manifest %{name}.manifest
%{_includedir}/AL/*.h
%{_libdir}/libopenal.so
%{_libdir}/pkgconfig/openal.pc
