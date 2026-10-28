Name:       hailo-rt
Summary:    Hailo runtime
Version:    0.1
Release:    0
Group:      Multimedia/Libraries
License:    MIT, LGPL 2.1
ExclusiveArch: %{arm} aarch64
Source0:    %{name}-%{version}.tar.gz
Source100: protobuf-src.tar.gz
Source101: spdlog-src.tar.gz
Source102: eigen-src.tar.gz
Source103: cli11-src.tar.gz
Source104: json-src.tar.gz
Source105: dotwriter-src.tar.gz
Source106: readerwriterqueue-src.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
%define _unpackaged_files_terminate_build 0

%description
HailoRT is a lightweight, production-grade runtime library that runs on the host processor and provides a robust user-space library (the HailoRT Library) with intuitive APIs in C/C++ for optimized performance

%package devel
Summary:    Header and library files for HailoRT
Group:      Multimedia/Framework
Requires:   %{name}

%description devel
HailoRT (Dev)

%prep
%setup -q
%setup -q -T -D -a 100
%setup -q -T -D -a 101
%setup -q -T -D -a 102
%setup -q -T -D -a 103
%setup -q -T -D -a 104
%setup -q -T -D -a 105
%setup -q -T -D -a 106

mkdir -p hailort/external
mv protobuf-src hailort/external/
mv spdlog-src hailort/external/
mv eigen-src hailort/external/
mv cli11-src hailort/external/
mv json-src hailort/external/
mv dotwriter-src hailort/external/
mv readerwriterqueue-src hailort/external/

%build
%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif

cmake -H. -Bbuild -DCMAKE_BUILD_TYPE=Release -DHAILO_BUILD_EXAMPLES=1 -DHAILO_OFFLINE_COMPILATION=ON

cd build
make %{?jobs:-j%jobs}

%install

cd build
%make_install

%define LIB_DIR %(uname -m | grep -q '^arm' && echo lib || echo lib64)

mkdir -p %{buildroot}%{_includedir}/hailort
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_bindir}

strip %{buildroot}/usr/local/%{LIB_DIR}/libhailort.so.4.18.0
strip %{buildroot}/usr/local/bin/hailortcli

cp -a %{buildroot}/usr/local/include/* %{buildroot}%{_includedir}/
cp -a %{buildroot}/pkgconfig/HailoRT.pc %{buildroot}%{_libdir}/pkgconfig/
cp -a %{buildroot}/usr/local/%{LIB_DIR}/* %{buildroot}%{_libdir}/
cp -a %{buildroot}/usr/local/bin/* %{buildroot}%{_bindir}/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.MIT
%defattr(-,root,root,-)
%{_libdir}/libhailort.so.4.18.0
%{_libdir}/libhailort.so
%{_bindir}/*

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/hailo/*
