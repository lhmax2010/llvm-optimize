#
# spec file for package hdf5
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%define _mvapich2 0
%define _openmpi 0
%define _mpi 0

%define use_sz2 0

# TODO: The so numbers autodetected by update_so_version.sh
# do not match the so numbers that are actually buit.
%define sonum 101
%define sonum_CXX 101
# sonum / sonum_CXX has been modified to 101 as a workaround.
%define sonum_F 100
%define sonum_HL 100
%define sonum_HL_CXX 100
%define sonum_HL_F 100
%define sonum_TOOLS 100

Name:           hdf5
Version:        1.10.1
Release:        0
Summary:        Command-line programs for the HDF5 scientific data format
License:        BSD-3-Clause
Group:          Productivity/Scientific/Other
Url:            http://www.hdfgroup.org/HDF5/
Source0:        %{name}-%{version}.tar.gz
Source1001:	hdf5.manifest
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  gcc-fortran
BuildRequires:  krb5-devel
%if 0%{?use_sz2}
BuildRequires:  libsz2-devel
%endif
BuildRequires:  zlib-devel

Requires:       libhdf5-%{sonum} = %{version}
Requires:       libhdf5_cpp%{sonum_CXX} = %{version}
Requires:       libhdf5_fortran%{sonum_F} = %{version}
Requires:       libhdf5_hl%{sonum_HL} = %{version}
Requires:       libhdf5_hl_cpp%{sonum_HL_CXX} = %{version}
Requires:       libhdf5hl_fortran%{sonum_HL_F} = %{version}

%description
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains utility functions for working with HDF5 files.

%package -n libhdf5-%{sonum}
Summary:        Shared libraries for the HDF5 scientific data format
# To avoid unresolvable errors due to multiple providers of the library
Group:          Productivity/Scientific/Other
Provides:       libhdf5 = %{version}
Obsoletes:      libhdf5 < %{version}

%description -n libhdf5-%{sonum}
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains the HDF5 runtime libraries.


%package -n libhdf5_hl%{sonum_HL}
Summary:        High-level shared libraries for the HDF5 scientific data format
# To avoid unresolvable errors due to multiple providers of the library
Group:          Productivity/Scientific/Other
Provides:       libhdf5_hl = %{version}
Obsoletes:      libhdf5_hl < %{version}

%description -n libhdf5_hl%{sonum_HL}
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains the the high-level HDF5 runtime libraries.

%package -n libhdf5_cpp%{sonum_CXX}
Summary:        Shared libraries for the HDF5 scientific data format
# To avoid unresolvable errors due to multiple providers of the library
Group:          Productivity/Scientific/Other
Provides:       libhdf5_cpp = %{version}
Obsoletes:      libhdf5_cpp < %{version}

%description -n libhdf5_cpp%{sonum_CXX}
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains the HDF5 runtime libraries.

%package -n libhdf5_hl_cpp%{sonum_HL_CXX}
Summary:        High-level shared libraries for the HDF5 scientific data format
# To avoid unresolvable errors due to multiple providers of the library
Group:          Productivity/Scientific/Other
Provides:       libhdf5_hl_cpp = %{version}
Obsoletes:      libhdf5_hl_cpp < %{version}

%description -n libhdf5_hl_cpp%{sonum_HL_CXX}
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains the the high-level HDF5 runtime libraries.

%package -n libhdf5_fortran%{sonum_F}
Summary:        Shared libraries for the HDF5 scientific data format
# To avoid unresolvable errors due to multiple providers of the library
Group:          Productivity/Scientific/Other
Provides:       libhdf5_fortran = %{version}
Obsoletes:      libhdf5_fortran < %{version}

%description -n libhdf5_fortran%{sonum_F}
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains the HDF5 runtime libraries.

%package -n libhdf5hl_fortran%{sonum_HL_F}
Summary:        High-level shared libraries for the HDF5 scientific data format
# To avoid unresolvable errors due to multiple providers of the library
Group:          Productivity/Scientific/Other
Provides:       libhdf5hl_fortran = %{version}
Obsoletes:      libhdf5hl_fortran < %{version}

%description -n libhdf5hl_fortran%{sonum_HL_F}
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains the the high-level HDF5 runtime libraries.


%package devel-data
Summary:        Development data files for %{name}
Group:          Development/Libraries/Other

