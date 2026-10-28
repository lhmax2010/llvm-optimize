Name:           openblas
Version:        0.3.21
Release:        1
Summary:        An optimized BLAS library based on GotoBLAS2
License:        BSD-3-Clause and MIT and Apache-2.0
Group:          Productivity/Scientific/Math
Url:            http://www.openblas.net
Source0:        %{name}-%{version}.tar.gz
Source1001:	%{name}.manifest
BuildRequires:  gcc-fortran
BuildRequires:  update-alternatives
BuildRequires:  sed
Requires(post): update-alternatives
Requires(preun): update-alternatives

%description
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

%package     -n lib%{name}_serial0
Summary:        An optimized BLAS library based on GotoBLAS2, serial version
Group:          System/Libraries
Requires(post): update-alternatives
Requires(preun): update-alternatives
Obsoletes:      lib%{name}0 < %{version}
Provides:       lib%{name}0 = %{version}

%description -n lib%{name}_serial0
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

%package     -n lib%{name}_serial-devel
Summary:        Development libraries for OpenBLAS, serial version
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel-headers = %{version}
Requires:       lib%{name}_serial0 = %{version}

%description -n lib%{name}_serial-devel
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

This package contains the development libraries for serial OpenBLAS version.

%package     -n lib%{name}_openmp0
Summary:        An optimized BLAS library based on GotoBLAS2, OpenMP version
Group:          System/Libraries
Requires(post): update-alternatives
Requires(preun): update-alternatives
Obsoletes:      lib%{name}0
Obsoletes:      lib%{name}o0

%description -n lib%{name}_openmp0
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

This package contains the library compiled with OpenMP support.

%package     -n lib%{name}_openmp-devel
Summary:        Development libraries for OpenBLAS, OpenMP version
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel-headers = %{version}
Requires:       lib%{name}_openmp0 = %{version}

%description -n lib%{name}_openmp-devel
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

This package contains the development libraries for OpenMP OpenBLAS version.

%package     -n lib%{name}_pthreads0
Summary:        An optimized BLAS library based on GotoBLAS2, pthreads version
Group:          System/Libraries
Requires(post): update-alternatives
Requires(preun): update-alternatives
Obsoletes:      lib%{name}0
Obsoletes:      lib%{name}p0

%description -n lib%{name}_pthreads0
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

This package contains the library compiled with threading support.

%package     -n lib%{name}_pthreads-devel
Summary:        Development headers and libraries for OpenBLAS, pthreads version
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel-headers = %{version}
Requires:       lib%{name}_pthreads0 = %{version}

%description -n lib%{name}_pthreads-devel
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

This package contains the development libraries for pthreads OpenBLAS version.

%package        devel
Summary:        Development headers and libraries for OpenBLAS
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel-headers = %{version}
%ifarch %ix86 x86_64
Requires:       lib%{name}_pthreads-devel = %{version}
%else
Requires:       lib%{name}_openmp-devel = %{version}
%endif

%description    devel
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

This package contains the development libraries and headers for OpenBLAS.

%package        devel-headers
Summary:        Development headers for OpenBLAS
Group:          Development/Libraries/C and C++
Conflicts:      %{name}-devel < %{version}

%description    devel-headers
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

This package contains headers for OpenBLAS.

%package        devel-static
Summary:        Static version of OpenBLAS
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel = %{version}

%description    devel-static
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

This package contains the static libraries.

%prep
%define _toolchain_override gcc
%setup -q
cp %{SOURCE1001} .

# Disable utest. It causes blocking QB buiding.
sed -i "s|ctest utest|ctest|" Makefile
sed -i "s|tests shared|shared|" Makefile

cd ..
# Prepare build for serial, pthreads and OpenMP versions
cp -ar %{name}-%{version} openmp
cp -ar %{name}-%{version} pthreads
cp -ar %{name}-%{version} serial
#mv %{name}-%{version} serial

# cp %{SOURCE1} .

%build
%if 0%{?asan}
export EXTRALIB+="-lasan"
%endif

export LDFLAGS+=" -Wl,-z,noexecstack"

