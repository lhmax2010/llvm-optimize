Name:           xxhash
VCS:            platform/upstream/xxhash#5b300f8dac755b6116991f38cb33aaf998c30aef
Version:        0.8.3
Release:        1.1
Summary:        Non-cryptographic hash algorithm
License:        BSD-2-Clause AND GPL-2.0-only
URL:            https://github.com/Cyan4973/xxHash
Source0:        https://github.com/Cyan4973/xxHash/archive/v%{version}.tar.gz
Source1:        %{name}.manifest

BuildRequires:  gcc-c++
BuildRequires:  pkg-config

%description
xxHash is a hash algorithm. It completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash functions.
Hashes are identical on all platforms.

%package -n libxxhash
Summary:        Non-cryptographic hash algorithm
License:        BSD-2-Clause

%description -n libxxhash
xxHash is a hash algorithm. It completes the SMHasher test suite which
evaluates collision, dispersion and randomness qualities of hash functions.
Hashes are identical on all platforms.

%package devel
Summary:        Headers for xxHash, a non-cryptographic hash algorithm
License:        BSD-2-Clause
Requires:       %name = %{version}-%{release}
Requires:       libxxhash = %{version}-%{release}

%description devel
Headers and other development files for xxHash.

%prep
%setup -q -n xxHash-%{version}
cp %{SOURCE1} .

%build
export CFLAGS="%{optflags} -DXXH_X86DISPATCH_ALLOW_AVX=1"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="%{?build_ldflags}"
make %{?_smp_mflags} prefix=%{_prefix} libdir=%{_libdir}

%install
export CFLAGS="%{optflags} -DXXH_X86DISPATCH_ALLOW_AVX=1"
export CXXFLAGS="%{optflags}"
export LDFLAGS="%{?build_ldflags}"
make install DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir}
rm -rf %{buildroot}%{_libdir}/libxxhash.a

# Remove documentation and man pages (Tizen recommendation)
%remove_docs

%post -n libxxhash -p /sbin/ldconfig
%postun -n libxxhash -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/xxh*

%files -n libxxhash
%{_libdir}/libxxhash.so.*

%files devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libxxhash.so