%description devel-data
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains generic files needed to create projects that use
any version of HDF5.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries/Other
Requires:       %{name} = %{version}
Requires:       %{name}-devel-data = %{version}
%if 0%{?use_sz2}
Requires:       libsz2-devel
%endif
# Required by Fortran programs?
Requires:       libhdf5-%{sonum} = %{version}
Requires:       libhdf5_cpp%{sonum_CXX} = %{version}
Requires:       libhdf5_fortran%{sonum_F} = %{version}
Requires:       libhdf5_hl%{sonum_HL} = %{version}
Requires:       libhdf5_hl_cpp%{sonum_HL_CXX} = %{version}
Requires:       libhdf5hl_fortran%{sonum_HL_F} = %{version}

%description devel
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package contains all files needed to create projects that use
HDF5.

%package  devel-static
Summary:        Static development files for %{name}
Group:          Development/Libraries/Other
Requires:       %{name}-devel = %{version}

%description devel-static
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package provides the static libraries for HDF5.

%package examples
Summary:        Examples for %{name}
Group:          Documentation/Other
Requires:       libhdf5-%{sonum} = %{version}
Requires:       libhdf5_cpp%{sonum_CXX} = %{version}
Requires:       libhdf5_fortran%{sonum_F} = %{version}
Requires:       libhdf5_hl%{sonum_HL} = %{version}
Requires:       libhdf5_hl_cpp%{sonum_HL_CXX} = %{version}
Requires:       libhdf5hl_fortran%{sonum_HL_F} = %{version}

%description examples
HDF5 is a data model, library, and file format for storing and
managing data. It supports an unlimited variety of datatypes, and
is designed for flexible and efficient I/O and for high volume and
complex data. HDF5 is portable and is extensible, allowing
applications to evolve in their use of HDF5.

The HDF5 technology suite is designed to organize, store, discover,
access, analyze, share, and preserve diverse, complex data in
continuously evolving heterogeneous computing and storage environments.

HDF5 supports all types of data stored digitally, regardless of origin
or size. Petabytes of remote sensing data collected by satellites,
terabytes of computational results from nuclear testing models, and
megabytes of high-resolution MRI brain scans are stored in HDF5 files,
together with metadata necessary for efficient data sharing,
processing, visualization, and archiving.

This package provides examples of HDF5 library use.

%prep
%setup -q
cp %{SOURCE1001} .

echo "prepare parallel builds: %{_mpi}"
for build_dir in build %{_mpi}; do
    mkdir $build_dir
    ln -s ../configure $build_dir
done

%build
export F9X=gfortran
export CFLAGS="%{optflags}"
%if 0%{?asan}
export LIBS+="-lasan"
%endif

# workaround for known gcc issue, see RELEASE.txt
if gcc --version |grep -q " 4\.[68]"; then
	export CFLAGS="${CFLAGS/-O2/-O0}"
fi
%ifarch %arm
# we want to have useful H5_CFLAGS on arm too
test -e config/linux-gnueabi || cp config/linux-gnu config/linux-gnueabi
%endif

export CFLAGS="$CFLAGS -Wno-incompatible-pointer-types -Wno-implicit-function-declaration"

# NOTE: --enable-unsupported is required when --enable-fortran
# and/or --enable-cxx is enabled along with --enable-threadsafe.
# Building with thise combination results in thread-safe C
# libraries and non-thread-safe fotran and/or C++ libraries. So
# you have to explicitly allow building the thread-safe C
# library and the non-thread-safe C++ and fortran libraries in
# order to make sure people don't assume that their fotran or
# C++ code is thread-safe.  Since our users are going to be
# accessing this through other programs, this doesn't matter.

mkdir -p build
pushd build
%configure \
  --docdir=%{_docdir}/%{name} \
  --disable-dependency-tracking \
  --enable-fortran \
  --enable-fortran2003 \
  --enable-unsupported \
  --enable-hl \
  --enable-shared \
  --enable-cxx \
  --enable-threadsafe \
  --enable-build-mode=production \
  --with-szlib \
  --with-pthread

make V=1 %{?_smp_mflags}
popd

%install
make install DESTDIR=%{buildroot} -C "build"

find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot}%{_datadir}/hdf5_examples -type f \
                 | grep -v ".sh$" | xargs chmod 644

pushd %{buildroot}%{_libdir}
ln -s libhdf5.so libhdf5_serial.so
popd