# Only x86/x86-64 CPUs support DYNAMIC_ARCH
%ifarch %ix86 x86_64
%define openblas_target DYNAMIC_ARCH=1 TARGET=NEHALEM
%endif
%ifarch armv7l
%define openblas_target TARGET=ARMV7 ARM_SOFTFP_ABI=1
%endif
%ifarch armv7hl
%define openblas_target TARGET=ARMV7
%endif
%ifarch aarch64
%define openblas_target TARGET=ARMV8
%endif
%ifarch riscv64
%define openblas_target TARGET=RISCV64_GENERIC
%endif

cd ..
# Make serial, threaded and OpenMP versions
make -C serial %{?_smp_mflags} %{?openblas_target} USE_THREAD=0 USE_OPENMP=0 LIBNAMESUFFIX=serial \
        FC=gfortran COMMON_OPT="%{optflags}" NUM_THREADS=64 V=1
make -C openmp %{?_smp_mflags} %{?openblas_target} USE_THREAD=1 USE_OPENMP=1 LIBNAMESUFFIX=openmp \
        FC=gfortran COMMON_OPT="%{optflags}" NUM_THREADS=64 V=1
make -C pthreads %{?_smp_mflags} %{?openblas_target} USE_THREAD=1 USE_OPENMP=0 LIBNAMESUFFIX=pthreads \
        FC=gfortran COMMON_OPT="%{optflags}" NUM_THREADS=64 V=1

%install
cd ..
# Install serial library and headers
make -C serial USE_THREAD=0 LIBNAMESUFFIX=serial \
        OPENBLAS_LIBRARY_DIR=%{buildroot}%{_libdir} \
        OPENBLAS_INCLUDE_DIR=%{buildroot}%{_includedir}/%{name} \
        OPENBLAS_CMAKE_DIR=%{buildroot}%{_libdir}/cmake/%{name} \
        PREFIX=%{buildroot}%{_prefix} install

# Put libraries in correct location
rm -rf %{buildroot}%{_libdir}/lib%{name}*

# Install the serial library
install -D -p -m 755 serial/lib%{name}_serial.so %{buildroot}%{_libdir}/lib%{name}_serial.so.0
install -D -p -m 644 serial/lib%{name}_serial.a %{buildroot}%{_libdir}/lib%{name}_serial.a

# Install the OpenMP library
install -D -p -m 755 openmp/lib%{name}_openmp.so %{buildroot}%{_libdir}/lib%{name}_openmp.so.0
install -D -p -m 644 openmp/lib%{name}_openmp.a %{buildroot}%{_libdir}/lib%{name}_openmp.a

# Install the threaded library
install -D -p -m 755 pthreads/lib%{name}_pthreads.so %{buildroot}%{_libdir}/lib%{name}_pthreads.so.0
install -D -p -m 644 pthreads/lib%{name}_pthreads.a %{buildroot}%{_libdir}/lib%{name}_pthreads.a

# Fix source permissions (also applies to LAPACK)
find -name \*.f -exec chmod 644 {} +

# Remove pkgconfig file, it can't be configured for different library suffixes we use and, as such, is useless
#rm -fr %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i 	"s|%{buildroot}||g" %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Dummy target for update-alternatives
install -d %{buildroot}/%{_sysconfdir}/alternatives
ln -s lib%{name}.so.0 %{buildroot}/%{_libdir}/lib%{name}.so.0
ln -s lib%{name}.so.0 %{buildroot}/%{_sysconfdir}/alternatives/lib%{name}.so.0
ln -s lib%{name}.so.0 %{buildroot}/%{_libdir}/libblas.so.3
ln -s lib%{name}.so.0 %{buildroot}/%{_libdir}/libcblas.so.3
ln -s lib%{name}.so.0 %{buildroot}/%{_libdir}/liblapack.so.3
ln -s lib%{name}.so.0 %{buildroot}/%{_sysconfdir}/alternatives/libblas.so.3
ln -s lib%{name}.so.0 %{buildroot}/%{_sysconfdir}/alternatives/libcblas.so.3
ln -s lib%{name}.so.0 %{buildroot}/%{_sysconfdir}/alternatives/liblapack.so.3

# Fix symlinks
pushd %{buildroot}%{_libdir}
ln -sf lib%{name}.so.0 lib%{name}.so
# Serial libraries
ln -sf lib%{name}_serial.so.0 lib%{name}_serial.so
# OpenMP libraries
ln -sf lib%{name}_openmp.so.0 lib%{name}_openmp.so
# Threaded libraries
ln -sf lib%{name}_pthreads.so.0 lib%{name}_pthreads.so

