Name:          ne10
Summary:       A library of common math and DSP functions optimized for ARM NEON
Version:       1.2.1
Release:       0
Group:         System/ Uncategorized
Packager:      Geunsik Lim <geunsik.lim@samsung.com>
License:       BSD-3-Clause
URL:           https://projectne10.github.com/Ne10/
Source0:       %{name}-%{version}.tar.gz
Source1001:    %{name}.manifest

# build-time dependencies
BuildRequires:	gcc gcc-c++ cmake

# Support only ARM architectures
ExclusiveArch: %{arm} aarch64

%description
Ne10 is a library of common, useful functions that have been heavily optimised
for ARM-based CPUs equipped with NEON SIMD capabilities. It provides consistent,
well-tested behaviour, allowing for painless integration into a wide variety of
applications. The library currently focuses primarily around math, signal
processing, image processing, and physics functions.

The library provides some of the fastest implementations of key
operations available for the ARM v7-A and v8-A architectures,
particularly focusing on math, signal processing, image processing,
and physics functions.

%package devel
Summary:       Development files for Ne10, a math/DSP library for ARM NEON
Requires:      %{name} = %{version}
Requires:      %{name} = %{version}

%description devel
The library provides some of the fastest implementations of key
operations available for the ARM v7-A and v8-A architectures,
particularly focusing on math, signal processing, image processing,
and physics functions.

This package contains the development files.


%prep
%setup -q
cp %{SOURCE1001} .

%build
# https://wiki.tizen.org/ASan#.E2.80.9Cmultiple_definition_of.E2.80.9D_linking_error_due_to_-fno-common
%{?asan:%restore_fcommon}

export LANG=C

export CFLAGS="${CFLAGS} -Wno-implicit-function-declaration"
%{?_toolchain:
%if %{toolchain_is clang}
export CFLAGS="${CFLAGS} -fno-integrated-as"
%endif
}

mkdir build && cd build

# Generate a configuration file
%cmake \
    %ifarch %{arm}
    -DNE10_LINUX_TARGET_ARCH=armv7 \
    %else
    -DNE10_LINUX_TARGET_ARCH=aarch64 \
    %endif
    -DNE10_BUILD_STATIC=ON \
    -DNE10_BUILD_SHARED=ON \
    -DNE10_BUILD_UNIT_TEST=OFF \
    -DGNULINUX_PLATFORM=ON ..

# Compile the source files
make %{?_smp_mflags}


%install
for i in inc/*.h; do
    install -p -D -m 0644 $i %{buildroot}/%{_includedir}/$(basename $i)
done

mkdir -p %{buildroot}%{_libdir}
install -m 0644 ./build/modules/libNE10.a %{buildroot}%{_libdir}
install -m 0644 ./build/modules/libNE10.so %{buildroot}%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%attr(0644,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.a

%files devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%attr(0644,root,root) %{_includedir}/*.h
%attr(0644,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/*.a


%changelog
* Fri Aug 14 2020 Geunsik Lim <geunsik.lim@samsung.com>
- Supported both .so and .a files
- Added .spec file to generate a Ne10 RPM package
