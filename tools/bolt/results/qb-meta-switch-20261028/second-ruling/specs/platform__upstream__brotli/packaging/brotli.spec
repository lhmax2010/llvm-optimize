Name:       brotli
Summary:    Lossless Compression Algorithm
Version:    1.1.1
Release:    0

# ==========================================================
License:    MIT
# ==========================================================

Group:      Productivity/Archiving/Compression
Source0:    %{name}-%{version}.tar.gz
Source10:   CMakeLists_static_library.patch
Source1001: %{name}.manifest

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires:  cmake

%description
This package contains the brotli command line utility to compress and
decompress data with the brotli compression algorithm.

Brotli is a generic-purpose lossless compression algorithm that
compresses data using a combination of a modern variant of the LZ77
algorithm, Huffman coding and 2nd order context modeling, with a
compression ratio comparable to the best currently available
general-purpose compression methods. It is similar in speed with
deflate but offers more dense compression.

%package -n libbrotlicommon
Summary:        Common Library for Brotli Compression
Group:          System/Libraries

%description -n libbrotlicommon
Common library for the Brotli general purpose lossless data
compression algorithm.

%package -n libbrotlidec
Summary:        Library for Brotli Decompression
Group:          System/Libraries

%description -n libbrotlidec
Decompression library for the Brotli general purpose lossless data
compression algorithm.

%package -n libbrotlienc
Summary:        Library for Brotli Compression
Group:          System/Libraries

%description -n libbrotlienc
Compression library for the Brotli general purpose lossless data
compression algorithm.

%package -n libbrotli-devel
Summary:        Development and Header Files for Brotli Compression
Group:          Development/Libraries/C and C++
Requires:       libbrotlicommon = %version-%release
Requires:       libbrotlidec = %version-%release
Requires:       libbrotlienc = %version-%release
Provides:       libbrotlicommon-devel = %version-%release
Provides:       libbrotlidec-devel = %version-%release
Provides:       libbrotlienc-devel = %version-%release
Obsoletes:      libbrotlicommon-devel < %version-%release
Obsoletes:      libbrotlidec-devel < %version-%release
Obsoletes:      libbrotlienc-devel < %version-%release

%description -n libbrotli-devel
Development and headers files for (de)compressing data using the
Brotli general purpose lossless compression algorithm.

%define keepstatic 1

%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE10}

# ==========================================================
# build section
# how to actually build the software we are packaging
# ==========================================================
%build
mkdir -p build
cd build
%cmake \
       -DCMAKE_C_FLAGS="-fPIC -DBROTLI_ENCODER_CLEANUP_ON_OOM" \
       -DCMAKE_CXX_FLAGS="-fPIC" \
       -DCMAKE_EXE_LINKER_FLAGS="-pie -Wl,-z,relro,-z,now" \
       -DCMAKE_SHARED_LINKER_FLAGS="-Wl,-z,relro,-z,now" \
       ..

make %{?_smp_mflags}
cd -


# ==========================================================
# install section
# how to actually build the software we are packaging
# ==========================================================
%install
cd build
%{make_install}
cd -

%remove_docs

%clean

%post   -n libbrotlicommon -p /sbin/ldconfig
%postun -n libbrotlicommon -p /sbin/ldconfig
%post   -n libbrotlidec -p /sbin/ldconfig
%postun -n libbrotlidec -p /sbin/ldconfig
%post   -n libbrotlienc -p /sbin/ldconfig
%postun -n libbrotlienc -p /sbin/ldconfig

# ==========================================================
# files section
# The list of files that will be installed in the end
# user’s system.
# ==========================================================
%files
%manifest %{name}.manifest
%license LICENSE
%_bindir/brotli

%files -n libbrotlicommon
%manifest %{name}.manifest
%license LICENSE
%_libdir/libbrotlicommon.so.*

%files -n libbrotlidec
%manifest %{name}.manifest
%license LICENSE
%_libdir/libbrotlidec.so.*

%files -n libbrotlienc
%manifest %{name}.manifest
%license LICENSE
%_libdir/libbrotlienc.so.*

%files -n libbrotli-devel
%manifest %{name}.manifest
%license LICENSE
%_includedir/brotli/
%_libdir/*.so
%_libdir/*.a
%_libdir/pkgconfig/*.pc