rm -rf %{buildroot}%{_libdir}/cmake

# Fix cmake config file
# sed -i 's|%{buildroot}||g' %{buildroot}%{_libdir}/cmake/%{name}/*.cmake

# Delete info about OBS host cpu
%ifarch %ix86 x86_64
sed -i '/#define OPENBLAS_NEEDBUNDERSCORE/,/#define OPENBLAS_VERSION/{//!d}' %{buildroot}%{_includedir}/%{name}/openblas_config.h
%endif

%post -n lib%{name}_serial0
%{_sbindir}/update-alternatives --install \
   %{_libdir}/libblas.so.3 libblas.so.3 %{_libdir}/lib%{name}_serial.so.0  20
%{_sbindir}/update-alternatives --install \
   %{_libdir}/libcblas.so.3 libcblas.so.3 %{_libdir}/lib%{name}_serial.so.0  20
%{_sbindir}/update-alternatives --install \
   %{_libdir}/liblapack.so.3 liblapack.so.3 %{_libdir}/lib%{name}_serial.so.0  20
%{_sbindir}/update-alternatives --install \
   %{_libdir}/lib%{name}.so.0 lib%{name}.so.0 %{_libdir}/lib%{name}_serial.so.0  20
/sbin/ldconfig

%preun -n lib%{name}_serial0
if [ "$1" = 0 ] ; then
   %{_sbindir}/update-alternatives --remove libblas.so.3 %{_libdir}/lib%{name}_serial.so.0
   %{_sbindir}/update-alternatives --remove libcblas.so.3 %{_libdir}/lib%{name}_serial.so.0
   %{_sbindir}/update-alternatives --remove liblapack.so.3 %{_libdir}/lib%{name}_serial.so.0
   %{_sbindir}/update-alternatives --remove lib%{name}.so.0 %{_libdir}/lib%{name}_serial.so.0
fi

%postun -n lib%{name}_serial0 -p /sbin/ldconfig

%posttrans -n lib%{name}_serial0
if [ "$1" = 0 ] ; then
  if ! [ -f %{_libdir}/lib%{name}.so.0 ] ; then
      %{_sbindir}/update-alternatives --auto lib%{name}.so.0
  fi
fi

%post -n lib%{name}_openmp0
%{_sbindir}/update-alternatives --install \
   %{_libdir}/libblas.so.3 libblas.so.3 %{_libdir}/lib%{name}_openmp.so.0  20
%{_sbindir}/update-alternatives --install \
   %{_libdir}/libcblas.so.3 libcblas.so.3 %{_libdir}/lib%{name}_openmp.so.0  20
%{_sbindir}/update-alternatives --install \
   %{_libdir}/liblapack.so.3 liblapack.so.3 %{_libdir}/lib%{name}_openmp.so.0  20
%{_sbindir}/update-alternatives --install \
%ifarch %ix86 x86_64
   %{_libdir}/lib%{name}.so.0 lib%{name}.so.0 %{_libdir}/lib%{name}_openmp.so.0  20
%else
   %{_libdir}/lib%{name}.so.0 lib%{name}.so.0 %{_libdir}/lib%{name}_openmp.so.0  50
%endif
/sbin/ldconfig

%preun -n lib%{name}_openmp0
if [ "$1" = 0 ] ; then
   %{_sbindir}/update-alternatives --remove libblas.so.3 %{_libdir}/lib%{name}_openmp.so.0
   %{_sbindir}/update-alternatives --remove libcblas.so.3 %{_libdir}/lib%{name}_openmp.so.0
   %{_sbindir}/update-alternatives --remove liblapack.so.3 %{_libdir}/lib%{name}_openmp.so.0
   %{_sbindir}/update-alternatives --remove lib%{name}.so.0 %{_libdir}/lib%{name}_openmp.so.0
fi

%postun -n lib%{name}_openmp0 -p /sbin/ldconfig

%posttrans -n lib%{name}_openmp0
if [ "$1" = 0 ] ; then
  if ! [ -f %{_libdir}/lib%{name}.so.0 ] ; then
      %{_sbindir}/update-alternatives --auto lib%{name}.so.0
  fi
fi

%post -n lib%{name}_pthreads0
%{_sbindir}/update-alternatives --install \
   %{_libdir}/libblas.so.3 libblas.so.3 %{_libdir}/lib%{name}_pthreads.so.0  20