# delete examples from parallel builds
rm -rf %{buildroot}%{_libdir}/mpi/gcc/*/share/hdf5_examples
%fdupes -s %{buildroot}/%{_datadir}

# rpm macro for version checking
mkdir -p %{buildroot}%{_sysconfdir}/rpm
cat > %{buildroot}%{_sysconfdir}/rpm/macros.hdf5 <<EOF
#
# RPM macros for hdf5 packaging
#
%_hdf5_sonum  %{sonum}
%_hdf5_version  %{version}
EOF

%post -n libhdf5-%{sonum} -p /sbin/ldconfig
%postun -n libhdf5-%{sonum} -p /sbin/ldconfig
%post -n libhdf5_hl%{sonum_HL} -p /sbin/ldconfig
%postun -n libhdf5_hl%{sonum_HL} -p /sbin/ldconfig
%post -n libhdf5_cpp%{sonum_CXX} -p /sbin/ldconfig
%postun -n libhdf5_cpp%{sonum_CXX} -p /sbin/ldconfig
%post -n libhdf5_hl_cpp%{sonum_HL_CXX} -p /sbin/ldconfig
%postun -n libhdf5_hl_cpp%{sonum_HL_CXX} -p /sbin/ldconfig
%post -n libhdf5_fortran%{sonum_F} -p /sbin/ldconfig
%postun -n libhdf5_fortran%{sonum_F} -p /sbin/ldconfig
%post -n libhdf5hl_fortran%{sonum_HL_F} -p /sbin/ldconfig
%postun -n libhdf5hl_fortran%{sonum_HL_F} -p /sbin/ldconfig

%files
%manifest hdf5.manifest
%defattr(-,root,root)
%{_bindir}/gif2h5
%{_bindir}/h52gif
%{_bindir}/h5clear
%{_bindir}/h5copy
%{_bindir}/h5debug
%{_bindir}/h5diff
%{_bindir}/h5dump
%{_bindir}/h5format_convert
%{_bindir}/h5import
%{_bindir}/h5jam
%{_bindir}/h5ls
%{_bindir}/h5mkgrp
%{_bindir}/h5perf_serial
%{_bindir}/h5redeploy
%{_bindir}/h5repack
%{_bindir}/h5repart
%{_bindir}/h5stat
%{_bindir}/h5unjam
%{_bindir}/h5watch

%files -n libhdf5-%{sonum}
%defattr(-,root,root)
%doc COPYING ACKNOWLEDGMENTS README.txt
%doc release_docs/HISTORY-1_8_0-1_10_0.txt
%doc release_docs/RELEASE.txt
%defattr(0755,root,root)
%{_libdir}/libhdf5.so.%{sonum}
%{_libdir}/libhdf5.so.%{sonum}.*
%{_libdir}/libhdf5_serial.so

%files -n libhdf5_hl%{sonum_HL}
%defattr(-,root,root)
%doc COPYING
%defattr(0755,root,root)
%{_libdir}/libhdf5_hl.so.%{sonum_HL}
%{_libdir}/libhdf5_hl.so.%{sonum_HL}.*

%files -n libhdf5_cpp%{sonum_CXX}
%defattr(-,root,root)
%doc COPYING
%defattr(0755,root,root)
%{_libdir}/libhdf5_cpp.so.%{sonum_CXX}
%{_libdir}/libhdf5_cpp.so.%{sonum_CXX}.*

%files -n libhdf5_hl_cpp%{sonum_HL_CXX}
%defattr(-,root,root)
%doc COPYING
%defattr(0755,root,root)
%{_libdir}/libhdf5_hl_cpp.so.%{sonum_HL_CXX}
%{_libdir}/libhdf5_hl_cpp.so.%{sonum_HL_CXX}.*

%files -n libhdf5_fortran%{sonum_F}
%defattr(-,root,root)
%doc COPYING
%defattr(0755,root,root)
%{_libdir}/libhdf5_fortran.so.%{sonum_F}
%{_libdir}/libhdf5_fortran.so.%{sonum_F}.*

%files -n libhdf5hl_fortran%{sonum_HL_F}
%defattr(-,root,root)
%doc COPYING
%defattr(0755,root,root)
%{_libdir}/libhdf5hl_fortran.so.%{sonum_HL_F}
%{_libdir}/libhdf5hl_fortran.so.%{sonum_HL_F}.*

%files devel-data
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/rpm/macros.hdf5

%files devel
%defattr(-,root,root)
%doc release_docs/HISTORY-1_0-1_8_0_rc3.txt
%doc release_docs/RELEASE.txt
%doc ACKNOWLEDGMENTS README.txt
%{_bindir}/h5c++
%{_bindir}/h5cc
%{_bindir}/h5fc
%{_includedir}/*.h
%{_libdir}/*.so
%exclude %{_libdir}/libhdf5_serial.so
%{_libdir}/*.settings
%{_includedir}/*.mod

%files devel-static
%defattr(-,root,root)
%{_libdir}/*.a

%files examples
%defattr(-,root,root)
%{_datadir}/hdf5_examples
