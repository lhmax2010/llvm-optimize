Name:       lbs-server-plugin-replay
Summary:    LBS Server plugin library for replay mode
Version:    0.2.10
Release:    1
Group:      Location/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    lbs-server-plugin-replay.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(hal-rootstrap)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
LBS Server plugin library for replay mode

%define DATADIR /etc/lbs-server

%prep
%setup -q
cp %{SOURCE1} .

%build
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DFULLVER=%{version} -DMAJORVER=${MAJORVER} \
        -DLIB_DIR=%{_libdir} \
        -DHAL_LIB_DIR=%{_hal_libdir} \
        -DHAL_LICENSE_DIR=%{_hal_licensedir} \

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

mkdir -p  %{buildroot}/hal/etc/location
cp -a nmea-log/*.log %{buildroot}/hal/etc/location

%post
rm -rf %{_libdir}/liblbs-server-plugin.so
ln -sf %{_hal_libdir}/libhal-backend-location.so %{_libdir}/liblbs-server-plugin.so
#for compatible with old version
#ln -sf %{_hal_libdir}/libhal-backend-location.so %{_libdir}/libSLP-lbs-plugin-replay.so
#ln -sf %{_hal_libdir}/libhal-backend-location.so %{_libdir}/libSLP-lbs-plugin.so
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest lbs-server-plugin-replay.manifest
%{_hal_licensedir}/%{name}/LICENSE
%defattr(-,root,root,-)
%{_hal_libdir}/*.so*
/hal/etc/location/*