%{_sbindir}/update-alternatives --install \
   %{_libdir}/libcblas.so.3 libcblas.so.3 %{_libdir}/lib%{name}_pthreads.so.0  20
%{_sbindir}/update-alternatives --install \
   %{_libdir}/liblapack.so.3 liblapack.so.3 %{_libdir}/lib%{name}_pthreads.so.0  20
%{_sbindir}/update-alternatives --install \
%ifarch %ix86 x86_64
   %{_libdir}/lib%{name}.so.0 lib%{name}.so.0 %{_libdir}/lib%{name}_pthreads.so.0  50
%else
   %{_libdir}/lib%{name}.so.0 lib%{name}.so.0 %{_libdir}/lib%{name}_pthreads.so.0  20
%endif
/sbin/ldconfig

%preun -n lib%{name}_pthreads0
if [ "$1" = 0 ] ; then
   %{_sbindir}/update-alternatives --remove libblas.so.3 %{_libdir}/lib%{name}_pthreads.so.0
   %{_sbindir}/update-alternatives --remove libcblas.so.3 %{_libdir}/lib%{name}_pthreads.so.0
   %{_sbindir}/update-alternatives --remove liblapack.so.3 %{_libdir}/lib%{name}_pthreads.so.0
   %{_sbindir}/update-alternatives --remove lib%{name}.so.0 %{_libdir}/lib%{name}_pthreads.so.0
fi

%postun -n lib%{name}_pthreads0 -p /sbin/ldconfig

%posttrans -n lib%{name}_pthreads0
if [ "$1" = 0 ] ; then
  if ! [ -f %{_libdir}/lib%{name}.so.0 ] ; then
      %{_sbindir}/update-alternatives --auto lib%{name}.so.0
  fi
fi

%files -n lib%{name}_serial0
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/lib%{name}_serial.so.0
%ghost %{_libdir}/lib%{name}.so.0
%ghost %{_libdir}/libblas.so.3
%ghost %{_libdir}/libcblas.so.3
%ghost %{_libdir}/liblapack.so.3
%ghost %{_sysconfdir}/alternatives/lib%{name}.so.0
%ghost %{_sysconfdir}/alternatives/libblas.so.3
%ghost %{_sysconfdir}/alternatives/libcblas.so.3
%ghost %{_sysconfdir}/alternatives/liblapack.so.3

%files -n lib%{name}_serial-devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}_serial.so

%files -n lib%{name}_openmp0
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/lib%{name}_openmp.so.0
%ghost %{_libdir}/lib%{name}.so.0
%ghost %{_libdir}/libblas.so.3
%ghost %{_libdir}/libcblas.so.3
%ghost %{_libdir}/liblapack.so.3
%ghost %{_sysconfdir}/alternatives/lib%{name}.so.0
%ghost %{_sysconfdir}/alternatives/libblas.so.3
%ghost %{_sysconfdir}/alternatives/libcblas.so.3
%ghost %{_sysconfdir}/alternatives/liblapack.so.3

%files -n lib%{name}_openmp-devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}_openmp.so

%files -n lib%{name}_pthreads0
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/lib%{name}_pthreads.so.0
%ghost %{_libdir}/lib%{name}.so.0
%ghost %{_libdir}/libblas.so.3
%ghost %{_libdir}/libcblas.so.3
%ghost %{_libdir}/liblapack.so.3
%ghost %{_sysconfdir}/alternatives/lib%{name}.so.0
%ghost %{_sysconfdir}/alternatives/libblas.so.3
%ghost %{_sysconfdir}/alternatives/libcblas.so.3
%ghost %{_sysconfdir}/alternatives/liblapack.so.3

%files -n lib%{name}_pthreads-devel
%defattr(-,root,root,-)
%{_libdir}/lib%{name}_pthreads.so

%files devel
%defattr(-,root,root,-)
%doc Changelog.txt GotoBLAS* LICENSE README.md
%{_libdir}/documentation.list
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*

%files devel-headers
%defattr(-,root,root,-)
%{_includedir}/%{name}/

%files devel-static
%defattr(-,root,root,-)
%{_libdir}/lib%{name}_serial.a
%{_libdir}/lib%{name}_openmp.a
%{_libdir}/lib%{name}_pthreads.a

%changelog
