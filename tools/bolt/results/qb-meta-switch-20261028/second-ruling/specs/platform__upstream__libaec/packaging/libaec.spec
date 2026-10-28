#
# spec file for package libaec
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


Name:           libaec
Version:        1.0.1
Release:        0
Summary:        Adaptive Entropy Coding library
#---License is BSD, however there is a non-enforced NASA patent on the
#---algorithm, see patent.txt
License:        BSD-2-Clause
Group:          Productivity/Archiving/Compression
Url:            https://gitlab.dkrz.de/k202009/libaec
Source0:        %{name}-%{version}.tar.gz
Source1001:	libaec.manifest

BuildRequires:  cmake
BuildRequires:  gcc-c++

%description
Libaec provides lossless compression of signed or unsigned integers
(samples) of sizes 1 to 32 bits wide. The library achieves best
results for low entropy data as often encountered in space imaging
instrument data or numerical model output from weather or climate
simulations.

%package -n libaec0
Summary:        Adaptive Entropy Coding library
Group:          System/Libraries

%description -n libaec0
Libaec provides lossless compression of signed or unsigned integers
(samples) of sizes 1 to 32 bits wide. The library achieves best
results for low entropy data as often encountered in space imaging
instrument data or numerical model output from weather or climate
simulations. While floating point representations are not directly
supported, they can also be efficiently coded by grouping exponents
and mantissa.

Libaec implements Golomb Rice coding as defined in the Space Data
System Standard documents 121.0-B-2 and 120.0-G-2.

%package devel
Summary:        Development files for libaec, a library for Adaptive Entropy Coding library
Group:          Development/Libraries/C and C++
Requires:       libaec0 = %{version}

%description devel
Devel files for libaec (Adaptive Entropy Coding library).

%package -n libsz2
Summary:        Lossless compression library for scientific data
Group:          System/Libraries

%description -n libsz2
Drop-in replacement for the SZIP library
(http://www.hdfgroup.org/doc_resource/SZIP).

%package -n sz2-devel
Summary:        Development files for libsz2
Group:          Development/Libraries/C and C++
Requires:       libaec-devel = %{version}
Requires:       libsz2 = %{version}
Provides:       libsz2-devel = %{version}
Obsoletes:      libsz2-devel < %{version}

%description -n sz2-devel
Header files for libsz2, a drop-in replacement for the
SZIP library (http://www.hdfgroup.org/doc_resource/SZIP).

%prep
%setup -q -T -a 0 -c
cp %{SOURCE1001} .

%build
%cmake -DCMAKE_C_FLAGS="%{optflags} -std=gnu99"
make %{?_smp_mflags}

%install
%make_install

%post -n libaec0 -p /sbin/ldconfig
%post -n libsz2 -p /sbin/ldconfig

%postun -n libaec0 -p /sbin/ldconfig
%postun -n libsz2 -p /sbin/ldconfig

%files -n libaec0
%manifest libaec.manifest
%doc README.md Copyright.txt doc/patent.txt
%{_bindir}/aec
%{_libdir}/libaec.so.0*

%files devel
%{_includedir}/libaec.h
%{_libdir}/libaec.so

%files -n libsz2
%manifest libaec.manifest
%doc README.SZIP
%{_libdir}/libsz.so.2*

%files -n sz2-devel
%{_includedir}/szlib.h
%{_libdir}/libsz.so
